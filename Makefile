install-interface:
	cd web/ && npm install

install-backend:
	pip3 install -r requirements.txt  
	
install: install-backend install-interface

run-interface: 
	cd web/ && npm start

run-backend:
	python3 main.py

run: run-interface run-backend
