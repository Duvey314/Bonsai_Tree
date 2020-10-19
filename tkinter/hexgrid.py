import tkinter
from hexagon import Hexagon

class HexGrid:

    def __init__(self, myCanvas: tkinter.Canvas, rad=0, rot='pointy', size=20):
        self.rad = rad
        self.rot = rot
        self.size = size
        self.myCanvas = myCanvas
        self.canvas_width = myCanvas.winfo_width()
        self.canvas_height = myCanvas.winfo_height()
        self.grid = self.gen_grid()


    def gen_grid(self):
        grid = []
        for x in range(-self.rad,self.rad+1):
            for y in range(-self.rad,self.rad+1):
                for z in range(-self.rad,self.rad+1):
                    if (x+y+z == 0):
                        hexagon = Hexagon(self.myCanvas, x,y,z,size=self.size,rot=self.rot)
                        grid.append(hexagon)
        print("foo")
        return(grid)
    
    def draw_grid(self):
        for obj in self.grid:
            obj.draw()
    
    def change_orientation(self):
        self.myCanvas.delete('all')

        if self.rot == 'pointy':
            self.rot = 'flat'
            self.grid = self.gen_grid()
            self.draw_grid()
            print(self.rot)
            
        elif self.rot == 'flat':
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
    
    def get_dist(self,a,b):
        return (abs(a.x-b.x) + abs(a.y-b.y) + abs(a.z-b.z))/2

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
