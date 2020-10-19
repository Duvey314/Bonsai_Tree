#TO DO
# separate hex object logic from hex drawing

import math
import tkinter
class Hexagon:
    '''
    This is the hexagon class. Stores the values of each hexagon
    '''
    def __init__(self, myCanvas: tkinter.Canvas, x: int = 0, y=0, z=0, size=20, centx=0, centy=0, col='#ffffff', rot='pointy',id=0):
        self.centx = centx
        self.centy = centy
        self.size  = size
        self.x = x
        self.y = y
        self.z = z
        self.col = col
        self.rot = rot
        self.myCanvas = myCanvas
        self.canvas_height = myCanvas.winfo_height()
        print(myCanvas.winfo_height())
        self.canvas_width = myCanvas.winfo_width()

        # need the . in 3/2 to make 3.0/2
        if (self.x == 0 and self.y == 0 and self.z == 0):
            self.centx = self.canvas_width / 2
            self.centy = self.canvas_height / 2
            print("one")
        else:
            print("two")
            if self.rot == 'flat':
                self.centx = (self.size * ((3.0 / 2) * self.x)) + (self.canvas_width / 2)
                self.centy = (self.size * ((math.sqrt(3) / 2) * self.x + math.sqrt(3) * self.z)) + (self.canvas_height / 2)
            elif self.rot == 'pointy':
                self.centx = (self.size * (math.sqrt(3) * self.x + math.sqrt(3) / 2 * self.z)) + (self.canvas_height / 2)
                self.centy = (self.size * ((3.0 / 2) * self.z)) + (self.canvas_width / 2)

    def draw(self):
        '''
        This function draws the hexagon on a tkinter canvas.
        '''
        points = []
        if (self.rot == 'flat'):
            for i in range(6):
                angle = (i * 2 * math.pi) / 6
                points.extend((self.centx + self.size * math.cos(angle),
                       self.centy + self.size * math.sin(angle)))
        elif (self.rot == 'pointy'):
            for i in range(6):
                angle = ((i - 0.5) * 2 * math.pi) / 6
                points.extend((self.centx + self.size * math.cos(angle),
                       self.centy + self.size * math.sin(angle)))
        else:
            return 'error'
        
        self.id=(self.myCanvas.create_polygon(points, outline='#000000', 
            fill=self.col, width=1))

    def coord(self):
        return (self.x, self.y, self.z)

    def set_color(self, col="#000000"):
        self.col = col
        self.draw()

    def coord_axial(self):
        q = self.x
        r = self.z
        return (q, r)

    def pix_coord(self):
        return (self.centx, self.centy)
    
    # def print_coord(self):
    #     print(f"{self.x},{self.y},{self.z}")