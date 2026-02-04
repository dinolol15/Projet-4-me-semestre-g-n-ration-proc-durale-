import random as ran
import pyglet as py
from pyglet.window import key, mouse


window = py.window.Window(750, 500)

cell = py.shapes.Rectangle(x=50, y=150, width=100, height=100, color=(50, 225, 30))

batch = py.graphics.Batch()
shapes = []

@window.event 
def on_key_press(symbol, modifier):
    if symbol == key.A:
        for i in range(1, 4):
            for j in range(1, 4):
                p = py.shapes.Rectangle(x=i*50,
                                y=j*50,
                                width=50,
                                height=50,
                                color=tuple([ran.randint(0, 255) for _ in range(3)]),
                                batch=batch,    
                                )
                shapes.append(p)

def update(dt):
    pass

py.clock.schedule_interval(update, 1/60.)

@window.event()
def on_draw():
    window.clear()
    batch.draw()
        

if __name__ == "__main__":
    py.app.run()
    
