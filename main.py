import eel
from typing import List, Tuple

from searcher import FileSearchEngine

# Type defs
StartSize = Tuple[int, int]
StartPos = Tuple[int, int]

SearchFileRet = List[dict]

# Structire
# [{name: ..., path: ..., type: ...}]

s = FileSearchEngine('D:\GDrive\School 19_20')

@eel.expose("search_file")
def search_file(filename: str) -> str:
    print('Searching for files')
    res = s.simple_search(filename)
    resDicts = []
    for i in res:
        resDicts.append(i.__dict__)
    print(res)
    return resDicts
    


class SearchApp:
    def __init__(self, host: str, port: str, start_size: StartSize, start_pos: StartPos):
        self.host = host
        self.port = port
        self.startSize = start_size
        self.startPosition = start_pos
        eel.init('src', [".js", ".jsx", ".html"])

    def start(self) -> None:
        eel.start({'port': 3000}, host=self.host, port=self.port, size=self.startSize, blocking=False)


if __name__ == "__main__":
    # app = SearchApp('localhost', "3020", (1280, 800), (0, 0))
    # app.start()
    print('Setup')
    eel.init('web\src', [".js", ".jsx", ".html"])
    eel.start({'port': 3000}, host='localhost', port="3020", size=(1000, 700), block=False)
    print('Started...')
    eel.spawn(search_file, 'test')
    while True:
        eel.sleep(1.0)