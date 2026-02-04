import pyglet as py
from pyglet.window import key, mouse

window = py.window.Window(750, 500)


@window.event 
def on_key_press(symbol, modifier):
    if symbol == key.A:
        print("A")



if __name__ == "__main__":
    py.app.run()
    
