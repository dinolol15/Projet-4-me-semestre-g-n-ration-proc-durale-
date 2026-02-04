import random as ran
import pyglet as py
from pyglet.window import key, mouse


window = py.window.Window()
window.set_fullscreen(True)
tilemap = (100, 100, 5, 5)
batch = py.graphics.Batch()
shapes = []

@window.event 
def on_key_press(symbol, modifier):
    if symbol == key.A:
        shapes=[]
        for i in range(tilemap[0]):
            for j in range(tilemap[1]):
                p = py.shapes.Rectangle(x=i*tilemap[2],
                                y=j*tilemap[3],
                                width=tilemap[2],
                                height=tilemap[3],
                                color=tuple([ran.randint(0, 255) for _ in range(3)]),
                                batch=batch,    
                                )
                shapes.append(p)


@window.event()
def on_draw():
    window.clear()
    batch.draw()
        

if __name__ == "__main__":
    py.app.run()
    
