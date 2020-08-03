import eel
from typing import List, Tuple
import subprocess, os, platform
import sys

import keyboard
import pyautogui
import pystray
from PIL import Image


from searcher import FileSearchEngine
from utils import sortByFolder
import time
import json

# Type defs
StartSize = Tuple[int, int]
StartPos = Tuple[int, int]
SearchFileRet = List[dict]

class SearchApp:
    def __init__(self, host: str, dev_port: str, port: str, start_size: StartSize, start_pos: StartPos, root_dir: str, prod: bool=True, search_timeout=5.0):
        """Initialize the search app

        Args:
            host (str): The ipadress to host the app
            dev_port: The port the webapp is hosted on (in dev mode)
            port (str): The port to expose (for the websocket)
            start_size (StartSize): The size of the main window when starting up
            start_pos (StartPos): The position on the screen when starting the application
            root_dir (str): The root directory where all searches take place
        """
        self.host = host
        self.dev_port = dev_port
        self.port = port
        self.startSize = start_size
        self.startPosition = start_pos
        self.root_dir = root_dir
        self.search_timeout = search_timeout
        self.file_search = FileSearchEngine(root_dir, search_timeout)

        # The hotkey to use when opening from the background
        self.hotkey = 'ctrl+shift+space'
        self.hotkey_callback = None
        # Set environment (prod/dev)
        self.prod = prod
        # Tray icon
        self.icon_name = "FileSearcher"
        self.icon = None
        if self.prod:
            if getattr(sys, 'frozen', False):
                self.icon_image_path = os.path.join(sys._MEIPASS, "web\\build\\icon.png")
            else:
                self.icon_image_path = "web\\build\\icon.png"
            print(self.icon_image_path)
        else:
            self.icon_image_path = "web\\public\\icon.png"
        self.icon_image = None

        # Socket handling
        self.open_sockets = None

        # Initialize the app
        if self.prod:
            eel.init('web\\build', [".js", ".jsx", ".html"])
        else:
            eel.init('web\\src', [".js", ".jsx", ".html"])

    # !-- LIFECYCLE METHODS --!

    def show(self):
        """ Show is triggered when the hotkey is pressed so it unbinds the hotkey and shows"""
        # Removes the tray icon 
        if self.icon != None:
            self.icon.stop()
        # Unbind the hotkey to avoid conflicts
        keyboard.remove_hotkey(self.hotkey_callback)
        # Show the app
        if self.prod: 
            # In production we show the build page
            eel.show('index.html')
        else:
            # In dev we show the dev server
            eel.show({'port': self.dev_port})
        
    def start(self) -> None:
        """ Start the app, show the window and create all the important bindings. """
        if not self.prod:
            eel.start({'port': self.dev_port}, host=self.host, port=int(self.port), size=self.startSize, blocking=True, close_callback=lambda p,s: self.close_callback(p,s))
        else:
            #eel.start({"file": 'index.html', 'port': 3000}, host=self.host, port=self.port, size=self.startSize, blocking=True, close_callback=lambda p,s: self.close_callback(p,s))
            eel.start('index.html', host=self.host, port=int(self.port), size=self.startSize, blocking=True, close_callback=lambda p,s: self.close_callback(p,s))


    def start_background_process(self, _) -> None:
        """Starts a background process in which we wait for the hotkey to be pressed.
        Note: This method should only be called from self.create_tray_icon()
        Args:
            _ (None): Is required to be passed as in the callback for the icon but is not used
        """
        # Makes the icon visible
        self.icon.visible = True
        # Creates the hotkey and binds self.show() to the trigger
        self.hotkey_callback = keyboard.add_hotkey(self.hotkey, lambda: self.show(), suppress=True)

    def close_callback(self, _, sockets):
        """ Runs the background process when the main window is closed """
        # Save the open sockets so we can correctly close them when needed
        self.open_sockets = sockets 
        # Start the tray icon which then start the background process
        self.create_tray_icon()

    def quit(self):
        """ Remove hotkeys and make sure all sockets are closed """
        print("Quitting the application")
        # Wrap it in an extra try except because some libaries suppress 
        # some errors and try to keep their loop alive
        try:
            try:
                keyboard.remove_all_hotkeys()
            except AttributeError:
                pass
            print("Hotkeys removed")
            # Stop the filewather from the FileSearchEngine
            self.file_search.stop_watcher()
            print("Watchers stopped")
            self.icon.stop()
            print("Removed the icon")
            if not self.open_sockets:
                print("No open sockets")
                self.kill_program()
            # Wait for the sockets to close
            print("Waiting for sockets")
            time.sleep(1)
            self.kill_program()
        except:
            self.kill_program()

    def kill_program(self):
        """ Stops (kills) this program """
        pid = os.getpid()
        if platform.system() == 'Darwin':
            kill_cmd = f"kill -9 {pid}"
        elif platform.system() == "Windows":
            kill_cmd = f"taskkill /F /PID {pid} /T"
        else:
            kill_cmd = f"kill -9 {pid}"
        os.system(kill_cmd)


    def create_tray_icon(self) -> None:
        """ Creates the tray icon and starts the background processes as soon as the icon is created. """
        # Setup the icon
        self.icon = pystray.Icon(self.icon_name, self.load_icon_img(), title=self.icon_name, menu=pystray.Menu(
            pystray.MenuItem(
                "Open FileSearcher",
                lambda: self.show(), # Shows the application on click
                default=True # Default action, so this also gets triggered when clicking on the icon itself
            ),
            pystray.MenuItem(
                "Quit",
                lambda: self.quit() # Quits the application on click
            )
        ))
        # Run the icon and start the background process
        self.icon.run(self.start_background_process)
        

    # !-- SETTINGS --! 

    def update_search_engine(self):
        """ Updates the search engine settings
            Note: it creates a new search engine
        """
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
        """Loads the settings from file_name

        Args:
            file_name (str, optional): The filename pointing to the settings file. Defaults to "settings.json".

        Returns:
            dict: The settings is a dictionary
        """
        if os.path.isfile(file_name):
            with open(file_name, 'r') as f:
                settings = json.load(f)
            return settings
    
        return {}

    # !-- HELPER METHODS --!

    def load_icon_img(self) -> Image:
        """ Load image loads the icon image into self.icon_image """
        # Check if the given path is actually a file and then load the image
        if os.path.isfile(self.icon_image_path):
            self.icon_image = Image.open(self.icon_image_path)
        return self.icon_image    
     

    # !-- EEL EXPOSED METHODS --!

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
    # Get the screen resolution
    s_w, s_h = pyautogui.size()
    # Define the default width and height of the application
    w, h = 1000, 800
    # Calculate the position where the window should be shown
    pos_w, pos_h = ((s_w/2)-(w/2)), ((s_h/2)+(h/2))
    # Check cmd args to see if we are in dev or prod
    prod = not len(sys.argv) == 2 # True if there is an extra arg specified but gets inverted, so extra arg = dev 
    # Create the app
    app = SearchApp('localhost',8080, "3020", (w, h), (pos_w, pos_h), root_dir, prod=prod)
    # Automatically update the settings.
    err = app.update_settings(settings)
    if err != '' :
        print("Error when updating settings:", err)
    # Start the app 
    app.start() # Blocking
    app.quit() # Always make sure that the app closes correctly