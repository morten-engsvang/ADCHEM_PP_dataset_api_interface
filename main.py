#Main driving script for the API interface
#
#
#
#
########################## Imports ###########################
import os

##############################################################


########################## Settings ##########################
#Location to put the input data, it will check if something is still there and if not download it.
input_data_location = "/home/engsvang/programs/ADCHEM_PP_dataset_api_interface/input_test"
#Set the time range for the modelling, restricted to months at the finest resolution.
year_start = 2015
year_end = 2015
month_start = 1
month_end = 12
#Set the spatial range for the modelling, latitude and longitude in degrees.
#Avoid downloading for the entire world if possible. I recommend either northern or southern hemisphere.
latitudes = [0,90] #Negative: southern hemisphere, positive: northern hemisphere
longitudes = [-180,180] #Negative: western hemisphere, positive: eastern hemisphere
##############################################################


########################## Folder creation ##########################





#####################################################################