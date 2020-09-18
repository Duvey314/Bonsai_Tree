import math

TWO_PI = math.pi * 2
width = 500
height = 500
radius = 40.0

size(500, 500)


class Hexagon:

    def __init__(self, centx=0, centy=0, rad=1, x=0, y=0, z=0, col='#34eb52',rot='pointy'):
        self.centx = centx
        self.centy = centy
        self.rad = rad
        self.x = x
        self.y = y
        self.z = z
        self.col = col
        self.rot = rot

    def draw(self):
        fill(self.col)
        if (self.rot == 'flat'):
            beginShape()
            for i in range(6):
                angle = (i * TWO_PI) / 6
                vertex(self.centx + self.rad * cos(angle),
                    self.centy + self.rad * sin(angle))
            endShape(CLOSE)
        elif (self.rot == 'pointy'):
            beginShape()
            for i in range(6):
                angle = ((i-0.5) * TWO_PI)/6
                vertex(self.centx + self.rad * cos(angle),
                    self.centy + self.rad * sin(angle))
            endShape(CLOSE)
        else:
            return 'error'
    
    def coord(self):
        return (self.x,self.y,self.z)
    
    def coord_axial(self):
        q = self.x
        r = self.z
        return (q,r)
    
    def pix_coord(self):
        #need the . in 3/2 to make 3.0/2
        if self.rot == 'flat':
            self.centx = (self.rad * ((3.0/2) * self.y))+(width/2)
            self.centy = (self.rad * ((sqrt(3)/2) * self.y + sqrt(3) * self.z)) + (height/2)
        elif self.rot == 'pointy':
            self.centx = (self.rad * (sqrt(3) * self.y + sqrt(3)/2 * self.z)) + (height/2)
            self.centy = (self.rad * ((3.0/2) * self.z))+(width/2)
            
        return (self.centx,self.centy)
    
    def rot(self):
        return (self.rot)

hex1 = Hexagon(250.0, 250.0, 20.0, 0,0,0, col='#3455e5', rot='pointy')

hex1.draw()
#print(hex1.rot())

def draw_ring(radius=1, s = 20, rot='flat'):
    ring_list = []
    print "%d/%d: (%d,%d,%d) " % (0,0,0,0,0)
    print # blank line between rings
    
    # enumerate coords in rings 1..n-1; this doesn't work for the origin
    for ring in range(1,radius+1):
        # start in the upper right corner ...
        (x,y,z) = (0,-ring,ring)
        # ... moving clockwise (south-east, or +x,-z)
        move = [1,0,-1]         
    
        # each ring has six more coordinates than the last
        for i in range(6*ring):
            centx=0
            centy=0
            hexagon = Hexagon(centx,centy,s,x,y,z,rot=rot)
            print(hexagon.pix_coord())
            # print first to get the starting hex for this ring
            print "%d/%d: (%d,%d,%d) " % (ring,i,x,y,z)
            ring_list.append(hexagon)
            # then move to the next hex
            (x,y,z) = map(sum, zip((x,y,z), move))
    
            # when a coordinate has a zero in it, we're in a corner of
            # the ring, so we need to turn right
            if 0 in (x,y,z):
                # left shift the zero through the move vector for a
                # right turn
                i = move.index(0)
                (move[i-1],move[i]) = (move[i],move[i-1])
    
        print # blank line between rings
        
    return (ring_list)

ring_list = draw_ring(radius=2, s=30, rot='pointy')    
for obj in ring_list:
    obj.draw()
