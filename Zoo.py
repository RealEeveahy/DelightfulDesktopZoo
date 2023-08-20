import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess
import json
from functools import partial

class mainWindow():
    def __init__(self):
        #create a window, define display
        self.window = tk.Tk()
        self.window.title("Mae's Delightful Desktop Zoo!")
        self.window.iconbitmap("DelightfulDesktopZoo/images/favicon.ico")

        #define the size and position
        self.window.geometry('758x500+800+100')
        #retain the size
        self.window.resizable(False, False)

        #create a navigation bar
        self.navBar = tk.Frame(self.window, bg="#c4c4c4", height= 40)
        self.navBar.grid(row=0, column=0, sticky="ew", columnspan= 6)

        #define a dictionary to store each pet
        self.running_subprocess = {}
        #define a dictionary to store the end_pet buttons
        self.end_buttons = {}
        self.endList = []

        #create a button for adding a new pet
        addpet_size = (38,38)
        addpet_Image = Image.open("DelightfulDesktopZoo/images/addpet.png")
        resized_addpet = addpet_Image.resize(addpet_size)
        addpet_tk = ImageTk.PhotoImage(resized_addpet)
        self.addPet = tk.Button(self.window, image=addpet_tk, bd=0, width=addpet_size[0], height=addpet_size[1], bg="#c4c4c4")
        self.addPet.grid(row=0,column=0, sticky="w")

        #place the page title
        self.titleLabel = tk.Label(text="Welcome to Mae's Delightful Desktop Zoo! Please choose a pet to begin playing!", font=("Helvetica", 16))
        self.titleLabel.grid(row=1, column=0, pady= 1, columnspan= 3)

        #define a directory for pet files
        pets_files = os.listdir('DelightfulDesktopZoo/pets')
        pets_list = [filename for filename in pets_files if filename.endswith(".json")]

        #for pet menu, define variables
        row_count = 2
        col_count = 0
        button_image_size = (200, 200)

        #create a button for each pet
        for pet in pets_list:
            pet_filename = os.path.join('DelightfulDesktopZoo/pets', pet)

            with open(pet_filename, "r") as json_file:
                pet_data = json.load(json_file)

            pet_image = Image.open(os.path.join('DelightfulDesktopZoo/pets', pet_data["default_icon"]))
            pet_image = pet_image.resize(button_image_size)
            
            pet_image_tk = ImageTk.PhotoImage(pet_image)

            self.petButton = tk.Button(self.window, image=pet_image_tk, text=pet_data["name"], compound= tk.BOTTOM, bd=0, 
                                       width= button_image_size[0], height= button_image_size[1] + 5,
                                       command=lambda pet=pet: self.run_script(pet))
            self.petButton.photo = pet_image_tk
            self.petButton.grid(row=row_count, column=col_count, padx=5, pady= 5)

            self.destroy_pet = tk.Button(self.window, text='x', width=5, height=5,
                                          bg='red', command=lambda pet=pet: self.end_pet(pet))
            self.destroy_pet.grid(row=row_count, column=col_count, sticky="ne")
            self.destroy_pet.grid_forget()

            self.end_buttons[pet] = self.destroy_pet
            
            col_count +=1
            if col_count > 2:
                col_count = 0
                row_count +=1
        
        self.hide_buttons()
        self.window.mainloop()

    def hide_buttons(self):
        for b in self.endList:
            b.grid_forget()

    def run_script(self, pet):
        #spawn in a pet when clicked
        try:
            process = subprocess.Popen(["python", "DelightfulDesktopZoo/Pet1.py", pet])
            self.running_subprocess[pet] = process
            endbutton = self.end_buttons[pet]
            endbutton.grid()
        except Exception as e:
            print(f"Error running {pet}.py: {e}")

    def end_pet(self, pet):
        if pet in self.running_subprocess:
            process = self.running_subprocess[pet]
            process.terminate()
            del self.running_subprocess[pet]

mainWindow()