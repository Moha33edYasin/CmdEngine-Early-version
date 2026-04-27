# CmdEngine

A lightweight **terminal-based shape printer and generator** with tools for **modeling, animating, and mathematical operations**.
Designed for experimenting with ASCII shapes, basic 3D projections, and simple animation logic inside command-line environments.

---

## Features

### Shape Modeling

* **2D built-in shapes:** rectangle, triangle, circle
* **3D built-in shapes:** cube, cylinder, sphere *(early stage)*
* **Shape modifiers:** subdivide, duplicate, mirror
* **Text handling objects** for printing and layout

### Animation System

A variety of animation utilities for both shapes and characters:

* `animation()` — translation and scale tracking
* `shape_animation()` — flipping or shape-change animations
* `subdivide_animation()` — subdivision animation
* `unite_animation()` — individual-character scale-space animation
* `style_animation()` — builder-cell/unit flipping animations
* `text_animation()` — animated text display
* `draw_animation()` — animated “flow of drawing” effect

### Tools Included

* ies: `Vec2`, `Vec3`
* Logical and helper tools for geometry & scene management

---

## 🧱 Examples

### **2D Shape Example**

```python
from cmn.models import *

square = Rectangle(10, 10)
square.draw()
```

### **3D Shape Example**

```python
from cmn.projection import *

world = World(width=30, height=25, space=' ')
cube = Cube(5, 5, 5)

cube.grab(10, 10, 0)
cube.rotate_x(45)
cube.rotate_y(45)
cube.rotate_z(45)
cube.add_points()

World.draw()
```
This should output:
<img width="206" height="353" alt="image" src="https://github.com/user-attachments/assets/41b274a2-a915-489b-aa5e-28dc5492de56" />

### **Animation Example**

```python
from cmn.animation import Animation
triangle = Triangle(5, 5, n_of_edges=[2, 3], unite=2, cell="★")
Animator = Animation(triangle)

Animator.translation(10, 15, "grab")
world.add_to_sence(triangle)

while True:
    world.refresh()
```

This should output:  
<img width="432" height="642" alt="example" src="https://github.com/user-attachments/assets/9e7b7d40-a78f-41ae-a942-470a8caed0cd" />

### **More Examples**  

You may check `Boom.py` for 2D and `view.py` for 3D.

---

## 🤝 Contributing

Contributions, feature requests, and issues are welcome!
