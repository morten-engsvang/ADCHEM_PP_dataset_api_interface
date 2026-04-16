#Main driving script for the API interface
#
#
#
#
########################## Imports ###########################
import os
import CAMS_API

##############################################################


########################## Settings ##########################
#Location to put the input data, it will check if something is still there and if not download it.
input_data_location = "/home/engsvang/programs/ADCHEM_PP_dataset_api_interface/input_test"
#Set the time range for the modelling, restricted to months at the finest resolution.
years = [2019] #List of years to download for
month_range = [1,12] #List of months to include, if in doubt include all months.
#Set the spatial range for the modelling, latitude and longitude in degrees.
#Avoid downloading for the entire world if possible. I recommend either northern or southern hemisphere.
latitudes = [0,90] #Negative: southern hemisphere, positive: northern hemisphere
longitudes = [-180,180] #Negative: western hemisphere, positive: eastern hemisphere
##############################################################


########################## Folder creation ##########################
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
    "months": month_range,
    "latitudes": latitudes,
    "longitudes": longitudes
}
# Maybe I should do some error checking here, e.g. if lat long is in the correct sequence
#####################################################################

########################## Call subscripts ##########################
#Calling subscripts for the API calls, in addition they check if the data is already present
#CAMS do not have a true API, you have to manually request datasets to get the links.
CAMS_API.CAMS_download(input_data_location+"/CAMS",years,latitudes,longitudes)

#####################################################################