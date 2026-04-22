import os
from pathlib import Path
import zipfile

def extract_zip_by_extension(archive_path, dest_folder, extension):
    """Extract only files with a given extension from a .zip archive."""
    os.makedirs(dest_folder, exist_ok=True)

    with zipfile.ZipFile(archive_path, "r") as zf:
        members = [m for m in zf.namelist() if m.endswith(extension)]

        for member in members:
            filename = os.path.basename(member)
            with zf.open(member) as src, open(os.path.join(dest_folder, filename), "wb") as dst:
                dst.write(src.read())
            print(f"Extracted: {filename}")

def download_all(input_data_location,years, month_array):
    print("\n -------------------------------------------------")
    print("\n ------- Downloading data from EDGAR HTAPv3 ------")
    print("\n -------------------------------------------------")
    version = "v32" #v3 is only valid until 2018, v32 is valid until 2020
    downloads_dir  = Path("./downloads/HTAPv3")
    downloads_dir.mkdir(exist_ok=True)
    subsets = ["BC", "CO", "NH3", "NMVOC", "NOx", "OC", "PM10", "PM2.5", "SO2"]
    if month_array[0] == 1:
        previous_year = years[0] - 1
        download_years = years + [previous_year]
    for year in download_years:
        for component in subsets:
            url = f"https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/htap_{version}/gridmaps_01x01/fluxes/{component}/edgar_HTAP{version}_{year}_{component}.zip"
            output = downloads_dir/f"edgar_HTAP_{year}_{component}.zip"
            command = f"curl {url} --output {output}"
            print(command)
            os.system(command)
            extract_zip_by_extension(output, input_data_location, ".nc")
    print("\n -------------------------------------------------")
    print("\n ------- Downloading data from EDGAR HTAPv3 done -")
    print("\n -------------------------------------------------")