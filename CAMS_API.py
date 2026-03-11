from __future__ import annotations
import requests
import time
import json
import os
import zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
import CAMS_API_datasets as helper
import settings as settings

# ── CONFIG ────────────────────────────────────────────────────────────────────

TOKEN_CACHE = Path("tokens.json")
OUTPUT_DIR  = Path("./downloads")
OUTPUT_DIR.mkdir(exist_ok=True)

USERNAME = settings.ECCAD_USERNAME
PASSWORD = settings.ECCAD_PASSWORD

SSO_TOKEN_URL = "https://sso.aeris-data.fr/auth/realms/aeris/protocol/openid-connect/token"
CLIENT_ID     = "eccad-vjs"
LINKS_URL     = "https://api.sedoo.fr/eccad-catalogue-rest/downloads/links"
SUBMIT_URL    = "https://api.sedoo.fr/eccad-catalogue-rest/downloads/files"


# ── LOGIN HELPER ──────────────────────────────────────────────────────────────

def _do_login(page, tokens: dict) -> None:
    """
    Navigate to the ECCAD login page, click the SSO sign-in button,
    fill credentials, and wait until the token has been captured.
    Uses token capture as the completion signal rather than URL changes,
    since hash-based routing (#/auth/login) doesn't trigger Playwright
    navigation events.
    """
    page.goto("https://eccad.sedoo.fr/#/auth/login")
    page.wait_for_timeout(2000)

    # Click the "Sign in / Register" button to trigger the SSO redirect
    page.click("button:has-text('Sign in / Register'), a:has-text('Sign in / Register'), "
               "button:has-text('Login'), a:has-text('Login'), "
               "button:has-text('Sign In')")

    # Fill credentials on the Keycloak SSO page
    page.wait_for_selector("input[name='username'], input[type='email']", timeout=15_000)
    page.fill("input[name='username'], input[type='email']", USERNAME)
    page.fill("input[name='password'], input[type='password']", PASSWORD)

    # The Keycloak submit button is an <input>, not a <button>
    page.click("input#kc-login")

    # Wait for the token exchange rather than watching the URL
    print("  Waiting for token capture...")
    for _ in range(30):  # up to 30s
        if "access_token" in tokens:
            print("  Login successful.")
            return
        page.wait_for_timeout(1000)

    raise RuntimeError("Login timed out — token was never captured.")


# ── TOKEN MANAGEMENT ──────────────────────────────────────────────────────────

def _token_response_handler(tokens: dict):
    """Returns a Playwright response handler that captures SSO tokens."""
    def handler(response):
        if "sso.aeris-data.fr" in response.url and "token" in response.url:
            try:
                data = response.json()
                if "access_token" in data:
                    tokens.update(data)
                    tokens["obtained_at"] = time.time()
                    print("  Tokens captured.")
            except Exception:
                pass
    return handler


def get_tokens_via_browser() -> dict:
    tokens = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()
        page.on("response", _token_response_handler(tokens))
        _do_login(page, tokens)
        browser.close()

    if not tokens:
        raise RuntimeError("Failed to capture tokens — check credentials.")

    TOKEN_CACHE.write_text(json.dumps(tokens, indent=2))
    return tokens


def load_cached_tokens() -> dict | None:
    if TOKEN_CACHE.exists():
        return json.loads(TOKEN_CACHE.read_text())
    return None


def refresh_access_token(tokens: dict) -> dict:
    resp = requests.post(SSO_TOKEN_URL, data={
        "grant_type":    "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "client_id":     CLIENT_ID,
    })
    resp.raise_for_status()
    new_tokens = resp.json()
    new_tokens["obtained_at"] = time.time()
    TOKEN_CACHE.write_text(json.dumps(new_tokens, indent=2))
    print("  Token refreshed.")
    return new_tokens


def is_token_expired(tokens: dict, buffer: int = 60) -> bool:
    return time.time() > (tokens.get("obtained_at", 0) + tokens.get("expires_in", 300) - buffer)


def get_valid_tokens() -> dict:
    tokens = load_cached_tokens()
    if not tokens:
        print("No cached tokens — logging in via browser...")
        return get_tokens_via_browser()
    if is_token_expired(tokens):
        print("Token expired — refreshing...")
        try:
            return refresh_access_token(tokens)
        except Exception as e:
            print(f"Refresh failed ({e}) — re-logging in via browser...")
            return get_tokens_via_browser()
    return tokens


def make_session(tokens: dict) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type":  "application/json",
        "Accept":        "application/json, text/plain, */*",
        "Origin":        "https://eccad.sedoo.fr",
        "Referer":       "https://eccad.sedoo.fr/",
        "User-Agent":    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
    })
    return s


# ── DATASET SUBMISSION ────────────────────────────────────────────────────────

def submit_request(session: requests.Session, ds: dict) -> None:
    """
    Submit a dataset request via a direct POST with the JSON payload.

    The server returns 302 in two cases:
      - New request created and being processed (success)
      - Duplicate request detected — server deduplicates silently

    Both cases are fine: we detect the outcome by polling the links
    endpoint for a new entry rather than relying on the response body.
    """
    # Don't follow the redirect automatically — we only care that the
    # request was received, not where it redirects to
    resp = session.post(SUBMIT_URL, json=ds["payload"], allow_redirects=False)

    print(f"  Response status: {resp.status_code}")
    print(f"  Response body:   {resp.text[:200]}")

    if resp.status_code in (200, 201, 302):
        print("  Request submitted successfully.")
    else:
        resp.raise_for_status()


# ── POLLING ───────────────────────────────────────────────────────────────────

def get_existing_request_dates(session: requests.Session) -> set:
    """Snapshot all requestDates currently in the queue."""
    resp = session.get(LINKS_URL)
    resp.raise_for_status()
    return {entry["requestDate"] for entry in resp.json()}


def wait_for_new_downloads(
    session: requests.Session,
    tokens: dict,
    known_dates: set,
    poll_interval: int = 20,
    timeout: int = 3600,
) -> list[dict]:
    """
    Poll the downloads/links endpoint until a new request entry appears
    with all files ready (link present and size > 0).
    Returns the list of download dicts for that request.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:

        # Proactively refresh token if needed mid-wait
        if is_token_expired(tokens):
            tokens  = refresh_access_token(tokens)
            session = make_session(tokens)

        resp = session.get(LINKS_URL)
        resp.raise_for_status()
        entries = resp.json()

        for entry in entries:
            if entry["requestDate"] in known_dates:
                continue  # Pre-existed before our submission

            downloads = entry.get("downloads", [])
            if not downloads:
                print(f"  New request found ({entry['requestDate']}) — still processing...")
                continue

            ready   = [d for d in downloads if d.get("link") and d.get("size", 0) > 0]
            pending = [d for d in downloads if not d.get("link") or d.get("size", 0) == 0]

            if pending:
                print(f"  {len(ready)}/{len(downloads)} files ready, waiting...")
            else:
                print(f"  All {len(ready)} files ready!")
                return ready

        print(f"  No new completed request yet — checking again in {poll_interval}s...")
        time.sleep(poll_interval)

    raise TimeoutError("Download never became ready within timeout.")


# ── FILE DOWNLOAD ─────────────────────────────────────────────────────────────

def download_file(session: requests.Session, url: str, filename: str) -> None:
    dest = OUTPUT_DIR / filename
    print(f"  Downloading -> {dest}")
    with session.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done  = 0
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                done += len(chunk)
                if total:
                    print(f"    {done/1e6:.1f} / {total/1e6:.1f} MB ({100*done/total:.0f}%)", end="\r")
    print(f"\n  Saved: {dest}")


# ── File extraction ─────────────────────────────────────────────────────────────
def extract(CAMS_DIR: Path, zip_path: Path) -> None:
    """Unzip, move the .nc file out, then remove the zip and extracted folder."""
    extract_dir = zip_path.with_suffix("")  # e.g. downloads/CAMS-GLOB-OCE_....zip -> downloads/CAMS-GLOB-OCE_...

    print(f"  Extracting {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    # Move all .nc files up to OUTPUT_DIR
    nc_files = list(extract_dir.rglob("*.nc"))
    if not nc_files:
        print(f"  Warning: no .nc files found in {extract_dir}")
    for nc_file in nc_files:
        dest = CAMS_DIR / nc_file.name
        os.rename(nc_file, dest)
        print(f"  Moved: {nc_file.name} -> {dest}")

    # Remove the extracted folder and the zip
    #for f in extract_dir.rglob("*"):
    #    if f.is_file():
    #        os.remove(f)
    #os.remove(extract_dir)
    #os.remove(zip_path)
    #print(f"  Cleaned up {zip_path.name}")

# ── DATASETS ──────────────────────────────────────────────────────────────────
# Add one entry per download request you want to submit.
# Each payload should match the JSON the site sends when you manually request.
def make_dataset(years, latitudes, longitudes) -> list[dict]:
    DATASETS = [{"payload": helper.make_yearly_payload_CAMS_GLOB_OCE(year, latitudes, longitudes)} for year in years]

    return DATASETS

# ── MAIN ──────────────────────────────────────────────────────────────────────

def CAMS_download(CAMS_DIR,years,latitudes,longitudes):
    
    tokens  = get_valid_tokens()
    session = make_session(tokens)

    DATASETS = make_dataset(years, latitudes, longitudes)

    for i, ds in enumerate(DATASETS):
        name = ds["payload"]["nameDataset"]
        print(f"\n[{i+1}/{len(DATASETS)}] Requesting: {name}")

        # Refresh token if needed before starting
        if is_token_expired(tokens):
            tokens  = refresh_access_token(tokens)
            session = make_session(tokens)

        # 1. Snapshot existing requests BEFORE submitting
        known_dates = get_existing_request_dates(session)
        print(f"  {len(known_dates)} existing requests on record.")

        # 2. Submit the dataset request via direct POST
        submit_request(session, ds)

        # 3. Poll until all files in the new request are ready
        print("  Polling for completed downloads...")
        ready_files = wait_for_new_downloads(session, tokens, known_dates)

        # 4. Download every file in this request
        for dl in ready_files:
            filename = Path(dl["filenamePath"]).name  # e.g. CAMS-GLOB-OCE_...zip
            download_file(session, dl["link"], filename)
            extract(Path(CAMS_DIR),OUTPUT_DIR / filename)
    print("\n -------------------------------------------------")
    print("\n ------------------- CAMS done -------------------")
    print("\n -------------------------------------------------")
