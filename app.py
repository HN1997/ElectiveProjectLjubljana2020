from tkinter import *
from PIL import ImageTk, Image
import window2

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



import os 
import wget

# Main
window = Tk()
window.title("Humap")
window.configure(background="black", height=700, width=700)

def click():
    fiName = firstLastName.get()
    print("[+] Target : " + fiName)

    
    window2.NewWindow(fiName, master=window)
    
    print("[+] Searched done")
    

#Photos
photo1 = PhotoImage(file="nmap.png")
Label(window, image=photo1, bg="black").grid(row=0, column=0, sticky=W)

# Labels
Label(window, text="Enter first and last name: ", bg="black", fg="white",
      font="none 12 bold").grid(row=1, column=0, sticky=N)

# Text entry box
firstLastName = Entry(window, width=20, bg="white")
firstLastName.grid(row=2, column=0, sticky=N)

# Add search button
Button(window, text="Search", width=6, command=click).grid(
    row=3, column=0, sticky=N, pady=10)


# Run the main loop
window.mainloop()
