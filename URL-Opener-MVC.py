from tkinter import *
from tkinter.ttk import Treeview

from db import Database
import webbrowser
import schedule
import time
import threading
import subprocess
import validators
from tkinter import messagebox, ttk
import tkinter as tk

file = "zapsplat_fantasy_magic_ping_wand_90s_style_dreamy_003_64946.mp3"

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hours = []
for i in range(24):
    hours.append(i)
minutes = []
for i in range(60):
    minutes.append(i)

screen_width = 1100
screen_height = 450

# opens web browser
def job(one_link):
    webbrowser.open(str(one_link), new=2)
    if file is not None:
        subprocess.call(["afplay", file])


def generate_schedule(day_index):
    if day_index == 0:
        return schedule.every().monday
    elif day_index == 1:
        return schedule.every().tuesday
    elif day_index == 2:
        return schedule.every().wednesday
    elif day_index == 3:
        return schedule.every().thursday
    elif day_index == 4:
        return schedule.every().friday
    elif day_index == 5:
        return schedule.every().saturday
    elif day_index == 6:
        return schedule.every().sunday


def cancel_job(index):
    schedule.cancel_job(schedule.get_jobs(tag=index)[0])


class Model:
    def __init__(self):
        self.db = Database('timetable.db')
        schedule.clear()
        self.whole_schedule = []
        for row in self.db.fetch():
            self.whole_schedule.append(row)

        for n in range(len(self.whole_schedule)):
            weekday = days.index(self.whole_schedule[n][1])
            hour = int(self.whole_schedule[n][2])
            minute = int(self.whole_schedule[n][3])
            link = self.whole_schedule[n][4]
            generate_schedule(weekday).at(("%02d" % hour) + ":" + ("%02d" % minute)).do(job, link).tag(
                self.whole_schedule[n][0])

        self.whole_schedule.clear()

    def add_to_db(self, day, hour, minute, url):
        self.db.insert(day, hour, minute, url)

    def remove_from_db(self, index):
        self.db.remove(index)

    def update_item_in_db(self, index, day, hour, minute, url):
        self.db.update(index, day, hour, minute, url)

    def add_new_job(self, day, hour, minute, url, index):
        if index == -1:
            last_row = self.db.fetchLastRow()
            generate_schedule(days.index(day)).at(("%02d" % int(hour)) + ":" + ("%02d" % int(minute))).do(job,
                                                                                                          url).tag(
                last_row[0])
        else:
            generate_schedule(days.index(day)).at(("%02d" % int(hour)) + ":" + ("%02d" % int(minute))).do(job,
                                                                                                          url).tag(
                index)

    def retrieve_all_rows(self):
        rows = []
        for row in self.db.fetch():
            rows.append(row)
        return rows


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.day_text = StringVar()
        self.day_label = Label(parent, text='Day', font=('bold', 14), pady=20)
        self.day_text.set('Monday')
        self.drop_days = OptionMenu(parent, self.day_text, *days)
        self.day_label.grid(row=0, column=0, sticky=W)
        self.drop_days.grid(row=0, column=1)

        self.hour_text = StringVar()
        self.hour_label = Label(parent, text='Hour', font=('bold', 14))
        self.hour_text.set(hours[0])
        self.drop_hours = OptionMenu(parent, self.hour_text, *hours)
        self.hour_label.grid(row=0, column=2, sticky=W)
        self.drop_hours.grid(row=0, column=3)

        self.minute_text = StringVar()
        self.minute_label = Label(parent, text="Minute", font=('bold', 14))
        self.minute_text.set(minutes[0])
        self.drop_minutes = OptionMenu(parent, self.minute_text, *minutes)
        self.minute_label.grid(row=1, column=0, sticky=W)
        self.drop_minutes.grid(row=1, column=1)

        self.url_text = StringVar()
        self.url_label = Label(parent, text='URL Link', font=('bold', 14))
        self.url_label.grid(row=1, column=2, sticky=W)
        self.url_entry = Entry(parent, textvariable=self.url_text)
        self.url_entry.grid(row=1, column=3)

        self.sound_text = IntVar()
        self.sound_label = Label(parent, text='Sound on?', font=('bold', 14))
        self.sound_label.grid(row=2, column=0, sticky=W)
        options = ['Yes', 'No']
        for i in options:
            self.sound_text.set(i)
        self.sound_radio_yes = Radiobutton(parent, text="Yes", variable=self.sound_text, value=1, command=self.sound_on_clicked)
        self.sound_radio_no = Radiobutton(parent, text="No", variable=self.sound_text, value=2, command=self.sound_off_clicked)
        self.sound_text.set(1)
        self.sound_radio_yes.grid(row=2, column=1, sticky=W, pady=20)
        self.sound_radio_no.grid(row=2, column=2, sticky=W, pady=20)

        columns = ("apt", "day", "hour", "minute", "link")

        self.parts_list = Treeview(parent, columns=columns, show="headings")
        self.parts_list.place(x=20, y=200)
        self.parts_list.heading("apt", text="Appointment Index")
        self.parts_list.heading("day", text="Day")
        self.parts_list.heading("hour", text="Hour")
        self.parts_list.heading("minute", text="Minute")
        self.parts_list.heading("link", text="URL Link")
        self.parts_list.bind('<<TreeviewSelect>>', self.select_item)
        self.scrollbar = Scrollbar(parent)
        self.scrollbar.place(x=1050, y=200)
        self.parts_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.parts_list.yview)

        self.add_btn = Button(parent, text='Add', width=12, command=self.add_button_clicked)
        self.add_btn.place(x=screen_width * (1 / 6), y=170)

        self.remove_btn = Button(parent, text='Remove', width=12, command=self.remove_button_clicked)
        self.remove_btn.place(x=screen_width * (2 / 6), y=170)

        self.edit_btn = Button(parent, text='Save Changes', width=12, command=self.update_button_clicked)
        self.edit_btn.place(x=screen_width * (3 / 6), y=170)

        self.open_btn = Button(parent, text="Open", width=12, command=self.open_button_clicked)
        self.open_btn.place(x=screen_width * (4 / 6), y=170)

        self.instructions_btn = Button(parent, text="Instructions", width=12, command=self.instructions_button_clicked)
        self.instructions_btn.place(x=screen_width * (5 / 6), y=170)

        self.controller = None
        self.selected_item = None

    def set_controller(self, controller):
        self.controller = controller

    def select_item(self, event):
        try:
            self.selected_item = self.parts_list.item(self.parts_list.selection())["values"]
            self.day_text.set(self.selected_item[1])
            self.hour_text.set(self.selected_item[2])
            self.minute_text.set(self.selected_item[3])
            self.url_entry.delete(0, END)
            self.url_entry.insert(END, self.selected_item[4])
        except IndexError:
            pass

    def add_button_clicked(self):
        new_day = self.day_text.get()
        new_hour = self.hour_text.get()
        new_minute = self.minute_text.get()
        new_url = self.url_text.get()

        if self.controller:
            if validators.url(new_url):
                for item in self.parts_list.get_children():
                    self.parts_list.delete(item)
                self.parts_list.insert("", "end", (new_day, new_hour, new_minute, new_url))
                self.clear_text()
                self.controller.add_item(new_day, new_hour, new_minute, new_url)
            else:
                messagebox.showerror("Error", "Must input a valid URL!")

    def remove_button_clicked(self):
        if self.controller:
            self.controller.remove_item(self.selected_item[0])
            self.clear_text()

    def update_button_clicked(self):
        new_day = self.day_text.get()
        new_hour = self.hour_text.get()
        new_minute = self.minute_text.get()
        new_url = self.url_text.get()

        if self.controller:
            for item in self.parts_list.get_children():
                self.parts_list.delete(item)
            self.parts_list.insert("", "end", (new_day, new_hour, new_minute, new_url))
            self.clear_text()
            self.controller.update_item(self.selected_item[0], new_day, new_hour, new_minute, new_url)

    def open_button_clicked(self):
        try:
            self.selected_item = self.parts_list.item(self.parts_list.selection())["values"]

            webbrowser.open(str(self.selected_item[4]), new=2)
        except IndexError:
            pass

    def instructions_button_clicked(self):
        messagebox.showinfo("Instructions", "Choose day, hour, minute, and enter a valid URL address.\n"
                                            "Click 'Add' to add to your schedule.\n"
                                            "Select the item in the schedule, "
                                            "then the corresponding entries would show up.\n"
                                            "Click 'Remove' to remove from your schedule. "
                                            "Or edit any entry if you want to edit the appointment.\n"
                                            "Click 'Save Changes' to save the changes you make.\n"
                                            "Click 'Open' to open the URL manually.")

    def sound_on_clicked(self):
        global file
        file = None

    def sound_off_clicked(self):
        global file
        file = ""

    def clear_text(self):
        self.day_text.set("Monday")
        self.hour_text.set(hours[0])
        self.minute_text.set(minutes[0])
        self.url_entry.delete(0, END)

    def populate_parts_list(self, rows):
        for item in self.parts_list.get_children():
            self.parts_list.delete(item)

        for row in rows:
            self.parts_list.insert("", "end", values=row)

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def add_item(self, day, hour, minute, url):
        self.model.add_to_db(day, hour, minute, url)
        self.view.populate_parts_list(self.model.retrieve_all_rows())
        self.model.add_new_job(day, hour, minute, url, -1)

    def remove_item(self, index):
        self.model.remove_from_db(index)
        self.view.populate_parts_list(self.model.retrieve_all_rows())
        self.model.cancel_job(index)

    def update_item(self, index, day, hour, minute, url):
        self.model.update_item_in_db(index, day, hour, minute, url)
        self.model.cancel_job(index)
        self.model.add_new_job(day, hour, minute, url, index)
        self.view.populate_parts_list(self.model.retrieve_all_rows())


class URL_Opener(tk.Tk):
    def __init__(self):
        super().__init__()
        global file

        self.title("URL Opener")
        self.geometry(str(screen_width) + "x" + str(screen_height))

        # create a model
        model = Model()

        # create a view and place it on the root window
        view = View(self)
        view.place(x=0, y=0)
        view.populate_parts_list(model.retrieve_all_rows())

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


app = URL_Opener()


def url_opener():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = threading.Thread(target=url_opener)
thread.daemon = True
thread.start()

app.mainloop()
