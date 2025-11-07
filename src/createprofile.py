import customtkinter as tk
from css.stylesheet import *
from PIL import ImageTk, Image
import shutil
import json

from pages.questionnaire import ask_questions

from tkinter import filedialog

import csv

def enter_info(screen, username):
    clear(screen)

    s = tk.CTkFrame(screen, fg_color = "transparent")

    s.grid_rowconfigure(0, weight=0)
    s.grid_rowconfigure(1, weight=1)
    s.grid_rowconfigure(2, weight=1)
    s.grid_columnconfigure(0, weight=1)
    s.grid_columnconfigure(1, weight=1)
    s.grid_columnconfigure(2, weight=1)
    s.grid_columnconfigure(3, weight=1)
    s.grid_columnconfigure(4, weight=1)
    s.grid_columnconfigure(5, weight=1)

    userinfo_frame = tk.CTkFrame(s, fg_color="transparent")
    userinfo_frame.grid(row=1, column=1, padx=10, pady=(0, 5))
    userinfo_frame.grid_columnconfigure(0, weight=1)

    logo = tk.CTkLabel(userinfo_frame, image = tk.CTkImage(dark_image = Image.open("assets/logo.png"), size = (300, 150)), text = "", pady = 0)
    logo.grid(row=0, column=0)

    #chatgpt function
    def alternate_names(csv_file_path):
        combined_list = ["Name"]
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                girl = row['Girl Name'].strip()
                boy = row['Boy Name'].strip()
                combined_list.extend([girl, boy])  # Alternate: Girl, Boy
        return combined_list

    name_frame = tk.CTkFrame(userinfo_frame, fg_color = "transparent")
    name_frame.grid(row=1, column=0, pady=5)

    namebox = tk.CTkOptionMenu(master = name_frame, values = alternate_names("data/babynames.csv"), width = 150, height = 50)
    namebox.pack(side = "left")

    lastnamebox = tk.CTkOptionMenu(master = name_frame, values = open("data/lastnames.txt").read().split(",\n"), width = 150, height = 50)
    lastnamebox.pack(side = "left")

    namebox.set("Name")
    lastnamebox.set("Last Name")

    genderframe = tk.CTkFrame(master = userinfo_frame, fg_color = "transparent")
    genderlabel = Text(master = genderframe, text = "What gender are you?")

    malebox = tk.CTkCheckBox(master = genderframe, onvalue = 1, offvalue = 0, text = "Male")
    femalebox = tk.CTkCheckBox(master = genderframe, onvalue = 1, offvalue = 0, text = "Female")
    malebox.toggle()
    femalebox.toggle()

    genderlabel.pack()
    malebox.pack(side = "left")
    femalebox.pack(side = "left")

    genderframe.grid(row=2, column = 0, pady = 5)

    phonenumberframe = tk.CTkFrame(master = userinfo_frame, corner_radius = 0)
    phonenumberlabel = Text(master = phonenumberframe, text = "Select your phone number below")

    def update_phone(number):
        phonenumberlabel.configure(text = f"{number:.0f}")

    phonenumberslider = Slider(master = phonenumberframe, from_ = 1000000000, to = 10000000000, command = update_phone, width = 300)

    phonenumberlabel.pack()
    phonenumberslider.pack()

    buttonframe = tk.CTkFrame(master = phonenumberframe, fg_color = "transparent")

    def shiftslider(amount):
        phonenumberslider.set(phonenumberslider.get() + amount)
        update_phone(phonenumberslider.get())

    minus1 = Button(master = buttonframe, text = "-1", command = lambda: shiftslider(-1), width = 50)
    minus10 = Button(master = buttonframe, text = "-10", command = lambda: shiftslider(-10), width = 50)
    minus100 = Button(master = buttonframe, text = "-100", command = lambda: shiftslider(-100), width = 50)
    plus100 = Button(master = buttonframe, text = "+100", command = lambda: shiftslider(100), width = 50)
    plus10 = Button(master = buttonframe, text = "+10", command = lambda: shiftslider(10), width = 50)
    plus1 = Button(master = buttonframe, text = "+1", command = lambda: shiftslider(1), width = 50)
    minus1.pack(side = "left")
    minus10.pack(side = "left")
    minus100.pack(side = "left")
    plus100.pack(side = "left")
    plus10.pack(side = "left")
    plus1.pack(side = "left")

    buttonframe.pack()

    phonenumberframe.grid(row=3, column=0, pady=5)

    pf_frame = tk.CTkFrame(master = s, fg_color = "transparent")

    #im getting really lazy
    spacer = tk.CTkFrame(pf_frame, width = 0, height = 50, fg_color = "transparent")
    spacer.pack()

    pf_label = Text(master = pf_frame, text = "Your Profile Picture")
    pf_label.pack()

    pf_image = LoadedImage(master = pf_frame, image = "data/default.png", size = (200, 200))
    pf_image.pack()

    spacer = tk.CTkFrame(pf_frame, width = 0, height = 10, fg_color = "transparent")
    spacer.pack()

    def change_pf_image():
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")]
        )
        if file_path:
            pf_image.change_image(file_path)

    # Button to open file dialog and update image
    pf_button = Button(master=pf_frame, text="Change Image", command=change_pf_image, corner_radius = 0)
    pf_button.pack(fill = "both", expand = True)

    biobox = TextBox(master=pf_frame, height = 100, placeholder_text = "A short bio about yourself...")
    biobox.pack(fill = "both", expand = True, pady = 5)

    def get_info():
        shutil.copy2(pf_image.imagepath, f"data/pf_images/{username}.{pf_image.imagepath.split(".")[-1]}")

        user_data = {
            "name": namebox.get(),
            "last_name": lastnamebox.get(),
            "bio": biobox.get("0.0", "end"),
            "gender": [malebox.get(), femalebox.get()],
            "phone_number": int(phonenumberslider.get()),
            "image": f"{username}.{pf_image.imagepath.split(".")[-1]}",
            "settings": {
                "dark_mode": True
            }
        }

        data = json.load(open("data/users.json"))
        data[username]["data"] = user_data
        json.dump(data, open("data/users.json", "w"))

        ask_questions(s, username)

    submitbutton = Button(master = pf_frame, text = "Take our quiz", command = get_info, width = 200, corner_radius = 0)
    submitbutton.pack()

    pf_frame.grid(row = 1, column = 3)

    s.place(relx=0, rely=0, relwidth=1, relheight=1)
