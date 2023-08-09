from tkinter import *
from create_options import CreateOptions
from delete_edit_watermark import DeleteEditWatermark
from save_image import Save

class MainOptions():
    def __init__(self, window, canvas, watermarks, pillow_size):
        self.additional_window = Toplevel()
        self.additional_window.config(width=300, height=150)
        self.additional_window.title("Main Options")
        
        self.option_lab = Label(self.additional_window, text="Watermark", font=("", 15))
        self.option_lab.place(x=90, y=0)

        self.create_but = Button(self.additional_window, text="Create", width=17, command=lambda: self.create_watermark(canvas, pillow_size, watermarks))
        self.create_but.place(x=80, y=30)

        self.edit_but = Button(self.additional_window, text="Edit", width=17, state="disabled", command=lambda: self.edit_watermark(canvas, watermarks, pillow_size))
        self.edit_but.place(x=80, y=55)

        self.delete_but = Button(self.additional_window, text="Delete", width=17, state="disabled", command=lambda: self.delete_watermark(canvas, watermarks))
        self.delete_but.place(x=80, y=80)

        self.save_but = Button(self.additional_window, text="Save", width=17, command=lambda: self.save_img(window, canvas))
        self.save_but.place(x=80, y=105)
        

    def create_watermark(self, canvas, pillow_size, watermarks):
       CreateOptions(c=canvas, psize=pillow_size, dictionary_lst=watermarks, mode="create", delete_but=self.delete_but, edit_but=self.edit_but)


    def delete_watermark(self, canvas, watermarks):
       DeleteEditWatermark(c=canvas, wmarks=watermarks, main_delete_but=self.delete_but, main_edit_but=self.edit_but, delete_object=True)


    def edit_watermark(self, canvas, watermarks, pillow_size):
       DeleteEditWatermark(c=canvas, wmarks=watermarks,  main_delete_but=self.delete_but, main_edit_but=self.edit_but, createopt=CreateOptions, psize=pillow_size, add_delete=False, delete_object=False)        


    def save_img(self, window, canvas):
        Save(w=window, c=canvas)
