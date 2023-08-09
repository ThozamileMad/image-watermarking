from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageGrab


class Save():
    def __init__(self, w, c):
        self.window = w
        
        self.additional_window = Toplevel()
        self.additional_window.config(width=500, height=500)
        self.additional_window.title("Save Image")

        self.canvas = c

        self.help_but = Button(self.additional_window, text="Help?", command=lambda: messagebox.showinfo(title="Help Info", message="Enter the file name, extension and location that you wish to save your image in."))
        self.help_but.place(x=20, y=20)

        self.name_widgets = {"user_input": ""}
        self.extension_widgets = {"user_input": ""}
        self.location_widgets = {"user_input": ""}

        self.create_widgets(label_txt="File Name", create_what="entry", labxy=[80, 120], entspinxy=[63, 150], butxy=[61, 171], watermark_dict=self.name_widgets)
        self.create_widgets(label_txt="File Extension", create_what="combobox", labxy=[296, 120], entspinxy=[300, 150], butxy=[298, 171], watermark_dict=self.extension_widgets, cvalues=["png", "jpg", "jpeg"], combobox_width=17)
        self.create_widgets(label_txt="File Location", create_what="combobox", labxy=[185, 250], entspinxy=[150, 280], butxy=[182, 301], watermark_dict=self.location_widgets, cvalues=[fr"C:\Users\Joel Dube\{filename}" for filename in ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos"]], combobox_width=28)

        self.save_but = Button(self.additional_window, text="Save", width=17, command=self.save)
        self.save_but.place(x=182, y=400)
         

    def create_widgets(self, label_txt, create_what, labxy, entspinxy, butxy, watermark_dict, combobox_width=None, cvalues=None):
        label = Label(self.additional_window, text=label_txt, font=("", 15))
        label.place(x=labxy[0], y=labxy[1])

        if create_what == "entry":
            text_field = Entry(self.additional_window)
            text_field.place(x=entspinxy[0], y=entspinxy[1])
        elif create_what == "spinbox":
            text_field = Spinbox(self.additional_window, from_=1, to=50)
            text_field.place(x=entspinxy[0], y=entspinxy[1])
        else:
            text_field = Combobox(self.additional_window, values=cvalues, width=combobox_width)
            text_field.place(x=entspinxy[0], y=entspinxy[1])

        button = Button(self.additional_window, text="Set", width=17, command=lambda: self.validate_input(text_field.get(), label["text"].lower(), watermark_dict))
        button.place(x=butxy[0], y=butxy[1])

        watermark_dict["label"] = label
        watermark_dict["text_field"] = text_field
        watermark_dict["button"] = button


    def validate_input(self, user_input, text_input, widgets):                
        empty_box = True
        number_box = True
        
        if user_input == "":
            messagebox.showerror(title="Error", message=f"The value entered in the {text_input} text field is empty, set valid input.")
        else:
            empty_box = False
            
        try:
            int(user_input)
            messagebox.showerror(title="Error", message=f"The value entered in the {text_input} text field is a number, set valid input.")
        except ValueError:
            number_box = False

        if not empty_box and not number_box:
            user_input = widgets["text_field"].get()
            widgets["user_input"] = user_input
            messagebox.showinfo(title="Set successful", message=fr"{widgets['label']['text']} successfully set to {user_input}.")

        
    def save(self):
        file_name = self.name_widgets["user_input"]
        file_extension = self.extension_widgets["user_input"]
        file_path = self.location_widgets["user_input"]
        filelocation = f"{file_path}\{file_name}.{file_extension}"

        x=self.window.winfo_rootx()+self.canvas.winfo_x()
        y=self.window.winfo_rooty()+self.canvas.winfo_y()
        x1=x+self.canvas.winfo_width()
        y1=y+self.canvas.winfo_height()

        try:
            ImageGrab.grab().crop((x ,y, x1, y1)).save(filelocation)
            messagebox.showinfo(title="Save Successful", message=fr"File saved in {file_path}")
            self.window.destroy()
        except ValueError or FileNotFoundError:
            messagebox.showerror(title="Error", message=fr"Invalid file path({filelocation})")
