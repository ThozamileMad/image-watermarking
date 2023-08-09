from tkinter import Toplevel, Label, Button, messagebox
from tkinter.ttk import Combobox

class DeleteEditWatermark():
    def __init__(self, c, wmarks,  main_delete_but, main_edit_but, createopt=None, psize=None, add_delete=True, delete_object=True):
        self.watermarks = wmarks
        
        self.additional_window = Toplevel()
        self.additional_window.config(width=500, height=500)
        self.additional_window.title("Delete Watermark")
        
        self.canvas = c
        self.pillow_size = psize
        
        self.help_but = Button(self.additional_window, text="Help?", command=lambda:  messagebox.showinfo(title="Help Info", message="Enter the name of the Watermark you wish to delete in the Combobox then click select."))
        self.help_but.place(x=20, y=20)
        
        self.watermark_label = Label(self.additional_window, text="")
        self.watermark_label.place(x=165, y=70)
        
        self.label = Label(self.additional_window, text="Select Watermark", font=("", 16))
        self.label.place(x=165, y=250)

        self.combobox_values = [dictionary["name"] for dictionary in self.watermarks]
        self.combobox = Combobox(self.additional_window, values=self.combobox_values, width=27)
        self.combobox.place(x=160, y=290)

        if add_delete:
            self.select = Button(self.additional_window, text="Select", command=lambda: self.set_watermark(createopt))
            self.select.place(x=230, y=315)
        
            self.delete = Button(self.additional_window, text="Delete", state="disabled")
            self.delete.place(x=229, y=340)
        else:
            self.help_but.config(command=lambda:  messagebox.showinfo(title="Help Info", message="Enter the name of the Watermark you wish to edit in the Combobox then click select followed by edit to edit watermark."))
            
            self.select = Button(self.additional_window, text="Select", command=lambda: self.set_watermark(createopt, delete=False))
            self.select.place(x=230, y=315)

            self.edit = Button(self.additional_window, text="Edit", state="disabled")
            self.edit.place(x=235, y=340)
            
        self.selected_dictionary = None
        self.selected_watermark = None

        self.main_delete_but = main_delete_but
        self.main_edit_but = main_edit_but

    
    def set_watermark(self, createopt, delete=True):
        combobox_text = self.combobox.get()
        if combobox_text not in self.combobox_values:
            messagebox.showerror(title="Error", message="Watermark doesn't exist.")
        else:
            selected_dict = None
            for dictionary in self.watermarks:
                if dictionary["name"] == combobox_text:
                    self.selected_dictionary = dictionary
                    self.selected_watermark =  combobox_text
                    if self.selected_watermark in self.combobox_values:
                        self.watermark_label.config(text=combobox_text, font=dictionary["font_size"], fg=dictionary["color"])
                        if delete:
                            self.delete.config(state="active", command=self.delete_watermark)
                        else:
                            self.edit.config(state="active", command=lambda: self.edit_watermark(createopt))


    def edit_watermark(self, createopt):
        self.combobox_values.remove(self.selected_watermark)
        self.combobox.config(values=self.combobox_values)
        widgets = [self.additional_window, self.help_but, self.watermark_label, self.label, self.combobox, self.select]
        for widget in widgets:
            widget.destroy()
        createopt(self.canvas, self.pillow_size, self.watermarks, "edit", selected_watermark=self.selected_watermark)
                                

    def delete_watermark(self):
        for obj in self.selected_dictionary["objects"]:
            self.canvas.delete(obj)
        self.delete.config(state="disabled")
        
        self.combobox_values.remove(self.selected_watermark)
        self.combobox.config(values=self.combobox_values)
        
        self.watermark_label.config(text="")
        if self.combobox_values == []:
            self.main_edit_but.config(state="disabled")
            self.main_delete_but.config(state="disabled")
            self.additional_window.destroy()
        self.watermarks.remove(self.selected_dictionary)


        

                
        
        
            


            

        
            

        
        



