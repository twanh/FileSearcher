install-interface:
	@echo "Installing interface dependencies"
	cd web/ ;	npm install
	
install-backend:
	@echo "Installing backend dependencies"
	pip3 install -r requirements.txt  
	
install: install-backend install-interface

build-interface:
	@echo "Building the interface"
	cd web/ ; npm run build

build-backend: build-interface
	@echo "Building the application"
	python -m eel main.py web/build --onefile --noconsole --hidden-import pkg_resources.py2_warn
	
build: install build-interface build-backend
	@echo "Build complete!"
