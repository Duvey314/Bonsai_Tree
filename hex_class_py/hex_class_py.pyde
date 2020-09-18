

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
        
        #need the . in 3/2 to make 3.0/2
        if (self.x == 0 and self.y == 0 and self.z == 0):
            self.centx = width/2
            self.centy = height/2
        else:
            if self.rot == 'flat':
                self.centx = (self.rad * ((3.0/2) * self.y))+(width/2)
                self.centy = (self.rad * ((sqrt(3)/2) * self.y + sqrt(3) * self.z)) + (height/2)
            elif self.rot == 'pointy':
                self.centx = (self.rad * (sqrt(3) * self.y + sqrt(3)/2 * self.z)) + (height/2)
                self.centy = (self.rad * ((3.0/2) * self.z))+(width/2)

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
    
    def set_color(self, col="#000000"):
        self.col = col
    
    def coord_axial(self):
        q = self.x
        r = self.z
        return (q,r)
    
    def pix_coord(self):
        return (self.centx,self.centy)
    
    def rot(self):
        return (self.rot)
    

class HexGrid:
    
    def __init__(self, rad = 0, rot = 'pointy', s = 10):
        self.rad = rad
        self.rot = rot
        self.s = s
        self.grid = self.gen_grid()
    
    def gen_grid(self):
        grid = []
        hexagon = Hexagon(rad=self.s,x=0,y=0,z=0,rot=self.rot)
        grid.append(hexagon)
        print "%d/%d: (%d,%d,%d) " % (0,0,0,0,0)
        print # blank line between rings
        
        # enumerate coords in rings 1..n-1; this doesn't work for the origin
        for ring in range(1,self.rad+1):
            # start in the upper right corner ...
            (x,y,z) = (0,-ring,ring)
            # ... moving clockwise (south-east, or +x,-z)
            move = [1,0,-1]         
        
            # each ring has six more coordinates than the last
            for i in range(6*ring):
                hexagon = Hexagon(rad=self.s,x=x,y=y,z=z,rot=self.rot)
                hexagon.pix_coord()
                print(hexagon.pix_coord())
                # print first to get the starting hex for this ring
                print "%d/%d: (%d,%d,%d) " % (ring,i,x,y,z)
                grid.append(hexagon)
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
            
        return (grid)
    
    def draw_grid(self):
        for obj in self.grid:
            obj.draw()
    
    def set_hex_col(self,(x,y,z)=(0,0,0),col="#000000"):
        for obj in self.grid:
            if obj.x == x and obj.y == y and obj.z == z:
                obj.set_color()
                obj.draw()
                return
        

def setup():
    size(800,800)
    grid1 = HexGrid(rad=6, s=20, rot='flat')
    grid1.draw_grid()

def draw():
    pass
    
