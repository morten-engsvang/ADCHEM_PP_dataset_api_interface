import os

def download_emission_factors(input_data_location):
    url = "https://www.geo.vu.nl/~gwerf/GFED/GFED4/ancill/GFED4_Emission_Factors.txt"
    output = f"{input_data_location}/GFED4_Emission_Factors.txt"
    command = f"curl {url} --output {output}"
    print(command)
    os.system(command)

def download_fire_data(input_data_location, year):
    if year >= 2017:
        suffix = "_beta"
    else:
        suffix = ""
    url = f"https://www.geo.vu.nl/~gwerf/GFED/GFED4/GFED4.1s_{year}{suffix}.hdf5"
    output = f"{input_data_location}/GFED4.1s_{year}.hdf5"
    command = f"curl {url} --output {output}"
    print(command)
    os.system(command)

def GFED_download(years, input_data_location):
    print("\n -------------------------------------------------")
    print("\n --------------- GFED4 download started ----------")
    print("\n -------------------------------------------------")
    download_emission_factors(input_data_location)
    for year in years:
        download_fire_data(input_data_location, year)
    print("\n -------------------------------------------------")
    print("\n --------------- GFED4 download done -------------")
    print("\n -------------------------------------------------")