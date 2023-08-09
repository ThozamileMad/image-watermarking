from tkinter import *
from tkinter import messagebox

class CreateOptions():
    def __init__(self, c, psize, dictionary_lst, mode, selected_watermark=None, delete_but=None, edit_but=None):
        self.additional_window = Toplevel()
        self.additional_window.config(width=500, height=500)
        self.additional_window.title("Watermark Configurations")
        
        self.canvas = c
        self.pillow_size = psize
        self.current_watermark_text = "Watermark"
        self.starting_x = self.calculatexy(51, 0)
        self.starting_y = self.calculatexy(47, 1)

        self.dictionary = {}
        self.ctext_data = dictionary_lst
        self.watermark_text_widgets = {"label": None,"text_field": None, "button": None}
        self.watermark_font_widgets = {"label": None,"text_field": None, "button": None, "font": ""}
        self.watermark_size_widgets = {"label": None,"text_field": None, "button": None, "size": 0}
        self.watermark_color_widgets  = {"label": None,"text_field": None, "button": None, "color": "black"}
        self.watermark_angle_widgets  = {"label": None,"text_field": None, "button": None, "angle": 0}
        
        
        if mode == "create":
            self.ctext = self.canvas.create_text(self.starting_x, self.starting_y, text="Watermark", font=("", 0))
            self.final_xy = [[self.starting_x, self.starting_y]]
        else:
            for dictionary in self.ctext_data:
                if dictionary["name"] == selected_watermark:
                    for ctext in dictionary["objects"]:
                        if ctext != dictionary["objects"][-1]:
                            self.canvas.delete(ctext)
                    self.ctext = dictionary["objects"][-1]
                    self.final_xy = [[dictionary["x"], dictionary["y"]]]
                    self.additional_window.title("Edit Watermark")
                    self.current_watermark_text = dictionary["name"]
                    self.watermark_font_widgets["font"] = dictionary["font_size"][0]
                    self.watermark_size_widgets["size"] = dictionary["font_size"][1]
                    self.watermark_color_widgets["color"] = dictionary["color"]
                    self.watermark_angle_widgets["angle"] = dictionary["angle"]
                    self.ctext_data.remove(dictionary)
            
        self.ctext_lst = [self.ctext]
        self.create_widgets(label_txt="Watermark Text", create_what=Entry, labxy=[50, 20], entspinxy=[63, 50], butxy=[64, 71], watermark_dict=self.watermark_text_widgets, widget="watermark_text")
        self.create_widgets(label_txt="Watermark Font", create_what=Entry, labxy=[287, 20], entspinxy=[300, 50], butxy=[301, 71], watermark_dict=self.watermark_font_widgets, widget="watermark_font")
        self.create_widgets(label_txt="Watermark Size", create_what=Spinbox, labxy=[50, 150], entspinxy=[58, 180], butxy=[64, 201], watermark_dict=self.watermark_size_widgets, widget="watermark_size")
        self.create_widgets(label_txt="Watermark Color", create_what=Entry, labxy=[287, 150], entspinxy=[300, 180], butxy=[301, 201], watermark_dict=self.watermark_color_widgets, widget="watermark_color")
        self.create_widgets(label_txt="Watermark Angle", create_what=Spinbox, labxy=[50, 280], entspinxy=[58, 310], butxy=[64, 331], watermark_dict=self.watermark_angle_widgets, widget="watermark_angle")

        self.text_positioning_button = Button(self.additional_window, text="Text Positioning", width=16, height=8, command=lambda:  messagebox.showinfo(title="How to position Watermark", message="Click and drag the Watermark using the cursor."))
        self.text_positioning_button.place(x=287, y=280)

        self.size_error_label = Label(self.additional_window, fg="red", text="")
        self.size_error_label.place(x=50, y=228)
        
        self.color_error_label = Label(self.additional_window, fg="red", text="")
        self.color_error_label.place(x=250, y=228)
        
        self.angle_error_label = Label(self.additional_window, fg="red", text="")
        self.angle_error_label.place(x=50, y=358)

        self.move_watermark = True
        self.canvas.bind("<B1 Motion>", self.position_text)

        self.save_button = Button(self.additional_window, text="Save Watermark", command=lambda: self.save_watermark())
        self.save_button.place(x=200, y=450)

        self.delete_but = delete_but
        self.edit_but = edit_but
        

    def save_watermark(self):
        is_ok = messagebox.askokcancel(title="Confirm Save", message="Are you sure you want to save this Watermark")
        if is_ok:
            self.canvas.delete(self.ctext)
            self.additional_window.destroy()
            self.move_watermark = False
            
            xcor = self.final_xy[-1][0]
            ycor = self.final_xy[-1][1]
            self.ctext = self.canvas.create_text(xcor, ycor, text=self.current_watermark_text, font=(self.watermark_font_widgets["font"], self.watermark_size_widgets["size"]), fill=self.watermark_color_widgets["color"], angle=self.watermark_angle_widgets["angle"])

            dict_data = [["name", f"{self.current_watermark_text}"], ["objects", self.ctext_lst], ["font_size", (self.watermark_font_widgets["font"], self.watermark_size_widgets["size"])], ["color", self.watermark_color_widgets["color"]], ["angle", self.watermark_angle_widgets["angle"]], ["x", xcor], ["y", ycor]]
            for data in dict_data:
                self.dictionary[data[0]] = data[1]
            self.dictionary["objects"].append(self.ctext)
            self.ctext_data.append(self.dictionary)

            try:
                self.delete_but.config(state="active")
                self.edit_but.config(state="active")
            except AttributeError:
                pass

       
    def calculatexy(self, num, index_num):
        equation = num/100 * self.pillow_size[index_num] * 2
        return equation


    def create_widgets(self, label_txt, create_what, labxy, entspinxy, widget, butxy, watermark_dict):
        label = Label(self.additional_window, text=label_txt, font=("", 15))
        label.place(x=labxy[0], y=labxy[1])

        text_field = create_what(self.additional_window)
        text_field.place(x=entspinxy[0], y=entspinxy[1])

        button = Button(self.additional_window, text="Set", width=16, command=lambda: [self.apply_command(watermark_dict, widget)])
        button.place(x=butxy[0], y=butxy[1])

        watermark_dict["label"] = label
        watermark_dict["text_field"] = text_field
        watermark_dict["button"] = button
        

    def validate_input(self, dictionary, error_label, change, text, error, error_text):
        try:
            dictionary["label"].config(fg="black")
            error_label.config(text="")
            if change == "size":
                user_input = text.replace(" ", "")
                self.canvas.itemconfig(self.ctext, font=(self.watermark_font_widgets["font"], int(user_input)))
                self.watermark_size_widgets["size"] = int(user_input)
            elif change == "color":
                if text != "":
                    self.canvas.itemconfig(self.ctext, fill=text)
                    self.watermark_color_widgets["color"] = text
                else:
                    self.canvas.itemconfig(self.ctext, fill="black")
            elif change == "angle":
                user_input = text.replace(" ", "")
                self.canvas.itemconfig(self.ctext, angle=int(user_input))
                self.watermark_angle_widgets["angle"] = int(user_input)
        except error:
            dictionary["label"].config(fg="red")
            error_label.config(text=error_text)   


    def apply_command(self, dictionary, widget):
        text = dictionary["text_field"].get()
        if widget == "watermark_text":
            self.canvas.itemconfig(self.ctext, text=text)
            self.current_watermark_text = text
        elif widget == "watermark_font":
            self.canvas.itemconfig(self.ctext, font=(text, self.watermark_size_widgets["size"]))
            self.watermark_font_widgets["font"] = text
        elif widget == "watermark_size":
            self.validate_input(dictionary, self.size_error_label, "size", text, ValueError, "Invalid input, use numbers")       
        elif widget == "watermark_color":
            self.validate_input(dictionary, self.color_error_label, "color", text, TclError, "Invalid input, use the correct color or code.")
        elif widget == "watermark_angle":
            self.validate_input(dictionary, self.angle_error_label, "angle", text, ValueError, "Invalid input, use numbers") 


    def position_text(self, e):
        if self.move_watermark:
            self.canvas.delete(self.ctext)
            self.final_xy.append([e.x, e.y])
            self.ctext = self.canvas.create_text(e.x, e.y, text=self.current_watermark_text, font=(self.watermark_font_widgets["font"], self.watermark_size_widgets["size"]), fill=self.watermark_color_widgets["color"], angle=self.watermark_angle_widgets["angle"]) 
            self.dictionary["name"] = f"{self.current_watermark_text}"
            self.dictionary["objects"] = self.ctext_lst
            self.dictionary["font_size"] = (self.watermark_font_widgets["font"], self.watermark_size_widgets["size"])
            self.dictionary["color"] = self.watermark_color_widgets["color"]
            self.dictionary["objects"].append(self.ctext)
