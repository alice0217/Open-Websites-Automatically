# URL Opener

This Desktop GUI APP built with Python & Tkinter opens URL links automatically with a sound effect like class bell and has a database that stores all the essential information so that a user doesn't have to input the same information every time he/she opens the app. 

[Link to Source Code](https://github.com/bradtraversy/part_manager)

[Link to Brad's Youtube Channel](https://www.youtube.com/user/TechGuyWeb)

## Table of Contents
- [Inspiration](#insipiration)
- [Interface](#interface)
- [How to Use it](#how-to-use-it)
- [Reminders](#reminders)
- [TODO](#todo)

## Inspiration:
At the beginning of 2021, I was taking online classes because of COVID-19. Between class breaks, I would sit away from my computer to relax but meanwhile found it annoying to check the time constantly to make sure I would not be late for class. Therefore, I was thinking about making a desktop app to open class zoom links automatically for me. In addition, add a sound effect to remind me in case I'm a little far from my computer. This is my inspiration! :star2:

## Interface:
  ![WechatIMG2056](https://user-images.githubusercontent.com/71456398/114523986-671e1c80-9c77-11eb-8f3e-5e763d129563.jpeg)

## How to Use it:
  1. Enter all essential information. 
     - Weekday: Enter an integer from 1 to 5 to represent Monday to Friday 
     - Hour: in 24h form
     - Minute in 2 digits such as, 05 or 50. 
     - Link: a URL link.
  2. After four entries, click <code>Add</code> to save information in the table below. 
  3. If you want to edit anything, click that specific row in the table and the corresponding entries will appear in the entry boxes again. After editing, click <code>Save Changes</code> to save all the changes you made. 
  4. If you want to delete anything, choose that specific row row in the table and click <code>Remove</code>. 
  5. If you want to open the web browser manually, click that specific row and click <code>Start</code>. 

## Reminders:
  1. The web browsers must all start with https://. for example, www.google.com won't work but https://google.com will work. 
  2. Once any information is edited, restart the APP so that all changed information can be updated in the database. Otherwise, for example, if you set a link to be open at 12:13 and you didn't restart the program, the web browser won't pop up unless you restart the program before 12:13. 
  3. The time (hour & minute) must be consistent with the time zone of your computer.  

## TODO:
- Require the user to fill in all entries. Flash a message if any input is missing.
- Change "Weekday" (Monday to Friday) to "Day" (Monday to Sunday). 
- Change entries boxes to something like "radio" input type in HTML to let the user choose from a limited number of choices to avoid wrong input. 
- Make the app looks nicer.
