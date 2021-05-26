import sqlite3, datetime, sys
from tkinter import *
import tkinter.simpledialog as simpledialog

def checkTableExists(db):
    db.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='entries'")
    if db.fetchone()[0] == 1:
        return True
    else:
        return False

def createTable(db, dbcon):
    db.execute("CREATE TABLE entries (date TEXT, time TEXT, note TEXT)")

def logTime(db, note):
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")
    sqladd = "INSERT INTO entries VALUES ('" + date + "', '" + time + "', '" + note + "')"
    db.execute(sqladd)

def getAllEntries(db):
    entries = db.execute("SELECT date, time, note FROM entries").fetchall()
    return entries

def getTodaysEntries(db):
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    entries = db.execute("SELECT date, time, note FROM entries WHERE date LIKE '" + date + "'").fetchall()
    return entries

def clearEntries(db):
    db.execute("DELETE FROM entries")
    alertPopup("Entries Cleared", "All entries have been cleared.")

def alertPopup(title, message):
    base = Tk()
    base.title(title)
    width = 400
    height = 200
    screenWidth = base.winfo_screenwidth()
    screenHeight = base.winfo_screenheight()
    xPos = (screenWidth - width)/2
    yPos = (screenHeight - height)/2
    base.geometry('%dx%d+%d+%d' % (width, height, xPos, yPos))
    window = Label(base, text=message, width=80, height=10)
    window.pack()
    button = Button(base, text="OK", command=base.destroy, width=10)
    button.pack()
    mainloop()

def convertEntriesToText(entries):
    text = ""
    for listing in entries:
        date = listing[0]
        time = listing[1]
        note = listing[2]
        text += date + " - " + time + " - " + note + "\n"
    return text

def popupEntries(entries):
    alertPopup("track-time - View Entries", entries)

def runApp():
    dbconnection = sqlite3.connect("track-time.db")
    db = dbconnection.cursor()
    if len(sys.argv) > 2:
        alertPopup("track-time - Error", "Too many arguments.")
    else:
        if len(sys.argv) == 2:
            if sys.argv[1] == "listall":
                popupEntries(convertEntriesToText(getAllEntries(db)))
            elif sys.argv[1] == "listtoday":
                popupEntries(convertEntriesToText(getTodaysEntries(db)))
            elif sys.argv[1] == "add":
                entryNote = input("Enter note for time entry: ")
                logTime(db, entryNote)
            elif sys.argv[1] == "clear":
                clearEntries(db)
            else:
                alertPopup("track-time - Error", "Invalid argument.")
        else:
            popupEntries(convertEntriesToText(getTodaysEntries(db)))
    dbconnection.commit()
    dbconnection.close()

runApp()
