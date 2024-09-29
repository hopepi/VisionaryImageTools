import cv2
from AdvancedImage import AdvancedImage

class Flip:
    def __init__(self,image_path):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)

    def flip_image(self, add_sharpness=False):
        advanced_image = AdvancedImage(self.image)
        image = self.image
        if add_sharpness:
            image = advanced_image.sharpen_image()
        flipped_image = cv2.flip(image, 1)
        return flipped_image
