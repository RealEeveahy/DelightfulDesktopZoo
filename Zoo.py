import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess
import json
from functools import partial

class mainWindow():
    def __init__(self):
        #create a window
        self.window = tk.Tk()
        self.window.title("Mae's Delightful Desktop Zoo!")
        self.window.iconbitmap("DelightfulDesktopZoo/images/favicon.ico")

        #define the size and position
        self.window.geometry('758x500+100+100')
        #retain the size
        self.window.resizable(False, False)

        self.navBar = tk.Frame(self.window, bg="#c4c4c4", height= 40)
        self.navBar.grid(row=0, column=0, sticky="ew", columnspan= 6)

        self.window.wm_attributes('-transparentcolor', 'black')

        addpet_size = (38,38)
        addpet_Image = Image.open("DelightfulDesktopZoo/images/addpet.png")
        resized_addpet = addpet_Image.resize(addpet_size)
        addpet_tk = ImageTk.PhotoImage(resized_addpet)
        self.addPet = tk.Button(self.window, image=addpet_tk, bd=0, width=addpet_size[0], height=addpet_size[1], bg="#c4c4c4")
        self.addPet.grid(row=0,column=0, sticky="w")

        self.titleLabel = tk.Label(text="Welcome to Mae's Delightful Desktop Zoo! Please choose a pet to begin playing!", font=("Helvetica", 16))
        self.titleLabel.grid(row=1, column=0, pady= 1, columnspan= 3)

        button_image_size = (200, 200)

        pets_files = os.listdir('DelightfulDesktopZoo/pets')
        pets_list = [filename for filename in pets_files if filename.endswith(".json")]

        row_count = 2
        col_count = 0
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
            
            col_count +=1
            if col_count > 2:
                col_count = 0
                row_count +=1

        self.window.mainloop()

    def run_script(self, pet):
        try:
            subprocess.Popen(["python", "DelightfulDesktopZoo/Pet1.py", pet])
        except Exception as e:
            print(f"Error running {pet}.py: {e}")

        #self.window.destroy()

mainWindow()