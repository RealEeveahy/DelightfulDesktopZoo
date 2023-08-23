import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import subprocess
import json
import shutil

class mainWindow(tk.Tk):
    addpet_image_tk = None
    new_default_path = None
    new_idle_path = None
    new_walk_path = None

    def __init__(self):
        #create a window, define display
        self.window = tk.Tk()
        self.window.title("Mae's Delightful Desktop Zoo!")
        self.window.iconbitmap("images/favicon.ico")

        #define the size and position
        self.window.geometry('758x500+800+100')
        #retain the size
        self.window.resizable(False, False)

        #create frames for pages
        self.pet_select = tk.Frame(self.window)
        self.new_pet = tk.Frame(self.window)

        #create a navigation bar
        self.navBar = tk.Frame(self.pet_select, bg="#c4c4c4", height= 40)
        self.navBar.grid(row=0, column=0, sticky="ew", columnspan= 6)

        #define a dictionary to store each pet
        self.running_subprocess = {}
        #define a dictionary to store the end_pet buttons
        self.end_buttons = {}
        self.endList = []

        actionForPath = {
            "default": mainWindow.new_default_path,
            "idle": mainWindow.new_idle_path,
            "walk": mainWindow.new_walk_path
        }

        #create a button for adding a new pet
        if mainWindow.addpet_image_tk is None:
            addpet_size = (38,38)
            addpet_Image = Image.open("images/addpet.png")
            resized_addpet = addpet_Image.resize(addpet_size)
            mainWindow.addpet_image_tk = ImageTk.PhotoImage(resized_addpet)

        self.addPet = tk.Button(self.pet_select, image=mainWindow.addpet_image_tk, bd=0, width=addpet_size[0], height=addpet_size[1],
                                 bg="#c4c4c4", command=self.show_pet_create)
        self.addPet.grid(row=0,column=0, sticky="w")

        #place the page title
        self.titleLabel = tk.Label(self.pet_select, text="Welcome to Mae's Delightful Desktop Zoo! Please choose a pet to begin playing!", font=("Helvetica", 16))
        self.titleLabel.grid(row=1, column=0, pady= 1, columnspan= 3)

        #define a directory for pet files
        pets_files = os.listdir('pets')
        pets_list = [filename for filename in pets_files if filename.endswith(".json")]

        #for pet menu, define variables
        self.row_count = 2
        self.col_count = 0
        self.button_image_size = (200, 200)

        #create a button for each pet
        for pet in pets_list:
            self.create_pet_button(pet=pet)

        #initialise the add_pet page
        new_pet_title = tk.Label(self.new_pet, text="Create a new pet", font=("Helvetica", 16))
        new_pet_title.grid(row=1,column=0,)

        new_pet_close = tk.Button(self.new_pet, text='x', width=2, height=1,
                                  bg='red', command=self.show_pet_select)
        new_pet_close.grid(row=1,column=5, sticky="e")

        #field for pet name
        name_label = tk.Label(self.new_pet, text="Name", font=("Helvetica", 12))
        name_label.grid(row=2,column=0, padx=3)
        new_pet_name = tk.Entry(self.new_pet)
        new_pet_name.grid(row=2,column=1)

        #field for a pet's default display image
        defaultimg_label = tk.Label(self.new_pet, text="Default Image", font=("Helvetica", 12))
        defaultimg_label.grid(row=3, column=0, padx=3)
        self.defaultimg_name = tk.Label(text="",font=("Helvetica", 8))
        defaultimg_button = tk.Button(self.new_pet, text="Upload an image",width=15,height=1,
                                      command=lambda: open_file_dialog(self, filename_label=self.defaultimg_name, 
                                                                                 action="default"))
        defaultimg_button.grid(row=3,column=1)
        self.defaultimg_name.grid(row=3,column=2, sticky=tk.E)
        self.defaultimg_name.grid_remove()

        #field for a pet's idle sheet
        idlesheet_label = tk.Label(self.new_pet, text="Idle Spritesheet", font=("Helvetica", 12))
        idlesheet_label.grid(row=4, column=0, padx=3)
        self.idlesheet_name = tk.Label(text="",font=("Helvetica", 8))
        idlesheet_button = tk.Button(self.new_pet, text="Upload an image",width=15,height=1,
                                      command=lambda self=self: open_file_dialog(self, filename_label=self.idlesheet_name, 
                                                                                 action="idle"))
        idlesheet_button.grid(row=4,column=1)
        self.idlesheet_name.grid(row=4,column=2, sticky=tk.E)
        self.idlesheet_name.grid_remove()

        #field for a pet's walk sheet
        walksheet_label = tk.Label(self.new_pet, text="Walking Spritesheet", font=("Helvetica", 12))
        walksheet_label.grid(row=5, column=0, padx=3)
        self.walksheet_name = tk.Label(text="",font=("Helvetica", 8))
        walksheet_button = tk.Button(self.new_pet, text="Upload an image",width=15,height=1,
                                      command=lambda self=self: open_file_dialog(self, filename_label=self.walksheet_name, 
                                                                                 action="walk"))
        walksheet_button.grid(row=5,column=1)
        self.walksheet_name.grid(row=5,column=2, sticky=tk.E)
        self.walksheet_name.grid_remove()

        #button to finalise pet creation
        create_pet = tk.Button(self.new_pet, text="Confirm & Create", width=15, height=1,
                               command= lambda self=self: self.generate_pet(new_pet_name.get(), mainWindow.new_default_path))
        create_pet.grid(row=6,column=0, padx= 5)

        self.show_pet_select()
        self.window.mainloop()

    def show_pet_create(self):
        self.new_pet.grid()
        self.pet_select.grid_remove()
    def show_pet_select(self):
        self.pet_select.grid()
        self.new_pet.grid_remove()

    def hide_buttons(self):
        for b in self.endList:
            b.grid_forget()

    def create_pet_button(self,pet):
        pet_filename = os.path.join('pets', pet)

        with open(pet_filename, "r") as json_file:
            pet_data = json.load(json_file)

        pet_image = Image.open(os.path.join('pets', pet_data["default_icon"]))
        pet_image = pet_image.resize(self.button_image_size)
        
        pet_image_tk = ImageTk.PhotoImage(pet_image)

        self.petButton = tk.Button(self.pet_select, image=pet_image_tk, text=pet_data["name"], compound= tk.BOTTOM, bd=0, 
                                    width=self.button_image_size[0], height=self.button_image_size[1] + 5,
                                    command=lambda pet=pet: self.run_script(pet))
        self.petButton.photo = pet_image_tk
        self.petButton.grid(row=self.row_count, column=self.col_count, padx=5, pady= 5)

        self.destroy_pet = tk.Button(self.pet_select, text='x', width=5, height=2,
                                        bg='red', command=lambda pet=pet: self.end_pet(pet))
        self.destroy_pet.grid(row=self.row_count, column=self.col_count, sticky="ne")
        self.destroy_pet.grid_remove()

        self.end_buttons[pet] = self.destroy_pet
        
        self.col_count +=1
        if self.col_count > 2:
            self.col_count = 0
            self.row_count +=1

    def run_script(self, pet):
        #spawn in a pet when clicked
        try:
            if pet not in self.running_subprocess:
                process = subprocess.Popen(["python", "Pet1.py", pet])
                self.running_subprocess[pet] = process
                endbutton = self.end_buttons[pet]
                endbutton.grid()
        except Exception as e:
            print(f"Error running {pet}.py: {e}")

    def end_pet(self, pet):
        if pet in self.running_subprocess:
            process = self.running_subprocess[pet]
            process.terminate()
            endbutton = self.end_buttons[pet]
            endbutton.grid_remove()
            del self.running_subprocess[pet]

    def generate_pet(self, name, default_path):
        #get size of default sprite
        print(default_path)
        sprite_default = Image.open(default_path)
        sprite_size = sprite_default.size
        #serialize data for new pet
        data = {
            "name": name,
            "default_icon": default_path,
            "idle_actions": "idle, walk",
            "reactions": "",
            "sprite_size": f"({sprite_size[0]},{sprite_size[1]})"
        }
        #create a json file for the pet data
        file_name = (f'pets/{name}.json')
        with open(file_name, "w") as json_file:
            json.dump(data, json_file)
        #create a file directory for the pets images and place its images inside
        sprite_folder = f'pets/{name}_images'
        if not os.path.exists(sprite_folder):
            os.mkdir(sprite_folder)
            
        default_filename = f"{name}_default.png"
        default_destination = os.path.join(sprite_folder, default_filename)
        shutil.copyfile(default_path, default_destination)

        idle_filename = f"{name}_idlesheet.png"
        idle_destination = os.path.join(sprite_folder, idle_filename)
        shutil.copyfile(mainWindow.new_idle_path, idle_destination)

        walk_filename = f"{name}_walksheet.png"
        walk_destination = os.path.join(sprite_folder, walk_filename)
        shutil.copyfile(mainWindow.new_walk_path, walk_destination)

        #add the pet to the selection menu
        self.create_pet_button(pet=f"{name}.json")
        self.show_pet_select()

def open_file_dialog(self, filename_label, action):
    file_path = filedialog.askopenfilename(
        filetypes=[("PNG files", "*.png")],
        title="Select a PNG File",
        multiple=False
    )
    if file_path:
        print(f"Selected File: {file_path}")
        filename_label.config(text=f"Selected File: {file_path}")
        filename_label.grid()
        if action == "default": mainWindow.new_default_path = file_path
        elif action == "idle": mainWindow.new_idle_path = file_path
        elif action == "walk": mainWindow.new_walk_path = file_path

mainWindow()