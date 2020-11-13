import sys
import math

LAPS = 3

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'
        
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y
            
        
    @classmethod
    def from_list(cls, li):
        x, y = map(float, li)
        return cls(x, y)
        
    def to_list(self):
        return [self.x, self.y]


class Vector(Point):
    def __init__(self, x=0.0, y=0.0):
        super(Vector, self).__init__(x, y)
    
    @classmethod
    def from_point(cls, p):
        return cls(p.x, p.y)
        
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)
    __radd__ = __add__
        
    def __sub__(self, other):
        return self+(-other)
    __rsub__ = __sub__
        
    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)
    __rmul__ = __mul__
    
    
class Pod:
    def __init__(self, teamname, number, villain=False):
        self._teamname = teamname
        self._number = number
        self._villain = villain
        self._opponent = None
        
        self._frame = 0
        self._location = Point()
        self._next_checkpoint = Point()
        self._speed = Vector()
        self._distance = 0
        self._angle = 0
        self._thrust = 100
        
        self._lap = 1
        self._visited_checkpoints = []
        self._all_checkpoints_visited = False
        
        
    def is_villain(self):
        return self._villain
        
    def set_opponent(self, pod):
        self._opponent = pod
        
    def increment_frame(self):
        self._frame += 1
        
    def set_location(self, x, y):
        self._speed = Vector(x, y) - Vector(self._location.x, self._location.y)
        self._location = Point(x, y)
        
    def set_checkpoint(self, x, y):
        cp = Point(x, y)
        
        if self._frame == 1:
            self._next_checkpoint = cp
        else:
            if cp != self._next_checkpoint:
                if cp in self._visited_checkpoints:
                    self._all_checkpoints_visited = True
                    if cp == self._visited_checkpoints[0]:
                        self._lap +=1
                else:
                    self._visited_checkpoints.append(self._next_checkpoint)
                
                self._next_checkpoint = cp
                
    def set_distance(self, distance):
        self._distance = distance
    
    def set_angle(self, angle):
        self._angle = angle
        
    def accelerate(self, thrust_diff):
        self._thrust += thrust_diff
        
    def get_instructions(self):
        next_x = int(self._next_checkpoint.x)
        next_y = int(self._next_checkpoint.y)
        th = self._thrust
        return f'{next_x} {next_y} {th}'
        
        
class Game:
    def __init__(self):
        self.hero = Pod("Team 42", 1)
        self.villain = Pod("Opponent", 1, True)
        
        self.hero.set_opponent(self.villain)
        self.villain.set_opponent(self.hero)
        
    def get_data(self):
        x, y, nx, ny, nd, na = [int(i) for i in input().split()]
        ox, oy = [int(i) for i in input().split()]
        
        self.hero.increment_frame()
        self.hero.set_location(x, y)
        self.hero.set_checkpoint(nx, ny)
        self.hero.set_distance(nd)
        self.hero.set_angle(na)
        self.villain.set_location(ox, oy)
        

# The game loop
game = Game()
while True:
    game.get_data()
    print(game.hero.get_instructions())
    
"""
boost_used = False

def pod_on_target(radius, distance, angle):
    return radius > distance * math.sin(math.radians(abs(angle)))
    
def opp_btw_pod_and_cp(radius, x, y, cp_x, cp_y, o_x, o_y):
    a = 1
    b = -(cp_y - y)/(cp_x - x)
    c = -(y*cp_x - cp_y*x)/(cp_x - x)
    
    d = (a*o_x + b*o_y + c)/math.sqrt(a**2+b**2)
    return d < (radius/4)
    
def opp_within_distance(distance, x, y, o_x, o_y):
    return math.sqrt((o_x-x)**2+(o_y-y)**2) < distance
    
    


# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, cp_x, cp_y, d, angle = [int(i) for i in input().split()]
    o_x, o_y = [int(i) for i in input().split()]

    # Parameters
    boost_used = False
    shield_r = 400
    cp_r = 600
    close_r = 2500
    opp_distance = 1200

    on_target = pod_on_target(cp_r, d, angle)
    opp_ahead = opp_btw_pod_and_cp(shield_r, x, y, cp_x, cp_y, o_x, o_y)
    opp_in_distance = opp_within_distance(opp_distance, x, y, o_x, o_y)
    # DEBUG INFO
    print(f'Distance: {d} [units]', file=sys.stderr, flush=True)
    print(f'Angle: {angle} [degrees]', file=sys.stderr, flush=True)
    print(f'On target: {on_target}', file=sys.stderr, flush=True)    
    print(f'Opp ahead: {opp_ahead}', file=sys.stderr, flush=True)
    print(f'Opp in distance: {opp_in_distance}', file=sys.stderr, flush=True)

    # Actually this case should never happen
    # as d is set to next CP if within cp_r
    if d < cp_r:
        th = 0
    # Approaching CP
    elif d < close_r:
        if on_target:
            # d==close_r --> 1
            # d==cp_r --> 
            distance_factor = d / close_r 
            angle_factor = 1 - abs(angle)/400
            th = min(100, int(100 * distance_factor * angle_factor))
        else:
            th = 25
    # Far away from CP
    else:
        if on_target:
            th = 'BOOST'
        else:
            if abs(angle)>90:
                th = 30
            elif abs(angle) > 50:
                th = 60
            elif abs(angle) > 20:
                th = 75
            else:
                th = 95

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print(f'{cp_x} {cp_y} {th}')
"""    