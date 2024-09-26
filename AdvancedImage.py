import random
import cv2
import numpy as np

class AdvancedImage:
    def __init__(self,image):
        self.image = image

    def decrease_brightness(self, value):
        # Parlaklığı azaltmak için görüntüyü koyulaştır
        # 0 ile 255 arasında bir değer olmalıdır
        value = max(0, min(255, value))

        # Parlaklığı azaltma
        darkened_image = cv2.subtract(self, (value, value, value, 0))  # BGR formatında çıkarma işlemi

        return darkened_image

    def sharpen_image(self):
        # Keskinleştirme için kernel tanımlama
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])

        sharpened = cv2.filter2D(self.image, -1, kernel)
        smoothed = cv2.GaussianBlur(sharpened, (3, 3), 0)
        return smoothed

    """
    def sharpen_image_with_blur(self):
        # Gaussian bulanıklaştırma
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # Kenarları keskinleştirme
        sharpened = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)

        return sharpened


    def unsharp_mask(self, sigma=1.0, alpha=1.5):
        # Gaussian bulanıklaştırma
        blurred = cv2.GaussianBlur(image, (0, 0), sigma)

        # Keskinleştirilmiş görüntüyü oluştur
        sharpened = cv2.addWeighted(image, 1 + alpha, blurred, -alpha, 0)

        return sharpened
    """

    def remove_black_background(self):
        # Görüntüyü bgr den rgba ya dönüştür
        b_channel, g_channel, r_channel = cv2.split(self.image)

        # Alfa kanalı eklemek için boş bir alfa kanalı oluştur
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # Tamamen opak

        # Tamamen siyah piksel tespiti
        black_pixels = (b_channel == 0) & (g_channel == 0) & (r_channel == 0)

        # Siyah alanları şeffaf yapmak
        alpha_channel[black_pixels] = 0  # Siyah bölgeler için alfa 0 (şeffaf)

        # Sonuç görüntüsünü oluştur
        result_rgba = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        return result_rgba

    def resize_image(self, scale_percent):
        """
        scale_percent yüzdelik olarak ne kadar büyüyeceğini ifade eder
        """
        scale_percent = scale_percent + 100
        # Yeni boyutları hesapla
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        new_size = (width, height)

        # Resmi yeniden boyutlandır
        resized_image = cv2.resize(self.image, new_size, interpolation=cv2.INTER_LINEAR)

        """
        cv2.resize(): OpenCV kütüphanesinin bir fonksiyonudur Bu fonksiyon,
        resmi belirtilen yeni boyutlara new_size göre yeniden boyutlandırır.

        interpolation=cv2.INTER_LINEAR: Yeniden boyutlandırma işlemi sırasında kullanılan interpolasyon yöntemidir
        Bu yöntem piksellerin daha pürüzsüz görünmesini sağlar.
        """

        return resized_image

    def add_brightness_contrast_random(self):
        # Rastgele beta ve alpha değerlerini belirle
        beta = random.randint(-30, 30)  # Parlaklık için -30 ile +30 arasında bir değer
        alpha = round(random.uniform(0.8, 1.2), 2)  # Kontrast için 0.8 ile 1.2 arasında bir değer

        # İlk olarak parlaklık ayarını yap
        image_bright = cv2.convertScaleAbs(self.image, alpha=1, beta=beta)
        # Ardından kontrast ayarını yap
        adjusted_image = cv2.convertScaleAbs(image_bright, alpha=alpha, beta=0)

        return adjusted_image

    def add_contrast(self):
        # Rastgele alpha değerini belirle (0.8 ile 1.5 arasında)
        alpha = round(random.uniform(0.8, 1.5), 2)  # 0.8 ile 1.5 arasında bir değer

        # Kontrast ayarını uygula
        adjusted_image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=0)

        return adjusted_image

    def color_distortion(self):
        # Renk kanallarını ayır
        b, g, r = cv2.split(self.image)

        # Her kanal için rastgele bir çarpan belirle
        b_factor = random.uniform(0.7, 1.2)  # Mavi kanal için çarpan
        g_factor = random.uniform(0.7, 1.2)  # Yeşil kanal için çarpan
        r_factor = random.uniform(0.7, 1.2)  # Kırmızı kanal için çarpan

        # Her kanalı çarpan ile çarp
        b = cv2.convertScaleAbs(b, alpha=b_factor, beta=0)
        g = cv2.convertScaleAbs(g, alpha=g_factor, beta=0)
        r = cv2.convertScaleAbs(r, alpha=r_factor, beta=0)

        # Kanalları birleştir
        distorted_image = cv2.merge((b, g, r))

        return distorted_image

    # ksize: Bulanıklık penceresinin boyutu
    def apply_blur(self, ksize=5):
        # Görüntüyü bulanıklaştır
        blurred_image = cv2.GaussianBlur(self.image, (ksize, ksize), 0)

        return blurred_image

