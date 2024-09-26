import tkinter as tk
from tkinter import filedialog
import os


class DirectorySelect:
    def __init__(self):
        pass

    def select_directory(self):
        root = tk.Tk()
        root.withdraw()

        directory = filedialog.askdirectory(title="Etiketli resimlerin bulunduğu dosyaları seçiniz Seçin")

        if directory:  # Eğer bir dizin seçildiyse
            images = {}
            labels = {}

            # Dizin içindeki dosyaları kontrol et
            for filename in os.listdir(directory):
                name, ext = os.path.splitext(filename)

                if ext.endswith('.png') or ext.endswith('.jpg') or ext.endswith('.jpeg'):
                    images[name] = os.path.join(directory, filename)  # Resim dosyalarını ekle
                elif ext.endswith('.txt'):
                    labels[name] = os.path.join(directory, filename)  # Txt dosyalarını ekle

            mappings = {}
            for img_name, img_path in images.items():
                if img_name in labels:  # Eğer aynı isme sahip bir txt dosyası varsa
                        mappings[img_path] = labels[img_name]

            print("Eşleşmeler:")
            for img, lbl in mappings.items():
                print(f"{img} --> {lbl}")

            return mappings



    def select_save_directory(self):
        root = tk.Tk()
        root.withdraw()

        directory = filedialog.askdirectory(title="Dizin Seçin")

        return directory



    def select_image_list(self):
        root = tk.Tk()
        root.withdraw()

        directory = filedialog.askdirectory(title="Lütfen resimlerin olduğu dizini seçiniz")

        if directory:
            images_list = []

            for filename in os.listdir(directory):
                if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    images_list.append(filename)

            return images_list



    def select_image(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Lütfen resmi seçiniz",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            return file_path
        else:
            print("Herhangi bir değer seçilmedi")

"""
test = DirectorySelect()
print(test.select_directory())
print(test.select_image_list())
print(test.select_image())
"""