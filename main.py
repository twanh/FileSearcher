import eel

from typing import Tuple

# Type defs
StartSize = Tuple[int, int]
StartPos = Tuple[int, int]


class SearchApp:
    def __init__(self, host: str, port: str, start_size: StartSize, start_pos: StartPos):
        self.host = host
        self.port = port
        self.startSize = start_size
        self.startPosition = start_pos
        eel.init('src', [".js", ".jsx", ".html"])

    def start(self) -> None:
        eel.start({'port': 3000}, host=self.host, port=self.port, size=self.startSize)

if __name__ == "__main__":
    app = SearchApp('localhost', "3020", (1280, 800), (0,0))
    app.start()
