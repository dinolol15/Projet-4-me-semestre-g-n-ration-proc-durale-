
"""
First docstring in my life duh

Projet de base, modificateur de maps
"""

import functools

from typing import Callable
import copy


import Some_tkinter as SomeTK

import pyglet
from pyglet.window import key
import math

from dataclasses import dataclass

type rgb_type = tuple[int, int, int]

from SquareMap import SquareMap as Square
from ImageDisplay import ImageDisplay as Image
from Camera import Camera



def floored_to(x, n):
    return n*math.floor(x/n)

@dataclass
class PointMemory:

    ref: Square
    max_id: tuple[int, int]

    max_depth: int = 1000

    @dataclass
    class Cell:
        x: int
        y: int
        previous_rgb: rgb_type
        rgb: rgb_type
        action_value: int = 0

        def get_info(self):
            return self.x, self.y, self.previous_rgb, self.rgb, self.action_value

    def __post_init__(self):
        self.memory: list[PointMemory.Cell] = []
        self.memory_step: int = -1

    def reinit(self):
        self.memory = []
        self.memory_step = -1

    #debuggers ---------------------------
    @staticmethod
    def memo_debug(func: Callable[..., ...]):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"Executing {func.__name__} ------------------------\nStats BEFORE execution:")
            print(self.memory_step)
            print(self.memory_size)
            res = func(self, *args, **kwargs)
            print("Stats AFTER execution:")
            print(self.memory_step)
            print(self.memory_size)
            return res
        return wrapper

    @staticmethod
    def depth_crop(func: Callable[..., ...]):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            diff = self.memory_size - self.max_depth
            if diff > 0:
                self.memory = self.memory[diff:]
                self.memory_step = self.max_depth - 1
            return res
        return wrapper

    @property
    def memory_integrity(self):
        return self.memory_step > -1 and len(self.memory) > 0

    @property
    def memory_size(self):
        return len(self.memory)

    def memo_update(self, x: int, y: int, rgb: rgb_type):
        diff = self.memory_size - self.memory_step - 1
        if diff > 0:
            self.memory = self.memory[:-diff]
        self.memory_step += 1
        self.memory.append(self.Cell(x, y, self.ref.get_pixel_rgb((x, y)), rgb))


    @depth_crop
    def edit_point(self, x: int, y: int, rgb: rgb_type) -> None:
        if 0 <= x < self.max_id[0] and 0 <= y < self.max_id[1]:
            self.memo_update(x, y, rgb)
            self.ref.set_pixel((x, y), rgb)


    @depth_crop
    def previous(self):
        if self.memory_step > 0:
            c = self.memory[self.memory_step].get_info()
            self.memory_step -= 1
            self.ref.set_pixel((c[0], c[1]), c[2])


    @depth_crop
    def next(self):
        diff = self.memory_size - self.memory_step - 1
        if diff > 0:
            self.memory_step += 1
            c = self.memory[self.memory_step].get_info()
            self.ref.set_pixel((c[0], c[1]), c[3])


#globals --------------------------------------
current = "draw"
SYSTEM_PAUSE = False
drawing_mode = "tangent"

drawing_color = (0, 0, 0)
drawing_size = 1

map_size = (50, 50)
tile_size = 4
map_base_size = 5.0

global s

def main():
    global SYSTEM_PAUSE
    global drawing_color
    global drawing_size

    global map_size
    global tile_size
    global map_base_size

    global s

    cam = Camera((1000, 1000))
    cam.debug_ui()

    s = Square(cam, "game", layer=0, map_dimensions=map_size, map_pixel_size=tile_size, size=map_base_size)
    s.rand_test()
    cam.window_objects.append(s)

    initial_map_data = copy.deepcopy(s.pixel_array)

    pointer = Square(cam, "game", layer=0, map_dimensions=(1, 1), map_pixel_size=tile_size, size=map_base_size, centered=False)
    pointer.rand_test()
    pointer.set_pixel((0, 0), (255, 255, 255))
    cam.window_objects.append(pointer)

    mouse_pointer = Image(cam, "UI", layer=0, centered=False, size=.1, zoom_scaling=False, position_scaling=False)
    mouse_pointer.import_image("pen_icon.png", "Icons")
    cam.window_UI_dynamic.append(mouse_pointer)

    #icons on the side
    toolbar_range = (450, 800)
    tools_back = pyglet.shapes.Rectangle(0, toolbar_range[0], 50, toolbar_range[1]-toolbar_range[0], (255, 255, 255), batch=cam.batch_UI)

    pen_tool_icon = Image(cam, "UI", layer=2, position=(5, 755), centered=False, size=0.1,
                          position_scaling=False, zoom_scaling=False)
    pen_tool_icon.import_image("pen_icon.png", "Icons")
    cam.window_UI_dynamic.append(pen_tool_icon)
    eraser_tool_icon = Image(cam, "UI", layer=2, position=(5, 705), centered=False, size=0.1,
                          position_scaling=False, zoom_scaling=False)
    eraser_tool_icon.import_image("eraser_icon.png", "Icons")
    cam.window_UI_dynamic.append(eraser_tool_icon)
    save_tool_icon = Image(cam, "UI", layer=2, position=(5, 655), centered=False, size=0.1,
                          position_scaling=False, zoom_scaling=False)
    save_tool_icon.import_image("save_icon.png", "Icons")
    cam.window_UI_dynamic.append(save_tool_icon)
    import_tool_icon = Image(cam, "UI", layer=2, position=(2, 605), centered=False, size=0.1,
                           position_scaling=False, zoom_scaling=False)
    import_tool_icon.import_image("import_icon.png", "Icons")
    cam.window_UI_dynamic.append(import_tool_icon)
    draw_options_icon = Image(cam, "UI", layer=2, position=(5, 555), centered=False, size=0.1,
                             position_scaling=False, zoom_scaling=False)
    draw_options_icon.import_image("draw_options_icon.png", "Icons")
    cam.window_UI_dynamic.append(draw_options_icon)
    generate_map_icon = Image(cam, "UI", layer=2, position=(2, 505), centered=False, size=0.14,
                              position_scaling=False, zoom_scaling=False)
    generate_map_icon.import_image("generate_icon.png", "Icons")
    cam.window_UI_dynamic.append(generate_map_icon)
    help_icon = Image(cam, "UI", layer=2, position=(13, 455), centered=False, size=0.1,
                              position_scaling=False, zoom_scaling=False)
    help_icon.import_image("help_icon.png", "Icons")
    cam.window_UI_dynamic.append(help_icon)

    #red pointer for selected tool
    tool_pointer = pyglet.shapes.Rectangle(0, 600, 50, 50, (255, 0, 0), batch=cam.batch_UI)
    cam.add_to_layer(tool_pointer, 1)
    def tool_pointer_update(obj: pyglet, camera: "Camera"):
        data: dict = {"draw": (0, 750),
                      "eraser": (0, 700),}
        global current
        obj.x = data[current][0]
        obj.y = data[current][1]
    tool_pointer_wrap = cam.DynamicWrapper(tool_pointer, cam, tool_pointer_update)
    cam.window_UI_dynamic.append(tool_pointer_wrap)



    memo = PointMemory(s, map_size)

    @cam.window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        global drawing_mode
        global SYSTEM_PAUSE
        if not SYSTEM_PAUSE:
            #draw tangent
            if cam.mouse_left and current == "draw":
                if drawing_mode == "tangent":
                    tangent_drawing(x, y, dx, dy, drawing_color)
                elif drawing_mode == "point":
                    point_drawing(int(x), int(y))
            elif cam.mouse_left and current == "eraser":
                tangent_drawing(x, y, dx, dy, (0, 0, 0))

    #draw point accordingly to the pen size
    def draw_square(x: int, y: int, rgb):
        size = drawing_size
        memo.edit_point(x, y, rgb) #center
        for i in range(1, size):
            l = 1 + 2 * i
            xp = x - i
            yp = y - i
            d = 1
            for n in range(2):
                for _ in range(l-1):
                    yp += 1 * d
                    memo.edit_point(xp, yp, rgb)
                for _ in range(l-1):
                    xp += 1 * d
                    memo.edit_point(xp, yp, rgb)
                d *= -1

    #the worse per-frame version of drawing
    def point_drawing(x: int, y: int):
        xx, yy = mouse_pos_viewport_transform(x, y)
        x_id, y_id = find_mouse_id(xx, yy)
        draw_square(x_id, y_id, drawing_color)

    #draw lines instead of points (better draw)
    def tangent_drawing(x, y, dx, dy, rgb: rgb_type):
        x1, y1 = mouse_pos_viewport_transform(x - dx, y - dy)
        x2, y2 = mouse_pos_viewport_transform(x, y)
        x1_id, y1_id = find_mouse_id(x1, y1)
        x2_id, y2_id = find_mouse_id(x2, y2)

        # number of tiles in between + the sign
        dx_id_s = x2_id - x1_id
        dy_id_s = y2_id - y1_id
        dx_id = abs(dx_id_s)
        dy_id = abs(dy_id_s)

        r: dict = {}  # {x: y}

        if dx_id == 0 or dy_id == 0:
            if dx_id == 0 and dy_id == 0:
                pass
            elif dx_id == 0 and dy_id != 0:
                dy_s = int(dy_id / (y2_id - y1_id))
                for i in range(0, (dy_id + 1) * dy_s, dy_s):
                    r[x1_id] = y1_id + i
            elif dx_id != 0 and dy_id == 0:
                dx_s = int(dx_id / (x2_id - x1_id))
                for i in range(0, (dx_id + 1) * dx_s, dx_s):
                    r[x1_id + i] = y1_id
        else:
            dx_s = int(dx_id / (x2_id - x1_id))
            dy_s = int(dy_id / (y2_id - y1_id))

            if dx_id >= dy_id:
                tng = dy_id * dy_s / dx_id  # the abs tangent always smaller than 1
                for i in range(0, (dx_id + 1) * dx_s, dx_s):
                    r[x1_id + i] = y1_id + round(tng * abs(i))
            else:
                tng = dx_id * dx_s / dy_id  # the abs tangent always smaller than 1
                for i in range(0, (dy_id + 1) * dy_s, dy_s):
                    r[x1_id + round(tng * abs(i))] = y1_id + i

        for i in r.keys():
            xx = i
            yy = r[i]
            draw_square(xx, yy, rgb)

    #tile lenght on screen
    def tile_len():
        return s.tile_size / cam.zoom_scale

    #illegal according to pycharm, access to mouse pos
    def mouse_pos():
        return cam.window._mouse_x, cam.window._mouse_y

    #mouse position on screen (relative to in-game)
    def mouse_pos_viewport():
        x = cam.pos_x + (cam.window._mouse_x - cam.window_center[0]) / cam.zoom_scale
        y = cam.pos_y + (cam.window._mouse_y - cam.window_center[1]) / cam.zoom_scale
        return x, y

    #the same thing as the one above but I kept it out of personal sentiment as a relic of the past
    def mouse_pos_viewport_transform(mx, my):
        x = cam.pos_x + (mx - cam.window_center[0]) / cam.zoom_scale
        y = cam.pos_y + (my - cam.window_center[1]) / cam.zoom_scale
        return x, y

    #gets the tile on which the mouse currently is (i.e. the tile of the map you draw upon)
    def find_mouse_id(x, y):
        t_len = tile_len()
        dc = s.downside_corner
        x_id = int(math.floor((x - dc[0]) / t_len))
        y_id = int(math.floor((y - dc[1]) / t_len))

        return x_id, y_id

    #the loop of pyglet and the start of globals apocalypse
    def update(dt):
        global SYSTEM_PAUSE
        global map_size
        global s

        dc = s.downside_corner
        t_len = tile_len()
        x, y = mouse_pos_viewport()
        x_id, y_id = find_mouse_id(x, y)
        max_id = map_size

        #pointer drawing animation
        if 0 <= x_id < max_id[0] and 0 <= y_id < max_id[1]:
            px, py = dc[0] + x_id*t_len, dc[1] + y_id*t_len
            pointer.pos_x, pointer.pos_y = [px, py]

        #pointer animation
        mouse_pointer.pos_x, mouse_pointer.pos_y = mouse_pos()


        #toolbar actions ----------------------
        def toolbar_action(n: int):
            global current
            global SYSTEM_PAUSE
            global s

            if n == 0: #draw tool
                current = "draw"
                mouse_pointer.import_image("pen_icon.png", "Icons")

            elif n == 1:
                current = "eraser"
                mouse_pointer.import_image("eraser_icon.png", "Icons")

            elif n == 2: #saving
                SYSTEM_PAUSE = True
                global s
                print("save")
                save_text = bytes(s.pixel_array)
                SomeTK.copy_win(save_text)
                SYSTEM_PAUSE = False

            elif n == 3: #importing
                SYSTEM_PAUSE = True
                print("import")
                import_data = []
                SomeTK.import_project(import_data)
                if len(import_data) > 0:
                    def load_func():
                        s.pixel_array = bytearray(import_data[0])
                        s.update_image()
                    SomeTK.reinit(load_func)
                SYSTEM_PAUSE = False

            elif n == 4: #paint settings
                global drawing_color
                global drawing_size
                print(drawing_color)
                SYSTEM_PAUSE = True
                print("pen settings")
                drawing_color, drawing_size = SomeTK.drawing_settings()
                print(drawing_color)
                SYSTEM_PAUSE = False

            elif n == 5: #new map
                SYSTEM_PAUSE = True
                global map_size
                new_dim_x, new_dim_y, new = SomeTK.create_new_map()
                map_size = (new_dim_x, new_dim_y)
                #reinitialize map after re-creation -----------------------------------------
                #fun fact, the function below was designed 2 months ago in anticipation of this very situation
                #basically you need to create a new pyglet.image.ImageData to refresh its values
                s.update_data_values(map_dimensions=map_size, map_pixel_size=tile_size)
                memo.max_id = map_size
                memo.reinit()
                s.pixel_array = bytearray(new)
                s.update_image()
                SYSTEM_PAUSE = False


            elif n == 6: #get some help
                print("Stop it, get some help.")

            elif n == 666: #reinit the whole map
                SYSTEM_PAUSE = True
                def reinit_func():
                    s.pixel_array = initial_map_data
                    s.update_image()
                SomeTK.reinit(reinit_func)
                SYSTEM_PAUSE = False

        #selection of tools on the toolbal
        if cam.mouse_left:
            if mouse_pos()[0] < 50 and toolbar_range[0] < mouse_pos()[1] < toolbar_range[1]:
                obj = math.floor((toolbar_range[1] - mouse_pos()[1]) / 50.0)
                toolbar_action(obj)

        #back and forth
        if cam.keys[key.Z]:
            print("prev")
            memo.previous()
        if cam.keys[key.X]:
            print("next")
            memo.next()

        #some keybinds
        if cam.keys[key.L]:
            toolbar_action(666)

        if cam.keys[key.S]:
            toolbar_action(2)

        if cam.keys[key.I]:
            toolbar_action(3)

        if cam.keys[key.P]:
            toolbar_action(4)

        if cam.keys[key.E]:
            toolbar_action(0)

        if cam.keys[key.D]:
            toolbar_action(1)

    #main pyglet loop
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()