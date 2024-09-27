import cv2
import numpy as np
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

class PixelDistanceMeasurement:
    def __init__(self, image_path, px_ratio):
        self.image_path = image_path
        self.px_ratio = px_ratio
        self.points = []
        self.distances = []
        self.load_image()
        self.mm = 0
        self.total_pixels = 0

    def load_image(self):
        self.img = cv2.imread(self.image_path)
        if self.img is None:
            raise FileNotFoundError(f"Image file '{self.image_path}' not found.")
        self.window_name = 'image'
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 800, 600)
        cv2.imshow(self.window_name, self.img)
        cv2.setMouseCallback(self.window_name, self.click_event)

    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_MBUTTONDOWN:  # Orta tıklama olayı
            self.points.append((x, y))
            cv2.circle(self.img, (x, y), 0, (0, 255, 0), -1)
            cv2.imshow(self.window_name, self.img)

            if len(self.points) == 2:
                print(f"x:{self.points[0][0] - self.points[1][0]}")
                print(f"y:{self.points[0][1] - self.points[1][1]}")

                distance = np.linalg.norm(np.array(self.points[0]) - np.array(self.points[1])) * self.px_ratio
                pixel = np.linalg.norm(np.array(self.points[0]) - np.array(self.points[1]))
                # print(f'Tıklanan iki nokta arasındaki mesafe: {distance} mm')
                # print(f'Tıklanan iki nokta arasındaki piksel: {pixel} px')
                self.distances.append(distance)
                # Noktaları sıfırlama işlemini kaldırdım, 4 nokta seçildikten sonra sıfırlanacak

            if len(self.points) == 4:
                # İlk noktalar için x1, y1
                x1=self.points[0][0] - self.points[1][0]
                y1=self.points[0][1] - self.points[1][1]
                x2=self.points[2][0] - self.points[3][0]
                y2=self.points[2][1] - self.points[3][1]
                print(f"y1: {y1}")
                self.mm = y1/10
                print("mm:",self.mm)
                print(f"y2: {y2}")
                print(f"y2/y1 : {y2/y1}")
                self.total_pixels=340*self.mm
                print(f"toplam pikesl sayısı {self.total_pixels}")


                print(f"piksel hata sayısı {np.abs(y2-self.total_pixels)}")

                print(f"milimetre hatası : {np.abs(y2-self.total_pixels)/self.mm}")                # 4 noktayı seçtikten sonra noktaları sıfırlayın
                self.points = []


    def save_distances_to_csv(self):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f'test_{current_time}'
        os.makedirs(folder_name, exist_ok=True)
        csv_filename = 'distances.csv'
        csv_filepath = os.path.join(folder_name, csv_filename)
        with open(csv_filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Distance (mm)"])
            for distance in self.distances:
                writer.writerow([distance])

    def plot_distances(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.distances, marker='o')
        plt.title('Distances Between Clicked Points')
        plt.xlabel('Measurement Index')
        plt.ylabel('Distance (mm)')
        plt.grid(True)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f'test_{current_time}'
        plot_filename = 'distances_plot.png'
        plot_filepath = os.path.join(folder_name, plot_filename)
        plt.savefig(plot_filepath)
        plt.show()

    def run(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.save_distances_to_csv()
        self.plot_distances()


