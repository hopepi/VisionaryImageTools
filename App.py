import tkinter as tk
from tkinter import messagebox
from DirectorySelect import DirectorySelect as ds
import cv2
from Rotation import Rotation
from ImageNoiseProcessor import ImageNoiseProcessor



def return_labeled_data():
    clear_widgets()

    global save_button, save_label, process_button, result_label
    save_path = ""
    all_label_dir = {}

    def get_all_label():
        nonlocal all_label_dir
        direct_select = ds()
        all_label_dir = direct_select.select_directory()

        if all_label_dir:
            first_item = list(all_label_dir.keys())[0]
            cleaned_item = first_item.split('\\')[0].strip()
            result_label.config(text=f"Selected Label Path: {cleaned_item} --> Tagged images count: {len(all_label_dir)}")
        else:
            result_label.config(text=f"Not found tagged image")

    def select_save_path():
        nonlocal save_path
        direct_select = ds()
        save_path = direct_select.select_save_directory()

        if save_path:
            save_label.config(text=f"Save Path: {save_path}")

    def start_process():
        if not all_label_dir:
            result_label.config(text="Error: No directory selected.")
            messagebox.showerror("Error", "No directory selected.")
            return
        if not save_path:
            save_label.config(text="Error: No save path selected.")
            messagebox.showerror("Error", "No save path selected.")
            return


        # Seçilen dizinler üzerinden işleme başla
        for image_path, txt_path in all_label_dir.items():
            Rotation(image_path, txt_path).process_image(rotate_label=True, save_path=save_path,remove_black=True,add_sharpened=True)
        messagebox.showinfo(title="Process Completed", message="Process completed successfully!")


    save_button = tk.Button(window, text="Select Save Path", command=select_save_path)
    save_button.pack(pady=10)

    save_label = tk.Label(window, text="")
    save_label.pack(pady=10)

    # Dizin seçme butonunu ekle
    directory_button = tk.Button(window, text="Select Directory for Labeled Data", command=get_all_label)
    directory_button.pack(pady=10)

    result_label = tk.Label(window, text="")
    result_label.pack(pady=10)

    # İşleme başla butonunu ekle
    process_button = tk.Button(window, text="Start Process", command=start_process)
    process_button.pack(pady=20)





def add_noise_to_batch():
    clear_widgets()

    noise_value = 0
    save_path = ""
    all_label_dir = {}
    checkbox_states = {
        "Poisson Noisy": False,
        "Salt And Pepper Noisy": False,
        "Gaussian Noise": False,
        "Random Pixel Noise": False,
        "Multiplicative Noise": False,
        "Brightness Contrast Random": False,
        "Random Contrast": False,
        "Color Distortion": False,
        "Add Blur": False
    }#Eleman eklicen zaman dikkat et ImageNoiseProcessorda güncelleme yapman lazım

    def update_noise_value(value):
        nonlocal noise_value
        noise_value = int(value)


    def click_progress():
        selected_count = 0
        selected_noisy=[]
        print(noise_value)
        for selected in checkbox_states.values():
            if selected:
                selected_count += 1

        if selected_count == 0:  # Hiçbir öğe seçili değilse
            messagebox.showerror("Error", "No selected options found")
            return
        if len(all_label_dir) == 0:
            messagebox.showerror("Error", "Please selected tagged image path")
            return
        if save_path == "":
            messagebox.showerror("Error", "Please selected save path")
            return
        for item, selected in checkbox_states.items():
            if selected:
                selected_noisy.append(item)
        image_noise_processor = ImageNoiseProcessor(save_path=save_path)
        image_noise_processor.add_random_noisy_label_images(all_image_tagged_map=all_label_dir,noisy_weight=noise_value,noisy_list=selected_noisy)



    def select_save_path():
        nonlocal save_path
        direct_select = ds()
        save_path = direct_select.select_save_directory()
        if save_path:
            save_label.config(text=f"Save Path: {save_path}")



    def select_tagged_images_directory():
        nonlocal all_label_dir
        direct_select = ds()
        all_label_dir = direct_select.select_directory()

        if all_label_dir:
            first_item = list(all_label_dir.keys())[0]
            print(first_item)
            cleaned_item = first_item.split('\\')[0].strip()
            directory_select_label.config(
                text=f"Selected Label Path: {cleaned_item} --> Tagged images count: {len(all_label_dir)}")
        else:
            directory_select_label.config(text=f"Not found tagged image")


    save_button = tk.Button(window, text="Select Save Path", command=select_save_path)
    save_button.pack(pady=10)

    save_label = tk.Label(window, text="")
    save_label.pack(pady=10)

    directory_select = tk.Button(window,text="Select tagged images directory",command=select_tagged_images_directory)
    directory_select.pack(pady=10)

    directory_select_label = tk.Label(window, text="")
    directory_select_label.pack(pady=10)

    checkbox_frame = tk.Frame(window)
    checkbox_frame.pack(pady=10)

    index = 0

    for item_name in checkbox_states.keys():
        var = tk.BooleanVar(value=checkbox_states[item_name])

        def update_state(item_name=item_name, var=var):
            checkbox_states[item_name] = var.get()

        checkbox = tk.Checkbutton(checkbox_frame, text=item_name, variable=var, command=update_state)
        checkbox.grid(row=index // 5, column=index % 5, padx=5, pady=5, sticky='w')

        index += 1


    label = tk.Label(window, text="--> !Recommendation: between 10% and 30%! <--")
    label.pack(pady=5)
    noise_scale = tk.Scale(window, from_=0, to=100, orient='horizontal',label="Noise Amount %",command=update_noise_value)
    noise_scale.pack(pady=5)


    process_button = tk.Button(window, text="Add Noise to Batch", command=click_progress)
    process_button.pack(pady=20)




def add_noise_to_single_image():
    clear_widgets()

    def onclick():
        print("Single image noise addition logic")

    process_button = tk.Button(window, text="Add Noise to Single Image", command=onclick)
    process_button.pack(pady=20)




def clear_widgets():
    for widget in window.winfo_children():
        widget.pack_forget()






def main_screen():
    global window, result_label
    window = tk.Tk()
    window.title("Image Processing Application")
    window.geometry("800x600")

    menu_bar = tk.Menu(window)

    operation_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Operations", menu=operation_menu)


    operation_menu.add_command(label="Return Labeled Data", command=return_labeled_data)
    operation_menu.add_command(label="Add Noise to Batch", command=add_noise_to_batch)
    operation_menu.add_command(label="Add Noise to Single Image", command=add_noise_to_single_image)

    window.config(menu=menu_bar)

    # Result mesajı için global bir label
    result_label = tk.Label(window, text="Please select an operation.")
    result_label.pack(pady=10)

    window.mainloop()

main_screen()
