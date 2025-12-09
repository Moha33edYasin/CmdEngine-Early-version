"""
Example 1:-
animation of a Building Smashing
"""

from time import sleep

from cmn.settings import __version__
from cmn.animation import Animation
from cmn.models import *

# Triggers, Sets
isBegin = False
isIntro = False
isHit = False
isBoomed = False
isConc = False
isEnded = False
loop = True
Timer = 0
deltaTime = 150
BOOMPARTICALS = [
    ('•', '◇'),
    ('°', ' ')
]
# Characters
World = World(width=43, height=43,  unite=1, space=' ')
s = Rectangle(width= 10, height=16, name="institude", n_of_edges=[1, 1], unite=2, cell= '□', fill='🧱') # to have perfect rectangle WIDTH <=> 1.1 HEIGHT
door = Rectangle(width= 5, height= 6, name="door", n_of_edges=[1, 1], unite=1, cell= '■', fill='🟫')
window1 = Rectangle(width= 5, height= 5, name="window", n_of_edges=[1, 1], unite=1, cell= '■', fill='🪟')
p = Point(x= 0, y= 0, cell='🧨')
EMPTY = Circle(raduis= 15, pull=2, smooth = 3, name="empty", n_of_edges=[1, 1], unite=1, cell= ' ', fill=' ')
BOOM = Circle(raduis=30, pull=6, smooth= 3, n_of_edges=[1, 1], unite=1, cell= '★', fill='◆')
END = Text('<THE END>', [17, 30], surface= World)
idMsg= [
    Text(['Welcome👋'], [17, 20], surface= World),
    Text('Collision Animation!!', [12, 19], surface= World),
    Text('Created by Programmer:', [10, 20], surface= World),
    Text('Pr.MOHAMMED YASIN😉', [12, 21], surface= World)
]
# Modeling
s.grab(23, 25)
window1.subdivide(1)
window1.grab(26, 26)
window2 = window1.duplicate(9, 0)
door.grab(32, 34)
door.add_text(Text('°', [3, 2], surface= door))
s.parent(window1)
s.parent(window2)
s.parent(door)
p.grab(1, 1)

EMPTY.grab(23, 24)

BOOM.grab(13, 20)
BOOM.add_text(Text('BOOM', [4, 10], surface= BOOM))
BOOM.add_text(Text('BOOM', [19, 4], surface= BOOM))
BOOM.add_text(Text('BOOM', [18, 10], surface= BOOM))
BOOM.add_text(Text('BOOM', [4, 4], surface= BOOM))
BOOM.add_text(Text('BOOM', [11, 5], [1, 1], surface= BOOM))
BOOM.add_text(Text('!!!!', [12, 5], [1, 1], surface= BOOM))
# Animations
np = Animation(p)
nBOOM = Animation(BOOM, speed=3)
nEND = Animation(END)
np.translation(35, 35, 'grab')
np.translation(0, 0, 'scale')
nBOOM.translation(0, 0, "scale")
nBOOM.reset()
nBOOM.style_animation(BOOMPARTICALS, 2)
nEND.translation(17, 0, 'grab')
# Controll animations
np.pause_animation()
nBOOM.pause_animation()
nEND.pause_animation()
while loop:
    Timer += 1
    World.refresh()
    # Introducion
    if not isBegin: World.add_text(idMsg[0])
    if Timer >= 10 and not isBegin:
        World.delete(idMsg[0])
        World.add_text(idMsg[1])
        isBegin = True
        
    # Collision run     
    if (Timer >= 30) & (not isIntro):
        World.delete(idMsg[1])
        World.add_to_sence(s)
        World.add_to_sence(p)
        np.resume_animation()
        isIntro = True
    # Detials    
    if (Timer >= 30) & (not isEnded) & (not isConc):
        print("  "  * (not isBoomed) + "    SBuild" + "       " * (not isBoomed) + "[Smashed]" * isBoomed + "|      P" + " [Boomed]" * isBoomed)
        print("_________________________________________")
        print("pos:", f"{s.pos}  |", p.pos)
        print(f"size:  {s.size}    |  {p.size}")
        print("_________________________________________")
    # When collision happens boomed
    if s.check_collisions(p, 1) and not isHit:
        World.delete(p)
        World.add_to_sence(EMPTY)
        np.pause_animation()
        deltaTime = Timer
        isHit = True
    if Timer - deltaTime == 3:
        World.delete(EMPTY)
        World.delete(s)
        World.add_to_sence(BOOM)
        nBOOM.resume_animation()
        isBoomed = True
    # Record boom gas size  
    if isBoomed & (not isConc): print("Boom area:", BOOM.size)
    # Conculsion about Devloper
    if Timer >= 61 and not isConc:
        World.delete(BOOM)
        World.add_text(idMsg[2])
        World.add_text(idMsg[3])
        isConc = True
    # Roteen end animation style
    if Timer >= 80 and not isEnded:
        World.delete(idMsg[2])
        World.delete(idMsg[3])
        World.add_text(END)
        nEND.resume_animation()
        isEnded = True
    # Bye Message for player    
    if Timer >= 108: World.add_text('Bye🤗...', [16, 22])
    # quit all
    if Timer == 109: loop = False
    sleep(.06)
# return this as a succsfully sample
print("Collision animation done succsfully...")  
print(f"℗ UPGE_CMD version {__version__}: succsfully work...")

