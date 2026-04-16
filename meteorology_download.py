import os

month_dictionary = {
    1: "jan",
    2: "feb",
    3: "mar",
    4: "apr",
    5: "may",
    6: "jun",
    7: "jul",
    8: "aug",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "dec"
}

def download_month(MET_DIR,year, month):
    month_name = month_dictionary[month]
    if year >= 2000:
        year_str = str(year-2000)
    else:
        year_str = str(year-1900)
    command = "curl --parallel https://www.ready.noaa.gov/data/archives/gdas1/gdas1." + month_name + year_str + ".w[1-5] --output " + MET_DIR + "/gdas1." + month_name + year_str + ".w#1"
    print("\nDownloading meteorological data for "+month_name+" "+str(year)+". With command:\n")
    print(command)
    os.system(command)

def meteorology_download(MET_DIR,years,months):
    #Function to download meteorological data that corresponds to the trajectories
    #Month_range is going to be generated from the HYSPLIT trajectories, which as standard goes up to two weeks backwards in time.
    #To make it simpler I just download a month back from the earliest trajectory.

    #--------------------------------#
    #Generate the years and months to download
    #--------------------------------#
    #First a check whether we need to download from the previous year, if the month range includes January, we need to download December from the previous year.
    print("\n -------------------------------------------------")
    print("\n --------------- Meteorology started -------------")
    print("\n -------------------------------------------------")
    if months[0] == 1:
        previous_year = years[0] - 1
        download_month(MET_DIR,previous_year, 12)
    #Then download the rest
    for year in years:
        for month in months:
            download_month(MET_DIR, year, month)

    print("\n -------------------------------------------------")
    print("\n --------------- Meteorology done ----------------")
    print("\n -------------------------------------------------")