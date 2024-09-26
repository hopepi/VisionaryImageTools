"""
MASAÜSTÜNDEKİ DOSYALARA KAYDETMEZ
PROJE TEST YAPIM AŞAMASINDADIR
"""

import cv2
import numpy as np
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
from AdvancedImage import AdvancedImage


class Rotation:
    def __init__(self, image):
        self.image = image  # self.image'ı doğrudan image ile ayarladık

    def rotate_image(self, angle):
        (height, width) = self.image.shape[:2]
        center = (width // 2, height // 2)
        transform_matrix = cv2.getRotationMatrix2D(center, angle, 0.71)
        rotated = cv2.warpAffine(self.image, transform_matrix, (width, height))
        return rotated

    def process_image(self, remove_black=False, add_sharpened=False, save_path=''):
        advanced_image = AdvancedImage(self.image)

        if add_sharpened:
            self.image = advanced_image.sharpen_image()

        # Eğer save_path boşsa mevcut dizini kullan
        if save_path == "":
            save_path = '.'  # Mevcut dizin

        # Kaydetme dizinini oluştur varsa yoksa
        os.makedirs(save_path, exist_ok=True)
        print(f"Directory created or already exists: {save_path}")

        # Belirli açı aralıklarında döndürme ve opsiyonel olarak arka planı kaldırma işlemi
        for angle in range(0, 360, 30):
            rotated_image = self.rotate_image(angle)  # Doğrudan angle'ı kullanıyoruz
            advanced_image_remove_back = AdvancedImage(rotated_image)
            result_image = advanced_image_remove_back.remove_black_background() if remove_black else rotated_image

            output_file_path = os.path.join(save_path, f'rotated_image_{angle}.png')
            success = cv2.imwrite(output_file_path, result_image)




test_image_path = 'resim4.jpeg'  # Test için kullanılan görüntü dosyasının yolu
image = cv2.imread(test_image_path)

if image is None:
    raise FileNotFoundError(f"{test_image_path} bulunamadı. Lütfen geçerli bir dosya yolu girin.")

rotation = Rotation(image)

try:
    # Test için görüntüyü döndür ve kaydet
    rotation.process_image(remove_black=True, add_sharpened=True)
except Exception as e:
    print(f"Test sırasında bir hata oluştu: {e}")

"""
Tk().withdraw()
save_path = askdirectory(title="Kayıt Yeri Seçin")  # Kullanıcıdan kayıt yeri seçmesini iste

#test
image = cv2.imread("resim4.jpeg")

if image is None:
    print("Image not found")
else:
    process_image(image, remove_black=True, add_sharpened=True, save_path=save_path)
"""
