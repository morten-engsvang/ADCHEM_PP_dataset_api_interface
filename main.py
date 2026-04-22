#Main driving script for the API interface
#
#
#
#
########################## Imports ###########################
import os
import numpy as np
import ATMOSPHERE_DATA_STORE_API
import CAMS_API
import meteorology_download
import CLIMATE_DATA_STORE_API
import COPERNICUS_MARINE_SERVICE_API
import GFED_download
##############################################################


########################## Settings ##########################
#Location to put the input data, it will check if something is still there and if not download it.
input_data_location = "/home/engsvang/programs/ADCHEM_PP_dataset_api_interface/input_test"
#Set the time range for the modelling, restricted to months at the finest resolution.
years = [2019] #List of years to download for
month_array = np.arange(1,2) #List of months to include (if december is to be included write 13 instead of 12), if in doubt include all months (1,13)
#Set the spatial range for the modelling, latitude and longitude in degrees.
#Avoid downloading for the entire world if possible. I recommend either northern or southern hemisphere.
latitudes = [0,90] #Negative: southern hemisphere, positive: northern hemisphere
longitudes = [-180,180] #Negative: western hemisphere, positive: eastern hemisphere
##############################################################

####################### Test Settings ########################
MET_DOWNLOAD = False
CAMS_DOWNLOAD = False
CLIMATE_DATA_STORE_DOWNLOAD = False
ATMOSPHERE_DATA_STORE_DOWNLOAD = False
COPERNICUS_MARINE_SERVICE_DOWNLOAD = False
GFED_DOWNLOAD = False

##############################################################

########################## Folder creation ##########################
if not os.path.exists(input_data_location+"/meteorology"):
    os.makedirs(input_data_location+"/meteorology")
else:
    print("Meteorology folder already exists, skipping creation.")

folders = ["CAMS","CAMS_conc_fields","CMS_ocean_products","Country_index","ERA5","GAINS_ECLIPSEv5_PN","GFED4_fire_emissions","GLOBALCover","HTAPv3"]
for folder in folders:
    if not os.path.exists(input_data_location+"/"+folder):
        os.makedirs(input_data_location+"/"+folder)
    else:
        print(folder+" folder already exists, skipping creation.")
#####################################################################

########################## Preprocessing ############################
ranges = {
    "years": years,
    "months": month_array,
    "latitudes": latitudes,
    "longitudes": longitudes
}
# Maybe I should do some error checking here, e.g. if lat long is in the correct sequence
#####################################################################

########################## Call subscripts ##########################
#Calling subscripts for the API calls, in addition they check if the data is already present
#First get the meteorological data needed for preprocessing. It is likely that the user already had it when they ran the HYSPLIT trajectories
if MET_DOWNLOAD:
    meteorology_download.meteorology_download(input_data_location+"/meteorology", years, month_array)

#CAMS do not have a true API, you have to manually request datasets to get the links.
if CAMS_DOWNLOAD:
    CAMS_API.CAMS_download(input_data_location+"/CAMS",years,latitudes,longitudes)

if CLIMATE_DATA_STORE_DOWNLOAD:
    CLIMATE_DATA_STORE_API.download_all(input_data_location,years,month_array,latitudes,longitudes)

if ATMOSPHERE_DATA_STORE_DOWNLOAD:
    ATMOSPHERE_DATA_STORE_API.download_all(input_data_location,years,month_array,latitudes,longitudes)

if COPERNICUS_MARINE_SERVICE_DOWNLOAD:
    COPERNICUS_MARINE_SERVICE_API.download_all(input_data_location,years,month_array,latitudes,longitudes)

if GFED_DOWNLOAD:
    GFED_download.GFED_download(years, input_data_location)

#####################################################################