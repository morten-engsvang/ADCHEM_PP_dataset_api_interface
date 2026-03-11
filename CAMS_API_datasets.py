def make_yearly_payload_CAMS_GLOB_OCE(year: int, latitudes, longitudes) -> dict:
    """Generate a payload for a given year, with correct date indices."""
    BASE_YEAR = 2000  # adjust if index 0 corresponds to a different year
    idx = year - BASE_YEAR
    return {
        "idDataset": 486,
        "idInventoryScenario": 8,
        "nameDataset": "CAMS-GLOB-OCE v4.1",
        "species": ["chbr3", "dms"],
        "allSpecies": True,
        "fullTimePeriod": False,
        "originFiles": False,
        "beginDateIndex": idx,
        "endDateIndex": idx,
        "nameFile": "CAMS-GLOB-OCE_Glb_0.94x1.25_oce_CHBr3_v4.1.nc",
        "scenario": "v4.1",
        "total": False,
        "dataType": "flux",
        "exportJson": False,
        "exportCSV": 0,
        "exportNETCDF": True,
        "resolutionId": 17,
        "categoryId": 46,
        "geospatialId": 1,
        "beginDate": f"{year}-01-01",
        "endDate": f"{year}-01-01",
        "resolution": "0.94x1.25",
        "latmin": latitudes[0], "latmax": latitudes[1],
        "lonmin": longitudes[0], "lonmax": longitudes[1],
        "intervalName": "Yearly",
        "sectors": ["All"],
        "allSector": True,
    }