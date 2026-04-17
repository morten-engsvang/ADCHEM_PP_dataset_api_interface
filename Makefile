run:
	@.venv/ADCHEM/bin/python main.py

setup: setup_virtualenv setup_passwords setup_api

setup_virtualenv:
	python3.9 -m venv .venv/ADCHEM
	.venv/ADCHEM/bin/python -m pip install --upgrade pip
	.venv/ADCHEM/bin/python -m pip install -r requirements.txt
	.venv/ADCHEM/bin/python -m playwright install

setup_passwords:
	@echo "#This file contains the login information after setup" > settings.py
	@chmod 700 settings.py
	@echo "----------------------------------"
	@echo "------Start of password setup-----"
	@echo "----------------------------------"
	@echo "Please enter username and password for the eccad website"; \
	read -p "Username: " username; \
	read -p "Password: " password; \
	echo "#ECCAD login_information" >> settings.py; \
	echo "ECCAD_USERNAME=\"$$username\"" >> settings.py; \
	echo "ECCAD_PASSWORD=\"$$password\"" >> settings.py

setup_api:
	@echo "Creating API key for the Climate Data Store API"
	@echo "Please enter the key which can be found on the website after login: https://cds.climate.copernicus.eu/how-to-api under 1. setup the CDS Api key"
	read -p "url: " url; \
	read -p "key: " key; \
	echo "#Climate Data Store API key" > ~/settings.py; \
	echo "CDS_url=\"$$url\"" >> ~/settings.py; \
	echo "CDS_key=\"$$key\"" >> ~/settings.py
	@echo "Creating API key for the Atmosphere Data Store API"
	@echo "Please enter the key which can be found on the website after login: https://ads.atmosphere.copernicus.eu/how-to-api under 1. setup the CDS Api key"
	read -p "url: " url; \
	read -p "key: " key; \
	echo "#Atmosphere Data Store API key" > ~/settings.py; \
	echo "ADS_url=\"$$url\"" >> ~/settings.py; \
	echo "ADS_key=\"$$key\"" >> ~/settings.py

clean:
	rm -rf downloads

clean_data:
	rm -rf downloads
	rm -rf input_test

cleanall:
	rm -rf .venv/ADCHEM
	rm -rf input_test
	rm -rf downloads
	rm settings.py