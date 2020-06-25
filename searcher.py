import os
from dataclasses import dataclass
from typing import List, Dict
import glob

    
@dataclass
class SearchResult:
    name: str
    path: str
    file_type: str


class SearchEngine:
    """ Search engine will index, and allow searching in the root_dir. """
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.file_types = FileTypes()

    def basic_search(self, query: str) -> List[Dict]:

        res = glob.glob(self.root_dir + '/**/*')


        return res
        

    def advanced_search(self, query: str, opts: dict):
        raise NotImplementedError

