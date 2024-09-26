import cv2

from AdvancedImage import sharpen_image

class Flip:
    def __init__(self,image):
        self.image = self

    def flip_image(self, add_sharpness=False):
        if add_sharpness:
            image = sharpen_image(image)
        flipped_image = cv2.flip(image, 1)
        return flipped_image
