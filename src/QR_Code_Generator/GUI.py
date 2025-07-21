import tkinter
import customtkinter

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App Frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("QR Code Generator")

#Adding UI Elements

title = customtkinter.CTkLabel(app, text="Insert QR Code Text")
title.pack(padx=10,pady=10)

QR_text = tkinter.StringVar()
text_box = customtkinter.CTkEntry(app, width=350, height=40, textvariable=QR_text)
text_box.pack()

# generate_button = customtkinter.CTkButton(app, text="Generate QR Code", command=generate_QR_code)

# Run App
app.mainloop()