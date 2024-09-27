"""
MASAÜSTÜNDEKİ DOSYALARA KAYDETMEZ
PROJE TEST YAPIM AŞAMASINDADIR
"""
import cv2
import numpy as np
import os
from AdvancedImage import AdvancedImage


class Rotation:
    def __init__(self, image_path,txt_path):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        self.txt_path = txt_path

    def rotate_image(self, angle):
        (height, width) = self.image.shape[:2]
        center = (width // 2, height // 2)
        transform_matrix = cv2.getRotationMatrix2D(center, angle, 0.9)
        rotated = cv2.warpAffine(self.image, transform_matrix, (width, height))
        return rotated,transform_matrix

    def process_image(self, remove_black=False, add_sharpened=False, save_path='',rotate_label=False):
        advanced_image = AdvancedImage(self.image)
        base_image_file_name = os.path.splitext(self.image_path)[0]
        if add_sharpened:
            self.image = advanced_image.sharpen_image()

        # Eğer save_path boşsa mevcut dizini kullan
        if save_path == "":
            save_path = '.'  # Mevcut dizin

        # Kaydetme dizinini oluştur varsa yoksa
        os.makedirs(save_path, exist_ok=True)


        if rotate_label:
            base_txt_file_name=os.path.splitext(self.txt_path)[0]
            labels = self.read_labels_from_file(self.txt_path)  # Etiket dosyasını oku

            for angle in range(0, 360, 45):
                rotated_image, transform_matrix = self.rotate_image(angle)  # Görüntüyü döndür
                advanced_image_remove_back = AdvancedImage(rotated_image)
                result_image = advanced_image_remove_back.remove_black_background() if remove_black else rotated_image

                # Etiketleri döndür ve yaz
                rotated_labels = []
                for label in labels:
                    class_id, x_center, y_center, width, height = label
                    rotated_label = self.rotate_labels(x_center, y_center, width, height, self.image.shape[1],
                                                       self.image.shape[0], transform_matrix)
                    rotated_labels.append([class_id] + list(rotated_label))  # Yeni etiketleri ekle

                output_txt_file_path = os.path.join(save_path, f'{base_txt_file_name}_{angle}.txt')
                self.write_labels_to_file(output_txt_file_path, rotated_labels)

                # Sonuç görüntüsünü kaydet
                output_image_file_path = os.path.join(save_path, f'{base_image_file_name}_{angle}.png')
                success = cv2.imwrite(output_image_file_path, result_image)


        else:
            # Belirli açı aralıklarında döndürme ve opsiyonel olarak arka planı kaldırma işlemi
            for angle in range(0, 360, 45):
                rotated_image = self.rotate_image(angle)  # Görüntüyü döndür
                advanced_image_remove_back = AdvancedImage(rotated_image)
                result_image = advanced_image_remove_back.remove_black_background() if remove_black else rotated_image

                output_image_file_path = os.path.join(save_path, f'{base_image_file_name}_{angle}.png')
                success = cv2.imwrite(output_image_file_path, result_image)

    def rotate_labels(self,x, y, width, height, image_width, image_height, transform_matrix):
        # Normalize edilmiş değerleri piksel değerlerine geri çevir
        x_pixel = x * image_width
        y_pixel = y * image_height
        width_pixel = width * image_width
        height_pixel = height * image_height

        # Bounding box köşelerini belirle piksel cinsinden
        corners = np.array([
            [x_pixel - width_pixel / 2, y_pixel - height_pixel / 2],
            [x_pixel + width_pixel / 2, y_pixel - height_pixel / 2],
            [x_pixel - width_pixel / 2, y_pixel + height_pixel / 2],
            [x_pixel + width_pixel / 2, y_pixel + height_pixel / 2]
        ])

        # Köşe noktalarını döndürme matrisi ile çarp
        ones = np.ones(shape=(len(corners), 1))
        corners_ones = np.hstack([corners, ones])

        rotated_corners = transform_matrix.dot(corners_ones.T).T

        # Yeni bounding boxı oluştur piksel cinsinden
        x_new_pixel = (rotated_corners[:, 0].min() + rotated_corners[:, 0].max()) / 2
        y_new_pixel = (rotated_corners[:, 1].min() + rotated_corners[:, 1].max()) / 2
        width_new_pixel = rotated_corners[:, 0].max() - rotated_corners[:, 0].min()
        height_new_pixel = rotated_corners[:, 1].max() - rotated_corners[:, 1].min()

        # Normalize edilerek geri döndür
        x_new_norm = x_new_pixel / image_width
        y_new_norm = y_new_pixel / image_height
        width_new_norm = min(width_new_pixel / image_width, 1.0)  # Genişliği 1 ile sınırlandır
        height_new_norm = min(height_new_pixel / image_height, 1.0)  # Yüksekliği 1 ile sınırlandır

        return x_new_norm, y_new_norm, width_new_norm, height_new_norm


    def read_labels_from_file(self, file_path):
        labels = []
        with open(file_path, 'r') as file:
            for line in file:
                # Satırı boşluklardan ayır ve değerleri bir liste olarak döndür
                values = line.strip().split()

                # İlk eleman sınıf (int), diğerleri x_center, y_center, width, height (float)
                label_class = int(values[0])
                x_center = float(values[1])
                y_center = float(values[2])
                width = float(values[3])
                height = float(values[4])

                # Her satırı ayrı bir liste yapıp labels listesine ekliyoruz
                labels.append([label_class, x_center, y_center, width, height])

        return labels

    def write_labels_to_file(self, file_path, labels):
        with open(file_path, 'w') as file:
            for label in labels:
                # label tuple'ını ayırıyoruz
                class_id, x_center, y_center, width, height = label

                x_center = x_center + 1 if x_center < 0 else x_center
                y_center = y_center + 1 if y_center < 0 else y_center
                # Sonuçları kontrol et
                print(f"x_center: {x_center}, y_center: {y_center}")
                width = width
                height = height

                # Dosyaya yazıyoruz
                file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

