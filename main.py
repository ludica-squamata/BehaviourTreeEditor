from pygame import init
from frontend import Renderer, EventManager, Block

init()
Renderer.init()
EventManager.init()

for pos in [(10, 10), (20+32, 10)]:
    b = Block(*pos)
    Renderer.add_block(b)
    EventManager.add_object(b)

while True:
    EventManager.update()
    Renderer.update()
