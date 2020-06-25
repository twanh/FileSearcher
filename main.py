import eel
from typing import List, Tuple
import subprocess, os, platform

from searcher import FileSearchEngine

# Type defs
StartSize = Tuple[int, int]
StartPos = Tuple[int, int]
SearchFileRet = List[dict]

class SearchApp:
    def __init__(self, host: str, port: str, start_size: StartSize, start_pos: StartPos, root_dir: str):
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
        self.file_search = FileSearchEngine(root_dir)
        eel.init('web\src', [".js", ".jsx", ".html"])

    def start(self) -> None:
        eel.start({'port': 3000}, host=self.host, port=self.port, size=self.startSize, blocking=False)

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
        return app.file_search.simple_search(search_query, ret_dic=True)

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

if __name__ == "__main__":
    # Create the search app
    app = SearchApp('localhost', "3020", (1000, 800), (0, 0), "D:\GDrive\School 19_20")
    # Start the app
    app.start()
    # Loop so the app does not autoclose
    while True:
        eel.sleep(1.0)