# URL Opener

This Desktop GUI APP built with Python using the Tkinter library opens URL links scheduled by the user. 

## Table of Contents
- [Inspiration](#insipiration)
- [Interface](#interface)
- [Instructions](#instructions)
- [Notice](#notice)
- [Changes](#changes)
- [2021 Version](#2021-version)

## Inspiration
In the beginning of 2021, I was taking online classes because of the COVID-19 pandemic. Between class breaks, I would sit away from my laptop to relax but meanwhile found it annoying to check the time constantly to make sure I would not be late for class. Therefore, I was thinking about making an app to open class links aund me in case I'm a little far from my laptop. 

## Interface
<img width="1100" alt="image" src="https://user-images.githubusercontent.com/71456398/180375246-b6a5f707-76e7-4746-be14-857ea21b5224.png">

## Instructions
  1. Enter all inputs. Select a day, hour, minute, and enter a valid URL address. If no valid link is entered, an error window will pop up. 
  2. After entering, <code>Add</code> to schedule. All appointments can be seen in the table at the bottom.  
  3. To edit, select the row in the table and the corresponding entries will appear in the entry boxes again. After editing, <code>Save Changes</code> to save all the changes you made. 
  4. To delete an appointment, select the row in the table and <code>Delete</code>. 
  5. To open the web browser manually, select the row and <code>Open</code>. 
  6. To turn on or off bell, click the radio button <code>yes</code> or <code>no</code>. 

## Notice
  1. The web browsers must be a URL address. for example, www.google.com won't work but https://google.com will work. 
  2. The time (hour & minute) must be consistent with the time zone of your computer.  
  
## Changes
Changes I made since my first version in 2021:
  1. Made the schedule sync with the database so there's no need to restart the program if the database is changed.
  2. Made the app throw an error if any entry is missing. 
  3. Changed "Weekday" to "Day" to add Saturday and Sunday as options. 
  4. Changed text entry boxes to dropdown menu so that the program doesn't have to check user inputs, and it's more user-friendly. 
  5. Made bell a choice for the user in case that the user doesn't want any sound. 
  6. Replaced <code>ListBox</code> with <code>Treeview</code> to make it more user-friendly by showing the user what each column represents. 
  7. Added a <code>Instructions</code> button for the user to understand how this app works. 
  8. Used MVC model for easier and faster future modification. 
  
 ## 2021 Version
  ![1](https://user-images.githubusercontent.com/71456398/180378832-561ac578-6147-4102-a086-63f70eae07a7.jpeg)
 Drawbacks:
  1. Weekday input is from 1 to 5, which is not user-friendly at all. 
  2. It doesn't throw an error if any entry is missing. 
  3. The user has to restart the program if they add, delete, or change anything in order to update the schedule.  
  4. The schedule table is hard to read without column headers. 
 
