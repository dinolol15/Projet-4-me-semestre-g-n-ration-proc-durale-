
"""
Module testing de Adrien
"""

#standard lib
import random as ran

#3rd party
import pyglet as py
from pyglet.window import key

#local modules
import carte as Carte
import matrix_manager as mm

window = py.window.Window()

dimension = (5, 5)
batch = py.graphics.Batch()
shapes = []


@window.event
def on_key_press(symbol, modifier):
    """Pyglet testeur sur activation de touche clavier"""
    if symbol == key.A:
        print("A was pressed")
        a = input("choix ")
        if a == "1":
            tilemap = Carte.w_f_c_simplified(
                mm.create_matrix((100, 100),
                                 {Carte.Water: 1, Carte.Coast: 2},
                                 )
            )
        else:
            #erreurs de typage
            tilemap = Carte.w_f_c_evolved(
                mm.create_matrix(
                    (100, 100),
                    {"baba": 2},
                ),
                10,
                [20, 3, Carte.Water],
                6,
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

#relic of the past, loses pylint points

# def matrice_creation(dimension_x, dimension_y):
#     """Fonction créant une matrice"""
#     matrice = []
#     for i in range(dimension_x):
#         matrice.append([])
#         for y in range(dimension_y):
#             pass

#---------------
@window.event
def on_draw():
    """pyglet dessinateur"""
    window.clear()
    batch.draw()

if __name__ == "__main__":
    py.app.run()
