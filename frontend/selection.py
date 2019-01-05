from pygame import Rect
from .renderer import Renderer
from .basewidget import BaseWidget


class Selection(BaseWidget):
    def __init__(self, x, y):
        self.rect = Rect(x, y, 1, 1)
        self.color = 0, 255, 255
        Renderer.selection = self
        Renderer.on_selection = True

    def on_mouse_motion(self, pos, buttons):
        if buttons[0]:
            self.rect.width = pos[0]-self.rect.x
            self.rect.height = pos[1]-self.rect.y

    def on_mouse_up(self, pos, button):
        Renderer.on_selection = False
        self.rect.normalize()
        return self.rect

    def __repr__(self):
        return 'Selection Object @{},{},{},{}'.format(*self.rect)


class SelectionBlock(BaseWidget):
    rel_x, rel_y = 0,0

    def __init__(self, pos, *objects):
        self.objects = objects
        self.rect = Rect(pos, (0, 0)).unionall([obj.rect for obj in objects])

    def on_mouse_down(self, pos, button):
        self.rel_x, self.rel_y = pos[0] - self.rect.x, pos[1] - self.rect.y

    def on_mouse_motion(self, pos, buttons):
        selected = None
        for obj in self.objects:
            if obj.rect.collidepoint(pos):
                selected = obj
                break


