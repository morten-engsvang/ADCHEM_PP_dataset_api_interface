import copernicusmarine
import settings

def global_ocean_biogeo_hindcast(input_data_location, year, month, latitudes, longitudes):
    print("\n Global Dataset.\n")
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_bgc_my_0.25deg_P1M-m",
        #dataset_version="202406", aka. take the newest version, previous versions are not available.
        variables=["no3", "nppv", "ph"],
        minimum_longitude=longitudes[0],
        maximum_longitude=longitudes[1],
        minimum_latitude=latitudes[0],
        maximum_latitude=latitudes[1],
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        #Set to only download water column surface data
        minimum_depth=0.5057600140571594,
        maximum_depth=0.5057600140571594,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"mercatorfreebiorys2v4_global_mean_{year}{month:02d}.nc"
    )

def atlantic_iberian_biscay_irish_ocean_biogeo_hindcast(input_data_location, year, month):
    print("\n Atlantic Iberian Biscay Irish Ocean Biogeochemistry Hindcast.\n")
    copernicusmarine.subset(
        dataset_id="cmems_mod_ibi_bgc-car_my_0.027deg_P1M-m",
        variables=["ph"],
        minimum_longitude=-19.082841873168945,
        maximum_longitude=5.084567070007324,
        minimum_latitude=26.16535758972168,
        maximum_latitude=56.082942962646484,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0.4940253794193268,
        maximum_depth=0.4940253794193268,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"CMEMS_IBI_BIO_PH_mean_{year}{month:02d}.nc"
    )
    copernicusmarine.subset(
        dataset_id="cmems_mod_ibi_bgc-nut_my_0.027deg_P1M-m",
        variables=["nh4", "no3"],
        minimum_longitude=-19.082841873168945,
        maximum_longitude=5.084567070007324,
        minimum_latitude=26.16535758972168,
        maximum_latitude=56.082942962646484,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0.4940253794193268,
        maximum_depth=0.4940253794193268,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"CMEMS_IBI_BIO_NH4_NO3_mean_{year}{month:02d}.nc"
    )
    copernicusmarine.subset(
        dataset_id="cmems_mod_ibi_bgc-plankton_my_0.027deg_P1M-m",
        variables=["nppv"],
        minimum_longitude=-19.082841873168945,
        maximum_longitude=5.084567070007324,
        minimum_latitude=26.16535758972168,
        maximum_latitude=56.082942962646484,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0.4940253794193268,
        maximum_depth=0.4940253794193268,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"CMEMS_IBI_BIO_NPPV_mean_{year}{month:02d}.nc"
    )

def baltic_sea_biogeo_reanalysis(input_data_location, year, month):
    print("\n Baltic Sea Biogeochemistry Reanalysis.\n")
    copernicusmarine.subset(
        dataset_id="cmems_mod_bal_bgc_my_P1M-m",
        variables=["nh4", "no3", "nppv", "ph"],
        minimum_longitude=9.041542053222656,
        maximum_longitude=30.207401275634766,
        minimum_latitude=53.008296966552734,
        maximum_latitude=65.8909912109375,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0.5016462206840515,
        maximum_depth=0.5016462206840515,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"BAL-MYP-ERGOM_BGC-MonthlyMeans-{year}{month:02d}.nc"
    )

def mediterranean_sea_biogeo_reanalysis(input_data_location, year, month):
    print("\n Mediterranean Sea Biogeochemistry Reanalysis.\n")
    copernicusmarine.subset(
        dataset_id="cmems_mod_med_bgc-nut_my_4.2km_P1M-m",
        variables=["nh4", "no3"],
        minimum_longitude=-5.541666507720947,
        maximum_longitude=36.29166793823242,
        minimum_latitude=30.1875,
        maximum_latitude=45.97916793823242,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=1.0182366371154785,
        maximum_depth=1.0182366371154785,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"{year}{month:02d}01_m-OGS--NUTR-MedBFM3-MED_re.nc"
    )

def atlantic_european_north_west_shelf_biogeo_reanalysis(input_data_location, year, month):
    print("\n Atlantic European North West Shelf Biogeochemistry Reanalysis.\n")
    copernicusmarine.subset(
        dataset_id="cmems_mod_nws_bgc-ph_my_7km-3D_P1M-m",
        variables=["ph"],
        minimum_longitude=-19.88888931274414,
        maximum_longitude=12.999670028686523,
        minimum_latitude=40.06666946411133,
        maximum_latitude=65.00125122070312,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0,
        maximum_depth=0,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"metoffice_foam1_amm7_NWS_PHPH_mm{year}{month:02d}.nc"
    )
    copernicusmarine.subset(
        dataset_id="cmems_mod_nws_bgc-pp_my_7km-3D_P1M-m",
        variables=["nppv"],
        minimum_longitude=-19.88888931274414,
        maximum_longitude=12.999670028686523,
        minimum_latitude=40.06666946411133,
        maximum_latitude=65.00125122070312,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0,
        maximum_depth=0,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"metoffice_foam1_amm7_NWS_PPRD_mm{year}{month:02d}.nc"
    )
    copernicusmarine.subset(
        dataset_id="cmems_mod_nws_bgc-no3_my_7km-3D_P1M-m",
        variables=["no3"],
        minimum_longitude=-19.88888931274414,
        maximum_longitude=12.999670028686523,
        minimum_latitude=40.06666946411133,
        maximum_latitude=65.00125122070312,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0,
        maximum_depth=0,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"metoffice_foam1_amm7_NWS_NITR_mm{year}{month:02d}.nc"
    )

def arctic_ocean_biogeo_reanalysis(input_data_location, year, month):
    print("\n Arctic Ocean Biogeochemistry Reanalysis.\n")
    copernicusmarine.subset(
        dataset_id="cmems_mod_arc_bgc_my_ecosmo_P1M",
        variables=["no3", "nppv"],
        minimum_longitude=-180,
        maximum_longitude=179.75,
        minimum_latitude=43.5,
        maximum_latitude=90,
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0,
        maximum_depth=0,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"{year}{month:02d}_mm-NERSC-MODEL-ECOSMO-ARC-RAN.nc"
    )

def sea_ice_cover(input_data_location, year, month, latitudes, longitudes):
    print("\n Sea Ice Cover.\n")
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_phy-all_my_0.25deg_P1M-m",
        variables=["siconc_cglo"],
        minimum_longitude=longitudes[0],
        maximum_longitude=longitudes[1],
        minimum_latitude=latitudes[0],
        maximum_latitude=latitudes[1],
        start_datetime=f"{year}-{month:02d}-01T00:00:00",
        end_datetime=f"{year}-{month:02d}-01T00:00:00",
        minimum_depth=0.5057600140571594,
        maximum_depth=0.5057600140571594,
        coordinates_selection_method="strict-inside",
        netcdf_compression_level=1,
        disable_progress_bar=True,
        username=settings.CMS_USERNAME,
        password=settings.CMS_PASSWORD,
        output_directory=input_data_location,
        output_filename=f"cmems_mod_glo_phy-all_my_0.25deg_P1M-m-{year}{month:02d}.nc"
    )

def download_all(input_data_location, years, month_array, latitudes, longitudes):
    print("\n ---------------------------------------------------")
    print("\n - Downloading data from Copernicus Marine Service -")
    print("\n ---------------------------------------------------")
    if month_array[0] == 1:
        previous_year = years[0] - 1
        prev_year_flag = True
    print("\n Downloading ocean surface values, monthly means unless specified.")
    print("\n From Global Ocean Biogeochemistry Hindcast: pH, NO3 and net primary production of biomass (nppv)")
    print("\n From Atlantic-Iberian Biscay Irish- Ocean BioGeoChemistry NON ASSIMILATIVE Hindcast climatology subset: pH, NO3, NH4, nppv")
    print("\n From Baltic Sea Biogeochemistry Reanalysis: pH, NO3, NH4, nppv")
    print("\n From Mediterranean Sea Biogeochemistry Reanalysis: NO3, NH4. Don't know why we don't use pH and nppv (legacy from Pontus)")
    print("\n From Atlantic- European North West Shelf- Ocean Biogeochemistry Reanalysis: pH, NO3, nppv")
    print("\n From Arctic Ocean Biogeochemistry Reanalysis: NO3, nppv. However this dataset is currently not used due to a lack of variables\n")

    if prev_year_flag:
        global_ocean_biogeo_hindcast(input_data_location, previous_year, 12, latitudes, longitudes)
        atlantic_iberian_biscay_irish_ocean_biogeo_hindcast(input_data_location, previous_year, 12)
        baltic_sea_biogeo_reanalysis(input_data_location, previous_year, 12)
        mediterranean_sea_biogeo_reanalysis(input_data_location, previous_year, 12)
        atlantic_european_north_west_shelf_biogeo_reanalysis(input_data_location, previous_year, 12)
        arctic_ocean_biogeo_reanalysis(input_data_location, previous_year, 12)
        sea_ice_cover(input_data_location, previous_year, 12, latitudes, longitudes)
    for year in years:
        for month in month_array:
            global_ocean_biogeo_hindcast(input_data_location, year, month, latitudes, longitudes)
            atlantic_iberian_biscay_irish_ocean_biogeo_hindcast(input_data_location, year, month)
            baltic_sea_biogeo_reanalysis(input_data_location, year, month)
            mediterranean_sea_biogeo_reanalysis(input_data_location, year, month)
            atlantic_european_north_west_shelf_biogeo_reanalysis(input_data_location, year, month)
            arctic_ocean_biogeo_reanalysis(input_data_location, year, month)
            sea_ice_cover(input_data_location, year, month, latitudes, longitudes)
    print("\n ---------------------------------------------------")
    print("\n -- Download from Copernicus Marine Service done ---")
    print("\n ---------------------------------------------------")