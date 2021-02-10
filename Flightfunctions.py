import math
import random as rnd
import Flightvisual as fv

reso = (1280,720)
middle = (640,360)

# spawn plane function
def PLANE():
    # 0:type - 1:rectangle 2:centerloc 3:hitbox 4:velocity vector 5:velocity multiplier 6:angle 7:lines 8:scale 9:collideable 10: points
    x = reso[0]
    y = reso[1]
    side = rnd.randint(1, 4)
    offset = 50 #spawns the plane outside of the visable screen!
    if side == 1: location = [rnd.randint(0, x), -offset]
    if side == 2: location = [x + offset, rnd.randint(0, y)]
    if side == 3: location = [rnd.randint(0, x), y + offset]
    if side == 4: location = [-offset, rnd.randint(0, y)]
    centerdistance = math.sqrt((location[0] - middle[0]) ** 2 + (location[1] - middle[1]) ** 2)
    velocity = (round((middle[0] - location[0]) / centerdistance, 2), round((middle[1] - location[1]) / centerdistance, 2))
    angle = math.degrees(math.atan2(velocity[0], velocity[1]))
    # planetype:(n) with their charecteristics: rectangle,hitbox,velocity and points
    ptype = rnd.randint(1,100)
    if ptype <= 70: #standard plane
        rect = fv.p1.get_rect()
        n,box,velmp,points =1, 21,50,100
    if ptype > 70 and ptype <= 90: #fast plane
        rect = fv.p2.get_rect()
        n,box,velmp,points = 2,16,90,150
    if ptype > 90: #big plane A380
        rect = fv.p3.get_rect()
        n,box,velmp,points = 3,30,30,200
    new = [n,rect,location,box,velocity,velmp,angle,[],1,True,points]
    new[1].center = location
    return new

# spawn cloud function
def CLOUD():
    #0:rectangle 1:centerloc 2:velocity vector 3:angle
    side = rnd.randint(1, 4)
    offset = 400
    if side == 1:   location = [rnd.randint(0, reso[0]), -offset]
    if side == 2:   location = [reso[0] + offset, rnd.randint(0, reso[1])]
    if side == 3:   location = [rnd.randint(0, reso[0]), reso[1] + offset]
    if side == 4:  location = [-offset, rnd.randint(0, reso[1])]
    centerdistance = math.sqrt((location[0] - middle[0]) ** 2 + (location[1] - middle[1]) ** 2)
    velocity = (round((middle[0] - location[0]) / centerdistance, 2), round((middle[1] - location[1]) / centerdistance, 2)) #travels over the middle
    angle    = rnd.randint(0,360) #random orientation
    rect     = fv.cloud.get_rect()
    new      = [rect,location,velocity,angle]
    new[0].center = location
    return new

#approach function: based on location and heading angle
def APP(l,a):
    land = False
    margin = 15 #more or less the strictness in approaching the runway
    nl = (747,253) #north gate
    sl = (534,466) #south gate
    na = -45 # heading angle for north
    sa = 135 # heading angle for south
    d1 = math.sqrt((l[0]-nl[0])**2 + (l[1]-nl[1])**2)
    d2 = math.sqrt((l[0]-sl[0])**2 + (l[1]-sl[1])**2)
    if d1 < margin and na-margin <= a <= na+margin :
        land = True
    if d2 < margin and sa-margin <= a <= sa+margin:
        land = True
    return land

# PointsCLose function: compare two coordinate tuples and returns boolean state if they are in within a given range
def PCL(a, b, r):
    c = abs(a[0] - b[0])
    d = abs(a[1] - b[1])
    e = math.sqrt(c ** 2 + d ** 2)
    if e < r:
        f = True
    else:
        f = False
    return f

# DiReCtion function: determines the velocity components and heading angle between two coordinate tuples.
def DRC(a, b):
    c = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    if c<0.5:
        velocity,angle = 0,0
    else:
        velocity = ((b[0] - a[0]) / c, (b[1] - a[1]) / c)
        angle = math.degrees(math.atan2(velocity[0], velocity[1]))
    return velocity, angle



