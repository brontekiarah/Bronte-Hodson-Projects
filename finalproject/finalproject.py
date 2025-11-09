#!/usr/bin/env python

"""
Davenport University
Class Info: CISP253-mon/wed-Winter_2025
Author: Bronte Hodson
Contact:  bhodson@email.davenport.edu
Date:	18/04/2025

# Program name: bhodson11_finalproject

# ...Doc String Description of program...
This program will enable users to manage a task list
application that includes features for task creating,
displaying, modifying, completing, archiving and exporting
tasks to an Excel spreadsheet. It uses SQLite3 for the
database, Tkinter for the GUI, and Openpyxl for enabling the
export of tasks to an Excel spreadsheet.

"""

##############################################################
# Import the needed modules, packages, and specific components
# ex.  import this
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import sqlite3
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from dropdown_menu import create_dropdown


##############################################################
##############################################################
# Functions & Classes
# Keep your main() function at the top of this section.

global init_db, add_task, get_tasks, mark_complete

os.chdir(os.path.dirname(os.path.abspath(__file__))) #sets current working directory
DB_FILE = os.path.join(os.getcwd(), 'finalproject.db') #creates full file path
XLSX_FILE = os.path.join(os.getcwd(), 'finalproject.xlsx') #sets up a path for saving the excel file

def main():
    init_db()  # Make sure DB exists

    root = Tk() #create the main window
    root.geometry("1024x768") #set the size of the window
    root.title("Task Manager") #set the title of the window

    #make labels
    #main title
    Label(root, text="Task List Manager", font = ("Arial", 18, "bold")).place(x = 50, y = 20) #display the title

    #task description
    Label(root, text="Task Description:").place(x=100, y=80) #label for task description
    description_entry = Entry(root, width = 50) #inout box for entering description
    description_entry.place(x = 300, y = 80) #position of the task description entry box

    #due date
    Label(root, text="Due Date (YYYY-MM-DD):").place(x = 100, y = 120) #label for due date
    due_entry = Entry(root, width = 50) #input box for due date
    due_entry.place(x = 300, y = 120) #position of the sue date entry box

    # priority dropdown
    tk.Label(root, text="Priority:").place(x = 100, y = 160) #label for priority
    priority_var = StringVar() #variable to hold selcted value
    priority_var.set("High") #default selection
    tk.OptionMenu(root, priority_var, "High", "Medium", "Low").place(x = 300, y = 150) #location of the dropdown box

    # category dropdown
    tk.Label(root, text="Category:").place(x = 100, y = 200) #label for category
    category_var = StringVar() #variable for category selection
    category_var.set("Work") #default category
    tk.OptionMenu(root, category_var, "Work", "Personal", "Shopping").place(x = 300, y = 190) #location of the dropdown box

    # task display box
    task_list = Listbox(root, width = 80, height = 15) #listbox to show tasks
    task_list.place(x = 80, y = 300) #posisition of the listbox

    show_completed_var = BooleanVar() #checkbox variable to show/hide completed tasks

    # function to load task list
    def refresh_task_list():
        task_list.delete(0, END) #clear the list box
        for task in get_tasks(show_completed_var.get()): #get filtered task list
            status = "[X] " if task[2] else "[ ] " #show checkbox if completed
            display = f"{status}{task[1]} - Due: {task[3]} - {task[5]}" #format task display
            task_list.insert(END, display) #add to listbox

    #function to add task
    def add_task_to_db():
        desc = description_entry.get() #get description input
        due = due_entry.get() #get due date input
        priority_map = {"High": 1, "Medium": 2, "Low": 3} #map priority text to numbers
        priority = priority_map[priority_var.get()] #get priority number
        category = category_var.get() #get category

        if not desc or not due:
            messagebox.showerror("Input Error", "All fields are required!") #show error if missing input
            return

        try:
            add_task(desc, due, priority, category) #save task to database
            refresh_task_list() #reload the task list
            description_entry.delete(0, END) #clear description field
            due_entry.delete(0, END) #clear due date field
        except Exception as e:
            messagebox.showerror("Error", str(e)) #show an unexpected error

    #function mark tasks as complete
    def mark_selected_complete():
        selected = task_list.curselection() #get selected task
        if not selected:
            messagebox.showinfo("No Selection", "Please select a task to mark as complete.")
            return
        task_id = get_tasks(show_completed_var.get())[selected[0]][0] #get task id
        mark_complete(task_id) #mark the task as completed
        refresh_task_list() #reload the list

    #create buttons
    Button(root, text = "Submit Task", width = 20, command = add_task_to_db).place(x = 140, y = 250) #button to submit task
    Button(root, text = "Mark Complete", width = 20, command = mark_selected_complete).place(x = 340, y = 250) #button to mark task as done
    Button(root, text = "Export to Excel", width = 20, command = export_to_excel).place(x = 540, y = 250) #button to export tasks
    Checkbutton(root, text = "Show Completed", variable = show_completed_var, command=refresh_task_list).place(x = 100, y = 600) #show completed checkbox

    refresh_task_list() #load all tasks when program starts
    root.mainloop()

#function creates the database table if it doesn't already exist.
def init_db():

    conn = sqlite3.connect(DB_FILE) #connect to the SQLite database using the path stored in DB_FILE
    c = conn.cursor() #create cursor object to execute SQL commands
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0,
        due_date TEXT,
        priority INTEGER,
        category TEXT,
        created_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
        updated_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
    )''')
    conn.commit() #save changes to the database
    conn.close() #close the connection to free resources

#function inserts a task into the database
def add_task(description, due, priority, category):

    #check if description and due date were provided; if not, stop the function
    if not description or not due:
        raise ValueError("All fields are required")

    #Connect to the database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #insert the new task with default "completed = 0" (not completed)
    c.execute('''INSERT INTO tasks (description, completed, due_date, priority, category)
                 VALUES (?, 0, ?, ?, ?)''', (description, due, priority, category))
    conn.commit()  #commit the changes
    conn.close()  #close the database connection

#function returns a list of tasks. Filters out completed if not selected
def get_tasks(show_completed=False):

    #connect to the database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #show all tasks if show_completed is True
    if show_completed:
        c.execute("SELECT * FROM tasks")
    else:
        c.execute("SELECT * FROM tasks WHERE completed = 0")
    tasks = c.fetchall() #fetch all task records from the result
    conn.close() #close the connection
    return tasks #return the list of tasks

#function marks a task as completed by updating the database
def mark_complete(task_id):

    #connect to the database
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #update the 'completed' status of the task with the matching id
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit() #save the change
    conn.close() #close the connection

#exports task data into an Excel file
def export_to_excel():
    tasks = get_tasks(show_completed=False) #get active (not completed) tasks
    archived = [t for t in get_tasks(show_completed=True) if t[2] == 1] #get completed tasks (where completed = 1)

    wb = Workbook() #create a new Excel workbook

    #use the default sheet and rename it to "Tasks"
    ws = wb.active
    ws.title = "Tasks"

    archive = wb.create_sheet("Archived") #create a second sheet named "Archived"

     #define headers for both sheets
    headers = ["#", "Date", "Note", "Details"]
    ws.append(headers)
    archive.append(headers)

    #add tasks to the "Tasks" sheet
    i = 1
    for t in tasks:
        ws.append([i, t[3], t[1], t[5]])
        i += 1

    #add archived tasks to the "Archived" sheet
    j = 1
    for t in archived:
        archive.append([j, t[3], t[1], t[5]])
        j += 1

    #style and format both sheets
    for sheet in [ws, archive]:
        for col in ['A', 'B', 'C', 'D']:
            sheet.column_dimensions[col].width = 20
        for cell in sheet[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")

    wb.save(XLSX_FILE) #save the workbook to the file path
    messagebox.showinfo("Export Complete", "Tasks exported to Excel successfully!") #show a message to confirm export success


#############################################################
# All add all remaining Functions & Classes below
# Keep Functions & Classes in separate sections.


######################################################
#This code is required for the main() function to work
# Must be the very last command in your program.

if __name__ == "__main__":
    main()

# EOF #