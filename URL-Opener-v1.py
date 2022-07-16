from tkinter import *
from db import Database
from datetime import datetime
import webbrowser
import schedule
import time
import threading
import subprocess

# create a database to store the data
db = Database('timetable.db')

# sound effect
file = "zapsplat_fantasy_magic_ping_wand_90s_style_dreamy_003_64946.mp3"

# populate the list table with data from db
def populate_list():
    parts_list.delete(0, END)
    for row in db.fetch():
        parts_list.insert(END, row)


def add_item():
    new_day = day_text.get()
    new_hour = hour_text.get()
    new_minute = minute_text.get()
    new_url = url_text.get()

    db.insert(day_text.get(), hour_text.get(),
              minute_text.get(), url_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (day_text.get(), hour_text.get(),
                            minute_text.get(), url_text.get()))
    clear_text()
    populate_list()
    day[days.index(new_day)].at(("%02d" % int(new_hour)) + ":" + ("%02d" % int(new_minute))).do(job, new_url)


def select_item(event):
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)
        day_text.set(selected_item[1])
        hour_text.set(selected_item[2])
        minute_text.set(selected_item[3])
        url_entry.delete(0, END)
        url_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()

    schedule.clear()
    # log_schedule()
    for n in range(len(today_schedule)):
        if selected_item[0] != today_schedule[n][0]:
            weekday = days.index(today_schedule[n][1])
            hour = int(today_schedule[n][2])
            minute = int(today_schedule[n][3])
            zoom = today_schedule[n][4]
            day[weekday].at(("%02d" % hour) + ":" + ("%02d" % minute)).do(job, zoom)

def update_item():
    new_day = day_text.get()
    new_hour = hour_text.get()
    new_minute = minute_text.get()
    new_url = url_text.get()
    db.update(selected_item[0], day_text.get(), hour_text.get(),
              minute_text.get(), url_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (day_text.get(), hour_text.get(),
                            minute_text.get(), url_text.get()))
    clear_text()
    populate_list()

    schedule.clear()
    day[days.index(new_day)].at(("%02d" % int(new_hour)) + ":" + ("%02d" % int(new_minute))).do(job, new_url)

    for n in range(len(today_schedule)):
        if selected_item[0] != today_schedule[n][0]:
            weekday = days.index(today_schedule[n][1])
            hour = int(today_schedule[n][2])
            minute = int(today_schedule[n][3])
            zoom = today_schedule[n][4]
            day[weekday].at(("%02d" % hour) + ":" + ("%02d" % minute)).do(job, zoom)

def class_start():
    try:
        global selected_item2
        index1 = parts_list.curselection()[0]
        selected_item2 = parts_list.get(index1)

        webbrowser.open(str(selected_item2[4]), new=2)
    except IndexError:
        pass


def clear_text():
    day_text.set("Monday")
    hour_text.set(hours[0])
    minute_text.set(minutes[0])
    url_entry.delete(0, END)


# Create window object
app = Tk()

# day input
day_text = StringVar()
day_label = Label(app, text='Day', font=('bold', 14), pady=20)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# set initial menu text
day_text.set('Monday')
drop_days = OptionMenu(app, day_text, *days)
day_label.grid(row=0, column=0, sticky=W)
drop_days.grid(row=0, column=1)

# hour input
hour_text = StringVar()
hour_label = Label(app, text='Hour', font=('bold', 14))
hours = []
for i in range(24):
    hours.append(i)
hour_text.set(hours[0])
drop_hours = OptionMenu(app, hour_text, *hours)
hour_label.grid(row=0, column=2, sticky=W)
drop_hours.grid(row=0, column=3)

# minute input
minute_text = StringVar()
minute_label = Label(app, text="Minute", font=('bold', 14))
minutes = []
for i in range(60):
    minutes.append(i)
minute_text.set(minutes[0])
drop_minutes = OptionMenu(app, minute_text, *minutes)
minute_label.grid(row=1, column=0, sticky=W)
drop_minutes.grid(row=1, column=1)

# url link input
url_text = StringVar()
url_label = Label(app, text='URL Link', font=('bold', 14))
url_label.grid(row=1, column=2, sticky=W)
url_entry = Entry(app, textvariable=url_text)
url_entry.grid(row=1, column=3)

# sound button
sound_text = IntVar()
sound_label = Label(app, text='Sound on?', font=('bold', 14))
sound_label.grid(row=2, column=0, sticky=W)
options = ['Yes', 'No']
for i in options:
    sound_text.set(i)
sound_radio_yes = Radiobutton(app, text="Yes", variable=sound_text, value=1)
sound_radio_no = Radiobutton(app, text="No", variable=sound_text, value=2)
sound_text.set(1)
sound_radio_yes.grid(row=2, column=1, sticky=W, pady=20)
sound_radio_no.grid(row=2, column=2, sticky=W, pady=20)

parts_list = Listbox(app, height=8, width=50, border=0)
parts_list.grid(row=4, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=4, column=3)
# Set scroll to listbox
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)
# Bind select
parts_list.bind('<<ListboxSelect>>', select_item)

# Buttons
add_btn = Button(app, text='Add', width=12, command=add_item)
add_btn.grid(row=3, column=0, pady=20)

remove_btn = Button(app, text='Remove', width=12, command=remove_item)
remove_btn.grid(row=3, column=1)

edit_btn = Button(app, text='Save Changes', width=12, command=update_item)
edit_btn.grid(row=3, column=2)

class_btn = Button(app, text="Open", width=12, command=class_start)
class_btn.grid(row=3, column=3)

app.title('URL Opener')
app.geometry('730x350')

populate_list()

# weekday() returns the day as an integer
today_int = datetime.now().weekday()
today_schedule = []

for i in range(parts_list.size()):
    item = parts_list.get(i)
    # item[1] is the day in String
    if today_int == days.index(item[1]):
        today_schedule.append(item)

# opens the url link
def job(one_link):
    webbrowser.open(str(one_link), new=2)
    # print(sound_text.get())
    if sound_text.get() == 1:
        subprocess.call(["afplay", file])


day = [schedule.every().monday,
       schedule.every().tuesday,
       schedule.every().wednesday,
       schedule.every().thursday,
       schedule.every().friday,
       schedule.every().saturday,
       schedule.every().sunday]

# plan what to open today
for n in range(len(today_schedule)):
    weekday = days.index(today_schedule[n][1])
    hour = int(today_schedule[n][2])
    minute = int(today_schedule[n][3])
    zoom = today_schedule[n][4]
    day[weekday].at(("%02d" % hour) + ":" + ("%02d" % minute)).do(job, zoom)

today_schedule.clear()

def url_opener():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = threading.Thread(target=url_opener)
thread.daemon = True
thread.start()

app.mainloop()
