class Hexagon:

    def __init__(self, x=0, y=0, z=0, size=20, centx=0, centy=0, col='#ffffff', rot='pointy',id=0):
        self.centx = centx
        self.centy = centy
        self.size  = size
        self.x = x
        self.y = y
        self.z = z
        self.col = col
        self.rot = rot

        # need the . in 3/2 to make 3.0/2
        if (self.x == 0 and self.y == 0 and self.z == 0):
            self.centx = canvas_width / 2
            self.centy = canvas_height / 2
        else:
            if self.rot == 'flat':
                self.centx = (self.size * ((3.0 / 2) * self.x)) + (canvas_width / 2)
                self.centy = (self.size * ((math.sqrt(3) / 2) * self.x + math.sqrt(3) * self.z)) + (canvas_height / 2)
            elif self.rot == 'pointy':
                self.centx = (self.size * (math.sqrt(3) * self.x + math.sqrt(3) / 2 * self.z)) + (canvas_height / 2)
                self.centy = (self.size * ((3.0 / 2) * self.z)) + (canvas_width / 2)

    def draw(self):
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
        
        self.id=(myCanvas.create_polygon(points, outline='#000000', 
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


class HexGrid:

    def __init__(self, rad=0, rot='pointy', size=20):
        self.rad = rad
        self.rot = rot
        self.size = size
        self.grid = self.gen_grid()

    def gen_grid(self):
        grid = []
        hexagon = Hexagon(0,0,0,size=self.size,rot=self.rot)
        for x in range(-self.rad,self.rad+1):
            for y in range(-self.rad,self.rad+1):
                for z in range(-self.rad,self.rad+1):
                    if (x+y+z == 0):
                        hexagon = Hexagon(x,y,z,size=self.size,rot=self.rot)
                        grid.append(hexagon)
        return(grid)
    
    def draw_grid(self):
        for obj in self.grid:
            obj.draw()
    
    def change_orientation(self):
        if self.rot == 'pointy':
            myCanvas.delete('all')
            self.rot = 'flat'
            self.grid = self.gen_grid()
            self.draw_grid()
            print(self.rot)
            
        elif self.rot == 'flat':
            myCanvas.delete('all')
            self.rot = 'pointy'
            self.grid = self.gen_grid()
            self.draw_grid()
            print(self.rot)
            

    def draw_coord(self):
        for obj in self.grid:
            myCanvas.create_text(obj.centx, obj.centy, font="Times 6",text = "{},{},{}".format(obj.x, obj.y, obj.z),)

    def show_neighbors(self,x,y,z):
        neighbors = []
        cube_directions = [
        (+1, -1, 0), (+1, 0, -1), (0, +1, -1), 
        (-1, +1, 0), (-1, 0, +1), (0, -1, +1)]
        # for direction in cube_directions:
        #     neighbor = [x+direction[0],y+direction[1],z+direction[2]]
        #     neighbors.append(neighbor)
        for direction in cube_directions:
            neighbor = grid.ret_hex_cube(x+direction[0],y+direction[1],z+direction[2])
            neighbors.append(neighbor)
        return(neighbors)

    def rotate_grid(self,times=1):
        for i in range(times):
            for obj in self.grid:
                
                x = obj.y * (-1)
                y = obj.z * (-1)
                z = obj.x * (-1)
                
                obj.x = y
                obj.y = z
                obj.z = x
        self.draw_grid()
        self.draw_coord()

    def set_hex_col(self, x, y, z, col="#000000"):
        for obj in self.grid:
            if obj.x == x and obj.y == y and obj.z == z:
                obj.set_color()
                obj.draw()
                return
    
    def ret_hex_cube(self, x, y, z):
        for obj in self.grid:
            if obj.x == x and obj.y == y and obj.z == z:
                return obj
    
    def ret_hex_id(self, hex_id):
        for obj in self.grid:
            if obj.id == hex_id:
                return obj

    # def cube_round(self, (x, y, z)=(0, 0, 0)):
    #     rx = round(x)
    #     ry = round(y)
    #     rz = round(z)

    #     x_diff = abs(rx - x)
    #     y_diff = abs(ry - y)
    #     z_diff = abs(rz - z)

    #     if x_diff > y_diff and x_diff > z_diff:
    #         rx = -ry - rz
    #     elif y_diff > z_diff:
    #         ry = -rx - rz
    #     else:
    #         rz = -rx - ry

    #     return (rx, ry, rz)

    # def get_coord(self, coord_x, coord_y):
    #     if self.rot == 'flat':
    #         x = ((2. / 3) * (coord_x - (width / 2))) / self.rad
    #         y = ((-1. / 3) * (coord_x - (width / 2)) + sqrt(3) / 3 * (coord_y - (height / 2))) / self.rad
    #         z = -z-y

    #     elif self.rot == 'pointy':
    #         z = (sqrt(3) / 3 * (coord_x - width / 2) - 1. / 3 * (coord_y - height / 2)) / self.rad
    #         y = (2. / 3 * (coord_y - height / 2)) / self.rad
    #         x = (-z)-y

    #     return self.cube_round((x,y,z))

    # def axial_to_cube(self, q, r):
    #     z = q
    #     y = r
    #     x = -z - y
    #     return (x, y, z)


# importing tkinter module 
from tkinter import *
  
# importing the choosecolor package 
from tkinter.colorchooser import *
import math

def choose_color(): 
    global color_pick
    # variable to store hexadecimal code of color 
    color_pick = askcolor()[1] 
    print(color_pick)
    
def callback(event):
    x = event.x
    y = event.y
    item = event.widget.find_closest(x, y)[0]
    hexagon = grid.ret_hex_id(item)
    if variable.get() == 'neighbor':
        neighbor=grid.show_neighbors(hexagon.x,hexagon.y,hexagon.z) 
        for hexagon in neighbor:
            hexagon.set_color(color_pick)
    elif variable.get() == 'point':     
        event.widget.itemconfigure(item,fill=color_pick)



canvas_width  = 400
canvas_height = 400

global color_pick
color_pick = "#000000"

# init tk
root = Tk()

# create canvas
myCanvas = Canvas(root, bg="white", height=canvas_height, width=canvas_width)

# draw grid

grid = HexGrid(6,'pointy',15)
grid.draw_grid()

myCanvas.pack()

# create frame to put control buttons onto
frame = Frame(root, bg='grey', width=canvas_width, height=canvas_height/5)
frame.pack(fill='x')
rot_button = Button(frame, text="orientation", command=grid.change_orientation)
rot_button.pack(side='bottom', padx=10)
button = Button(frame, text = "Select color", 
                   command = choose_color) 
button.pack() 

global variable 
variable = StringVar(root)
variable.set("point") # default value

w = OptionMenu(root, variable, "point", "neighbor")
w.pack()

myCanvas.bind("<Button-1>", callback)


    

# add to window and show
root.mainloop()