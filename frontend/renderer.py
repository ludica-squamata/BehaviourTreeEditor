from pygame import display, draw, Rect, mouse
from pygame.sprite import LayeredUpdates
import os


class Renderer:
    blocks = None
    on_selection = False
    selection = None

    @classmethod
    def init(cls):
        cls.blocks = LayeredUpdates()
        mouse.set_pos((320, 240))
        display.set_mode((640, 480))
        cls.rect_selection = Rect(0, 0, 0, 0)
        os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0, 0)

    @classmethod
    def add_block(cls, block):
        if block not in cls.blocks:
            cls.blocks.add(block, layer=1)

    @classmethod
    def del_block(cls, block):
        if block in cls.blocks:
            cls.blocks.remove(block)

    @classmethod
    def update(cls):
        fondo = display.get_surface()
        fondo.fill((0, 0, 0))
        if cls.on_selection:
            draw.rect(fondo, cls.selection.color, cls.selection.rect, 1)

        cls.blocks.update()
        cls.blocks.draw(fondo)

        display.update()
