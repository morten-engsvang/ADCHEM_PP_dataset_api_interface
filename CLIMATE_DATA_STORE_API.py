import cdsapi
import settings
from pathlib import Path
import zipfile

def surface_albedo_download(input_data_location, years, month_array, latitudes, longitudes):
    if month_array[0] == 1:
        previous_year = years[0] - 1
    download_years = years + [previous_year]
    for year in download_years:
        dataset = "reanalysis-era5-land-monthly-means"
        request = {
            "product_type": ["monthly_averaged_reanalysis_by_hour_of_day"],
            "variable": ["forecast_albedo"],
            "year": str(year),
            "month": [
                "01", "02", "03",
                "04", "05", "06",
                "07", "08", "09",
                "10", "11", "12"
            ],
            "time": [
                "00:00", "01:00", "02:00",
                "03:00", "04:00", "05:00",
                "06:00", "07:00", "08:00",
                "09:00", "10:00", "11:00",
                "12:00", "13:00", "14:00",
                "15:00", "16:00", "17:00",
                "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00"
            ],
            "data_format": "netcdf",
            "download_format": "unarchived",
            "area": [latitudes[1], longitudes[0], latitudes[0], longitudes[1]]
        }
        target = input_data_location+"/Albedo_surface_" + str(year) + ".nc"
        client = cdsapi.Client(url=settings.CDS_url, key=settings.CDS_key)
        client.retrieve(dataset, request, target)

def sea_surface_temperature_download(input_data_location, years, month_array, latitudes, longitudes):
    if month_array[0] == 1:
        previous_year = years[0] - 1
    download_years = years + [previous_year]
    for year in download_years:
        dataset = "reanalysis-era5-single-levels-monthly-means"
        request = {
            "product_type": ["monthly_averaged_reanalysis_by_hour_of_day"],
            "variable": ["sea_surface_temperature"],
            "year": str(year),
            "month": [
                "01", "02", "03",
                "04", "05", "06",
                "07", "08", "09",
                "10", "11", "12"
            ],
            "time": [
                "00:00", "01:00", "02:00",
                "03:00", "04:00", "05:00",
                "06:00", "07:00", "08:00",
                "09:00", "10:00", "11:00",
                "12:00", "13:00", "14:00",
                "15:00", "16:00", "17:00",
                "18:00", "19:00", "20:00",
                "21:00", "22:00", "23:00"
            ],
            "data_format": "netcdf",
            "download_format": "unarchived",
            "area": [latitudes[1], longitudes[0], latitudes[0], longitudes[1]]
        }
        target = input_data_location+"/ERA5_SST_monthly_" + str(year) + ".nc"
        client = cdsapi.Client(url=settings.url, key=settings.key)
        client.retrieve(dataset, request, target)

def download_land_cover(input_data_location, downloads_dir, years, month_array, latitudes, longitudes):
    output_dir = Path(input_data_location)
    if month_array[0] == 1:
        previous_year = years[0] - 1
    download_years = years + [previous_year]
    for year in download_years:
        if year <= 2015:
            dataset_version = "v2_0_7cds"
        else: 
            dataset_version = "v2_1_1"
        dataset = "satellite-land-cover"
        request = {
            "variable": "all",
            "year": str(year),
            "version": dataset_version,
            "area": [latitudes[1], longitudes[0], latitudes[0], longitudes[1]]
        }
        target = downloads_dir/f"LandCover_{year}.zip"
        client = cdsapi.Client(url=settings.CDS_url, key=settings.CDS_key)
        client.retrieve(dataset, request, target)

        with zipfile.ZipFile(target, 'r') as zip_ref:
            zip_contents = zip_ref.namelist()
            print("Files in zip:", zip_contents)
            zip_ref.extractall(output_dir)

        extracted_files = list(output_dir.glob(f"*LC-L4-LCCS-Map-300m-P1Y-{year}-*.nc"))
        new_name = f"GLOBAL-COVER-LC-L4-LCCS-Map-300m-P1Y-{year}-{dataset_version}.nc"
        extracted_files[0].rename(output_dir / new_name)
        print(f"File saved as: {output_dir / new_name}")

def download_all(input_data_location, years, month_array, latitudes, longitudes):
    print("\n -------------------------------------------------")
    print("\n --- Downloading data from Climate Data Store ----")
    print("\n -------------------------------------------------")
    print("\n Downloading surface albedo data from ERA5 Land reanalysis")
    #First download surface albedo data for the relevant years.
    surface_albedo_download(input_data_location, years, month_array, latitudes, longitudes)
    #Then download sea surface temperature data for the relevant years.
    print("\n Downloading sea surface temperature data from ERA5 reanalysis") 
    sea_surface_temperature_download(input_data_location, years, month_array, latitudes, longitudes)
    #Then download land cover data for the relevant years
    downloads_dir  = Path("./downloads")
    downloads_dir.mkdir(exist_ok=True)
    print("\n Downloading land cover data from satellite land cover dataset")
    download_land_cover(input_data_location, downloads_dir, years, month_array, latitudes, longitudes)
    print("\n -------------------------------------------------")
    print("\n ------ Climate Data Store download complete -----")
    print("\n -------------------------------------------------")