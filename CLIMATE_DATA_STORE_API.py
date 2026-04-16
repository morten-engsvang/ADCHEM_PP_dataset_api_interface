import cdsapi
import settings

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
        client = cdsapi.Client(url=settings.url, key=settings.key)
        client.retrieve(dataset, request, target)


def download_all(input_data_location, years, month_array, latitudes, longitudes):
    print("\n -------------------------------------------------")
    print("\n --- Downloading data from Climate Data Store ----")
    print("\n -------------------------------------------------")
    print("\n Downloading surface albedo data from ERA5 Land reanalysis")
    surface_albedo_download(input_data_location, years, month_array, latitudes, longitudes)