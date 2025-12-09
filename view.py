"""
Example 2:-
stimulation for 3D sence 
"""

from math import pi
from time import sleep

from cen.settings import __version__

from cen.models import World
from cen.projection import Cube, Cylinder, Sphere

World = World(width=70, height=43, space=' ')

c = Cube(10, 10, 10, cell= "×")
cy = Cylinder(8, 2, 20, cell= "*")
s = Sphere(8, 5, 10, cell= "*")

c.grab(10, 23, 0)
cy.grab(40, 32, 0)
s.grab(33, 10, 0)

c.rotate_z(0 * pi / 180)
c.rotate_y(50 * pi / 180)
c.rotate_x(20 * pi / 180)

cy.rotate_z(0 * pi / 180)
cy.rotate_y(45 * pi / 180)
cy.rotate_x(45 * pi / 180)

s.rotate_z(0 * pi / 180)
s.rotate_y(20 * pi / 180)
s.rotate_x(0 * pi / 180)

c.add_points('*')
cy.add_points('`')
s.add_points('~')

World.draw()

""" for i in range(6):
    c.rotate_z(0 * pi / 180)
    c.rotate_y(i * 2 * pi / 180)
    c.rotate_x(i * 2 * pi / 180)

    c.add_points('*')

    World.refresh()
    sleep(.1)

    c.delete() """

# return this as a succsfully sample
print("3D_view done succsfully...")  
print(f"℗ UPGE_CMD version {__version__}: succsfully work...")
