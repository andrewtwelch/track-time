import sqlite3, datetime, sys
from tkinter import *
import tkinter.simpledialog as simpledialog

class TkTable:
    def __init__(self,root,data):
        rows = len(data)
        columns = len(data[0])
        for x in range(rows):
            for y in range(columns):
                if y == 0:
                    self.e = Entry(root, width=10, font=('Calibri',12))
                elif y == 1:
                    self.e = Entry(root, width=11, font=('Calibri',12))
                else:
                    self.e = Entry(root, width=50, font=('Calibri',12))
                self.e.grid(row=x, column=y)
                self.e.insert(END, data[x][y])

def showHelp():
    title = "track-time - Help"
    text = "To add entry, app.py add"
    text += "\nTo view today's entries, app.py listtoday"
    text += "\nTo view all entries, app.py listall"
    text += "\nTo clear all entries, app.py clear\n"
    alertPopup(title,text,140)

def checkTableExists():
    db.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='entries'")
    if db.fetchone()[0] == 1:
        return True
    else:
        return False

def createTable():
    db.execute("CREATE TABLE entries (date TEXT, time TEXT, note TEXT)")

def logTime(note):
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%I:%M %p")
    sqladd = "INSERT INTO entries VALUES ('" + date + "', '" + time + "', '" + note + "')"
    db.execute(sqladd)

def getAllEntries():
    entries = db.execute("SELECT date, time, note FROM entries").fetchall()
    return entries

def getTodaysEntries():
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    entries = db.execute("SELECT date, time, note FROM entries WHERE date LIKE '" + date + "'").fetchall()
    return entries

def clearEntries():
    db.execute("DELETE FROM entries")
    alertPopup("Entries Cleared", "All entries have been cleared.", 60)

def alertPopup(title, message, height=100):
    base = Tk()
    base.title(title)
    width = 400
    screenWidth = base.winfo_screenwidth()
    screenHeight = base.winfo_screenheight()
    xPos = (screenWidth - width)/2
    yPos = (screenHeight - height)/2
    base.geometry('%dx%d+%d+%d' % (width, height, xPos, yPos))
    window = Label(base, text=message, width=80, font=("Calibri", 12))
    window.pack()
    button = Button(base, text="OK", command=base.destroy, width=10)
    button.pack()
    mainloop()

def addEntryPopup():
    def submitForm(event=None):
        note = note_var.get()
        logTime(note)
        base.destroy()

    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%I:%M %p")
    message = "Enter note for time entry\nDate: " + date + "\nTime: " + time
    base = Tk()
    base.title("track-time - Add Entry")
    note_var = StringVar()
    width = 400
    height = 300
    screenWidth = base.winfo_screenwidth()
    screenHeight = base.winfo_screenheight()
    xPos = (screenWidth - width)/2
    yPos = (screenHeight - height)/2
    base.geometry('%dx%d+%d+%d' % (width, height, xPos, yPos))
    window = Label(base, text=message, width=200, height=10, font=("Calibri", 12))
    window.pack()
    text = Entry(base, textvariable=note_var, width=180)
    text.pack()
    text.focus()
    button = Button(base, text="Add", command=submitForm, width=15)
    button.pack()
    base.bind('<Return>', submitForm)
    mainloop()

def popupEntries(entries):
    if len(entries) == 0:
        alertPopup("track-time - No Entries", "There are no entries for this selection.\n", 75)
    else:
        base = Tk()
        base.title("track-time - View Entries")
        screenWidth = base.winfo_screenwidth()
        screenHeight = base.winfo_screenheight()
        xPos = screenWidth/4
        yPos = screenHeight/4
        base.geometry('+%d+%d' % (xPos, yPos))
        table = TkTable(base,entries)
        mainloop()

def menuPopup():
    title = "track-time - Menu"
    message = "Welcome to track-time"
    message2 = "To add an entry, run 'app.py add'\n"
    base = Tk()
    base.title(title)
    height = 220
    width = 400
    screenWidth = base.winfo_screenwidth()
    screenHeight = base.winfo_screenheight()
    xPos = (screenWidth - width)/2
    yPos = (screenHeight - height)/2
    base.geometry('%dx%d+%d+%d' % (width, height, xPos, yPos))
    window = Label(base, text=message, width=80, font=("Calibri", 12))
    window.pack()
    window2 = Label(base, text=message2, width=80, font=("Calibri", 12))
    window2.pack()
    button1 = Button(base, text="List All Entries", command=listAll, width=30, font=("Calibri", 12))
    button1.pack()
    button2 = Button(base, text="List Today's Entries", command=listToday, width=30, font=("Calibri", 12))
    button2.pack()
    button3 = Button(base, text="Clear All Entries", command=clearEntries, width=30, font=("Calibri", 12))
    button3.pack()
    button4 = Button(base, text="Exit", command=base.destroy, width=30, font=("Calibri", 12))
    button4.pack()
    mainloop()

def listAll():
    popupEntries(getAllEntries())

def listToday():
    popupEntries(getTodaysEntries())

def runApp():
    dbconnection = sqlite3.connect("track-time.db")
    global db
    db = dbconnection.cursor()
    if checkTableExists() == False:
        createTable()
    if len(sys.argv) > 2:
        alertPopup("track-time - Error", "Too many arguments.\n")
    else:
        if len(sys.argv) == 2:
            if sys.argv[1] == "listall":
                #popupEntries(getAllEntries(db))
                listAll(db)
            elif sys.argv[1] == "listtoday" or sys.argv[1] == "list":
                #popupEntries(getTodaysEntries(db))
                listToday()
            elif sys.argv[1] == "add":
                addEntryPopup()
            elif sys.argv[1] == "clear":
                clearEntries(db)
            elif sys.argv[1] == "help":
                showHelp()
            else:
                alertPopup("track-time - Error", "Invalid argument.\n")
        else:
            #showHelp()
            menuPopup()
    dbconnection.commit()
    dbconnection.close()

runApp()
