import tkinter as tk
from tkinter import messagebox
from DirectorySelect import DirectorySelect as ds
import cv2
from Rotation import Rotation



def return_labeled_data():
    clear_widgets()

    global save_button, save_label, process_button, result_label
    save_path = ""
    all_label_dir = {}

    def getAllLabel():
        nonlocal all_label_dir
        direct_select = ds()
        all_label_dir = direct_select.select_directory()

    def select_save_path():
        nonlocal save_path
        direct_select = ds()
        save_path = direct_select.select_save_directory()

    def start_process():
        if not all_label_dir:
            result_label.config(text="Error: No directory selected.")
            messagebox.showerror("Error", "No directory selected.")
            return
        if not save_path:
            result_label.config(text="Error: No save path selected.")
            messagebox.showerror("Error", "No save path selected.")
            return

        # Seçilen dizinler üzerinden işleme başla
        for image_path, txt_path in all_label_dir.items():
            Rotation(image_path, txt_path).process_image(rotate_label=True, save_path=save_path,remove_black=True,add_sharpened=True)
        result_label.config(text="Process completed successfully!")

    save_button = tk.Button(window, text="Select Save Path", command=select_save_path)
    save_button.pack(pady=10)

    save_label = tk.Label(window, text="No Save Path selected.")
    save_label.pack(pady=10)

    # Dizin seçme butonunu ekle
    directory_button = tk.Button(window, text="Select Directory for Labeled Data", command=getAllLabel)
    directory_button.pack(pady=10)

    result_label = tk.Label(window, text="")
    result_label.pack(pady=10)

    # İşleme başla butonunu ekle
    process_button = tk.Button(window, text="Start Process", command=start_process)
    process_button.pack(pady=20)





def add_noise_to_batch():
    clear_widgets()

    def onclick():
        print("Batch noise addition logic")

    # Batch noise butonunu ekle
    process_button = tk.Button(window, text="Add Noise to Batch", command=onclick)
    process_button.pack(pady=20)






def add_noise_to_single_image():
    clear_widgets()

    def onclick():
        print("Single image noise addition logic")

    # Single image noise butonunu ekle
    process_button = tk.Button(window, text="Add Noise to Single Image", command=onclick)
    process_button.pack(pady=20)




def clear_widgets():
    for widget in window.winfo_children():
        widget.pack_forget()






def main_screen():
    global window, result_label
    window = tk.Tk()
    window.title("Image Processing Application")
    window.geometry("600x400")  # Set window size

    # Create a menu bar
    menu_bar = tk.Menu(window)

    operation_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Operations", menu=operation_menu)

    # Add menu items
    operation_menu.add_command(label="Return Labeled Data", command=return_labeled_data)
    operation_menu.add_command(label="Add Noise to Batch", command=add_noise_to_batch)
    operation_menu.add_command(label="Add Noise to Single Image", command=add_noise_to_single_image)

    window.config(menu=menu_bar)

    # Result mesajı için global bir label oluştur
    result_label = tk.Label(window, text="Please select an operation.")
    result_label.pack(pady=10)

    window.mainloop()

main_screen()
