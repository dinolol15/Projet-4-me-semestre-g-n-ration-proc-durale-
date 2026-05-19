
"""
First docstring in my life duh

Projet de base, modificateur de maps
"""

import functools
import math
from dataclasses import dataclass
import copy
from typing import Callable

import pyglet
from pyglet.window import key




import some_tkinter as SomeTK
from square_map import SquareMap as Square
from image_display import ImageDisplay as Image
from camera import Camera


type RgbType = tuple[int, int, int]





@dataclass
class PointMemory:
    """erm some docstring"""

    ref: Square
    max_id: tuple[int, int]

    max_depth: int = 1000

    @dataclass
    class Cell:
        """Placeholder for memory cells"""
        x: int
        y: int
        previous_rgb: RgbType
        rgb: RgbType
        action_value: int = 0

        def get_info(self):
            """get its info duh"""
            return self.x, self.y, self.previous_rgb, self.rgb, self.action_value

    def __post_init__(self):
        self.memory: list[PointMemory.Cell] = []
        self.memory_step: int = -1

    def reinit(self):
        """Wipe the memory"""
        self.memory = []
        self.memory_step = -1

    #debuggers ---------------------------
    @staticmethod
    def memo_debug(func: Callable[..., ...]):
        """Debugger for memory variables"""

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
        """If memory too large, wipes the furthest elements"""
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
    def memory_size(self):
        """Get the memory size"""
        return len(self.memory)

    def memo_update(self, x: int, y: int, rgb: RgbType):
        """Update the memory (repeats in for several methods)"""
        diff = self.memory_size - self.memory_step - 1
        if diff > 0:
            self.memory = self.memory[:-diff]
        self.memory_step += 1
        self.memory.append(self.Cell(x, y, self.ref.get_pixel_rgb((x, y)), rgb))

    @depth_crop
    def edit_point(self, x: int, y: int, rgb: RgbType) -> None:
        """Edits the pixel directly on the SquareMap"""
        if 0 <= x < self.max_id[0] and 0 <= y < self.max_id[1]:
            self.memo_update(x, y, rgb)
            self.ref.set_pixel((x, y), rgb)

    @depth_crop
    def previous(self):
        """Return to previous action like ctrl z"""
        if self.memory_step > 0:
            c = self.memory[self.memory_step].get_info()
            self.memory_step -= 1
            self.ref.set_pixel((c[0], c[1]), c[2])


    @depth_crop
    def next(self):
        """Return to next action like ctrl shift z"""
        diff = self.memory_size - self.memory_step - 1
        if diff > 0:
            self.memory_step += 1
            c = self.memory[self.memory_step].get_info()
            self.ref.set_pixel((c[0], c[1]), c[3])



@dataclass
class DrawingModule:
    """
    Better off with a class than that war crime of globals
    """
    system_pause: bool = False
    current: str = "draw"
    drawing_mode: str = "tangent"
    drawing_color: RgbType = (0, 0, 0)
    drawing_size: int = 1
    map_size: tuple[int, int] = (50, 50)
    tile_size: int = 4
    map_base_size: float = 5.0

    def __post_init__(self):
        self.cam = Camera((1000, 1000))
        self.cam.debug_ui()

        #create squaremap
        self.square = Square(
            self.cam,
            "game",
            layer=0,
            map_dimensions=self.map_size,
            map_pixel_size=self.tile_size,
            size=self.map_base_size
        )
        self.square.rand_test()
        self.cam.window_objects.append(self.square)
        self.initial_map_data = copy.deepcopy(self.square.pixel_array)

        #mouse pointer
        self.pointer = Square(
            self.cam,
            batch="game",
            layer=0,
            map_dimensions=(1, 1),
            map_pixel_size=self.tile_size,
            size=self.map_base_size,
            centered=False
        )
        self.pointer.set_pixel((0, 0), (255, 255, 255))
        self.cam.window_objects.append(self.pointer)
        self.mouse_pointer = Image(
            self.cam,
            batch="UI",
            layer=0,
            centered=False,
            size=.1,
        )
        self.mouse_pointer.position_scaling = False
        self.mouse_pointer.zoom_scaling = False
        self.mouse_pointer.import_image("pen_icon.png", "Icons")
        self.cam.window_ui_dynamic.append(self.mouse_pointer)

        # icons on the side with some fixed values
        self.toolbar_range = (450, 800)
        tools_back = pyglet.shapes.Rectangle(
            0,
            self.toolbar_range[0],
            50,
            self.toolbar_range[1] - self.toolbar_range[0],
            color=(255, 255, 255),
            batch=self.cam.batch_ui
        )
        self.cam.window_ui_static.append(tools_back)

        # this single line above is for the only purpose of avoiding a pylint error
        pen_tool_icon = Image(self.cam, "UI", 2, position=(5, 755), centered=False, size=0.1)
        pen_tool_icon.import_image("pen_icon.png", "Icons")
        self.cam.window_ui_dynamic.append(pen_tool_icon)
        eraser_tool_icon = Image(self.cam, "UI", 2, position=(5, 705), centered=False, size=0.1)
        eraser_tool_icon.import_image("eraser_icon.png", "Icons")
        self.cam.window_ui_dynamic.append(eraser_tool_icon)
        save_tool_icon = Image(self.cam, "UI", 2, position=(5, 655), centered=False, size=0.1)
        save_tool_icon.import_image("save_icon.png", "Icons")
        self.cam.window_ui_dynamic.append(save_tool_icon)
        import_tool_icon = Image(self.cam, "UI", 2, position=(2, 605), centered=False, size=0.1)
        import_tool_icon.import_image("import_icon.png", "Icons")
        self.cam.window_ui_dynamic.append(import_tool_icon)
        draw_options_icon = Image(self.cam, "UI", 2, position=(5, 555), centered=False, size=0.1)
        draw_options_icon.import_image("draw_options_icon.png", "Icons")
        self.cam.window_ui_dynamic.append(draw_options_icon)
        generate_map_icon = Image(self.cam, "UI", 2, position=(2, 505), centered=False, size=0.14)
        generate_map_icon.import_image("generate_icon.png", "Icons")
        self.cam.window_ui_dynamic.append(generate_map_icon)
        help_icon = Image(self.cam, "UI", 2, position=(13, 455), centered=False, size=0.1)
        help_icon.import_image("help_icon.png", "Icons")
        self.cam.window_ui_dynamic.append(help_icon)
        self.sidebar_icons = [
            pen_tool_icon,
            eraser_tool_icon,
            save_tool_icon,
            import_tool_icon,
            draw_options_icon,
            generate_map_icon,
            help_icon
        ]
        for ob in self.sidebar_icons:
            ob.zoom_scaling = False
            ob.position_scaling = False

        # red pointer for selected tool
        self.tool_pointer = pyglet.shapes.Rectangle(
            0,
            600,
            50,
            50,
            (255, 0, 0),
            batch=self.cam.batch_ui
        )
        self.cam.add_to_layer(self.tool_pointer, 1)

        def tool_pointer_update(obj: pyglet, camera: "Camera"):
            """Commenting here yet again to say that the camera argument is necessary when passed,
            but pylint being itself does not admit it. It is kind of long to explain,
            so please just trust me and forgive this other pylint error
            """
            data: dict = {"draw": (0, 750),
                          "eraser": (0, 700), }
            obj.x = data[self.current][0]
            obj.y = data[self.current][1]
        tool_pointer_wrap = self.cam.DynamicWrapper(
            self.tool_pointer,
            self.cam, tool_pointer_update
        )
        self.cam.window_ui_dynamic.append(tool_pointer_wrap)

        #memory module
        self.memo = PointMemory(self.square, self.map_size)

        #push handlers
        self.cam.window.push_handlers(self)

        # main pyglet loop
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        pyglet.app.run()
        #end of the post_init ---------------------------

    def on_mouse_drag(self, x, y, dx, dy, *args):
        """Stuff handled by pyglet for mouse movement
        *args is here because pyglet passes 2 additional mystery args
        (that we don't use here anyway)"""
        if not self.system_pause:
            # draw tangent
            if self.cam.mouse_left and self.current == "draw":
                if self.drawing_mode == "tangent":
                    self.tangent_drawing(x, y, dx, dy, self.drawing_color)
                elif self.drawing_mode == "point":
                    self.point_drawing(int(x), int(y))
            elif self.cam.mouse_left and self.current == "eraser":
                self.tangent_drawing(x, y, dx, dy, (0, 0, 0))


    def draw_square(self, x: int, y: int, rgb):
        """To draw point accordingly to the pen size"""
        size = self.drawing_size
        self.memo.edit_point(x, y, rgb)  # center
        for i in range(1, size):
            l = 1 + 2 * i
            xp = x - i
            yp = y - i
            d = 1
            for _ in range(2):
                for _ in range(l - 1):
                    yp += 1 * d
                    self.memo.edit_point(xp, yp, rgb)
                for _ in range(l - 1):
                    xp += 1 * d
                    self.memo.edit_point(xp, yp, rgb)
                d *= -1


    def point_drawing(self, x: int, y: int):
        """the worse per-frame version of drawing"""
        xx, yy = self.mouse_pos_viewport_transform(x, y)
        x_id, y_id = self.find_mouse_id(xx, yy)
        self.draw_square(x_id, y_id, self.drawing_color)

    def tangent_drawing(self, x, y, dx, dy, rgb: RgbType):
        """draw lines instead of points (better draw)
        I object yet again to pylint, it's necessary to have all the args and
        operation steps here, I refuse to redo this hellish math"""
        x1, y1 = self.mouse_pos_viewport_transform(x - dx, y - dy)
        x2, y2 = self.mouse_pos_viewport_transform(x, y)
        x1_id, y1_id = self.find_mouse_id(x1, y1)
        x2_id, y2_id = self.find_mouse_id(x2, y2)

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

        for i in r.items():
            self.draw_square(i[0], i[1], rgb)

    def tile_len(self):
        """tile length on screen"""
        return self.square.tile_size / self.cam.zoom_scale


    def mouse_pos(self):
        """please sir, spare the convention points on those
        it's just so that I get the mouse position, nothing personal"""
        return self.cam.window._mouse_x, self.cam.window._mouse_y


    def mouse_pos_viewport(self):
        """mouse position on screen (relative to in-game)"""
        x = self.cam.pos_x + (self.cam.window._mouse_x - self.cam.window_center[0]) / self.cam.zoom_scale
        y = self.cam.pos_y + (self.cam.window._mouse_y - self.cam.window_center[1]) / self.cam.zoom_scale
        return x, y


    def mouse_pos_viewport_transform(self, mx, my):
        """the same thing as the one above
        but I kept it out of personal sentiment as a relic of the past"""
        x = self.cam.pos_x + (mx - self.cam.window_center[0]) / self.cam.zoom_scale
        y = self.cam.pos_y + (my - self.cam.window_center[1]) / self.cam.zoom_scale
        return x, y


    def find_mouse_id(self, x, y):
        """gets the tile on which the mouse currently is
        (i.e. the tile of the map you draw upon)"""
        t_len = self.tile_len()
        dc = self.square.downside_corner
        x_id = int(math.floor((x - dc[0]) / t_len))
        y_id = int(math.floor((y - dc[1]) / t_len))

        return x_id, y_id


    def update(self, dt):
        """Contrary to what pylint says, dt is required here as per pyglet"""

        dc = self.square.downside_corner
        t_len = self.tile_len()
        x, y = self.mouse_pos_viewport()
        x_id, y_id = self.find_mouse_id(x, y)
        max_id = self.map_size

        #pointer drawing animation
        if 0 <= x_id < max_id[0] and 0 <= y_id < max_id[1]:
            px, py = dc[0] + x_id*t_len, dc[1] + y_id*t_len
            self.pointer.pos_x, self.pointer.pos_y = [px, py]

        #pointer animation
        self.mouse_pointer.pos_x, self.mouse_pointer.pos_y = self.mouse_pos()


        #toolbar actions ----------------------
        def toolbar_action(n: int):
            """For different inputs"""
            if n == 0: #draw tool
                self.current = "draw"
                self.mouse_pointer.import_image("pen_icon.png", "Icons")

            elif n == 1:
                self.current = "eraser"
                self.mouse_pointer.import_image("eraser_icon.png", "Icons")

            elif n == 2: #saving
                self.system_pause = True
                print("save")
                save_text = bytes(self.square.pixel_array)
                SomeTK.copy_win(save_text, self.map_size)
                self.system_pause = False

            elif n == 3: #importing
                self.system_pause = True
                print("import")
                import_data = []
                SomeTK.import_project(import_data)
                if len(import_data) > 0:
                    def load_func():
                        data = import_data[1]
                        dim = import_data[0]
                        print(self.map_size)
                        self.map_size = dim
                        self.memo.max_id = self.map_size
                        self.memo.reinit()
                        print(self.map_size)
                        self.square.update_data_values(dim, self.tile_size)   #update ImageData!
                        self.square.pixel_array = bytearray(data)
                        self.square.update_image()
                    SomeTK.reinit(load_func)
                self.system_pause = False

            elif n == 4: #paint settings
                self.system_pause = True
                print("pen settings")
                self.drawing_color, self.drawing_size = SomeTK.drawing_settings()
                self.system_pause = False

            elif n == 5: #new map
                self.system_pause = True
                new_dim_x, new_dim_y, new = SomeTK.create_new_map()
                self.map_size = (new_dim_x, new_dim_y)
                # reinitialize map after re-creation
                # Fun fact, the function below was designed 2 months ago in anticipation of
                # this very situation
                # Basically you need to create a new pyglet.image.ImageData to refresh
                # its values
                self.square.update_data_values(
                    map_dimensions=self.map_size,
                    map_pixel_size=self.tile_size
                )
                self.memo.max_id = self.map_size
                self.memo.reinit()
                self.square.pixel_array = bytearray(new)
                self.square.update_image()
                self.system_pause = False

            elif n == 6: #get some help
                print("Stop it, get some help.")

            elif n == 666: #reinit the whole map
                self.system_pause = True
                def reinit_func():
                    self.square.pixel_array = self.initial_map_data
                    self.square.update_image()
                SomeTK.reinit(reinit_func)
                self.system_pause = False

        #selection of tools on the toolbar
        if self.cam.mouse_left:
            c1 = self.toolbar_range[0] < self.mouse_pos()[1] < self.toolbar_range[1]
            if self.mouse_pos()[0] < 50 and c1:
                obj = math.floor((self.toolbar_range[1] - self.mouse_pos()[1]) / 50.0)
                toolbar_action(obj)

        #back and forth
        if self.cam.keys[key.Z]:
            print("prev")
            self.memo.previous()
        if self.cam.keys[key.X]:
            print("next")
            self.memo.next()

        #some keybinds
        if self.cam.keys[key.L]:
            toolbar_action(666)

        if self.cam.keys[key.S]:
            toolbar_action(2)

        if self.cam.keys[key.I]:
            toolbar_action(3)

        if self.cam.keys[key.P]:
            toolbar_action(4)

        if self.cam.keys[key.E]:
            toolbar_action(0)

        if self.cam.keys[key.D]:
            toolbar_action(1)

if __name__ == "__main__":
    dr = DrawingModule()
