import eel

def startup():
    eel.init('src', [".js", ".jsx", ".html"])
    eel.start({'port': 3000}, host='localhost', port="3020", size=(1280, 800))

if __name__ == '__main__':
    startup()
    