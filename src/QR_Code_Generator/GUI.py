from QR_Code_Generator import GenerateQR as qr
from Data import constants as const
from PIL import Image, ImageTk
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
    def __init__(self):
        self.qr = None

        # App Frame
        self.app = customtkinter.CTk()
        self.app.geometry("720x480")
        self.app.title("QR Code Generator")

        #Adding UI Elements
        self.title = customtkinter.CTkLabel(self.app, text="Input Box")
        self.title.pack(padx=10,pady=10)
        self.title.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        self.QR_text = tkinter.StringVar()
        self.text_box = customtkinter.CTkEntry(self.app, width=350, height=40, textvariable=self.QR_text)
        self.text_box.pack()
        self.text_box.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        generate_button = customtkinter.CTkButton(self.app, text="Generate QR Code", command=self.generate_qr_code)
        generate_button.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.my_label = None

        # Run App
        self.app.mainloop()

    def generate_qr_code(self):
        if self.my_label != None:
            self.my_label.destroy()
            self.my_label = None
        self.qr = qr.QR_Code(ecc=const.ecc_level.L, data_mode=const.data_mode.BYTE, data=self.text_box.get())
        self.qr.create_image(file_type=".png",pixel_size=400)
        img = Image.open("qr_code.png")
        img = ImageTk.PhotoImage(img)
        self.my_label = customtkinter.CTkLabel(self.app, image=img, text="")
        self.my_label.pack(pady=20)
        self.my_label.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)



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
