import tkinter as tk
import time
import json
from PIL import Image
import os
import random
import sys
import ast

class pet():
    def __init__(self): #Start()
        #create a window
        self.window = tk.Tk()

        if len(sys.argv) < 2:
            print("Usage: python pet_script.py <pet_name>")
            sys.exit(1)

        self.thisPet = sys.argv[1]
        self.pet_name = os.path.splitext(self.thisPet)[0]
        pet_filename = os.path.join("pets/",self.thisPet)
        with open(pet_filename, "r") as json_file:
                self.pet_data = json.load(json_file)
        print(f"Running script for {self.thisPet}")

        #get the screen size
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        #initialise position
        self.x = 0
        self.y = 0

        #initialise target position
        self.targetX = 200
        self.targetY = 200

        #initialise animation
        self.indexInAnimation = 0

        #define dimensions
        sprite_size_str = self.pet_data["sprite_size"]
        sprite_size_tuple = ast.literal_eval(sprite_size_str)
        self.sprite_width, self.sprite_height = sprite_size_tuple

        self.actionVar()
        self.directionCoefficient = 1

        #define default image, then list of images
        self.img = tk.PhotoImage(file=f'pets/{self.pet_name}_images/{self.pet_name}_default.png')

        #get a list of possible actions and reactions (click events)
        self.idlesList = self.pet_data["idle_actions"].split(", ")
        self.reactionsList = self.pet_data["reactions"].split(", ")
        #cut the spritesheets for each action
        for s in self.idlesList:
            self.cutSheet(s)
        if self.reactionsList != ['']:
            for s in self.reactionsList:
                self.cutSheet(s)

        #instantiate current action
        self.currentAction = self.idlesList[0]

        #set focuslight to black when window unfocused
        self.window.config(highlightbackground='black')

        #make window frameless
        self.window.overrideredirect(True)

        #make window draw over all others
        self.window.attributes('-topmost', True)

        #turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'black')

        #create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')

        #create a window of size 128x128 pixels at 0,0
        self.window.geometry('96x72+{x}+0' .format(x=str(self.x)))

        #add the image to our label
        self.label.configure(image=self.img)

        #give window to geometry manager
        self.label.pack()

        #make the pet clickable
        self.label.bind("<Button-1>", self.on_click)

        #run self.update() after 0ms when main starts
        self.window.after(0, self.update)
        self.window.mainloop()
    
    #action to do when pet is clicked
    def on_click(self, event):
        print("Clicked!")
        self.currentAction = self.reactionsList[random.randint(0,len(self.reactionsList)-1)]
        self.indexInAnimation = 0

    #container for variables
    def actionVar(self):
        self.targetPosition = (self.targetX, self.targetY)

        myX = self.x
        myY = self.y
        self.currentPosition = (myX, myY)

        self.speed = 2
    
    def cutSheet(self, param):
        sheet_filename = f'pets/{self.pet_name}_images/{self.pet_name}_{param}sheet.png'
        sheet_image = Image.open(sheet_filename)

        sheet_width, sheet_height = sheet_image.size
        numOfSprites = sheet_width // self.sprite_width

        #crop the spritesheet
        sprite_list = []
        for i in range(numOfSprites):
            left = i * self.sprite_width
            upper = 0
            right = left + self.sprite_width
            lower = self.sprite_height
            sprite = sheet_image.crop((left, upper, right, lower))
            sprite_list.append(sprite)

        sprite_folder = f'pets/{self.pet_name}_images/{self.pet_name}_{param}'
        if not os.path.exists(sprite_folder):
            os.mkdir(sprite_folder)

        for i, sprite in enumerate(sprite_list):
            file_path = os.path.join(sprite_folder, f"{param}_{i}.png")
            if not os.path.exists(file_path):
                sprite.save(file_path)
    
    def GetNewPosition(self):
        self.targetX = random.randint(0, self.screen_width)
        self.targetY = random.randint(0, self.screen_height)
        print(f'New target: {self.targetX}, {self.targetY}')

    def Walk(self):
        #define a target
        if self.currentPosition == self.targetPosition:
            self.GetNewPosition()
        #define movement direction
        if self.currentPosition[0] < self.targetPosition[0]:
            movementX = 1
        elif self.currentPosition[0] > self.targetPosition[0]:
            movementX = -1
        elif self.currentPosition[0] == self.targetPosition[0]:
            movementX = 0

        if self.currentPosition[1] < self.targetPosition[1]:
            movementY = 1
        elif self.currentPosition[1] > self.targetPosition[1]:
            movementY = -1
        elif self.currentPosition[1] == self.targetPosition[1]:
            movementY = 0
            
        #move right one pixel
        self.x += movementX
        self.y += movementY

        #Get the current image path
        image_path = f'pets/{self.pet_name}_images/{self.pet_name}_walk/walk_{self.indexInAnimation}.png'

        #add the image to our label
        img = tk.PhotoImage(file= image_path)

        #flip the img if needed
        if movementX == 1: 
            flipImg = img.subsample(x=1, y=1)
            self.directionCoefficient = 1
        elif movementX == -1: 
            flipImg = img.subsample(x=-1, y=1)
            self.directionCoefficient = -1
        elif movementX == 0: 
            flipImg = img

        self.label.configure(image=flipImg)
        self.label.image = flipImg

    def Idle(self):
        #Get the current image path
        image_path = f'pets/{self.pet_name}_images/{self.pet_name}_idle/idle_{self.indexInAnimation}.png'
        img = tk.PhotoImage(file= image_path)

        if self.directionCoefficient == 1: flipImg = img.subsample(x=1, y=1)
        elif self.directionCoefficient == -1: flipImg = img.subsample(x=-1, y=1)
        elif self.directionCoefficient == 0: flipImg = img

        self.label.configure(image=flipImg)
        self.label.image = flipImg
    
    def Knockdown(self):
        image_path = f'pets/{self.pet_name}_images/{self.pet_name}_knockdown/knockdown_{self.indexInAnimation}.png'
        img = tk.PhotoImage(file= image_path)

        self.label.configure(image = img)
        self.label.image = img

    def DecideAction(self):
        self.currentAction = self.idlesList[random.randint(0,len(self.idlesList)-1)]

    def update(self): #Update()
        #update variables
        self.actionVar()

        if self.currentAction == None:
            self.DecideAction()
        elif self.currentAction == 'walk':
            self.Walk()
        elif self.currentAction == 'idle':
            self.Idle()
        elif self.currentAction == 'knockdown':
            self.Knockdown()

        #create the window
        self.window.geometry('{sx}x{sy}+{x}+{y}' .format(x=str(self.x), y=str(self.y),sx=str(self.sprite_width),sy=str(self.sprite_height)))

        #give window to geometry manager
        self.label.pack()

        file_list = os.listdir(f'pets/{self.pet_name}_images/{self.pet_name}_{self.currentAction}')

        self.indexInAnimation += 1
        if self.indexInAnimation >= len(file_list):
            self.indexInAnimation = 0
            self.currentAction = None

        #call update after 20ms
        self.window.after(20, self.update)

pet()

