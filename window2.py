# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import * 
from tkinter import ttk
from PIL import ImageTk, Image

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from instaMap import instaSearch
from facebookMap import facebookSearch
from linkedinMap import linkedinSearch

import os 
import wget
 
 
class NewWindow(Toplevel):
    targetName = ""

    def __init__(self, targetName, master = None):
        global imgProf
        global globImgInsta
        global globImgFb

        style = ttk.Style()
        style.configure("BW.TLabel", background="black", foreground="white")

        super().__init__(master = master)
        self.targetName = targetName
        self.title(targetName)
        self.geometry("1000x1000")
        self.configure(bg='black')
            
        #Create a main frame
        main_frame = Frame(self, bg="black")
        main_frame.pack(fill=BOTH, expand=1)

        #Create a canvas
        my_canvas = Canvas(main_frame, bg="black")
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        #Add a scrollbar to the canvas
        my_scrollbar= ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        #Configure the canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

        #Create another frame inside the canvas
        second_frame = Frame(my_canvas, bg="black")

        #Add that new frame to a window in the canvas
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")
        
        
        label = ttk.Label(second_frame, text =targetName, style="BW.TLabel")
        label.grid(sticky=W, row=0, padx=525)

        
        instaSearch(targetName)
        facebookSearch(targetName)
        job, location, workinPlace, info, experienceTab, educationTab = linkedinSearch(targetName)

        imgProf = ImageTk.PhotoImage(Image.open("./target/target0.jpg"))  # PIL solution
        Label(second_frame, image=imgProf).grid(sticky=W, row = 1, padx=500)

        
        #### Linkedin results ####
        label = ttk.Label(second_frame, text ="Linkedin search found : ", style="BW.TLabel")
        label.grid(sticky=W, row = 2)
        

        labelJob = ttk.Label(second_frame, text = "Job : " + job, style="BW.TLabel")
        labelJob.grid(sticky=W, row = 3)

        labelLocation = ttk.Label(second_frame, text = "Location : " + location, style="BW.TLabel")
        labelLocation.grid(sticky=W, row = 4)

        labelWorkinPlace = ttk.Label(second_frame, text = "Working place : " + workinPlace, style="BW.TLabel")
        labelWorkinPlace.grid(sticky=W, row = 5)

        if(info==""):
            labelInfo = ttk.Label(second_frame, text = "Description : Not found", style="BW.TLabel")
            labelInfo.grid(sticky=W, row = 6)
        else:
            labelInfo = ttk.Label(second_frame, text = "Description : " + info, style="BW.TLabel")
            labelInfo.grid(sticky=W, row = 6)

        if(len(experienceTab) == 0):
            labelExp = ttk.Label(second_frame, text = "Experiences : Not found", style="BW.TLabel")
            labelExp.grid(sticky=W, row = 7)
        else:
            experiences = "Experiences : \n"
            for exp in experienceTab:
                experiences += exp + "\n"
            labelExp = ttk.Label(second_frame, text = experiences, style="BW.TLabel")
            labelExp.grid(sticky=W, row = 7)
        
        if(len(educationTab) == 0):
            labelEdu = ttk.Label(second_frame, text = "Education : Not found", style="BW.TLabel")
            labelEdu.grid(sticky=W, row = 8)
        else:
            educations = "Educations : \n"
            for edu in educationTab:
                educations += edu + "\n"
            labelEdu = ttk.Label(second_frame, text = educations, style="BW.TLabel")
            labelEdu.grid(sticky=W, row = 8)
        

        
        
        #### Instagram results ####
        label = ttk.Label(second_frame, text ="Instagram search found : ", style="BW.TLabel")
        label.grid(sticky=W, ipady=50)
        globImgInsta = []
        for imgName in os.listdir("target/"):
            image = Image.open("./target/" + imgName)
            image = image.resize((200, 200), Image.ANTIALIAS)
            globImgInsta.append(ImageTk.PhotoImage(image))  # PIL solution
            
        for im in globImgInsta:
            Label(second_frame, image=im).grid(sticky=W)
            

        
        #### Facebook results ####
        label = ttk.Label(second_frame, text ="Facebook search found : ", style="BW.TLabel", )
        label.grid(ipady=50, sticky=W)
        globImgFb = []
        for imgName in os.listdir("targetFB/"):
            image = Image.open("./targetFB/" + imgName)
            image = image.resize((200, 200), Image.ANTIALIAS)
            globImgFb.append(ImageTk.PhotoImage(image))  # PIL solution
            
        for im in globImgFb:
            Label(second_frame, image=im).grid(sticky=W)
        


 
 
