# FileSearcher
FileSearcher takes away the struggle of having to open a new explorer window and navigate slowly to a file or directory!

### Motivation for building File Searcher
When working on school projects I frequently have to open summaries, research, notes, etc... But searching for these files in windows explorer takes ages because it searches the whole file system and it usually does not even find the correct file or folder. File Searcher has one root folder it will search, so for my purpose I set it to the folder I store all my school files in.



## Install
### In development:
Use the makefile to install all dependencies.
  ```
  $ make install
  ```
This command install the dependencies for the backend and the interface.  
*Note: If `make` is not installed on your system run the following commands:*
```
$ pip install -r requirements.txt
$ cd web/
$ npm install
```

## Usage
### In development:
To run the app in development you need to have the interface (=frontend) development server running **before** you run the main application.  

So first run:
```
$ npm start 
```
Then run:
```
$ python main.py dev
```
The `dev` argument can be anything, we check if we are in development by checking the length of the arguments provided.

### In production (actually using the app)
Install the application and then run the main.exe

## Build
To build the app simply run:
```
$ make build
```
If you do not have make installed, you can follow the steps described in the `Makefile`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

