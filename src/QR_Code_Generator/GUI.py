import tkinter
import customtkinter
import turtle as trt
import numpy as np

#region Setup for Turtle
t = trt.Turtle()
t.screen.screensize(1920,1080)
t.screen.setup(width = 1.0, height = 1.0)
t.screen.bgcolor("Black")
t.color("White")
t.speed(0)
t.hideturtle()
#endregion


# System Settings
# customtkinter.set_appearance_mode("System")
# customtkinter.set_default_color_theme("blue")

# App Frame
# app = customtkinter.CTk()
# app.geometry("720x480")
# app.title("QR Code Generator")

#Adding UI Elements

# title = customtkinter.CTkLabel(app, text="Insert QR Code Text")
# title.pack(padx=10,pady=10)

# QR_text = tkinter.StringVar()
# text_box = customtkinter.CTkEntry(app, width=350, height=40, textvariable=QR_text)
# text_box.pack()

# generate_button = customtkinter.CTkButton(app, text="Generate QR Code", command=generate_QR_code)

# Run App
# app.mainloop()

class turtle_qr():
    def __init__(self, size):
        self.turtle = trt.Turtle()
        self.turtle.screen.screensize(1920,1080)
        self.turtle.screen.setup(width = 1.0, height = 1.0)
        self.turtle.screen.bgcolor("White")
        self.turtle.color("Black")
        self.turtle.speed(0)
        self.turtle.hideturtle()
        self.turtle.penup()
        self.size = size

    def draw_square(self, pos):
        self.turtle.penup()
        self.turtle.goto(pos[0], pos[1])
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.goto(pos[0], pos[1]+self.size)
        self.turtle.goto(pos[0]+self.size, pos[1]+self.size)
        self.turtle.goto(pos[0]+self.size, pos[1])
        self.turtle.goto(pos[0], pos[1])
        self.turtle.end_fill()
        self.turtle.penup()

    def draw_qr(self, qr: np.array):
        for y in range(len(qr)):
            for x in range(len(qr[y])):
                if qr[y][x] == "1":
                    self.draw_square(pos=[x*self.size,-y*self.size])
                elif qr[y][x] == True:
                    self.draw_square(pos=[x*self.size,-y*self.size])