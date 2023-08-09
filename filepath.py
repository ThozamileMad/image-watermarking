from tkinter import *
from tkinter import messagebox

class GetFilePath():
    def __init__(self, wmark_img):
        self.start_watermarking(wmark_img)
        

    def start_watermarking(self, wmark_img):
        print("Help Info: Enter the file path to upload image, for example:  C:/Users/Myname/Downloads/image.jpg.")
        is_valid = False
        while not is_valid:
            user_input = input("\nEnter image filepath: ")
            if self.write_to_file(user_input, wmark_img):
                is_valid = True


    def write_to_file(self, user_input, wmark_img):
        try:
            with open("image_path.txt", "w") as file:
                file.write(user_input)
            try:
                try:
                    wmark_img()
                    return True
                except PermissionError:
                    print("\nError: File not found please ensure that the file path entered, is valid and that the image file is in the directory.")
                    return False
            except AttributeError:
                print("\nError: File not found please ensure that the file path entered, is valid and that the image file is in the directory.")
                return False
        except FileNotFoundError:
            print("\nError: File not found please ensure that the file path entered, is valid and that the image file is in the directory.")
            return False
