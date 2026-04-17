from calendar import month

import cdsapi
import settings
from pathlib import Path
import zipfile

month_dictionary = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

def find_dates_for_download(year,month):
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        days = [1,31]
    elif month == 4 or month == 6 or month == 9 or month == 11:
        days = [1,31]
    elif month == 2:
        if year%4 == 0 and (year%100 != 0 or year%400 == 0):
            days = [1,29]
        else:
            days = [1,28]
    if month < 10:
        dates = f"{year}-0{month}-0{days[0]}/{year}-0{month}-{days[1]}"
    else:
        dates = f"{year}-{month}-0{days[0]}/{year}-{month}-{days[1]}"
    return dates

def initial_fields_api_call(input_data_location, year, month, latitudes, longitudes):
    output_dir = Path(input_data_location)
    downloads_dir  = Path(f"./downloads/EAC4_{year}_{month}")
    downloads_dir.mkdir(exist_ok=True)
    dates = find_dates_for_download(year, month)
    dataset = "cams-global-reanalysis-eac4"
    request = {
        "variable": [
            "carbon_monoxide",
            "ethane",
            "formaldehyde",
            "hydrogen_peroxide",
            "hydrophilic_black_carbon_aerosol_mixing_ratio",
            "hydrophilic_organic_matter_aerosol_mixing_ratio",
            "hydrophobic_black_carbon_aerosol_mixing_ratio",
            "hydrophobic_organic_matter_aerosol_mixing_ratio",
            "isoprene",
            "nitric_acid",
            "nitrogen_dioxide",
            "nitrogen_monoxide",
            "ozone",
            "peroxyacetyl_nitrate",
            "propane",
            "sea_salt_aerosol_0.03-0.5um_mixing_ratio",
            "sea_salt_aerosol_0.5-5um_mixing_ratio",
            "sea_salt_aerosol_5-20um_mixing_ratio",
            "sulphate_aerosol_mixing_ratio",
            "sulphur_dioxide"
        ],
        "model_level": [
            "45",
            "46",
            "47",
            "48",
            "49",
            "50",
            "51",
            "52",
            "53",
            "54",
            "55",
            "56",
            "57",
            "58",
            "59",
            "60"
        ],
        "date": dates,
        "time": [
            "00:00", "03:00", "06:00",
            "09:00", "12:00", "15:00",
            "18:00", "21:00"
        ],
        "data_format": "netcdf_zip",
        "area": [latitudes[1], longitudes[0], latitudes[0], longitudes[1]]    
    }
    target = downloads_dir/f"InitialFields_{year}_{month}.zip"
    client = cdsapi.Client(url=settings.ADS_url, key=settings.ADS_key)
    client.retrieve(dataset, request, target)

    with zipfile.ZipFile(target, 'r') as zip_ref:
            zip_contents = zip_ref.namelist()
            print("Files in zip:", zip_contents)
            zip_ref.extractall(downloads_dir)

    extracted_files = list(downloads_dir.glob(f"*.nc"))
    month_name = month_dictionary[month]
    new_name = f"CAMS_EAC4_{month_name}{year}.nc"
    extracted_files[0].rename(output_dir / new_name) #Rename and move to final directory
    print(f"File saved as: {output_dir / new_name}")

def initial_fields_download(input_data_location, years, month_array, latitudes, longitudes):
    if month_array[0] == 1:
        #Download for December of the previous year, to be sure that all trajectories ending in January can be covered.
        previous_year = years[0]-1
        print(f"Downloading initial fields for Dec {previous_year}")
        initial_fields_api_call(input_data_location, previous_year, 12, latitudes, longitudes)
    for year in years:
        for month in month_array:
            print(f"Downloading initial fields for {month_dictionary[month]} {year}")
            initial_fields_api_call(input_data_location, year, month, latitudes, longitudes)

def download_all(input_data_location, years, month_array, latitudes, longitudes):
    print("\n -------------------------------------------------")
    print("\n -- Downloading data from Atmosphere Data Store --")
    print("\n -------------------------------------------------")
    print("\n Downloading initial gas and particle concentration fields from CAMS global reanalysis")
    #Downloading gas and particle concentrations fields from CAMS global reanalysis
    initial_fields_download(input_data_location, years, month_array, latitudes, longitudes)
    print("\n -------------------------------------------------")
    print("\n ---- Atmosphere Data Store download complete ----")
    print("\n -------------------------------------------------")