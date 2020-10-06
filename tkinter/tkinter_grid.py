import hex_class

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