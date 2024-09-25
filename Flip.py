import cv2

from AdvancedImage import sharpen_image


def flip_image(image,add_sharpness=False):
    if add_sharpness:
        image = sharpen_image(image)
    flipped_image = cv2.flip(image, 1)
    return flipped_image

image = cv2.imread("resim4.jpeg")
new_image = flip_image(image)
cv2.imwrite("test.png",new_image)
