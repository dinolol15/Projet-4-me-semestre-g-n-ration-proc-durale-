"""
Programme gérant l'affichage 

auteur : Adrien Buschbeck
"""


import pyglet
from pyglet.window import key
from key_handler import KeyHandler
import matrix_manager



if __name__ == "__main__":
    window = pyglet.window.Window()
    #window.set_fullscreen(True)
    window.activate()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.A:
            print("a")
            

    pyglet.app.run()

