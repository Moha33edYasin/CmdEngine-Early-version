"""
CmdEngine
___________
***********

**control:
    1. modeling shapes:
        . default build-in 2D shape (rectangle, triangle, circle)
            >>> from cmn.models import Rectangle
            ... square = Rectangle(10, 10)
            ... square.draw()
        . default build-in 3D shape (cube, cyclinder, sphere) (this not very compeletable)
            >>> from models import World
            ... from projection import Cube
            ... world = World(width=20, height=20, space=' ')
            ... cube = Cube(5, 5, 5)
            ... cube.grab(10, 10, 0)
            ... cube.rotate_x(45)
            ... cube.rotate_y(45)
            ... cube.rotate_z(45)
            ... cube.add_points()
            ... World.draw()
        . some built-in modifires (subdivide, duplicate, mirror)
        . and have the ability to modify your own (this not very compeletable)
        . also provides text handling object 

    2. animating this literal objects:
        . animation() response for translation and scale tracking animations.

        . shape_animation() response shape flipping or changing animations.

        . subdivide_animation() response subdivision animations.

        . unite_animation() response scale space animations for indiviusal character

        . style_animation() response builder cell and unites flipping or changing animations

        . text_animation() response text displaying animations in surfaces

        . draw_animation response modifire for animating flow of drawing or printing particular shape
        
Example:-
    >>> Animator = Animation(square)
    ... Animator.translation(15, 15, "scale")
    ... world.add_to_sence(square)
    ... while True: world.refresh()

    3. provided some mathematical tools (Vec2, Vec3) and logical tools
    
"""


from .models import *
from .animation import *
from .projection import *
from .vectors import *
from .settings import *

__all__ = ("models", "animation", "projection", "vectors", "settings")


