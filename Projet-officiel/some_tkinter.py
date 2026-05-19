
"""
Tkinter stuff for popups and saving files
by Albert S

From top to bottom you may see a whole adventure of me discovering different method of yielding results while handling
tkinter widows at the same time
"""


import tkinter as tk
from tkinter import messagebox, Frame
from tkinter import ttk

from collections.abc import Callable

import savedata as sd
import os

#adrien things
import Carte
import matrix_manager as mm

import Convertisseur as cnv


#a simple reinitalization window
def reinit(exe: Callable):
    print("reinitialize")
    ttl = "WARNING: USE YOUR BRAIN AND READ THIS"
    msg = """You're either about to do something stupid or willingfully reinitialize your masterpiece. Are you sure you want to proceed?"""
    response = messagebox.askyesno(ttl, msg, icon="warning")
    if response:
        exe()
        print("reinit successful")
    else:
        print("reinit aborted")



TEXT_DESC = "Congrats on your brand new project! You can copy the data of your map with the following button:"

"""
Feat. Gemini AI, I'm sorry Adrian but I had to be efficient
That being said, that wasn't vibe code, just that I copied the snippets of code like a blueprint of a button to keep a
consistent design of windows
"""
def copy_win(copy_text: bytes, dim: tuple[int, int]):

    #if text too long to be on the screen
    show_text = str(copy_text)
    if len(show_text) > 50:
        show_text = show_text[:49] + "[...]"

    root = tk.Tk()
    root.title("Main Application")
    root.geometry("700x500")
    root.withdraw()

    #second popup window, in case I had an idea to add something before
    popup = tk.Toplevel(root)
    popup.title("Saving Project")

    #so to make the popup appear centered relative to the main window
    popup.geometry("500x500")

    def on_popup_close():
        # Destroying root will close the popup and exit the entire application
        root.destroy()
    popup.protocol("WM_DELETE_WINDOW", on_popup_close)

    #labels with copy text and description
    label = tk.Label(popup, text=TEXT_DESC, font=("Arial", 10), wraplength=300)
    label.pack(pady=(30, 5))

    border_frame = tk.Frame(popup, bg="black")
    border_frame.pack(pady=20)

    tbc = tk.Label(border_frame, text=show_text, font=("Arial", 11), width=40,)
    tbc.pack(padx=2, pady=2)

    label2 = tk.Label(popup, text="Your artwork's name:", font=("Arial", 10), wraplength=300)
    label2.pack(pady=(30, 5))

    writing = tk.Entry(popup, font=("Arial", 11))
    writing.pack(padx=30)

    def copy_action():
        text_to_copy = label["text"]
        root.clipboard_clear()
        root.clipboard_append(str(copy_text))

        #UI feedback
        copy_button.config(text="Copied!", bg="#4CAF50", fg="white", state="disabled")

    #function to save the said file inside a folder to read it later
    def save_file_action():
        main = "Projet-officiel"
        save_path = "Save_files"

        full_save_path = os.path.join(main, save_path)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        file_name = writing.get()
        file_path = os.path.join(save_path, file_name)

        #button color change
        def ui_feedback(mode: int = 0):
            if mode == 0:
                save_file_button.config(text=f"File not saved...", bg="#4CAF50", fg="white", state="normal")
            else:
                save_file_button.config(text=f"Saved {file_name}!", bg="#4CAF50", fg="white", state="disabled")

        def write_file():
            respp = messagebox.askyesno("SAVING", "You sure you wanna save your file?")
            if respp:
                sd.write_file(file_path, copy_text, dim)
                ui_feedback(1)
            else:
                ui_feedback(0)

        if os.path.exists(file_path):
            resp = messagebox.askyesno("WARNING: OVERWRITING SAVE",
                                       f'{file_name} already exists, do you want to overwrite it?',
                                       icon="warning")
            if resp:
                write_file()
            else:
                ui_feedback(0)
        else:
            write_file()

    buttons_frame = tk.Frame(popup)
    buttons_frame.pack(pady=10)

    #copy button
    copy_button = tk.Button(
        buttons_frame,
        text="Copy to Clipboard",
        command=copy_action,
        bg="#0078D4",
        fg="white",
        padx=10,
        pady=5
    )
    copy_button.grid(row=0, column=0)

    #file create button
    save_file_button = tk.Button(
        buttons_frame,
        text="Save as file!",
        command=save_file_action,
        bg="#0078D4",
        fg="white",
        padx=10,
        pady=5
    )
    save_file_button.grid(row=0, column=1)

    tk.mainloop()


def import_project(getter: list):
    """getter needed as something to 'send' the result while bypassing the mess of tkinter windows closing"""

    root = tk.Tk()
    root.title("Main Application")
    root.geometry("700x500")
    root.withdraw()

    popup = tk.Toplevel(root)
    popup.title("Importing Project")

    popup.geometry("500x200")

    def on_popup_close():
        #destroying popup closes the root and exits the application
        root.destroy()
    popup.protocol("WM_DELETE_WINDOW", on_popup_close)

    label = tk.Label(popup, text="Select the project to import:", font=("Arial", 10), wraplength=300)
    label.pack(pady=(30, 5))

    #list all saves in the directory + their paths
    def get_save_files() -> dict:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_directory, "Save_files")
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        save_files: dict = {}
        for filename in os.listdir(save_path):
            full_path = os.path.join(save_path, filename)
            if os.path.isfile(full_path) and sd.istype(full_path):
                save_files[filename] = full_path
        if not len(save_files) == 0:
            return save_files
        else:
            return {}

    saves = get_save_files() # ["file1", "file2", "file3"]
    choices = [i for i in saves.keys()]

    #the dropdown
    dropdown = ttk.Combobox(popup, values=choices, state="readonly", font=("Arial", 10))
    dropdown.pack(padx=15, pady=15)
    dropdown.set("Your save...")

    def import_action():
        select = dropdown.get()
        if select == "Your save...":
            import_button.config(text=f"Select something please", bg="red", fg="white", state="normal")
        else:
            path = saves[select]
            file, dim = sd.read_file(path)
            getter.append(file)
            getter.append(dim)
            popup.destroy()
            root.destroy()

    import_button = tk.Button(
        popup,
        text="Import!",
        command=import_action,
        bg="#0078D4",
        fg="white",
        padx=10,
        pady=5
    )
    import_button.pack()

    root.mainloop()


#pen settings tk interface
def drawing_settings():
    chosen_tile = ["#000000"]
    drawing_size = [1]

    root = tk.Tk()
    root.title("Main Application")
    root.geometry("400x500")

    color_label = tk.Label(root, text="Choose a tile to draw:")
    color_label.pack(pady=10)

    choices_frame = tk.Frame(root)
    choices_frame.pack(pady=10)

    def on_select():
        #grab the value of the currently selected option
        selected_value = selection_var.get()
        chosen_tile[0] = data_on_select[selected_value]

    selection_var = tk.StringVar(value="Blue Theme")

    blue = "#{:02x}{:02x}{:02x}".format(*(70, 130, 180))
    yellow = "#{:02x}{:02x}{:02x}".format(*(237, 201, 175))
    green = "#{:02x}{:02x}{:02x}".format(*(34, 139, 34))

    options = [
        ("Water", blue),
        ("Ground", green),
        ("Coast", yellow),
        ("Nothing (eraser)", "#000000"),
    ]

    data_on_select: dict = {}

    #create unique choice buttons
    for text, color in options:
        data_on_select[text] = color
        row = tk.Frame(choices_frame)
        row.pack(fill="x", padx=30, pady=5)


        rb = tk.Radiobutton(
            row,
            text=text,
            variable=selection_var,
            value=text,
            command=on_select,
            font=("Arial", 11)
        )
        rb.pack(side="left")

        tk.Frame(row, width=15).pack(side="left")

        color_square = tk.Frame(row, bg=color, width=16, height=16, bd=1, relief="solid")
        color_square.pack_propagate(False)  #prevent the square from collapsing
        color_square.pack(side="left")

    size_label = tk.Label(root, text="Set the size of the pen:")
    size_label.pack(pady=10)

    def on_slide(value):
        drawing_size[0] = value

    slider = tk.Scale(
        root,
        from_=1,
        to=5,
        orient="horizontal",
        command=on_slide,
        length=200
    )
    slider.pack(pady=0)

    def on_close():
        root.destroy()

    close_button = tk.Button(
        root,
        text="Save",
        command=on_close,
        bg="#0078D4",
        fg="white",
        padx=10,
        pady=5
    )
    close_button.pack(pady=5)

    root.mainloop()

    #returning ----------------------------

    hex_color = chosen_tile[0]
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    rgb_tuple = (r, g, b)

    final_draw_size = int(drawing_size[0])

    return rgb_tuple, final_draw_size


global map_data#will be returned later

def create_new_map() -> tuple[int, int, bytes]:

    root = tk.Tk()
    root.title("Generate new map")
    root.geometry("500x350")

    label = tk.Label(root, text="Select your settings to create a new map:", font=("Arial", 10), wraplength=300)
    label.pack(pady=(30, 5))

    dimension_frame = tk.Frame(root)
    dimension_frame.pack(padx=10)

    dim_l_x = tk.Label(dimension_frame, text="XY dimension (square):", font=("Arial", 11), wraplength=300)

    #for entries, check if digit typed, if not then do not place character
    def validate_integer(action, value_if_allowed):
        if action == '1':
            if value_if_allowed.isdigit() or value_if_allowed == "":
                return True
            else:
                return False
        return True

    vcmd = (root.register(validate_integer), '%d', '%P')

    #dimensions
    dim_e_x = tk.Entry(dimension_frame, width=30, validate='key', validatecommand=vcmd)
    dim_e_x.insert(0, "100")
    dim_e_y = tk.Entry(dimension_frame, width=30, validate='key', validatecommand=vcmd)
    dim_e_y.insert(0, "100")

    dim_l_x.grid(row=0, column=0)
    dim_e_x.grid(row=0, column=1)

    #humidity
    wet_frame = Frame(root)
    wet_frame.pack(pady=10)

    wet_label = tk.Label(wet_frame, text="Humidity:  ", font=("Arial", 11), wraplength=300)

    wet_slider = tk.Scale(
        wet_frame,
        from_=1,
        to=10,
        orient="horizontal",
        command=None,
        length=200
    )

    wet_label.grid(row=0, column=0)
    wet_slider.grid(row=0, column=1)
    wet_slider.set(6)

    frame2 = Frame(root)
    frame2.pack(pady=10)

    #n rivers start points
    waterpval_label = tk.Label(frame2, text="Number of rivers:  ", font=("Arial", 11), wraplength=300)

    waterpval_slider = tk.Scale(
        frame2,
        from_=1,
        to=20,
        orient="horizontal",
        command=None,
        length=200
    )
    waterpval_slider.set(5)

    waterpval_label.grid(row=0, column=0)
    waterpval_slider.grid(row=0, column=1)

    frame3 = Frame(root)
    frame3.pack(pady=10)

    rw_label = tk.Label(frame3, text="Random walk values(?):  ", font=("Arial", 11), wraplength=300)

    rw_e1 = tk.Entry(frame3, width=10, validate='key', validatecommand=vcmd)
    rw_e1.insert(0, "20")
    rw_e2 = tk.Entry(frame3, width=10, validate='key', validatecommand=vcmd)
    rw_e2.insert(0, "3")

    rw_tiles: dict = {
        "Water": Carte.Water,
        "Ground": Carte.Ground,
        "Coast": Carte.Coast,
    }
    rw_tiles_choices = ["Water", "Ground", "Coast"]

    rw_tile_dropdown = ttk.Combobox(frame3, values=rw_tiles_choices, state="readonly", font=("Arial", 10), width=10)
    rw_tile_dropdown.set("Water")

    rw_label.grid(row=0, column=0)
    rw_e1.grid(row=0, column=1)
    rw_e2.grid(row=0, column=2)
    rw_tile_dropdown.grid(row=0, column=3)

    #in here is the summary of all my guesswork about what all the arguments in Adrien's masterpiece mean
    def on_close():
        global map_data
        mtx = mm.create_matrix((int(dim_e_x.get()), int(dim_e_x.get())),{"baba": 2})
        wpv = int(waterpval_slider.get())
        rw = [int(rw_e1.get()), int(rw_e2.get()), Carte.Water]
        hmdt = int(wet_slider.get())

        #matrix, river points, random walk list, humidity
        map_data = Carte.w_f_c_evolved(mtx, wpv, rw, hmdt) #some typing problems here...
        root.destroy()

    generate_button = tk.Button(
        root,
        text="Generate!",
        command=on_close,
        bg="#0078D4",
        fg="white",
        padx=10,
        pady=5
    )
    generate_button.pack(pady=20)

    root.mainloop()
    #after that is the returning part

    #this converts the gotten map into bytes that can be directly put into a SquareMap
    global map_data
    try:
        map_data_colors = []
        for y in map_data:
            cc = []
            for x in y:
                cc.append(x.Color)
            map_data_colors.append(cc)
        map_data_bytes = cnv.convertisseur_tryhard(map_data_colors)
        return len(map_data[0]), len(map_data), map_data_bytes
    except: #no idea what error it yields, sometimes it does that's for sure
        return 0, 0, b""

