from tkinter import *

# create the window object
window = Tk()

# size the window
window.geometry('600x550')

# add title to the top bar
window.title("Please Select YES or NO")

w = Canvas(window, width=200, height=100)
w.pack()


def correct_quit(tk):
        tk.destroy()
        tk.quit()

quit = Button(window, text = "Quit", command = lambda :correct_quit(tk))
quit.pack()

mainloop()