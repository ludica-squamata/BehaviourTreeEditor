from pygame import QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame import event, K_ESCAPE
from pygame.sprite import LayeredDirty
from backend.util import terminate
from .selection import Selection, SelectionBlock

event_list = [QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]


class EventManager:
    objects = None
    active = None
    selected_objects = None
    selection = None
    widgets = []

    @classmethod
    def init(cls):
        cls.objects = LayeredDirty()
        cls.selected_objects = []

    @classmethod
    def add_object(cls, obj):
        if hasattr(obj, 'image'):
            cls.objects.add(obj)
        cls.widgets.append(obj)

    @classmethod
    def del_object(cls, obj):
        cls.objects.remove(obj)
        cls.widgets.remove(obj)

    @classmethod
    def update(cls):
        for e in event.get(event_list):
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                terminate()

            elif e.type == KEYDOWN:
                for obj in cls.selected_objects:
                    obj.on_key_down(e.key)

            elif e.type == KEYUP:
                for obj in cls.selected_objects:
                    obj.on_key_up(e.key)

            elif e.type == MOUSEBUTTONDOWN:
                cls.selected_objects.clear()
                cls.selection = None
                for obj in cls.widgets:
                    if obj.rect.collidepoint(e.pos):
                        obj.on_mouse_down(e.pos, e.button)
                        cls.selected_objects.append(obj)

                if not len(cls.selected_objects):
                    cls.selection = Selection(*e.pos)
                    for obj in cls.objects.sprites():
                        obj.deselect()

            elif e.type == MOUSEBUTTONUP:
                if cls.selection is not None:
                    rect = cls.selection.on_mouse_up(e.pos, e.button)
                    if rect is not None:  # active was selection
                        for obj in cls.widgets:
                            if rect.contains(obj.rect):
                                obj.select()
                                cls.selected_objects.append(obj)
                                obj.enabled = False
                        cls.add_object(SelectionBlock(e.pos, *cls.selected_objects))

                elif len(cls.selected_objects):
                    for obj in cls.selected_objects:
                        obj.on_mouse_up(e.pos, e.button)

            elif e.type == MOUSEMOTION:
                if cls.selection is not None:
                    cls.selection.on_mouse_motion(e.pos, e.buttons)
                elif len(cls.selected_objects):
                    for obj in cls.selected_objects:
                        obj.on_mouse_motion(e.pos, e.buttons)
