import os
from dataclasses import dataclass
from typing import List, Dict
import glob


class FileTypes:
    # File extensions
    document_ext = ['docx', 'doc', 'odt', 'pdf', 'gdoc', 'xls', 'xlsx', 'ods', 'ppt', 'pptx', 'md', 'gslides', 'gsheets']
    image_ext = ['gif', 'png', 'jpg', 'jpeg', 'webp', 'tiff', 'psd', 'ai']

    # Names
    directory = 'dir'
    document = 'doc'
    image = 'img'
    other = 'any'

    def get_file_type(self, path: str) -> str:
        if os.path.isdir(path): 
            return self.directory
        filename, ext = os.path.splitext(path)
        if ext in self.document_ext:
            return self.document
        if ext in self.image_ext:
            return self.image
        return self.other



    
@dataclass
class SearchResult:
    name: str
    path: str
    file_type: str


class Searcher:
    """ Searcher search the given root directory for matches with the given query. """
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.file_types = FileTypes()

    def basic_search(self, query: str) -> List[Dict]:

        


        return res
        

    def advanced_search(self, query: str, opts: dict):
        raise NotImplementedError

