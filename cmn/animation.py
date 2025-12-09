from .vectors import Vec2
from .models import Text

class Squence(dict):
    def __init__(self, length, animation):
        self.animation = animation
        self.cursor = 0
        self.header = 1
        self.length = length
        self.play = True
        self.frames = {}
        self.__gensq__()
    def __gensq__(self):
        for n in range(self.length):
            self.frames[n] = {
            'render': [self.animation.obj.shape_name, self.animation.obj.shape],    
            'trans' : self.animation.obj.pos.xy,
            'size': self.animation.obj.size,
            'subdiv': self.animation.obj.subvalue,
            'styl': (self.animation.obj.cell, self.animation.obj.fill),
            'txt': self.animation.obj.texts,
            'unite': [self.animation.obj.unite],
            'type': 'DEFULT'
            }

    def __read_data_from__(self, pointer): return self.frames[self.cursor][pointer]
    def __write_data_in__(self, pointer, data): self.frames[self.cursor].update({pointer : data})
    def __write_data_in_id__(self, pointer, id, data): self.frames[self.cursor][pointer][id] = data
    def __repr__(self): return f'Sequence( {self.frames} )'

    def append(self, type, delay= 1, **data):
        if self.header < self.length:
            self.animation.obj.animate_type = type
            [self.frames[self.header + i].update(data) for i in range(delay)]
            if self.frames[self.header]['type'] == 'DEFULT': self.frames[self.header]['type'] = type
            if type not in self.frames[self.header]['type']: self.frames[self.header]['type'] += f' AND {type}'
            self.header += delay

    def insert(self, **data): self.frames[self.header].update(data)
    def _squence_to(self, type= 'trans', sq_func= None):
        if self.play: sq_func(*self.frames[self.cursor][type])
    def fitframes(self, **data):[self.frames[self.header + fitpoint].update(data) for fitpoint in range(self.length - self.header)]
    def resume_animation(self): self.play = True
    def pause_animation(self): self.play = False
        
class Animation(Squence):
    pause = False
    def __init__(self, object, length= 100, speed= 1, passes= 1):
        self.obj = object
        self.speed = speed
        self.passes = passes
        self.playpass = 0
        object.animation = self
        super().__init__(length, self)

    def reset(self):
        self.header = 1

    def animate(self):
        self._squence_to('styl', self.obj.change_style)
        self._squence_to('trans', self.obj.set_pos)
        self._squence_to('size', self.obj.set_size)
        self._squence_to('unite', self.obj.set_unite)
        self.__write_data_in_id__('render', 1, self.obj.shape)
        self._squence_to('render', self.obj.create_shape)
        self._squence_to('subdiv', self.obj.subdivide)
        self._squence_to('txt', self.obj.multi_texts_add)
        # refresh objects
        if self.obj.__class__ == Text:self.obj.rewrite()
        # jump to the next frame if timeline is end repeat
        self.cursor += self.speed * self.play
        if self.playpass <= self.passes and self.cursor == self.length: 
            self.cursor %= self.length
            self.playpass += (1 if self.passes else 0) 
        delta = Vec2(*self.frames[self.cursor]['trans']) - Vec2(*self.frames[self.cursor - 1 * (self.cursor != 0)]['trans'])
        if 'SCALE' in self.frames[self.cursor]['type']: self.__write_data_in__('trans', (self.obj.pos + delta).xy)

    # create animation
    def translation(self, x=1, y= 1, t_squence = None, dltdelay= 1):
        Xtarget, Ytarget= x, y
        repos, resize = self.obj.pos, self.obj.size
        if t_squence == "grab":
            x -= self.obj.pos.x
            y -= self.obj.pos.y
        if t_squence == "scale":
            x -= self.obj.w
            y -= self.obj.h
        x //= self.speed
        y //= self.speed
        dx, dy = abs(x), abs(y)
        a, b = max(dx, dy), min(dx, dy)
        delay = a // b if b else a
        connect = {dx: [1, 0], dy: [0, 0]}
        dirx = x // dx if dx else 0
        diry = y // dy if dy else 0
        for fr in range(a):
            connect[b][1] = self.speed if fr % delay == 0 else 0
            connect[a][1] = self.speed
            if connect[a][0]: c, d = connect[a][1], connect[b][1]
            else: c, d = connect[b][1], connect[a][1]
            c, d = c * dirx, d * diry
            if t_squence == 'grab':
                if (self.obj.pos.x + c > Xtarget and dirx == 1) | (self.obj.pos.x + c < Xtarget and dirx == -1): c = (Xtarget - self.obj.pos.x) * dirx
                if (self.obj.pos.y + d > Ytarget and diry == 1) | (self.obj.pos.y + d < Ytarget and diry == -1): d = (Ytarget - self.obj.pos.y) * diry
                self.append(type = "LOCATION", delay = dltdelay, trans = self.obj.grab(c,d).xy)
                self.fitframes(trans = self.frames[self.header-1]['trans'])
            if t_squence == 'scale':
                self.obj.pos = Vec2(*self.frames[self.header-1]['trans'])
                scaleStep = self.obj.scale(c,d)
                if (self.obj.w + c > Xtarget and dirx == 1) | (self.obj.w + c < Xtarget and dirx == -1): c = Xtarget - self.obj.w
                if (self.obj.h + d > Ytarget and diry == 1) | (self.obj.h + d < Ytarget and diry == -1): d = Ytarget - self.obj.h
                self.append(type = "SCALE", delay = dltdelay, size = scaleStep[:2])
                self.header -= dltdelay
                self.append(type = "SCALE", delay = dltdelay, trans = scaleStep[2].xy)
                self.fitframes(size = self.frames[self.header-1]['size'])
                self.fitframes(trans = self.frames[self.header-1]['trans'])
        self.obj.pos, self.obj.w, self.obj.h = repos, *resize

    def shape_animation(self, shapes= [], delay = 1):
        [self.append(type= "RENDER", delay = delay, render = ['RenderDraw', shape]) for shape in shapes]
        self.fitframes(render = self.frames[self.header-1]['render'])    

    def subdivide_animation(self, _rv= [1, 1], cut_sq = [('|', '-', '+')], delay = 1):
        a, b = _rv
        amove = -1 if a > b else 1
        if len(cut_sq) < abs(a - b): cut_sq +=  [cut_sq[-1]] * (abs(a - b) - len(cut_sq))
        [self.append(type = "SUBDIVIDE", delay = delay, subdiv = (fr, *cut_sq[fr - a])) for fr in range(a, b)[::amove]]
        self.fitframes(subdiv = self.frames[self.header-1]['subdiv'])

    def unite_animation(self, uni_range= [1, 1], delay = 1):
        amove = -1 if uni_range[0] > uni_range[1] else 1
        a, b = min(*uni_range), max(*uni_range)
        [self.append(type = "UNITE", delay = delay, unite = [uni]) for uni in range(a, b)[::amove]]
        self.fitframes(unite = self.frames[self.header-1]['unite'])

    def style_animation(self, st_sq = [], delay = 1): 
        [self.append(type = "STYLE", delay = delay, styl = stl) for stl in st_sq]
        self.fitframes(styl = self.frames[self.header-1]['styl'])

    def text_animation(self, txt_sq = [], delay = 1):
        [self.append(type = "TEXT", delay = delay, txt = txt) for txt in txt_sq]
        self.fitframes(txt = self.frames[self.header-1]['txt']) 
   
    def draw_animation(self, t_draw= 'print', delay = 1):
        frameY = []
        frameX = ''
        frames = []
        for y, i in enumerate(self.obj.shape):
            if t_draw == 'build':
                for j in i:
                    frameX += j
                    frames.append(frameY + [frameX])
                frameX = ''
                frameY += [i]
            if t_draw == 'print': 
                frames.append(self.obj.shape[:y + 1])
        self.shape_animation(frames, delay = delay)