import cv2
import numpy as np


class ImageNoiseAugmentor:
    def __init__(self, image):
        self.image = image

    def add_poisson_noise(self):
        # Görüntü değerlerini 0-1 aralığına normalleştir
        image = self.image / 255.0

        # Poissona göre gürültü ekle
        noisy_image = np.random.poisson(image * 255.0) / 255.0

        # Sonuç görüntüsünü normalize etme
        noisy_image = np.clip(noisy_image * 255, 0, 255).astype(np.uint)

        return noisy_image

    def add_salt_and_pepper_noise(self, salt_prob=0.02, pepper_prob=0.02):
        noisy_image = np.copy(self.image)

        # Toplam piksel sayısını hesapla
        total_pixels = self.image.shape[0] * self.image.shape[1]

        # Salt (beyaz) piksel sayısı
        num_salt = int(salt_prob * total_pixels)
        # Pepper (siyah) piksel sayısı
        num_pepper = int(pepper_prob * total_pixels)

        # Salt için rastgele koordinatlar seçme
        salt_coords = [np.random.randint(0, i - 1, num_salt) for i in self.image.shape[:2]]

        # Pepper için rastgele koordinatlar seçme
        pepper_coords = [np.random.randint(0, i - 1, num_pepper) for i in self.image.shape[:2]]

        # Aynı koordinatların üst üste gelmesini engelleme kontrolü
        salt_set = set(zip(salt_coords[0], salt_coords[1]))
        pepper_set = set(zip(pepper_coords[0], pepper_coords[1]))

        # Salt ve Pepper koordinatlarının kesişimini engelleme kontrolü
        pepper_set = pepper_set - salt_set

        # Salt (beyaz) pikselleri ata
        for coord in salt_set:
            noisy_image[coord[0], coord[1], :] = 255

        # Pepper (siyah) pikselleri ata
        for coord in pepper_set:
            noisy_image[coord[0], coord[1], :] = 0

        return noisy_image

    def add_gaussian_noise(self, mean=0, var=10):
        image = self.image

        # Görüntü boyutlarını al
        row, col, ch = image.shape

        # Gaussian dağılıma sahip rastgele gürültü oluştur
        sigma = var ** 0.5  # Standart sapma
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        """
        Bu satır ortalama mean ve standart sapmaya sigma sahip bir 
        Gaussian dağılımından rastgele değerler oluşturur.
        """
        gauss = gauss.reshape(row, col, ch)

        # Gürültüyü görüntüye ekle
        noisy_image = image + gauss

        # Sonuç görüntüsünü normalize et ve uint8 dönüşümünü tamamla
        noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint)

        return noisy_image

