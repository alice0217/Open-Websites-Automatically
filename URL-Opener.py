from tkinter import *
from db import Database
from datetime import datetime
import webbrowser
import schedule
import time
import threading
import subprocess

db = Database('timetable.db')

file = "zapsplat_fantasy_magic_ping_wand_90s_style_dreamy_003_64946.mp3"

def populate_list():
    parts_list.delete(0, END)
    for row in db.fetch():
        parts_list.insert(END, row)


def add_item():
    db.insert(day_text.get(), hour_text.get(),
              minute_text.get(), zoom_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (day_text.get(), hour_text.get(),
                            minute_text.get(), zoom_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)

        day_entry.delete(0, END)
        day_entry.insert(END, selected_item[1])
        hour_entry.delete(0, END)
        hour_entry.insert(END, selected_item[2])
        minute_entry.delete(0, END)
        minute_entry.insert(END, selected_item[3])
        zoom_entry.delete(0, END)
        zoom_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], day_text.get(), hour_text.get(),
              minute_text.get(), zoom_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (day_text.get(), hour_text.get(),
                            minute_text.get(), zoom_text.get()))
    clear_text()
    populate_list()

def class_start():
    try:
        global selected_item2
        index1 = parts_list.curselection()[0]
        selected_item2 = parts_list.get(index1)

        webbrowser.open(str(selected_item2[4]), new=2)
    except IndexError:
        pass

def clear_text():
    day_entry.delete(0, END)
    hour_entry.delete(0, END)
    minute_entry.delete(0, END)
    zoom_entry.delete(0, END)


# Create window object
app = Tk()

day_text = StringVar()
day_label = Label(app, text='Weekday (Mon=1, Tue=2, etc)', font=('bold', 14), pady=20)
day_label.grid(row=0, column=0, sticky=W)
day_entry = Entry(app, textvariable=day_text)
day_entry.grid(row=0, column=1)

hour_text = StringVar()
hour_label = Label(app, text='Hour (24h form)', font=('bold', 14))
hour_label.grid(row=0, column=2, sticky=W)
hour_entry = Entry(app, textvariable=hour_text)
hour_entry.grid(row=0, column=3)

minute_text = StringVar()
minute_label = Label(app, text="Minute (05, 50, etc)", font=('bold', 14))
minute_label.grid(row=1, column=0, sticky=W)
minute_entry = Entry(app, textvariable=minute_text)
minute_entry.grid(row=1, column=1)

zoom_text = StringVar()
zoom_label = Label(app, text='Link', font=('bold', 14))
zoom_label.grid(row=1, column=2, sticky=W)
zoom_entry = Entry(app, textvariable=zoom_text)
zoom_entry.grid(row=1, column=3)

parts_list = Listbox(app, height=8, width=50, border=0)
parts_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# Set scroll to listbox
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)
# Bind select
parts_list.bind('<<ListboxSelect>>', select_item)

# Buttons
add_btn = Button(app, text='Add', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

edit_btn = Button(app, text='Save Changes', width=12, command=update_item)
edit_btn.grid(row=2, column=2)

class_btn = Button(app, text="Start", width=12, command=class_start)
class_btn.grid(row=2, column=3)

app.title('Web browser automatic open tool(Restart once any info is added/changed.)')
app.geometry('730x350')

populate_list()

today = datetime.now().weekday()
class_list = []

for i in range(parts_list.size()):
    example = parts_list.get(i)
    if str(today+1) == example[1]:
        class_list.append(example)


def job(one_link):
    webbrowser.open(str(one_link), new=2)
    subprocess.call(["afplay", file])


for n in range(len(class_list)):
    weekday = class_list[n][1]
    hour = class_list[n][2]
    minute = class_list[n][3]
    zoom = class_list[n][4]
    if int(weekday) == 1:
        schedule.every().monday.at(str(hour) + ":" + str(minute)).do(job, zoom)
    elif int(weekday) == 2:
        schedule.every().tuesday.at(str(hour) + ":" + str(minute)).do(job, zoom)
    elif int(weekday) == 3:
        schedule.every().wednesday.at(str(hour) + ":" + str(minute)).do(job, zoom)
    elif int(weekday) == 4:
        schedule.every().thursday.at(str(hour) + ":" + str(minute)).do(job, zoom)
    elif int(weekday) == 5:
        schedule.every().friday.at(str(hour) + ":" + str(minute)).do(job, zoom)

class_list.clear()

def zoom():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = threading.Thread(target=zoom)
thread.daemon = True
thread.start()

app.mainloop()
