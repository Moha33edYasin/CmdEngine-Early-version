'''
Hallo!! This Shape Creative Module
version 1.0.0
succssufuly work...
_______________________________________
'''
from .settings import DEFULT_HIGTH, DEFULT_WIDTH, CODE, __version__
from .settings import convert_to_bool, remote, remove_char
from .vectors import Vec3, Vec2
from  os import system
from math import log, floor

class Modifires:
    @staticmethod
    def subdivide(obj, value = 1, vert= '|', hor = '-', link = '+'):
        graph = obj.graph
        w, h = abs(obj.w), abs(obj.h)
        y_start, y_end = obj.up, h - obj.down
        value += 1
        for i in range(1, value):
            sub = i/value
            y_cut = obj.up + int(sub * (h - obj.up - obj.down))
            x_cut = obj.left + int(sub * (w * obj.unite - obj.left - obj.right)) - obj.__name__.startswith('right_triangle')
            for a, y in enumerate(graph[y_start:y_end]):
                y_coord = a + y_start
                start, inside = False, False
                lenx_s, lenx_e = 0, 0
                for n, x in enumerate(y):
                    if not inside and (x == obj.fill or x == hor or x == vert): 
                        start, inside = True, True
                        lenx_s = n
                    if inside and x == obj.cell:
                        lenx_e = n
                        break
                    if start & (y_coord == y_cut) & (n % obj.unite == 0): graph[y_coord][n] = hor if graph[y_coord][n] != vert else link # link nodes
                if lenx_s <= x_cut < lenx_e: graph[y_coord][x_cut] = vert if graph[y_coord][x_cut] != hor else link # link nodes
        obj.shape = obj.get_shape_from(graph)
        
    @staticmethod
    def duplicate(obj, x= 1, y= 1):
        if obj.__class__ == Text: 
            obj_copy = Text(obj.shape)
            obj_copy.surface = obj.surface
            obj_copy.vector = obj.vector
        else: obj_copy = Shape(height= obj.h, width= obj.w, unite= obj.unite, shape= None, n_of_edges = [obj.no_edgx, obj.no_edgy], cell= obj.cell, fill= obj.fill)    
        obj_copy.shape = obj.shape
        obj_copy.pos = obj.pos
        obj_copy.inherObj = obj.inherObj
        obj_copy.animation = obj.animation
        obj_copy.grab(x, y)
        return obj_copy
        
    @staticmethod    
    def mirror(obj, x= 1, y= 1, offset= 0, mirror_obj_name= None):
        mirror_obj = obj.duplicate(x= x * (obj.w + offset - 1), y= y * (obj.h + offset - 1))
        mirror_obj.reverse(x, y)
        mirror_obj.__name__ = mirror_obj_name
        return mirror_obj
        
    @staticmethod    
    def apply_mirror(obj):
        for v in obj.mirror_objects.values():
            obj.parent(object = v)
            
class Shape():
    no = -1
    enviroment = None
    objects = []
    modifires = Modifires()
    Build_Default_Shapes = {
          'point': -1, 
          'rectangle': -1,
    	  'right_triangle': -1,
          'smooth_right_triangle': -1,
          'triangle': -1, 
          'v_triangle': -1,
          'circle': -1,
          'hor_line': -1,
          'vert_line': -1,
          'text': -1,
          'world': -1,
          'default_name': -1}
          
    def __new__(cls, width=1, height=1, shape=None, smooth= 0, pos = (0, 0), name= 'default_name', n_of_edges= [1, 1], unite=1, cell= '*', fill= ' ', create= True):
        cls.no += 1
        return super().__new__(cls)
    def __init__(self, width=1, height=1, shape=None, smooth= 0, pos = (0, 0), name= 'default_name', n_of_edges= [1, 1], unite=1, cell= '*', fill= ' ', create= True):
        self.inherObj = self.enviroment
        self.w, self.h = width, height
        self.__prevw, self.__prevh = width, height
        self.pos = Vec2(*pos)
        self.vector = [1, 1]
        self.__unite = unite
        self.no_edgx, self.no_edgy = n_of_edges
        self.cell, self.fill = cell, fill
        self.no_sides = 2 if shape == 'rectangle' else 1
        self.__name__ = f'{name}'+ f'({self.no})' * convert_to_bool(self.no)
        self.up, self.down, self.right, self.left = [0] * 4
        self.subvalue = (0, '|', '-', '+')
        self.texts = []
        self.shape = []
        self.children = {}
        self.origion = self.pos + Vec2(self.w // 2, self.h // 2)
        self.animation = None
        self.animate_type = 'DEFULT'
        self.__updates = []
        self.__actions = []
        self.objects.append(self)
    
    # Remotes, Getters 
    @property
    def shape_name(self): return self.__name__.split('(')[0]
    @property
    def chart(self): return remote(clist= self.shape, chart = True)
    @property 
    def graph(self): return remote(clist= self.chart, graph = True)
    @property    
    def unite(self): return self.__unite
    @property
    def size(self): return self.w, self.h
    @property
    def style(self): return self.cell, self.fill 
    @property
    def mirror_objects(self):
        mirror_objs = {}
        for obj_name, obj in self.children.items():
            if obj_name.startswith('mirror:'): mirror_objs[obj_name] = obj
        return mirror_objs

    @property
    def updates(self): return self.__updates
    @property
    def actions(self): return self.__actions

    # Setters
    @unite.setter
    def unite(self, val):
        set = val - self.__unite
        state, line, space = [], '', self.fill * set
        if self.__class__ == Text:self.erase()
        for y, i in enumerate(self.shape):
            line = ''
            for x, j in enumerate(i):
                if set >= 0:
                    if x % self.__unite == 0 and x != len(i) - 1: line += j + space
                    else: line += j
                elif x % self.__unite == 0:
                    str_start_point, str_end_point = x, x + self.__unite
                    line += remove_char(self.shape[y][str_start_point:str_end_point], self.fill, abs(set))
            state.append(line)
        self.__unite = val
        self.shape = state
        
    @updates.setter
    def newUpdate(self, new_update): self.__updates.append(new_update)
    @updates.setter
    def updateToCut(self, removed_update): self.__updates.remove(removed_update)
    @updates.setter
    def updates(self, new_updates): self.__updates = new_updates
    @actions.setter
    def newAction(self, new_action): self.__actions.append(new_action)
    @actions.setter
    def actionToCut(self, removed_action): self.__actions.remove(removed_action)
    @actions.setter
    def actions(self, new_actions): self.__actions = new_actions
    
    # Progressors 
    def get_size(self): return max([len(i) for i in self.shape]), len(self.shape)    
    def get_shape_from(self, graph= None):
        if graph is None: graph = self.graph
        return remote(clist= graph, shape= True)  
          
    def get_corners(self):
        self.apply()
        corners = [[0, 0], [0, 1], [1, 0], [1, 1]]
        corners =  [[x[0] * (self.h - 1), x[1] * (self.w - 1)] for x in corners if self.shape[x[0] * (self.h - 1)][x[1] * (self.w - 1)] != self.fill]
        return corners
        
    def limit_of_shape(self):
        corners = self.get_corners()
        maxpointX = max([(Vec2(*x) - self.origion).x for x in corners])  
        maxpointY = max([(Vec2(*x) - self.origion).y for x in corners])    
        minpointX = min([(Vec2(*x) - self.origion).x for x in corners])  
        minpointY = min([(Vec2(*x) - self.origion).y for x in corners]) 
        farX, farY = maxpointX, maxpointY
        if abs(minpointX) > abs(maxpointX): farX = minpointX
        if abs(minpointY) > abs(maxpointY): farY = minpointY
        return farX, farY
        
    def displacement(self, refrence_obj):
        p1, p2 = self.pos, self.pos + Vec2(abs(self.w * self.unite * self.vector[0]), abs(self.h * self.vector[1]))
        p3, p4 = refrence_obj.pos, refrence_obj.pos + Vec2(abs(refrence_obj.w * refrence_obj.unite * refrence_obj.vector[0]), abs(refrence_obj.h * refrence_obj.vector[1]))
        maxpointX = max(p2.x, p4.x)
        maxpointY = max(p2.y, p4.y)
        minpointX = min(p1.x, p3.x)
        minpointY = min(p1.y, p3.y)
        return Vec2(minpointX, minpointY), Vec2(maxpointX, maxpointY)
    
    # Sets Function
    def reset(self, graph): self.shape = self.get_shape_from(graph)
    def set_shape(self, shape): self.shape = shape
    def set_unite(self, val): self.unite = val
    def set_pos(self, x, y): self.pos = Vec2(x, y)
    def set_size(self, w, h):
        self.__prevw, self.__prevh = self.w, self.h
        self.w, self.h = w, h
            
    # Creative Shapes    
    def create_shape(self, shape_name= None, shape= None, smooth= 0):
        self.shape = []
        revy, revx = False, False
        if self.h < -1: revy= True
        if self.w < -1: revx= True
        if self.h > -1: revy = False
        if self.w > -1: revx = False
        h, w = abs(self.h), abs(self.w)
        # shaping      
        if h == 0: self.shape = [self.cell * w]
        elif w == 0: self.shape = [self.cell] * h
        elif shape_name == 'rectangle': self.rectangle(w, h)
        elif shape_name == 'right_triangle': self.right_triangle(w, h, convert_to_bool(smooth))
        elif shape_name == 'triangle': self.triangle(w, h, 1, 0, convert_to_bool(smooth))
        elif shape_name == 'v_triangle': self.triangle(w, h, 0, 1, convert_to_bool(smooth))
        elif shape_name == 'circle': self.circle(w, h, smooth)
        elif shape_name == 'hor_line': self.hor_line(w)
        elif shape_name == 'vert_line': self.vert_line(h)
        elif shape_name != None: self.shape = shape
        if revx | revy: 
            self.grab((self.w - self.__prevw) * revx, (self.h - self.__prevh) * revy)
            self.reverse(revx, revy)
            
    # World Setups
    @classmethod
    def clear_world(cls): del cls.world
            
    # Drawers
    def refresh(self):
        self.inherObj.reset(self.inherObj.add_remove_objects(self, True))
        [obj.inherObj.reset(obj.inherObj.add_remove_objects(obj, True)) for obj in self.children.values()]
        [act() for act in self.actions]
        [update() for update in self.updates]
        [obj.inherObj.reset(obj.inherObj.add_remove_objects(obj)) for obj in self.children.values()]
        self.inherObj.reset(self.inherObj.add_remove_objects(self))

    def draw(self):
        if self.shape.__class__ is list:[print(row) for row in self.shape]
        else:
            rows = list(self.shape.split(CODE))
            [print(row) for row in rows]
    
    # Contorllers, Editors
    def select(self, pointer= [0, 0], select_box= [1, 1], name= 'default name'):
        px, py = pointer
        bx, by = select_box
        part = []
        for y in self.shape[py: py + by]: part.append(y[px: px + bx])
        selected = Shape(width= bx, height= by, unite= self.unite, cell= self.cell, fill= self.fill)
        selected.pos = Vec2(px, py)
        selected.inherObj = self
        selected.shape = part
        self.dissolve_vertixes(pointer, select_box)
        if name is None: return part
        selected.__name__ = name
        self.children[name] = selected
        
    def dissolve_vertixes(self, pointer= [0, 0], clear_box= [1, 1]):
        graph, px, py, bx, by = self.graph, *pointer, *clear_box
        fill = self.enviroment.fill if type(self) is Shape else self.fill
        for y in range(py, py + by): graph[y][px: px + bx] = fill * len(graph[y][px: px + bx])
        self.shape = self.get_shape_from(graph)
    def subdivide(self, value = 1, vert= '|', hor= '-', link= '+'):
        self.modifires.subdivide(self, value, vert, hor, link)
        self.subvalue = value, vert, hor, link
                       
    def change_style(self, cell = None, fill= None):
        if cell == None: cell = self.cell
        if fill == None: fill = self.fill
        graph = self.graph
        for n, i in enumerate(graph):
            for k, j in enumerate(i):
                if j == self.cell: graph[n][k] = cell
                elif j == self.fill: graph[n][k] = fill
        self.shape = self.get_shape_from(graph)        
        self.cell = cell
        self.fill = fill
        
    # Parent Progress
    def parent(self, obj = None, names_set= ('PARENTOBJECT:', 'PARENTOBJECT:')):
        w, h = abs(self.w), abs(self.h)
        minpoint, maxpoint = self.displacement(obj)
        self.children[names_set[0] + self.__name__] = self.duplicate(x=0, y=0)
        self.children[names_set[1] + obj.__name__] = obj
        if self.children.get(obj.__name__) != None: del self.children[obj.__name__]
        projected_w, projected_h = (maxpoint - minpoint).xy
        self.enviroment.add_to_sence(self)
        self.enviroment.add_to_sence(obj)
        self.shape = self.enviroment.select(pointer= minpoint.xy, select_box= (projected_w - 1, projected_h), name= None)
        self.names_set = names_set
        self.w, self.h = projected_w // self.unite, projected_h
        self.pos = minpoint
        self.enviroment.delete(obj)
        self.enviroment.delete(self)
        
    def unparent(self, names_set= None):
        if names_set is None: names_set = self.names_set
        self.w, self.h = self.children[names_set[0]].w, self.children[names_set[0]].h
        self.shape = self.children[names_set[0]].shape
        del self.children[names_set[0]]
        del self.children[names_set[1]]
    # Adders
    def add_remove_objects(self, obj, remove= False):
        x, y = obj.pos.xy
        shape = obj.shape
        world = self.graph
        if y >= 0 and x >= 0:
            for n, i in enumerate(shape):
                vy = y + n * self.vector[1]
                if vy < len(world):
                    for k, j in enumerate(i):
                        vx = x + k * self.vector[0]
                        if vx < len(world[vy]): world[vy][vx] = j if not remove else self.fill
        return world
    def add_object(self, obj):
        self.shape = self.get_shape_from(self.add_remove_objects(obj, False))
        if self.children.get(obj.__name__) == None: self.children[obj.__name__] = obj
        if obj.refresh not in self.updates: self.newUpdate = obj.refresh
        if obj.animation != None:
            if obj.animation.animate not in self.actions: self.newAction = obj.animation.animate
        obj.inherObj = self
    def remove_object(self, obj):
        self.shape = self.get_shape_from(self.add_remove_objects(obj, True))
        if self.children.get(obj.__name__) != None: del self.children[obj.__name__]
        if obj.refresh in self.updates: self.updateToCut = obj.refresh
        if obj.animation != None:
            if obj.animation.animate in self.actions: self.actionToCut = obj.animation.animate
        obj.inherObj = self.enviroment
        
    def add_text(self, text= '', pos= [0, 0], vector= [1, 0]):
        if type(text) == Text: 
            text.surface, self.children[text.__name__], txt, x, y, vector = self, text, text.txt, *text.pos.xy, text.vector
            if text.refresh not in self.updates: self.newUpdate = text.refresh
            if text.animation != None:
                if text.animation.animate not in self.actions: self.newAction = text.animation.animate
        else: txt, x, y = text, *pos
        graph = self.graph
        dirx, diry = vector
        x *= self.unite
        for n, ch in enumerate(txt):
            vx, vy = x + n * dirx, y + n * diry
            if y >= 0 and x >= 0 and vy < self.get_size()[1]:
                if vx < len(graph[vy]): graph[vy][vx] = ch
        self.shape = self.get_shape_from(graph)
        
    def multi_texts_add(self, *texts_id:list):
        if texts_id != []: [self.add_text(_id) for _id in texts_id]
    # Translatio, Scale, Reversion, Join, Duplication, Modifires
    def grab(self, x=1, y=1):
        self.pos += Vec2(x, y)
        return self.pos
    
    def scale(self, x= 1, y= 1, to_side= True):
        self.__prevw, self.__prevh = self.w, self.h
        self.h = int(self.h + y)
        self.w = int(self.w + x)
        if to_side: self.pos -= Vec2(x, y)
        return self.w, self.h, self.pos
    
    def rotate_side(self):
        self.apply()
        rotated = ['' * self.get_size()[1]] * self.get_size()[0]
        for y, i in enumerate(self.shape):
            for x, j in enumerate(i): rotated[x] = rotated[x].__add__(j)
        self.shape = rotated
        
    def join(self, obj, offset= 0):
        right, left = False, False
        w, h, _w, _h = abs(self.w), abs(self.h), abs(obj.w), abs(obj.h)
        graph = self.graph
        if len(self.graph) >= len(obj.graph):
            graph = self.graph
            cycle = obj.graph
            right = True
        else: 
            graph = obj.graph
            cycle = self.graph + [[self.enviroment.fill] * w] * (_h - w + 1)
            left = True
        for n, i in enumerate(cycle):
            if right:
                length = len(graph[n]) - 1 
                graph[n] =  graph[n][:length+offset] + i
            if left: [graph[n].insert(0, j) for j in i]
        if left: 
            self.pos = Vec2(obj.pos.x - w - offset - 1, obj.pos.y)
            self.h = obj.h
        self.w = _w + w + offset 
        self.shape = self.get_shape_from(graph)   
        
    def reverse(self, x= True, y= False):
        if x: self.apply()
        graph = self.graph
        if x:
            for n, i in enumerate(graph): graph[n] = i[::-1]
        if y:
            for n, i in enumerate(graph): 
                exc = graph[-1]
                graph.insert(n, exc)
                del graph[-1]
        self.shape = self.get_shape_from(graph)
        
    def duplicate(self, x= 1, y= 1):
        return self.modifires.duplicate(obj=self, x=x, y=y)
        
    def mirror(self, **kwargs):
        mirror_obj = self.modifires.mirror(obj=self, **kwargs)
        self.parent(object = mirror_obj, names_set= ('mirror:', 'mirror:'))
    def dis_mirror(self): self.unparent(names_set= ('mirror:', 'mirror:'))    
    
    # Appliers
    def apply(self):
    	for n, i in enumerate(self.shape):
            length = abs(self.w) - len(i)
            self.shape[n] = i.__add__(self.enviroment.fill * length)
    def apply_mirror_objects(self): self.modifires.apply_mirror(self)
    
    # Collisions Funcations     
    def on_collision(self, obj, dist= 1):
        x, w, y, h  = self.pos.x, abs(self.w) * self.unite, self.pos.y, abs(self.h)
        _x, _w, _y, _h = obj.pos.x, abs(obj.w) * obj.unite, obj.pos.y, abs(obj.h)
        if x + w + dist >= _x + _w >= x - dist and y + h + dist >= _y + _h >= y - dist: return 1
        return 0
        
    def check_collisions(self, obj, dist= 1):
        if self.on_collision(obj, dist) | obj.on_collision(self, dist) : return 1
        return 0

class Rectangle(Shape):
    no = -1
    def __init__(self, width= 0, height = 0, name= 'rectangle', n_of_edges= [1, 1], unite=1, cell= '*', fill= ' '):
        super().__init__(
        height= height,    
        width= width,
        name= 'rectangle',
        n_of_edges= n_of_edges,
        unite= unite,
        cell= cell,
        fill= fill
        )
        self.rectangle(width, height)    
    # Draw
    def rectangle(self, w= 0, h= 0):
        edgx = 1 if self.no_edgx > 0 else 0
        edgy = self.no_edgy - 1 if self.no_edgy > 0 else 1
        self.no_edgx, self.no_edgy = abs(self.no_edgx), abs(self.no_edgy)
        atom, space = f'{self.cell}{self.fill * (self.unite - 1)}', f'{self.fill * self.unite}'
        limiter = h + edgy * 2
        root = (edgx - self.no_edgx) * 2
        for y in range(limiter):
            if y < self.no_edgy or y >= limiter - self.no_edgy:
                ele = atom * (w + root + self.no_edgx * 2 - 3) + self.cell
            else:
                ele = f'{atom * self.no_edgx}{space * (w + root - 2)}{self.cell * self.no_edgx}'
            self.shape.append(ele)
        self.up, self.down = self.no_edgy, self.no_edgy
        self.right, self.left = self.no_edgx, self.no_edgx
class Triangle(Shape):
    no = -1
    def __new__(cls, width= 0, height= 0, smooth= 0, typeOftriangle= 'right', name= 'triangle', n_of_edges= [1, 1], unite=1, cell= '*', fill= ' '):
        return super().__new__(cls)
    def __init__(self, width= 0, height= 0, smooth= 0, typeOftriangle= 'right', name= 'triangle', n_of_edges= [1, 1], unite=1, cell= '*', fill= ' '):
        super().__init__(
        height= height,    
        width= width,
        name= 'triangle',
        n_of_edges= n_of_edges,
        unite= unite,
        cell= cell,
        fill= fill
        )
        if typeOftriangle == "right": self.right_triangle(width, height, smooth)
        if typeOftriangle == "normal_hor": self.triangle(width, height, 1, 0, smooth)
        if typeOftriangle == "normal_vert": self.triangle(width, height, 0, 1, smooth)
    
    def right_triangle(self, w = 0, h = 0, smooth_lines: bool = False):
        edgx = self.no_edgx - 1 if self.no_edgx > 0 else 0
        edgy = self.no_edgy - 1 if self.no_edgy > 0 else 0
        self.no_edgx, self.no_edgy = abs(self.no_edgx), abs(self.no_edgy)
        displacement = 0 if edgy else self.no_edgy - 1
        atom, space =  f'{self.cell}{self.fill * (self.unite - 1)}', f'{self.fill * self.unite}'   
        limiter = h + edgy
        root = w + edgx
        root_sq = [i for i in range(root)]
        ratio = root / limiter
        for y in range(limiter):
            _r = (y, root_sq[int(y * ratio)])[smooth_lines]
            if not y: ele = atom
            elif y >= limiter - self.no_edgy:
                if not edgy:
                    ele = atom * (root - displacement - 1) + self.cell
                    displacement -= 1
                else:
                    ele = atom * (root + displacement - 1) + self.cell
                    displacement += 1    
            else:
                n = self.no_edgx - 1
                ele =  f'{atom * self.no_edgx}{space * (_r - n)}{self.cell}'
            self.shape.append(ele)
        self.up, self.down = 1, self.no_edgy
        self.right, self.left = self.no_edgx, 1
        self.__name__ = 'right_triangle' + f'({self.no})' * convert_to_bool(self.no)
    def triangle(self, w = 0, h = 0, x = 1, y = 0, smooth_lines= True):
        if x: w = w // 2
        if y: h, w, self.__name__ = w // 2, h, 'v_triangle' + + f'({self.no})' * convert_to_bool(self.no)
        self.right_triangle(w, h, smooth_lines)
        self.reverse(x, 0)
        obj_copy = self.mirror(x = x, y = y, offset = -x, mirror_obj_name='half_triangle')
        screen = World(height= w, width= h, unite= 1, space= self.fill)
        screen.add_to_sence(self)
        screen.add_to_sence(obj_copy)
        self.shape = screen.sence
        
class Circle(Shape):
    no = -1
    def __new__(cls, raduis = 0, pull = 0, smooth= 0, name= 'circle', n_of_edges= [1, 1], unite=1, cell= '*', fill= ' '):
        return super().__new__(cls)
    def __init__(self, raduis = 0, pull = 0, smooth= 0, name= 'circle', n_of_edges= [1, 1], unite=1, cell= '*', fill= ' '):
        super().__init__(
        height= pull,
        width= raduis,
        name= 'circle',
        n_of_edges= n_of_edges,
        unite= unite,
        cell= cell,
        fill= fill
        )
        self.circle(raduis, pull, smooth)
        
    def circle(self, w = 0, pull = 0, smooth= 0):
        w //= 2
        cell, fill = (self.cell + self.fill * (self.unite - 1)) * self.no_edgx, self.fill * self.unite
        for r in range(w):
            rx = int(r * (w - r - 1) / 2 ** log(pull))
            rfix = int((w - rx - 1) * r * (w - r - 1) / (w * smooth)) if smooth else 0
            self.shape.append(self.inherObj.fill * (w - rx - rfix - 1) + cell + fill * (rx + rfix - 1) + fill * (rx + rfix) + cell * convert_to_bool(rx))

class Text(Shape):
    no = -1
    def __new__(cls, txt= 'untitled', pos= [0, 0], vector= [1, 0], surface= None, fill= ' '):
        return super().__new__(cls, name= 'text', shape= txt)
    def __init__(self, txt= 'untitled', pos= [0, 0], vector= [1, 0], surface= None, fill= ' '):
        self.inherObj = surface
        self.background = ''
        super().__init__(width= len(txt),
        				 height= 1,
                         name= 'text',
                         fill= fill)
        self.vector = vector                 
        self.shape = [txt]
        self.unite = surface.unite
        self.pos = Vec2(*pos)
        self.background = self.surface.shape[self.pos.y][self.pos.x : self.pos.x + self.length]
        self.surface.texts.append(self)
     
    @property
    def surface(self): return self.inherObj    
    @property
    def length(self): return len(self.txt)
    @property
    def txt(self): return self.shape[0]
    @surface.setter
    def surface(self, instance): self.inherObj = instance
    @txt.setter
    def txt(self, script): self.shape = script
    def uppercase(self): self.shape = [self.txt.upper()]
    def lowercase(self): self.shape = [self.txt.lower()]
    def erase(self): self.surface.add_text(self.background, self.pos.xy, self.vector)
    def rewrite(self):
        if self.surface.children.get(self.__name__) != None:
            self.erase()
            self.surface.add_text(self)
    def grab(self, x= 1, y= 1):
        if self.surface.children.get(self.__name__) != None: self.erase()
        self.pos += Vec2(x, y)
        if self.surface.children.get(self.__name__) != None: self.surface.add_text(self)
        return self.pos

class Point(Shape):
    no = -1
    def __new__(cls, cell = 'numical', x = 0, y = 0, z = 0, name= None): return super().__new__(cls)
    def __init__(self, cell = 'numical', x = 0, y = 0, z = 0, name= None):
        self.x, self.y, self.z = 0, 0, z
        super().__init__(
        cell= cell,
        pos = (x, y),
        name = 'point'
        )
        if cell == 'numical': self.cell = self.no
        self.nodePointpairs = []
        self.__name__ = self.no if name == None else name
        self.point()
    
    @property
    def shape_name(self): return 'point'
    @property
    def pos(self): return Vec3(self.x,self.y,self.z) if self.z else Vec2(self.x,self.y)
    @pos.setter
    def pos(self, val):
        if val.__class__ == Vec3: self.x, self.y, self.z = val.xyz
        if val.__class__ == Vec2: self.x, self.y = val.xy
    def point(self): self.shape = [f"{self.cell}"]
    def link(self, point, socket= '*'):
        x1, y1, x2, y2 = *self.pos.xy, *point.pos.xy
        lenX, lenY = x2 - x1, y2 - y1
        vx = lenX // abs(lenX) if lenX else 0
        vy = lenY // abs(lenY) if lenY else 0
        lenX, lenY = abs(lenX), abs(lenY)
        world = self.inherObj.graph
        offsetObj = self.inherObj.fill
        for dy in range(lenY if lenY else lenX):
            if lenY: dx = lenX * dy // lenY
            x, y = x1 + (dx if lenY else dy) * vx, y1 + dy * vy
            if 0 < y < len(world):
                if 0 < x < len(world[y]): world[y][x] = socket
        self.inherObj.shape = self.inherObj.get_shape_from(world)
        self.nodePointpairs.append(point)
        point.nodePointpairs.append(self)
    def clearlinks(self): 
        [self.link(nodeleg, self.inherObj.fill) for nodeleg in self.nodePointpairs]
        self.nodePointpairs = []
    @staticmethod
    def coordient_out(n): return -1 if 1 > abs(n - floor(n)) > 0 else int(n)

class World(Shape):
    no = -1
    def __new__(cls, height= DEFULT_HIGTH, width= DEFULT_WIDTH, unite= 1, space= ' '):
        return super().__new__(cls,
        height= height,    
        width= width,
        name= 'world',
        unite= unite,
        fill= space
        )
    def __init__(self, height= DEFULT_HIGTH, width= DEFULT_WIDTH, unite= 1, space= ' '):
        super().__init__(
        height= height,
        width= width,
        name= 'world',
        unite= unite,
        fill= space
        )
        self.shape = [space * width] * height
        Shape.enviroment = self
        
    @property 
    def map(self):
        return self.chart()
    @property
    def world(self):
        return self.graph
    @world.setter
    def world(self, graph):
        self.graph = graph   
    @property
    def sence(self): return self.shape
    def __add__(self, obj : Shape = None): return self.add_remove_objects(obj, False)
    def __sub__(self, obj : Shape = None): return self.add_remove_objects(obj, True)
    def add_to_sence(self, obj = None): self.add_object(obj)
    def delete(self, obj = None): self.remove_object(obj)
    def refresh(self):
        system("cls")
        [self.reset(self - obj) for obj in self.children.values()]
        [act() for act in self.actions]
        [update() for update in self.updates]
        [self.reset(self + obj) for obj in self.children.values()]
        self.draw()

if __name__ == "__main__":
    print(__doc__)