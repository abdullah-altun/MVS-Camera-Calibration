from hik_camera.hik_camera import HikCamera
import cv2
import os
from threading import Thread, Lock

lock = Lock()

class GetImages:
    def __init__(self, cap1, cap2, ips):
        self.cap1 = cap1
        self.cap2 = cap2
        self.ips = ips
        self.img1 = None
        self.img2 = None
        self.thread1 = None
        self.thread2 = None
        self.running = True

        self.foldercrate()

    def foldercrate(self):
        if not os.path.exists("images"):
            os.mkdir("images")
        if not os.path.exists("images/camera1"):
            os.mkdir("images/camera1")
        if not os.path.exists("images/camera2"):
            os.mkdir("images/camera2")

    def capture_images_thread(self, camera, camera_name, cam_idx):
        while self.running:
            with camera: 
                camera["ExposureAuto"] = "Off"
                camera["ExposureTime"] = 50000

                with lock:
                    img = camera.robust_get_frame()

                if cam_idx == 1:
                    self.img1 = img
                elif cam_idx == 2:
                    self.img2 = img

    def start_threads(self):
        self.thread1 = Thread(target=self.capture_images_thread, args=(self.cap1, "Camera 1", 1))
        self.thread2 = Thread(target=self.capture_images_thread, args=(self.cap2, "Camera 2", 2))

        self.thread1.start()
        self.thread2.start()

    def stop_threads(self):
        self.running = False
        self.thread1.join()
        self.thread2.join()

    def view(self):
        num = 0
        self.start_threads()  

        while True:
            if self.img1 is not None and self.img2 is not None:

                combined_image = cv2.hconcat([self.img1, self.img2])
                cv2.imwrite(f"images/combined_{str(num)}.png", combined_image)

                resized_combined = cv2.resize(combined_image, (1920, 540)) 
                cv2.imshow("Combined Image", resized_combined)

                k = cv2.waitKey(1)
                if k == 27:
                    break
                elif k == ord("s"): 
                    cv2.imwrite(f"images/camera1/{str(num)}.png", self.img1)
                    cv2.imwrite(f"images/camera2/{str(num)}.png", self.img2)
                    print(f"Images from both cameras saved as {num}.png!")
                    num += 1

        self.stop_threads() 
        cv2.destroyAllWindows()

ips = HikCamera.get_all_ips()
print("All camera IP addresses:", ips)

if len(ips) == 0:
    raise ValueError("Hiç kamera bulunamadı!")
elif len(ips) == 1:
    print("Sadece 1 kamera bulundu.")
    cam1_ip = ips[0]
    cam1 = HikCamera(ip=cam1_ip)
    cam2 = None
elif len(ips) >= 2:
    print("2 kamera bulundu.")
    cam1_ip = ips[0]
    cam2_ip = ips[1]
    cam1 = HikCamera(ip=cam1_ip)
    cam2 = HikCamera(ip=cam2_ip)

getImage = GetImages(cam1, cam2, ips)
getImage.view()
