import tkinter as tk
from DirectorySelect import DirectorySelect as ds
import cv2

def return_labeled_data():
    def onclick():
        """
        test
        """
        direct_select = ds()
        all_label_dir = direct_select.select_directory()


    result_label.config(text="Return Labeled Data option selected.")
    choose_button.config(text="Return Labeled Data option selected.",command=onclick)
    choose_button.pack(pady = 20)


def add_noise_to_batch():
    def onclick():
        print("test")
    result_label.config(text="Add Noise to Batch option selected.")
    choose_button.config(text="Add Noise to Batch option selected.",command=onclick)
    choose_button.pack(pady=20)

def add_noise_to_single_image():
    def onclick():
        print("test")
    result_label.config(text="Add Noise to Single Image option selected.")
    choose_button.config(text="Add Noise to Single Image option selected.",command=onclick)
    choose_button.pack(pady=20)

def main_screen():
    global window
    window = tk.Tk()
    window.title("Image Processing Application")
    window.geometry("600x400")  # Set window size

    # Create a menu bar
    menu_bar = tk.Menu(window)

    # Create an "Operations" menu
    operation_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Operations", menu=operation_menu)

    # Add menu items
    operation_menu.add_command(label="Return Labeled Data", command=return_labeled_data)
    operation_menu.add_command(label="Add Noise to Batch", command=add_noise_to_batch)
    operation_menu.add_command(label="Add Noise to Single Image", command=add_noise_to_single_image)

    # Add the menu to the window
    window.config(menu=menu_bar)

    # Add a label to show selected operations
    global result_label
    result_label = tk.Label(window, text="Please select an operation.")
    result_label.pack(pady=20)

    global choose_button
    choose_button = tk.Button(window, text="Test")

    window.mainloop()

main_screen()