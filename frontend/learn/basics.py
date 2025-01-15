from tkinter import *
from ttkbootstrap.constants import *
import ttkbootstrap as tb




#root = Tk() # This is normally in tkinter
root = tb.Window(themename="superhero") #This is the ttkbootstrap wanted us to use

root.title("Warehouse Program")
root.geometry('500x350')

counter = 0
def changer():
    global counter
    counter += 1
    if counter % 2 == 0:
        my_label.config(text="Hello World!")
    else:
        my_label.config(text="Goodbye World!")

my_label = tb.Label(text="Hello Guys!", font=("Halvetica", 28), bootstyle=DEFAULT)
my_label.pack(pady=50)


my_button = tb.Button(text="Click Me!", bootstyle="primary, outline", command=changer)
my_button.pack(pady=10)

root.mainloop()