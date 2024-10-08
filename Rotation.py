import uuid
import cv2
import numpy as np
import time
import os
from AdvancedImage import AdvancedImage
from FileReadToLabel import LabelProcessor  # LabelProcessorı içe aktarma

class Rotation:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)

    def rotate_image(self, angle):
        (height, width) = self.image.shape[:2]
        center = (width // 2, height // 2)
        transform_matrix = cv2.getRotationMatrix2D(center, angle, 0.9)
        rotated = cv2.warpAffine(self.image, transform_matrix, (width, height))
        return rotated, transform_matrix

    def process_image(self, remove_black=False, add_sharpened=False, save_path="", rotate_label=False,txt_path=""):
        advanced_image = AdvancedImage(self.image)
        base_image_file_name = os.path.splitext(os.path.basename(self.image_path))[0]  # Dosya adı ve uzantıyı ayır

        if add_sharpened:
            self.image = advanced_image.sharpen_image()

        if not save_path:  # Eğer save_path boş ise varsayılan olarak mevcut dizine yazdır
            save_path = '.'

        # Kaydetme dizini olup olmadığını kontrol et
        if not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=True)

        if rotate_label:
            base_txt_file_name = os.path.splitext(os.path.basename(txt_path))[0]  # Txt dosya adı
            labels = LabelProcessor.read_labels_from_file(txt_path)

            for angle in range(75, 360, 75):
                unique_id = str(uuid.uuid4())
                timestamp = int(time.time())
                rotated_image, transform_matrix = self.rotate_image(angle)
                advanced_image_remove_back = AdvancedImage(rotated_image)
                result_image = advanced_image_remove_back.remove_black_background() if remove_black else rotated_image

                # Etiketleri döndür ve yaz
                rotated_labels = []
                for label in labels:
                    class_id, x_center, y_center, width, height = label
                    rotated_label = self.rotate_labels(x_center, y_center, width, height, self.image.shape[1],
                                                       self.image.shape[0], transform_matrix)
                    rotated_labels.append([class_id] + list(rotated_label))

                output_txt_file_path = os.path.join(save_path,f'{base_txt_file_name[:10]}_{unique_id}_{timestamp}.txt')
                LabelProcessor.write_labels_to_file(output_txt_file_path, rotated_labels)


                output_image_file_path = os.path.join(save_path,f'{base_image_file_name[:10]}_{unique_id}_{timestamp}.png')
                success = cv2.imwrite(output_image_file_path, result_image)
                if not success:
                    print(f"Error saving image at {output_image_file_path}")

        else:
            for angle in range(75, 360, 75):
                unique_id = str(uuid.uuid4())
                timestamp = int(time.time())
                rotated_image, transform_matrix = self.rotate_image(angle)
                advanced_image_remove_back = AdvancedImage(rotated_image)
                result_image = advanced_image_remove_back.remove_black_background() if remove_black else rotated_image

                output_image_file_path = os.path.join(save_path,f'{base_image_file_name[:10]}_{unique_id}_{timestamp}.png')
                success = cv2.imwrite(output_image_file_path, result_image)
                if not success:
                    print(f"Error saving image at {output_image_file_path}")

    def rotate_labels(self, x, y, width, height, image_width, image_height, transform_matrix):
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