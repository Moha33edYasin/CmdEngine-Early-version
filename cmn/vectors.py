class Vec2:
    def __init__(self, x=0, y=0):
        self.x, self.y, self.z = x, y, 0

    @property    
    def xy(self):
        return self.x, self.y
    
    @xy.setter
    def xy(self, coordient):
        self.x, self.y = coordient[0], coordient[1]      
    
    def __repr__(self):
        return f'Vec2({self.x}, {self.y})'  
    
    def __add__(self, coordient):   
        return Vec2(self.x + coordient.x, self.y + coordient.y)
    
    def __sub__(self, coordient):   
        return Vec2(self.x - coordient.x, self.y - coordient.y)
    
    def __mul__(self, array):
        return Vec2(self.x * array[0][0] + self.y * array[0][1], self.x * array[1][0] + self.y * array[1][1])
    
    def __abs__(self):
        return Vec2(abs(self.x), abs(self.y))    
    
    def __round__(self):
        return Vec2(round(self.x), round(self.y))   
    
    @classmethod     
    def max(cls, vectors):
        mx, my = max([v.x for v in vectors]), max([v.y for v in vectors]) 
        return cls(mx, my)
         
    @classmethod     
    def min(cls, vectors):
        mx, my = min([v.x for v in vectors]), min([v.y for v in vectors]) 
        return cls(mx, my)
    
class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z
    
    @property    
    def xy(self):
        return self.x, self.y
    
    @property    
    def xyz(self):
        return self.x, self.y, self.z
    
    @property    
    def xz(self):
        return self.x, self.z
    
    @property    
    def yz(self):
        return self.y, self.z    
        
    def __repr__(self):
        return f'Vec3({self.x}, {self.y}, {self.z})'  
    
    def __add__(self, coordient):   
        return Vec3(self.x + coordient.x, self.y + coordient.y, self.z + coordient.z)
    
    def __sub__(self, coordient):   
        return Vec3(self.x - coordient.x, self.y - coordient.y, self.z - coordient.z)
    
    def __mul__(self, array):
        return Vec3(self.x * array[0][0] + self.y * array[0][1] + self.z * array[0][2], 
                    self.x * array[1][0] + self.y * array[1][1] + self.z * array[1][2],
                    self.x * array[2][0] + self.y * array[2][1] + self.z * array[2][2])
    
    def __abs__(self):
        return Vec3(abs(self.x), abs(self.y), abs(self.z))    
    
    def __round__(self):
        return Vec3(round(self.x), round(self.y), round(self.z))
    
    @classmethod     
    def max(cls, vectors):
        mx, my, mz = max([v.x for v in vectors]), max([v.y for v in vectors]), max([v.z for v in vectors]) 
        return cls(mx, my, mz)
    
    @classmethod     
    def min(cls, vectors):
        mx, my, mz = min([v.x for v in vectors]), min([v.y for v in vectors]), min([v.z for v in vectors]) 
        return cls(mx, my, mz)     
