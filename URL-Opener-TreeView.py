from tkinter import *
from tkinter.ttk import Treeview

from db import Database
import webbrowser
import schedule
import time
import threading
import subprocess
import validators
from tkinter import messagebox

# create a database to store the data
db = Database('timetable.db')

# sound effect
file = "zapsplat_fantasy_magic_ping_wand_90s_style_dreamy_003_64946.mp3"

error_window = False
screen_width = 1100
screen_height = 450


# commands
# populate the ListBox with data from db
def populate_list():
    for item in parts_list.get_children():
        parts_list.delete(item)

    for row in db.fetch():
        parts_list.insert("", 'end', values=row)


def add_item():
    global error_window
    new_day = day_text.get()
    new_hour = hour_text.get()
    new_minute = minute_text.get()
    new_url = url_text.get()

    if validators.url(new_url):
        db.insert(day_text.get(), hour_text.get(),
                  minute_text.get(), url_text.get())
        for item in parts_list.get_children():
            parts_list.delete(item)
        parts_list.insert("", "end", (day_text.get(), hour_text.get(),
                                      minute_text.get(), url_text.get()))
        clear_text()
        populate_list()

        row = db.fetchLastRow()

        generate_schedule(days.index(new_day)).at(("%02d" % int(new_hour)) + ":" + ("%02d" % int(new_minute))).do(job, new_url).tag(row[0])
    else:
        error_window = True
        messagebox.showerror("Error", "Must input a valid URL!")
        error_window = False


def select_item(event):
    try:
        global selected_item
        selected_item = parts_list.item(parts_list.selection())["values"]
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

    schedule.cancel_job(schedule.get_jobs(tag=selected_item[0])[0])

def update_item():
    new_day = day_text.get()
    new_hour = hour_text.get()
    new_minute = minute_text.get()
    new_url = url_text.get()
    db.update(selected_item[0], day_text.get(), hour_text.get(),
              minute_text.get(), url_text.get())

    for item in parts_list.get_children():
        parts_list.delete(item)

    parts_list.insert("", "end", (day_text.get(), hour_text.get(),
                                  minute_text.get(), url_text.get()))

    clear_text()
    populate_list()

    schedule.cancel_job(schedule.get_jobs(tag=selected_item[0])[0])
    generate_schedule(days.index(new_day)).at(("%02d" % int(new_hour)) + ":" + ("%02d" % int(new_minute))).do(job, new_url).tag(selected_item[0])


def class_start():
    try:
        global selected_item
        selected_item = parts_list.item(parts_list.selection())["values"]

        webbrowser.open(str(selected_item[4]), new=2)
    except IndexError:
        pass


def clear_text():
    day_text.set("Monday")
    hour_text.set(hours[0])
    minute_text.set(minutes[0])
    url_entry.delete(0, END)


def show_instructions():
    messagebox.showinfo("Instructions", "Choose day, hour, minute, and enter a valid URL address.\n"
                                        "Click 'Add' to add to your schedule.\n"
                                        "Select the item in the schedule, "
                                        "then the corresponding entries would show up.\n"
                                        "Click 'Remove' to remove from your schedule. "
                                        "Or edit any entry if you want to edit the appointment.\n"
                                        "Click 'Save Changes' to save the changes you make.\n"
                                        "Click 'Open' to open the URL manually.")


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

columns = ("apt", "day", "hour", "minute", "link")

parts_list = Treeview(app, columns=columns, show="headings")
parts_list.place(x=20, y=200)
parts_list.heading("apt", text="Appointment Index")
parts_list.heading("day", text="Day")
parts_list.heading("hour", text="Hour")
parts_list.heading("minute", text="Minute")
parts_list.heading("link", text="URL Link")
parts_list.bind('<<TreeviewSelect>>', select_item)
scrollbar = Scrollbar(app)
scrollbar.place(x=1050, y=200)
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)

# Buttons
add_btn = Button(app, text='Add', width=12, command=add_item)
add_btn.place(x=screen_width * (1 / 6), y=170)

remove_btn = Button(app, text='Remove', width=12, command=remove_item)
remove_btn.place(x=screen_width * (2 / 6), y=170)

edit_btn = Button(app, text='Save Changes', width=12, command=update_item)
edit_btn.place(x=screen_width * (3 / 6), y=170)

open_btn = Button(app, text="Open", width=12, command=class_start)
open_btn.place(x=screen_width * (4 / 6), y=170)

instructions_btn = Button(app, text="Instructions", width=12, command=show_instructions)
instructions_btn.place(x=screen_width * (5 / 6), y=170)

app.title('URL Opener')
app.geometry(str(screen_width) + "x" + str(screen_height))

populate_list()
schedule.clear()

whole_schedule = []

for item in parts_list.get_children():
    whole_schedule.append(parts_list.item(item)["values"])


# opens the url link
def job(one_link):
    webbrowser.open(str(one_link), new=2)
    if sound_text.get() == 1:
        subprocess.call(["afplay", file])
    return schedule.CancelJob


def generate_schedule(day_index):
    if day_index == 0:
        return schedule.every().monday
    elif day_index == 1:
        return schedule.every().tuesday


for n in range(len(whole_schedule)):
    weekday = days.index(whole_schedule[n][1])
    hour = int(whole_schedule[n][2])
    minute = int(whole_schedule[n][3])
    zoom = whole_schedule[n][4]
    generate_schedule(weekday).at(("%02d" % hour) + ":" + ("%02d" % minute)).do(job, zoom).tag(whole_schedule[n][0])


whole_schedule.clear()


def url_opener():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = threading.Thread(target=url_opener)
thread.daemon = True
thread.start()

app.mainloop()
