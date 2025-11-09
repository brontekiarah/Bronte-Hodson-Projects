from tkinter import *


def main():
    master = Tk() #create the main window
    key = 0 #default dropdown selection (0 = January)
    options = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September"
    ]
    dropdown(master, key, options) #create dropdown
    mainloop()

#function to create and pack a dropdown menu.
def dropdown(master, key, options):
    variable = StringVar(master) #holds the selected value
    variable.set(options[key]) #set the default selection
    w = OptionMenu(master, variable, *options) #create dropdown menu
    w.pack() #use pack layout manager to place it

#Creates a labeled dropdown menu and returns the selected variable
def create_dropdown(master, label_text, options):
    frame = Frame(master) #create a frame to group label + dropdown
    frame.pack(pady = 5) #add space between widgets

    Label(frame, text=label_text).pack(side=LEFT)  #add label to the left
    var = StringVar(master) #variable to store dropdown value
    var.set(options[0]) #set default value
    OptionMenu(frame, var, *options).pack(side=LEFT) #add dropdown next to label

    return var #return the variable so you can use .get() later


if __name__ == "__main__":
    main()