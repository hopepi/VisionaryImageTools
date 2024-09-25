"""
MASAÜSTÜNDEKİ DOSYALARA KAYDETMEZ
PROJE TEST YAPIM AŞAMASINDADIR
"""

import cv2
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
from AdvancedImage import sharpen_image, remove_black_background, resize_image


def rotate_image(image, angle):
    (height, width) = image.shape[:2]
    center = (width // 2, height // 2)
    transform_matrix = cv2.getRotationMatrix2D(center, angle, 0.71)
    rotated = cv2.warpAffine(image, transform_matrix, (width, height))
    return rotated

def process_image(image, remove_black=False, add_sharpened=False, save_path=''):
    if add_sharpened:
        image = sharpen_image(image)

    # Eğer save_path boşsa mevcut dizini kullan
    if save_path== "":
        save_path = '.'  #Mevcut dizin

    # Kaydetme dizinini oluştur varsa yoksa
    os.makedirs(save_path, exist_ok=True)
    print(f"Directory created or already exists: {save_path}")

    # Belirli açı aralıklarında döndürme ve opsiyonel olarak arka planı kaldırma işlemi
    for angle in range(0, 360, 30):
        rotated_image = rotate_image(image, angle)
        result_image = remove_black_background(rotated_image) if remove_black else rotated_image

        output_file_path = os.path.join(save_path, f'rotated_image_{angle}.png')
        success = cv2.imwrite(output_file_path, result_image)

        if success:
            print(f"Image saved successfully: {output_file_path}")
        else:
            print(f"Error saving image: {output_file_path}")


Tk().withdraw()
save_path = askdirectory(title="Kayıt Yeri Seçin")  # Kullanıcıdan kayıt yeri seçmesini iste

#test
image = cv2.imread("resim4.jpeg")

if image is None:
    print("Image not found")
else:
    process_image(image, remove_black=True, add_sharpened=True, save_path=save_path)
