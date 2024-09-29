import os
import random
from FileReadToLabel import LabelProcessor
import cv2
from Noisy import ImageNoiseAugmentor
from AdvancedImage import AdvancedImage


class ImageNoiseProcessor:
    def __init__(self,save_path):
        self.save_path = save_path
        self.__image__ = None

    def set_save_path(self, new_path):
        self.save_path = new_path

    def get_save_path(self):
        return self.save_path

    def add_random_noisy_label_images(self,all_image_tagged_map,noisy_weight,noisy_list):

        total_tagged_images = len(all_image_tagged_map)
        num_images_to_modify = int((noisy_weight / 100) * total_tagged_images)
        selected_images = random.sample(list(all_image_tagged_map.items()), num_images_to_modify)

        if not self.save_path:
            self.save_path = '.'

        half_num_images = num_images_to_modify // 2
        ordered_images = selected_images[:half_num_images]
        random_images = selected_images[half_num_images:]
        index = 0

        for image_path,txt_path in ordered_images:
            base_image_file_name = os.path.splitext(os.path.basename(image_path))[0]
            base_txt_file_name = os.path.splitext(os.path.basename(txt_path))[0]
            labels = LabelProcessor.read_labels_from_file(txt_path)

            noise_method = noisy_list[index % len(noisy_list)]
            self.__image__=cv2.imread(image_path)
            noisy_image = self.noisy_transactions(noisy_method_name=noise_method,image=self.__image__)

            output_image_file_path = os.path.join(self.save_path, f'{base_image_file_name}_{noise_method}.png')
            success = cv2.imwrite(output_image_file_path, noisy_image)
            if not success:
                print(f"Error saving image at {output_image_file_path}")
            else:
                output_txt_file_path = os.path.join(self.save_path, f'{base_txt_file_name}_{noise_method}.txt')
                LabelProcessor.write_labels_to_file(output_txt_file_path, labels)
            index += 1


        for image_path,txt_path in random_images:
            base_image_file_name = os.path.splitext(os.path.basename(txt_path))[0]
            base_txt_file_name = os.path.splitext(os.path.basename(image_path))[0]
            labels = LabelProcessor.read_labels_from_file(txt_path)

            noise_method = random.choice(noisy_list)
            self.__image__ = cv2.imread(image_path)
            noisy_image = self.noisy_transactions(noisy_method_name=noise_method, image=self.__image__)

            output_image_file_path = os.path.join(self.save_path, f'{base_image_file_name}_{noise_method}.png')
            success = cv2.imwrite(output_image_file_path, noisy_image)
            if not success:
                print(f"Error saving image at {output_image_file_path}")
            else:
                output_txt_file_path = os.path.join(self.save_path, f'{base_txt_file_name}_{noise_method}.txt')
                LabelProcessor.write_labels_to_file(output_txt_file_path, labels)
            index += 1

    def add_random_noisy_images(self, all_images, noisy_weight, noisy_list):
        total_tagged_images = len(all_images)
        num_images_to_modify = int((noisy_weight / 100) * total_tagged_images)
        selected_images = random.sample(all_images, num_images_to_modify)

        if not self.save_path:
            self.save_path = '.'

        half_num_images = num_images_to_modify // 2
        ordered_images = selected_images[:half_num_images]
        random_images = selected_images[half_num_images:]
        index = 0

        for image_path in ordered_images:
            base_image_file_name = os.path.splitext(os.path.basename(image_path))[0]

            noise_method = noisy_list[index % len(noisy_list)]
            self.__image__=cv2.imread(image_path)
            noisy_image = self.noisy_transactions(noisy_method_name=noise_method,image=self.__image__)

            output_image_file_path = os.path.join(self.save_path, f'{base_image_file_name}_{noise_method}.png')
            success = cv2.imwrite(output_image_file_path, noisy_image)
            if not success:
                print(f"Error saving image at {output_image_file_path}")
            index += 1

        for image_path in random_images:
            base_image_file_name = os.path.splitext(os.path.basename(image_path))[0]

            noise_method = noisy_list[index % len(noisy_list)]
            self.__image__=cv2.imread(image_path)
            noisy_image = self.noisy_transactions(noisy_method_name=noise_method,image=self.__image__)

            output_image_file_path = os.path.join(self.save_path, f'{base_image_file_name}_{noise_method}.png')
            success = cv2.imwrite(output_image_file_path, noisy_image)
            if not success:
                print(f"Error saving image at {output_image_file_path}")
            index += 1


    def noisy_transactions(self,noisy_method_name,image):
        if image is None:
            print("No image loaded.")
            return
        noisy = ImageNoiseAugmentor(image)
        advanced_image_tools= AdvancedImage(image)

        #Değişiklik yapılıcak yer

        if noisy_method_name == "Poisson Noisy":
            image = noisy.add_poisson_noise()
        elif noisy_method_name == "Salt And Pepper Noisy":
            image = noisy.add_salt_and_pepper_noise()
        elif noisy_method_name == "Gaussian Noise":
            image = noisy.add_gaussian_noise()
        elif noisy_method_name == "Random Pixel Noise":
            image = noisy.add_random_pixel_noise()
        elif noisy_method_name == "Multiplicative Noise":
            image = noisy.add_multiplicative_noise()
        elif noisy_method_name == "Brightness Contrast Random":
            image = advanced_image_tools.add_brightness_contrast_random()
        elif noisy_method_name == "Random Contrast":
            image = advanced_image_tools.add_contrast()
        elif noisy_method_name == "Color Distortion":
            image = advanced_image_tools.color_distortion()
        elif noisy_method_name == "Add Blur":
            image = advanced_image_tools.apply_blur()
        else:
            raise ValueError("invalidation process")
        return image