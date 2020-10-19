from hexgrid import HexGrid
from tkinter import *
# importing the choosecolor package 
from tkinter.colorchooser import *
import math

canvas_width  = 400
canvas_height = 400

global color_pick
color_pick = "#000000"
 
def choose_color(): 
    global color_pick
    # variable to store hexadecimal code of color 
    color_pick = askcolor()[1] 
    print(color_pick)
    
def left_click(event):
    x = event.x
    y = event.y
    item = event.widget.find_closest(x, y)[0]
    hexagon = grid.ret_hex_id(item)
    if variable.get() == 'neighbor':
        neighbor=grid.show_neighbors(hexagon.x,hexagon.y,hexagon.z) 
        for hexagon in neighbor:
            hexagon.set_color(color_pick)
    elif variable.get() == 'point':     
        hexagon.set_color(color_pick)
    # elif variable.get() == 'distance':
    #     hex_dist_a = hexagon
    #     hexagon.set_color(color_pick)
    #     hexagon.print_coord()
    #     print(grid.get_dist(hex_dist_a,hex_dist_b))

def right_click(event):
    x = event.x
    y = event.y
    item = event.widget.find_closest(x, y)[0]
    hexagon = grid.ret_hex_id(item)
    if variable.get() == 'neighbor':
        neighbor=grid.show_neighbors(hexagon.x,hexagon.y,hexagon.z) 
        for hexagon in neighbor:
            hexagon.set_color(color_pick)
    elif variable.get() == 'point':     
        hexagon.set_color(color_pick)
    # elif variable.get() == 'distance':
    #     hex_dist_b = hexagon
    #     hexagon.set_color(color_pick)
    #     hexagon.print_coord()
    #     print(grid.get_dist(hex_dist_a,hex_dist_b))

# init tk
root = Tk()

# create canvas
myCanvas = Canvas(root, bg="white", height=canvas_height, width=canvas_width)

# draw grid


grid = HexGrid(myCanvas,6,'pointy',15)
grid.draw_grid()


# create variables for hex distance
# global hex_dist_a
# global hex_dist_b
# hex_dist_a = Hexagon()
# hex_dist_b = Hexagon()

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

w = OptionMenu(root, variable, "point", "neighbor","distance")
w.pack()

myCanvas.bind("<Button-1>", left_click)
myCanvas.bind("<Button-3>", right_click)

    

# add to window and show
root.mainloop()