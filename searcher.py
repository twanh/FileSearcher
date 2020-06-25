import json
import os
from dataclasses import dataclass
from typing import Dict, List

from utils import getFileType


@dataclass
class SearchResult:
    """SearchResult is a dataclass that stores an individual search result
    Args:
        name (str): The name of the file (excluding the extension)
        path (str): The full path of the file
        file_type (str): The type of the file as specified in utils.FileTypes
    """
    name: str
    path: str
    file_type: str


class FileSearchEngine:
    """ FileSearchengine will index, and allow searching in the root_dir. """
    
    def __init__(self, root_dir: str, watch_timeout: int = 1, save_file: str = ''):
        """Initializes the FileSearchEngine with the root_path, the watch_timeout and the save_file

        Args:
            root_dir (str): The directory in which all searches should take place.
            watch_timeout (int, optional): The time to wait between (re)indexing the root_dir (used for the filewatcher). Defaults to 1
            save_file? (str, optional): The filename to save the index folder structure to. Defaults to the root_dir

        Raises:
            FileNotFoundError: If the root_directory specified does not exist

        Todo:
            * Implement the firlewatcher and have it re-index the root_dir on change.
        """

        # The directory in which all searches happen
        if not os.path.isdir(root_dir):
            raise FileNotFoundError
        self.root_dir = root_dir
        # The index stores the current folder/file structure
        self.index = []
        # Watch timeout. (min)
        self.timeout = watch_timeout
        # Check if a save_file was provided
        
        if save_file == '':
            clear = root_dir.lower().replace(" ", "_").replace("\\", "_").replace("/", "_")
            self.save_file = f'{clear}.json'
            print('new savefile ', self.save_file)
        else:
            self.save_file = save_file

        # Check if there is a index file otherwise create one.
        self.load_or_create_index()

    def load_or_create_index(self) -> None:
        """Checks if the index save file exists and if it does loads it, otherwise it will generate a new one and save it"""

        # Check if the file exists, it is a double check because in load_index we check again.
        # But it is not a costly opperation an it avoids the FileNotFoundError
        if os.path.isfile(os.path.join(os.getcwd(), self.save_file)):
            self.load_index() # Loads the index if the file exists
        else:
            # If the file does not exists create a new one and save it
            self.create_index()
            self.save_index()
    

    def load_index(self) -> None:
        """Loads the file index from self.save_file

        Raises:
            FileNotFoundError: If the provided save_file does not exists 
        """ 

        # Create the full path
        file_path = os.path.join(os.getcwd(), self.save_file)
        # Check if the file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError        
        try:    
            with open(file_path, 'r') as f:
                self.index = json.load(f)
        except:
            self.index = []


    def create_index(self) -> None:
        """Creates the index from the root directory"""
        # Loop trough everyfile and folder using os.walk and store all the files
        self.index = [[(root, dirs, files) for root, dirs, files in os.walk(self.root_dir)]]
    

    def save_index(self) -> None:
        """Saves the current index to the save_file in the current working directory"""
        # Create the full path
        file_path = os.path.join(os.getcwd(), self.save_file) 
        try:    
            with open(file_path, 'w') as f:
                json.dump(self.index, f, indent=4)
        except:
            #TODO:Implement loggin.
            pass

    def simple_search(self, query: str) -> List[SearchResult]:
        """Does a 'simple' search for the provided query in the root directory. 
        Simple in this case means that all the files and directories are matched against the query, there is no filtering or anything.

        Args:
            query (str): The query to search for

        Returns:
            List[SearchResult]: The results of the search
        """
        results: List[SearchResult] = []
        print(len(self.index))

        # Loop through everyitem in the index
        for item in self.index:
            # The index is generated with os.walk, so every item will have path, dirs and files in a tuple
            for path, dirs, files  in item:    
                # Loop trough the files and check if any of them match
                for file in files:    
                    # We use lower case here because it is a simple search, the aim is to quickly find matching files
                    if query.lower() in file.lower():
                        # If there is a match extract the needed data 
                        name, ext = os.path.splitext(file)
                        path = os.path.join(path, file)
                        file_type = getFileType(path)
                        # Create a searchresult and add it to the results list
                        res = SearchResult(name=name, path=path, file_type=file_type)
                        results.append(res)
                # Loop trough the directories and check if any of them match
                for direc in dirs:
                    if query.lower() in direc.lower():
                        name = direc
                        path = os.path.join(path, direc)
                        file_type = getFileType(path)
                        res = SearchResult(name=name, path=path, file_type=file_type)
                        results.append(res)
        return results

    def advanced_search(self, query: str, opts: dict):
        raise NotImplementedError