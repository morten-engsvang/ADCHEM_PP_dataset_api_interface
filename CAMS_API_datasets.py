from datetime import date

def make_yearly_payload_CAMS_GLOB_OCEv4_1(year: int, latitudes, longitudes) -> dict:
    """Generate a daily payload for a full year, with correct date indices."""
    BASE_DATE  = date(2000, 1, 1)
    begin_date = date(year, 1, 1)
    end_date   = date(year, 12, 31)
    begin_idx  = (begin_date - BASE_DATE).days
    end_idx    = (end_date   - BASE_DATE).days
    return {
        "idDataset": 486,
        "idInventoryScenario": 8,
        "nameDataset": "CAMS-GLOB-OCE v4.1",
        "species": ["chbr3", "dms"],
        "allSpecies": True,
        "fullTimePeriod": False,
        "originFiles": False,
        "beginDateIndex": begin_idx,
        "endDateIndex": end_idx,
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
        "endDate": f"{year}-12-31",
        "resolution": "0.94x1.25",
        "latmin": latitudes[0], "latmax": latitudes[1],
        "lonmin": longitudes[0], "lonmax": longitudes[1],
        "intervalName": "Daily",
        "sectors": ["All"],
        "allSector": True,
    }

def make_yearly_payload_CAMS_GLOB_OCEv3_1(year: int, latitudes, longitudes) -> dict:
    """Generate a daily payload for a full year, with correct date indices."""
    BASE_DATE  = date(2000, 1, 1)
    begin_date = date(year, 1, 1)
    end_date   = date(year, 12, 31)
    begin_idx  = (begin_date - BASE_DATE).days
    end_idx    = (end_date   - BASE_DATE).days
    return {
        "idDataset": 486,
        "idInventoryScenario": 419,
        "nameDataset": "CAMS-GLOB-OCE v3.1",
        "species": ["ch2br2","ch3i","chbr3", "dms"],
        "allSpecies": True,
        "fullTimePeriod": False,
        "originFiles": False,
        "beginDateIndex": begin_idx,
        "endDateIndex": end_idx,
        "nameFile": "CAMS-GLOB-OCE_Glb_0.5x0.5_oce_CH2Br2_v3.1.nc",
        "scenario": "v3.1",
        "total": False,
        "dataType": "flux",
        "exportJson": False,
        "exportCSV": 0,
        "exportNETCDF": True,
        "resolutionId": 5,
        "categoryId": 46,
        "geospatialId": 1,
        "beginDate": f"{year}-01-01",
        "endDate": f"{year}-12-31",
        "resolution": "0.5x0.5",
        "latmin": latitudes[0], "latmax": latitudes[1],
        "lonmin": longitudes[0], "lonmax": longitudes[1],
        "intervalName": "daily",
        "sectors": ["All"],
        "allSector": True,
    }

def make_yearly_payload_CAMS_GLOB_SOIL(year: int, latitudes, longitudes) -> dict:
    """Generate a monthly payload for a full year, with correct date indices."""
    #Due to the way they structure their dataset, we miss the first 
    #15 days of january and the last 15 days of december
    BASE_YEAR  = 2000
    begin_idx  = (year - BASE_YEAR) * 12          # January of that year
    end_idx    = begin_idx + 11                    # December of that year
    return {
        "idDataset": 488,
        "idInventoryScenario": 393,
        "nameDataset": "CAMS-GLOB-SOIL v2.4",
        "species": ["nox"],
        "allSpecies": True,
        "fullTimePeriod": False,
        "originFiles": False,
        "beginDateIndex": begin_idx,
        "endDateIndex": end_idx,
        "nameFile": "CAMS-GLOB-SOIL_Glb_0.5x0.5_soil_nox_v2.4.nc",
        "scenario": "v2.4",
        "total": False,
        "dataType": "flux",
        "exportJson": False,
        "exportCSV": 0,
        "exportNETCDF": True,
        "resolutionId": 5,
        "categoryId": 4432,
        "geospatialId": 1,
        "beginDate": f"{year}-01-15",
        "endDate": f"{year}-12-15",
        "resolution": "0.5x0.5",
        "latmin": latitudes[0], "latmax": latitudes[1],
        "lonmin": longitudes[0], "lonmax": longitudes[1],
        "intervalName": "Monthly",
        "sectors": ["All"],
        "allSector": True,
    }

def make_yearly_payload_CAMS_GLOB_ANT(year: int, latitudes, longitudes) -> dict:
    """Generate a monthly payload for a full year, with correct date indices."""
    #Due to the way they structure their dataset, we miss the first 
    #15 days of january and the last 15 days of december
    BASE_YEAR  = 2000
    begin_idx  = (year - BASE_YEAR) * 12          # January of that year
    end_idx    = begin_idx + 12 - 1          # January of the following year (to include December) 
    return {
        "allSector": True,
        "allSpecies": True,
        "beginDate": f"{year}-01-01",
        "beginDateIndex": begin_idx,
        "categoryId": 3,
        "dataType": "flux",
        "endDate": f"{year+1}-01-01",
        "endDateIndex": end_idx,
        "exportCSV": 0,
        "exportJson": False,
        "exportNETCDF": True,
        "fullTimePeriod": False,
        "geospatialId": 1,
        "idDataset": 479,
        "idInventoryScenario": 279,
        "intervalName": "Monthly",
        "latmax": latitudes[1],
        "latmin": latitudes[0],
        "lonmax": longitudes[1],
        "lonmin": longitudes[0],
        "nameDataset": "CAMS-GLOB-ANT v6.2",
        "nameFile": "CAMS-GLOB-ANT_Glb_0.1x0.1_anthro_acetylene_v6.2.nc",
        "originFiles": False,
        "resolution": "0.1x0.1",
        "resolutionId": 2,
        "scenario": "v6.2",
        "sectors": ["awb","agl","ags","com","fef_coal","fef_gas","fef_oil","fef","dep","ind","tnr","ene","ref","res","tro","shp","swd","slv","sum"],
        "species": ["bc","oc","ethane","other-aldehydes","ch4","so2","ethene","other-alkenes-and-alkynes","co","acetylene","ethers","other-aromatics","formaldehyde","pentanes","co2_short-cycle_org_c","co2_excl_short-cycle_org_c","alcohols","hexanes","propane","n2o","benzene","isoprene","propene","nh3","butanes","toluene","total-acids","total-ketones","nmvocs","chlorinated-hydrocarbons","monoterpenes","trimethylbenzene","nox","esters","other-vocs","xylene"],
    }

def make_yearly_payload_CAMS_GLOB_BIO(year: int, latitudes, longitudes) -> dict:
    """Generate a monthly payload for a full year, with correct date indices."""
    #Due to the way they structure their dataset, we miss the first 
    #15 days of january and the last 15 days of december
    BASE_YEAR  = 2000
    begin_idx  = (year - BASE_YEAR) * 12          # January of that year
    end_idx    = begin_idx + 12 - 1          # January of the following year (to include December) 
    return {
        "allSector": True,
        "allSpecies": True,
        "beginDate": f"{year}-01-01",
        "beginDateIndex": begin_idx,
        "categoryId": 26,
        "dataType": "flux",
        "endDate": f"{year+1}-01-01",
        "endDateIndex": end_idx,
        "exportCSV": 0,
        "exportJson": False,
        "exportNETCDF": True,
        "fullTimePeriod": False,
        "geospatialId": 1,
        "idDataset": 458,
        "idInventoryScenario": 327,
        "intervalName": "Monthly",
        "latmax": latitudes[1],
        "latmin": latitudes[0],
        "lonmax": longitudes[1],
        "lonmin": longitudes[0],
        "nameDataset": "CAMS-GLOB-BIO v3.1",
        "nameFile": "CAMS-GLOB-BIO_Glb_0.25x0.25_bio_acetaldehyde_v3.1.nc",
        "originFiles": False,
        "resolution": "0.25x0.25",
        "resolutionId": 4,
        "scenario": "v3.1",
        "sectors": ["All"],
        "species": ["methyl-bromide","methyl-chloride","methyl-iodide","ch4","co","mbo","acetaldehyde","acetic-acid","acetone","butanes-and-higher-alkanes","butenes-and-higher-alkenes","ethane","ethanol","ethene","formaldehyde","formic-acid","hydrogen-cyanide","isoprene","methanol","other-aldehydes","other-ketones","other-monoterpenes","pinene-a","pinene-b","propane","propene","sesquiterpenes","toluene"],
    }
