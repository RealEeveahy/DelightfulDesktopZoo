import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

class mainWindow():
    def __init__(self):
        #create a window
        self.window = tk.Tk()
        self.window.title("Mae's Delightful Desktop Zoo!")

        #define the size and position
        self.window.geometry('800x500+100+100')
        #retain the size
        self.window.resizable(False, False)

        pets_list = os.listdir('DelightfulDesktopZoo/pets')

        self.titleLabel = tk.Label(text="Welcome to Mae's Delightful Desktop Zoo! Please choose a pet to begin playing!", font=("Helvetica", 16))
        self.titleLabel.grid(row=0, column=0, pady= 1, columnspan= 3)

        button_image_size = (200, 200)

        row_count = 1
        col_count = 0
        for pet in pets_list:
            pet_image = Image.open(f'DelightfulDesktopZoo/pets/{pet}/{pet}_default.png')
            pet_image = pet_image.resize(button_image_size)
            
            pet_image_tk = ImageTk.PhotoImage(pet_image)

            self.petButton = tk.Button(self.window, image=pet_image_tk, text=pet, compound= tk.BOTTOM, bd=0, 
                                       width= button_image_size[0], height= button_image_size[1],
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
            subprocess.run(["python", "Pet1.py"])
        except Exception as e:
            print(f"Error running {pet}.py: {e}")

        self.window.destroy()

mainWindow()