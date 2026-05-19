
"""
Placeholder object for any image
Places said image into a sprite
"""

from typing import Literal, TYPE_CHECKING

import pyglet
from pyglet.gl import (
    glBindTexture,
    glTexParameteri,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_NEAREST,
)

# Since Camera is in another file, it's a bother to import the whole thing solely for the typing
# convention, what you can do is only import what you need at the time you need,
# not create loops of imports during runtime (you might crash your machine otherwise)
if TYPE_CHECKING:
    from camera import Camera

class ImageDisplay:
    """Consider it a pyglet sprite with position and bound to a camera
    that can also import images and un-blur the object
    and do many other cool things"""
    def __init__(self,
                 camera: "Camera",
                 batch: Literal["UI", "game"],
                 layer: int = 0,
                 position: tuple[int, int] = (0, 0),
                 centered: bool = True,
                 size: float = 1.0,
                 ):

        self.camera = camera
        self.layer = layer
        self.zoom_scaling: bool = True
        self.position_scaling: bool = True
        #if needed to hide at some point
        self.visible = True

        self.pos_x = position[0]
        self.pos_y = position[1]

        self.centered = centered
        self.size = size

        #placeholder
        solid_square = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 255))
        self.texture = solid_square.create_image(32, 32)

        if batch == "game":
            self.batch = camera.batch_game
        elif batch == "UI":
            self.batch = camera.batch_ui

        self.sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(self.texture, batch=self.batch)
        self.camera.add_to_layer(self.sprite, self.layer)


    #image handling -------------------------------------------------------------------------

    #add/overwrite with already known source
    def add_image(self, texture):
        """Direct transplant of texture for tryhards"""
        self.sprite.image = texture

    #search and load
    def import_image(self, name: str, path: str = "."):
        """Import image with path and name
        Very useful to keep images accessible in a separate folder
        to avoid clutter"""
        try:
            pyglet.resource.path = [path]
            pyglet.resource.reindex()
            img = pyglet.resource.image(name)
        except pyglet.resource.ResourceNotFoundException:
            print("Image not found")
        else:
            self.sprite.image = img


    #sprite stuff ---------------------------------------------------------------------

    def set_sprite_nearest(self):
        """The most important part of this project
        When you create a pixel map, then you get a blurred image
        OpenGL does that so the image doesn't get pixelated and all ugly
        But that's the opposite of what we seek, so you disable it here"""
        texture = self.sprite.image.get_texture()
        glBindTexture(texture.target, texture.id)
        #pylint gets confused here but the function is definitely working
        glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    @property
    def texture_dim(self) -> list[int]:
        """Get the dimensions of the sprite texture"""
        texture = self.sprite.image.get_texture()
        return [texture.width, texture.height]

    @property
    def texture_dim_scaled(self):
        """Dimensions but this time sized to the size on-screen"""
        return self.texture_dim[0] * self.scale, self.texture_dim[1] * self.scale

    @property
    def texture_offset(self) -> list[int]:
        """Half-distance useful for centering, relative to zoom of cam"""
        return [int(self.texture_dim_scaled[0] // 2), int(self.texture_dim_scaled[0] // 2)]

    @property
    def texture_dim_static(self):
        """The size of the texture relative to the object size"""
        return self.texture_dim[0] * self.size, self.texture_dim[1] * self.size

    @property
    def texture_offset_static(self) -> list[int]:
        """Half-distance but relative to object size again"""
        return [int(self.texture_dim_static[0] // 2), int(self.texture_dim_static[0] // 2)]

    @property
    def downside_corner(self) -> list[int]:
        """Gives the position of the bottom left corner
        Useful when object has centered image, and you want that specific corner"""
        return [self.pos_x - self.texture_offset_static[0],
                self.pos_y - self.texture_offset_static[1]]

    @property
    def viewport_pos(self):
        """Relays command to the camera"""
        return self.camera.get_position_on_viewport(self.pos_x, self.pos_y)

    @property
    def viewport_pos_downside(self):
        """Position of the bottom left in-game relative"""
        return self.camera.get_position_on_viewport(
            self.downside_corner[0],
            self.downside_corner[1],
        )

    @property
    def scale(self):
        """Getter of the sprite scale"""
        return self.sprite.scale

    #for centering
    def sprite_pos_offset(self):
        """Centering the sprite, direct command"""
        self.sprite.x -= self.texture_offset[0]
        self.sprite.y -= self.texture_offset[1]

    def update_sprite_pos(self):
        """Reposition according to camera, update zoom
        If no camera, stay in position"""
        if self.camera is not None:
            self.sprite.scale = self.size
            if self.zoom_scaling:
                self.sprite.scale *= self.camera.zoom_scale
            if self.position_scaling:
                vp = self.viewport_pos
                self.sprite.x = vp[0]
                self.sprite.y = vp[1]
            else:
                self.sprite.x = self.pos_x
                self.sprite.y = self.pos_y

        #no camera handling
        else:
            self.sprite.x = self.pos_x
            self.sprite.y = self.pos_y

        #always center
        if self.centered:
            self.sprite_pos_offset()

    #runtime update
    def update(self):
        """Called upon on_draw (in theory, if you coded the thing right)"""
        self.set_sprite_nearest()
        self.update_sprite_pos()
