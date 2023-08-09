from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from main_options import MainOptions
from filepath import GetFilePath

def watermark_image():
    window = Tk()
    window.title("Watermarking")
    
    file = open("image_path.txt")
    path = fr"{file.read()}"
    file.close()

    pillow_img = Image.open(path)
    pillow_size = pillow_img.size
    
    resized = False
    if pillow_size[0] > 400 or pillow_size[1] > 400:
        pillow_img = pillow_img.resize((350, 350))
        pillow_size = pillow_img.size
        resized = True
        
    img = ImageTk.PhotoImage(pillow_img)

    canvas = Canvas(width=pillow_size[0] * 2, height=pillow_size[1] * 2, bg="white", highlightthickness=0)
    canvas.create_image(pillow_size[0], pillow_size[1], image=img)
    canvas.pack()

    watermarks = []
    
    MainOptions(window=window, canvas=canvas, watermarks=watermarks, pillow_size=pillow_size)

    if resized:
        messagebox.showinfo(title="Sorry", message="Unfortunately this application is not built to watermark images with dimensions higher than 400x400. So images larger than adequate dimesions will be automatically resized.")
    
    window.mainloop()
    

GetFilePath(watermark_image)

