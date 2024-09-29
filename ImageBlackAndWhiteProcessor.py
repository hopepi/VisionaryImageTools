import os
import random
import cv2
from FileReadToLabel import LabelProcessor
from AdvancedImage import AdvancedImage

class ImageBlackAndWhiteProcessor:
    def __init__(self,save_path):
        self.save_path = save_path
        self.__image__ = None

    def set_save_path(self, new_path):
        self.save_path = new_path

    def get_save_path(self):
        return self.save_path

    def add_random_bw_label_images(self,all_image_tagged_map,bw_weight):
        total_tagged_images = len(all_image_tagged_map)
        num_images_to_modify = int((bw_weight / 100) * total_tagged_images)
        selected_images = random.sample(list(all_image_tagged_map.items()), num_images_to_modify)

        if not self.save_path:
            self.save_path = '.'

        for image_path, txt_path in selected_images:
            base_image_file_name = os.path.splitext(os.path.basename(image_path))[0]
            base_txt_file_name = os.path.splitext(os.path.basename(txt_path))[0]
            labels = LabelProcessor.read_labels_from_file(txt_path)

            self.__image__ = cv2.imread(image_path)
            advanced_image_tools = AdvancedImage(self.__image__)
            bw_image = advanced_image_tools.apply_black_and_white()

            output_image_file_path = os.path.join(self.save_path, f'{base_image_file_name}_blackAndWhiteFilter.png')
            success = cv2.imwrite(output_image_file_path, bw_image)
            if not success:
                print(f"Error saving image at {output_image_file_path}")
            else:
                output_txt_file_path = os.path.join(self.save_path, f'{base_txt_file_name}_blackAndWhiteFilter.txt')
                LabelProcessor.write_labels_to_file(output_txt_file_path, labels)

    def add_random_bw_images(self,all_images_list,bw_weight):
        total_tagged_images = len(all_images_list)
        num_images_to_modify = int((bw_weight / 100) * total_tagged_images)
        selected_images = random.sample(all_images_list, num_images_to_modify)

        if not self.save_path:
            self.save_path = '.'

        for image_path in selected_images:
            base_image_file_name = os.path.splitext(os.path.basename(image_path))[0]

            self.__image__ = cv2.imread(image_path)
            advanced_image_tools = AdvancedImage(self.__image__)
            bw_image = advanced_image_tools.apply_black_and_white()

            output_image_file_path = os.path.join(self.save_path, f'{base_image_file_name}_blackAndWhiteFilter.png')
            success = cv2.imwrite(output_image_file_path, bw_image)

            if not success:
                print(f"Error saving image at {output_image_file_path}")