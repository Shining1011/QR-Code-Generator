from QR_Code_Generator import GenerateQR as qr
from Data import constants as const
from PIL import Image, ImageTk
from sys import exit as exit_program
import tkinter
import customtkinter
import turtle as trt
import numpy as np

#region Setup for Turtle
# t = trt.Turtle()
# wn = trt.Screen()
# wn.tracer(0)
# t.screen.screensize(1920,1080)
# t.screen.setup(width = 1.0, height = 1.0)
# t.screen.bgcolor("Black")
# t.color("White")
# t.speed(0)
# t.hideturtle()
#endregion

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class GUI:
    def __init__(self,max_size: int):
        self.max_size_list = list(range(max_size))
        for ver in range(len(self.max_size_list)):
            self.max_size_list[ver] = str(ver+1)

        # App Frame
        self.app = customtkinter.CTk()
        self.app.geometry("720x480")
        self.app.title("QR Code Generator")

        #Adding UI Elements
        self.title = customtkinter.CTkLabel(self.app, text="Input Box")
        self.title.pack(padx=10,pady=10)
        self.QR_text = tkinter.StringVar()
        self.text_box = customtkinter.CTkEntry(self.app, width=350, height=40, textvariable=self.QR_text)
        self.text_box.pack()
        self.generate_button = customtkinter.CTkButton(self.app, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_button.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.ecc_options = customtkinter.CTkOptionMenu(self.app, values=["L","M","Q","H"])
        self.min_size_options = customtkinter.CTkOptionMenu(self.app, values=self.max_size_list)
        self.force_mask_options = customtkinter.CTkOptionMenu(self.app, values=["Auto", "1", "2", "3", "4", "5", "6", "7", "8"])
        self.my_label = customtkinter.CTkLabel(self.app, text="")
        self.my_label.pack(pady=20)

        self.my_label.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        self.ecc_options.place(relx=0.9, rely=0.2, anchor=tkinter.CENTER)
        self.min_size_options.place(relx=0.9, rely=0.4, anchor=tkinter.CENTER)
        self.force_mask_options.place(relx=0.9, rely=0.6, anchor=tkinter.CENTER)
        self.text_box.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        self.title.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        # Run App
        self.app.mainloop()

    def generate_qr_code(self):
        self.generate_button._state = customtkinter.DISABLED
        match self.ecc_options.get():
            case "L":
                ecc = const.ecc_level.L
            case "M":
                ecc = const.ecc_level.M
            case "Q":
                ecc = const.ecc_level.Q
            case "H":
                ecc = const.ecc_level.H
            case _:
                print("That error correction capacity does not exist")
                exit_program()
        match self.force_mask_options.get():
            case "Auto":
                force_mask = None
            case "1":
                force_mask = const.mask_level.VER_0
            case "2":
                force_mask = const.mask_level.VER_1
            case "3":
                force_mask = const.mask_level.VER_2
            case "4":
                force_mask = const.mask_level.VER_3
            case "5":
                force_mask = const.mask_level.VER_4
            case "6":
                force_mask = const.mask_level.VER_5
            case "7":
                force_mask = const.mask_level.VER_6
            case "8":
                force_mask = const.mask_level.VER_7
            case _:
                print("That mask level does not exist")
                exit_program()
        self.qr = qr.QR_Code(data=self.text_box.get(), ecc=ecc, force_mask=force_mask, min_ver=int(self.min_size_options.get()))
        self.qr.create_image(file_type=".png",pixel_size=400)
        img = Image.open("qr_code.png")
        img = ImageTk.PhotoImage(img)
        self.my_label.configure(image=img)
        self.generate_button._state = customtkinter.NORMAL



# class turtle_qr():
#     def __init__(self, size):
#         self.turtle = trt.Turtle()
#         self.turtle.screen.screensize(1920,1080)
#         self.turtle.screen.setup(width = 1.0, height = 1.0)
#         self.turtle.screen.bgcolor("White")
#         self.turtle.color("Black")
#         self.turtle.speed(0)
#         self.turtle.hideturtle()
#         self.turtle.penup()
#         self.size = size

#     def draw_square(self, pos):
#         self.turtle.penup()
#         self.turtle.goto(pos[0], pos[1])
#         self.turtle.pendown()
#         self.turtle.begin_fill()
#         self.turtle.goto(pos[0], pos[1]+self.size)
#         self.turtle.goto(pos[0]+self.size, pos[1]+self.size)
#         self.turtle.goto(pos[0]+self.size, pos[1])
#         self.turtle.goto(pos[0], pos[1])
#         self.turtle.end_fill()
#         self.turtle.penup()

#     def draw_qr(self, qr: np.array):

#         for y in range(len(qr)):
#             for x in range(len(qr[y])):
#                 if qr[y][x] == "1":
#                     self.draw_square(pos=[x*self.size,-y*self.size])
#                 elif qr[y][x] == True:
#                     self.draw_square(pos=[x*self.size,-y*self.size])
#         wn.update()
#         wn.mainloop()
