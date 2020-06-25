import eel
from typing import List, Tuple
import subprocess, os, platform
import sys

import keyboard

from searcher import FileSearchEngine
from utils import sortByFolder
import time
import json

# Type defs
StartSize = Tuple[int, int]
StartPos = Tuple[int, int]
SearchFileRet = List[dict]

class SearchApp:
    def __init__(self, host: str, port: str, start_size: StartSize, start_pos: StartPos, root_dir: str, search_timeout=5.0):
        """Initialize the search app

        Args:
            host (str): The ipadress to host the app
            port (str): The port to expose
            start_size (StartSize): The size of the main window when starting up
            start_pos (StartPos): The position on the screen when starting the application
            root_dir (str): The root directory where all searches take place
        """
        self.host = host
        self.port = port
        self.startSize = start_size
        self.startPosition = start_pos
        self.root_dir = root_dir
        self.search_timeout = search_timeout
        self.file_search = FileSearchEngine(root_dir, search_timeout)

        # The hotkey to use when opening from the background
        self.hotkey = 'ctrl+shift+space'
        self.hotkey_callback = None

        # Socket handling
        self.open_sockets = None

        # Initialize the app
        eel.init('web\src', [".js", ".jsx", ".html"])

    def show(self):
        """ Show is triggered when the hotkey is pressed so it unbinds the hotkey and shows"""
        # Unbind the hotkey to avoid conflicts
        keyboard.remove_hotkey(self.hotkey_callback)
        # Show the app
        eel.show({'port': 3000})
        
    def start(self) -> None:
        """ Start the app, show the window and create all the important bindings. """
        eel.start({'port': 3000}, host=self.host, port=self.port, size=self.startSize, blocking=True, close_callback=lambda p,s: self.close_callback(p,s))

    def start_background_process(self) -> None:
        """ Starts a background process in which we wait for the hotkey to be pressed. """
        self.hotkey_callback = keyboard.add_hotkey(self.hotkey, lambda: self.show(), suppress=True)

    def close_callback(self, _, sockets):
        """ Runs the background process when the main window is closed """
        # Save the open sockets so we can correctly close them when needed
        self.open_sockets = sockets 
        # Start the background waiting process
        self.start_background_process()

    def quit(self):
        """ Remove hotkeys and make sure all sockets are closed """
        print("Quitting the application")
        keyboard.remove_all_hotkeys()
        print("Hotkeys removed")
        # Stop the filewather from the FileSearchEngine
        self.file_search.stop_watcher()
        print("Watchers stopped")
        if not self.open_sockets:
            print("No open sockets")
            os.system('taskkill /F /IM python.exe /T')
        # Wait for the sockets to close
        print("Waiting for sockets")
        time.sleep(1)
        os.system('taskkill /F /IM python.exe /T')


    def update_search_engine(self):
        self.file_search = FileSearchEngine(self.root_dir, self.search_timeout)

    def save_settings(self, file_name='settings.json', settings={}) -> None:
        """Save the settings to a file

        Args:
            file_name (str, optional): The file to save the settings to. Defaults to 'settings.json'.
            settings (dict, optional): The settings to save. Defaults to the result of get_settings().
        """
        if len(settings) < 1 :
            settings = self.get_settings()
        with open(file_name, 'w') as f:
            json.dump(settings, f)

    @staticmethod
    def load_settings(file_name="settings.json") -> dict:
        if os.path.isfile(file_name):
            with open(file_name, 'r') as f:
                settings = json.load(f)
            return settings
    
        return {}

    ### !-- EEL EXPOSED METHODS --!

    @staticmethod
    @eel.expose("search_file")
    def search_file(search_query: str) -> List[dict]:
        """Search file is exposed to the interface and uses FileSearchEngine to search for the given query
 
        Args:
            search_query (str): The query to search for
        Returns:
            List[dict]: The search results
        """

        # This is a bit hacky, but the method has to be a static method because the javascript
        # does not have access to the class
        # This is if the self.file_search changes for example when the root_dir is changed, we can 
        # still access the correct variable
        return sortByFolder(app.file_search.simple_search(search_query, ret_dic=True))

    @staticmethod
    @eel.expose("open_file")
    def open_file(path: str) -> None: 
        """open_file is exposed to the interface and opens the file or folder specified in the path argument in the associated application

        Args:
            path (str): The path to the file/folder to open
        """
        # Check which operating system the user uses, because both methods do not work on the other os.
        if platform.system() == 'Darwin':
            # If on mac use the mac open terminal command
            subprocess.call(('open', path))
        elif platform.system() == 'Windows': 
            # On windows we can use os.startfile
            os.startfile(path)
        else:
            # Use the linux equivalent of open command
            subprocess.call(('xdg-open', path))

    @staticmethod
    @eel.expose("get_settings")
    def get_settings() -> object:
        """get settings returns the settings of the current app

        Returns:
            Object: Containing the settings.
        """
        settings = {
            "hotkey": app.hotkey,
            "root_dir": app.root_dir,
            "search_timeout": app.search_timeout
        }
        return settings

    @staticmethod
    @eel.expose("update_settings")
    def update_settings(settings: dict) -> str:
        """Save settings saves the settings and calls for a search engine update because it's values may have changed

        Args:
            settings (dict): The settings to update

        Returns:
            str: Error
        """
        error = ""
        # Check if the newly given directory is actually an directory
        if 'root_dir' in settings:
            if os.path.isdir(settings['root_dir']):
                app.root_dir = settings['root_dir']
            else:
                error = "The directory is not valid"
        # Set the hotkey
        if 'hotkey' in settings:
            app.hotkey = settings['hotkey']
        # Set the search timeout
        if 'search_timeout' in settings:
            app.search_timeout = float(settings['search_timeout'])
        # Update the search engine
        app.update_search_engine()
        app.save_settings(settings=settings)
        return error


if __name__ == "__main__":
    # Create the search app
    # Check if there are saved settings
    settings = SearchApp.load_settings('settings.json')
    if 'root_dir' in settings:
        root_dir = settings['root_dir']
    else:
        root_dir = 'D:\GDrive\School 19_20'
    app = SearchApp('localhost', "3020", (1000, 800), (0, 0), root_dir)
    err = app.update_settings(settings)
    if err != '' :
        print("Error when updating settings:", err)
    # Start the app 
    app.start()
    # Loop so the app does not autoclose
    
    app.quit()