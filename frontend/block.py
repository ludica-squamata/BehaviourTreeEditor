from pygame.sprite import DirtySprite
from pygame import Surface, K_DELETE
from .basewidget import BaseWidget
from .renderer import Renderer
from .eventmanager import EventManager


class Block(DirtySprite, BaseWidget):
    is_selected = False
    clicked = False
    enabled = True
    rel_x = 0
    rel_y = 0

    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((33, 33))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

    def select(self):
        self.is_selected = True
        self.image.fill((255, 0, 0))

    def deselect(self):
        self.is_selected = False
        self.image.fill((255, 255, 255))

    def on_key_down(self, key):
        if key == K_DELETE:
            EventManager.del_object(self)
            Renderer.del_block(self)

    def on_mouse_down(self, pos, button):
        self.clicked = True

    def on_mouse_up(self, pos, button):
        if self.enabled:
            if button == 1:
                if self.clicked:
                    self.select()
                    self.clicked = False
                self.rel_x, self.rel_y = pos[0]-self.rect.x, pos[1]-self.rect.y
            self.dirty = 1

    def on_mouse_motion(self, pos, buttons):
        if self.enabled:
            if buttons[0]:
                self.rect.topleft = pos[0]-self.rel_x, pos[1]-self.rel_y
            self.dirty = 1
