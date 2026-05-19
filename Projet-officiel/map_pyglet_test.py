import random as ran

import pyglet as py
from pyglet.window import key

import carte as Carte
import matrix_manager as mm



window = py.window.Window()

dimension = (5, 5)
batch = py.graphics.Batch()
shapes = []


@window.event
def on_key_press(symbol, modifier):
    """Docstring"""
    if symbol == key.A:
        print("A was pressed")
        a = input("choix ")
        if a == "1":
            tilemap = Carte.w_f_c_simplified(mm.create_matrix((50, 50),
                                                              {Carte.Water: 1, Carte.Coast: 2}, ))
        else:
            tilemap = Carte.w_f_c_evolved(
                mm.create_matrix((100, 100),{"baba": 2}),
                10,
                [20, 3, Carte.Water],
                6
            )
        print(tilemap)
        dimx = len(tilemap[1])
        dimy = len(tilemap)
        for i in range(dimy):
            for j in range(dimx):
                try:
                    tilemap[i][j].Color
                except AttributeError:
                    continue
                cell = py.shapes.Rectangle(x=50 + j*5,
                                           y=600 + i*(-5),
                                           width=5,
                                           height=5,
                                           color=tilemap[i][j].Color,
                                           batch=batch,
                                           )
                shapes.append(cell)
    if symbol == key.B:
        r = ran.choice(shapes)
        r.delete()
            
@window.event
def on_draw():
    """on pyglet draw"""
    window.clear()
    batch.draw()

if __name__ == "__main__":
    py.app.run()
