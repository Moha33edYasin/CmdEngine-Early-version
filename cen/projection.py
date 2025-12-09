from .models import Shape, Point
from .vectors import Vec2, Vec3
from math import tau, sin, cos, log, sqrt

class Shape2D(Shape):
    no = -1
    def __init__(self, width= 0, height = 0, unite=1, cell= '*', fill= ' '):
        super().__init__(height = height, width = width, unite = unite, cell = cell, fill = fill)

        self.origion = Vec2(0, 0)
        self.points = {}
    
    def convert_to_shape(self, link= '*'):
        XPoints, YPoints = [point.x for point in self.points.values()], [point.y for point in self.points.values()]
        maxPointX, maxPointY = max(XPoints), max(YPoints)
        minPointX, minPointY = min(XPoints), min(YPoints)
        self.add_points(link)
        self.shape = self.inherObj.select(pointer = [minPointX, minPointY], select_box = [maxPointX - minPointX + 1, maxPointY - minPointY + 1], name = None)
        self.delete()
    
    def setPoint(self, __points):
        last = max(list(self.points.keys())) if list(self.points.keys()) != [] else -1
        for point in __points:
            last += 1
            self.points[last] = point

    def locatePoints(self): 
        return self.pos.x - self.w // 2 - self.origion.x, self.pos.y - self.h // 2 - self.origion.y, self.pos.x + self.w // 2 - self.origion.x, self.pos.y + self.h // 2 - self.origion.y

    def linkPoints(self, vertixes, _by):
        numberOfvertixes = len(vertixes)
        for i in range(numberOfvertixes):
            linkedpoint1, linkedpoint2 = vertixes[i], vertixes[(i + 1) % numberOfvertixes]
            if self.points[linkedpoint2] not in self.points[linkedpoint1].nodePointpairs: 
                self.points[linkedpoint1].link(self.points[linkedpoint2], _by)

    def add_points(self, link= '*', org= True):
        self.linkPoints(list(self.points.keys()), link)
        [self.inherObj.add_object(point) for point in self.points.values()]
        if org : self.inherObj.add_object(Point("•", *(self.pos + self.origion).xy))

    def delete(self):
        self.linkPoints(list(self.points.keys()), self.inherObj.fill)
        self.inherObj.remove_object(Point("•", *(self.pos + self.origion).xy))
        for point in self.points.values(): point.inherObj.remove_object(point)
            
    # Controll
    def grab(self, x, y):
        for point in self.points.values(): point.pos += Vec2(x, y)
        self.origion += Vec2(x, y)

    def scale(self, x, y):
        for point in self.points.values():
            scale_array = [
            [self.w * x, 0],
            [0, self.h * y]
        ]
            length = sqrt(point.x ** 2 + point.y ** 2)
            normalize_array = [
            [1 / length, 0],
            [0, 1 / length]
        ]
            point.pos = round(point.pos * normalize_array * scale_array)

    def rotate(self, angle):
        angle %= tau
        sin_a, cos_a = sin(angle), cos(angle)
        rotation_array = [
            [cos_a, -sin_a],
            [sin_a, cos_a]
        ]
        for point in self.points.values(): point.pos = round((point.pos - self.origion) * rotation_array) + self.origion # normalize pos by origion

class Shape3D(Shape2D):
    no = -1
    def __init__(self, width= 0, height = 0, depth= 0, unite=1, cell= '*', fill= ' '):
        super().__init__(height, width, unite, cell, fill)
        self.d = depth
        self.pos = Vec3(0, 0, 0)
        self.origion = Vec3(0, 0, 0)
        self.faces = []

    def get_center(self, vertixes):
        mx, my, mz = max([self.points[v].x for v in vertixes]), max([self.points[v].y for v in vertixes]), max([self.points[v].z for v in vertixes])
        sx, sy, sz = max([self.points[v].x for v in vertixes]), max([self.points[v].y for v in vertixes]), max([self.points[v].z for v in vertixes])
        return (mx + sx) // 2 + self.origion.x, (my + sy) // 2 + self.origion.y, (mz + sz) // 2 + self.origion.z

    def locatePoints(self): 
        return (self.pos.x - self.w // 2 - self.origion.x, self.pos.y - self.h // 2 - self.origion.y, self.pos.z - self.d // 2 - self.origion.z,
                self.pos.x + self.w // 2 - self.origion.x, self.pos.y + self.h // 2 - self.origion.y, self.pos.z + self.d // 2 - self.origion.z)
    
    def setFaces(self, faces):
        for face in faces: self.faces.append(face)

    def linkFaces(self, faces, _by, relink = False):
        numberOffaces = len(faces)
        for i in range(numberOffaces): self.linkPoints(faces[i], _by)
        for face in faces:
            for v in face: self.points[v].nodePointpairs = []

    def add_points(self, link= '*', org= True):
        # Projection
        for point in self.points.values(): point.pos = Vec2(point.x, point.y)
        self.pos = Vec2(*self.pos.xy)
        self.origion = Vec2(*self.origion.xy)
        # Add faces
        self.linkFaces(self.faces, link)
        [self.inherObj.add_object(point) for point in self.points.values()]
        if org : self.inherObj.add_object(Point("•", *(self.pos + self.origion).xy))

    def delete(self):
        self.linkFaces(self.faces, self.inherObj.fill)
        self.inherObj.remove_object(Point("•", *(self.pos + self.origion).xy))
        for point in self.points.values(): point.inherObj.remove_object(point)
        # unprojection
        for point in self.points.values(): point.pos = Vec3(point.x, point.y, point.z)

    def deletvertix(self, v):
        self.points[v].clearlinks()
        del self.points[v]
        [face.remove(v) for face in self.faces if v in face]
        
    def merge(self, *vertixes):
        cx, cy, cz = self.get_center(vertixes)
        normal_faces_len = [len(face) for face in self.faces]
        for v in vertixes: self.deletvertix(v)
        self.points[vertixes[0]] = Point(vertixes[0], cx, cy, cz)
        [face.append(vertixes[0]) for n, face in enumerate(self.faces) if len(face) < normal_faces_len[n]]

    # Controll
    def grab(self, x, y, z):
        for point in self.points.values(): point.pos += Vec3(x, y, z)
        self.pos += Vec3(x, y, z)

    def scale(self, x, y, z):
        for point in self.points.values():
            scale_array = [
            [self.w * x, 0, 0],
            [0, self.h * y, 0],
            [0, 0, self.d * z]
        ]
            length = sqrt(point.x ** 2 + point.y ** 2 + point.z ** 2)
            normalize_array = [
            [1 / length, 0, 0],
            [0, 1 / length, 0],
            [0, 0, 1 / length]
        ]
        point.pos = round(point.pos * normalize_array * scale_array)

    def rotate_x(self, angle):
        angle %= tau
        sin_a, cos_a = sin(angle), cos(angle)
        rotation_x_array = [
            [1, 0, 0],
            [0, cos_a, -sin_a],
            [0, sin_a, cos_a]
        ]
        for point in self.points.values(): point.pos = round((point.pos - self.pos) * rotation_x_array) + self.pos

    def rotate_y(self, angle):
        angle %= tau 
        sin_a, cos_a = sin(angle), cos(angle)
        rotation_y_array = [
            [cos_a, 0, -sin_a],
            [0, 1, 0],
            [sin_a, 0, cos_a]
        ]
        for point in self.points.values(): point.pos = round((point.pos - self.pos) * rotation_y_array) + self.pos

    def rotate_z(self, angle):
        angle %= tau
        sin_a, cos_a = sin(angle), cos(angle)
        rotation_z_array = [
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ]
        for point in self.points.values(): point.pos = round((point.pos - self.pos) * rotation_z_array) + self.pos

# ____________________Built-in 2DShapes_____________
class Rectangle2D(Shape2D):
    def __init__(self, width=0, height=0, unite=1, cell='*', fill=' '):
        super().__init__(width, height, unite, cell, fill)
        self.setPoint(self.rect())

    def rect(self):
        cell, x1, y1, x2, y2 = self.cell, *self.locatePoints()
        points = [
        Point(cell, x1, y1, 0, 0),
        Point(cell, x2, y1, 0, 1),
        Point(cell, x2, y2, 0, 2),
        Point(cell, x1, y2, 0, 3)
        ]
        return points
        
class Triangle2D(Shape2D):
    def __init__(self, width=0, height=0, unite=1, cell='*', fill=' '):
        super().__init__(width, height, unite, cell, fill)
        self.setPoint(self.triangle())

    def triangle(self, angle):
        cell, x1, y1, x2, y2 = self.cell,  *self.locatePoints()
        ab = int(self.h / sin(angle)) if sin(angle) else 0
        bc1 = int(sqrt(ab ** 2 - self.h ** 2))
        bc2 = self.w - bc1
        points = [
        Point(cell, x1, y1, 0, 0),
        Point(cell, x1 - bc1, y2, 0, 1),
        Point(cell, x1 + bc2, y2, 0, 2),
        ]
        return points

class Circle2D(Shape2D):
    def __init__(self, x_raduis=1, y_raduis= 1, unite=1, cell='*', fill=' '):
        super().__init__(x_raduis, y_raduis, unite, cell, fill)
        self.setPoint(self.circle())

    def circle(self, pull= 1, smooth= 0):
        x, y, w = *self.pos.xy, self.w * 2 + 1
        cell = (self.cell + self.fill * (self.unite - 1)) * self.no_edgx
        points = []
        for r in range(w):
            rx = int(r * (w - r - 1) / 2 ** log(pull))
            rfix = int((w - rx - 1) * r * (w - r - 1) / (w * smooth)) if smooth else 0
            rad1 = Point(cell,  x - rx + rfix, y + r - w // 2, 0, 2 * r)
            rad2 = Point(cell, x + rx - rfix, y + r - w // 2, 0, 2 * r + 1)
            points += [rad1, rad2]
        return points

# ________________ Built-in 3DShapes _________________           
class Cube(Shape3D):
    def __init__(self, width=1, height=1, depth=1, unite=1, cell='*', fill=' '):
        super().__init__(width, height, depth, unite, cell, fill)
        points, self.faces = self.cube()
        self.setPoint(points)

    def cube(self):
        cell, x1, y1, z1, x2, y2, z2 = self.cell, *self.locatePoints()
        points = [
        Point(cell, x1, y1, z1, 0),
        Point(cell, x2, y1, z1, 1),
        Point(cell, x2, y2, z1, 2),
        Point(cell, x1, y2, z1, 3),
        
        Point(cell, x1, y1, z2, 4),
        Point(cell, x2, y1, z2, 5),
        Point(cell, x2, y2, z2, 6),
        Point(cell, x1, y2, z2, 7)
        ]
        faces = [
            [0, 1, 2, 3],
            [0, 3, 7, 4],
            [3, 2, 6, 7],
            [1, 2, 6, 5],
            [0, 1, 5, 4],
            [4, 5, 6, 7]
        ]
        return points, faces
    
class Cylinder(Shape3D):
    def __init__(self, raduis=1, pull=1, depth=1, unite=1, cell='*', fill=' '):
        super().__init__(raduis, pull, depth, unite, cell, fill)
        points, self.faces = self.cylinder(raduis, pull, depth, 0)
        self.setPoint(points)

    def cylinder(self, raduis= 1, pull= 1, depth= 1, smooth_value= 0):
        def circle(self, raduis = 1, pull= 1, smooth= 0):
            x, y = self.pos.xy
            cell = (self.cell + self.fill * (self.unite - 1)) * self.no_edgx
            points = []
            for r in range(raduis):
                rx = int(r * (raduis - r - 1) / 2 ** log(pull))
                rfix = int((raduis - rx - 1) * r * (raduis - r - 1) / (raduis * smooth)) if smooth else 0
                rad1 = Point(cell,  x - rx + rfix, y + r - raduis // 2, 0, 2 * r)
                rad2 = Point(cell, x + rx - rfix, y + r - raduis // 2, 0, 2 * r + 1)
                points += [rad1, rad2]
            return points
        faces = []
        points = []
        for i in range(2):
            base_points = circle(self, raduis, pull, smooth_value)
            for point in base_points: point.z += self.pos.z + depth // 2 * (-1 if i == 0 else 1)
            points += base_points
        for v in range(len(points)):
            face = [v, v + 1, v + len(base_points) + 1, v + len(base_points)]
            face = [vertex % len(points) for vertex in face]
            faces.append(face)
        return points, faces
    
class Sphere(Shape3D):
    def __init__(self, x_raduis=1, y_raduis= 1, depth=1, unite=1, cell='*', fill=' '):
        super().__init__(x_raduis, y_raduis, depth, unite, cell, fill)
        points, self.faces = self.sphere(x_raduis, y_raduis, depth, 0)
        self.setPoint(points)

    def sphere(self, raduis= 1, pull= 1, depth= 1, smooth= 0):
        def circle(self, raduis= 1, pull= 1, smooth= 0):
            x, y = self.pos.xy
            cell = (self.cell + self.fill * (self.unite - 1)) * self.no_edgx
            points = []
            for r in range(raduis):
                rx = int(r * (raduis - r - 1) / 2 ** log(pull))
                rfix = int((raduis - rx - 1) * r * (raduis - r - 1) / (raduis * smooth)) if smooth else 0
                rad1 = Point(cell,  x - rx + rfix, y + r - raduis // 2, 0, 2 * r)
                rad2 = Point(cell, x + rx - rfix, y + r - raduis // 2, 0, 2 * r + 1)
                points += [rad1, rad2]
            return points

        uplevels, depth = 0, depth - 1
        rows = {}
        faces = []
        points = []
        for level in range(depth + 1):
            rows[level] = []
            l_raduis = level * (raduis - level)
            row_points = circle(self, l_raduis, pull, smooth)
            rows[level] = row_points
            for point in row_points: point.z += self.pos.z + depth // 2 - level
            points += row_points
        for r in rows.values():
            flip = len(r)
            for p in range(flip):
                v = p + uplevels 
                face = [v, v + 1, v + flip + 1, v + flip]
                face = [vertex % len(points) for vertex in face]
                faces.append(face)
            uplevels += flip
        return points, faces

    