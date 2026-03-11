run:
	@.venv/ADCHEM/bin/python main.py

setup: setup_virtualenv setup_passwords

setup_virtualenv:
	python3 -m venv .venv/ADCHEM
	.venv/ADCHEM/bin/python -m pip install -r requirements.txt
	.venv/ADCHEM/bin/python -m playwright install

setup_passwords:
	@echo "#This file contains the login information after setup" > settings.py
	@echo "----------------------------------"
	@echo "------Start of password setup-----"
	@echo "----------------------------------"
	@echo "Please enter username and password for the eccad website"; \
	read -p "Username: " username; \
	read -p "Password: " password; \
	echo "#ECCAD login_information" >> settings.py; \
	echo "ECCAD_USERNAME=\"$$username\"" >> settings.py; \
	echo "ECCAD_PASSWORD=\"$$password\"" >> settings.py; \
	chmod 700 settings.py
   
clean:
	rm -rf downloads
	rm -rf input_test

cleanall:
	rm -rf .venv/ADCHEM
	rm -rf input_test
	rm -rf downloads
	rm settings.py