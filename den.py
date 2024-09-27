from hik_camera.hik_camera import HikCamera
import cv2
import os
from threading import Thread, Lock

lock = Lock()

def get_frame(cam, cam_name):
    with cam:
        cam["ExposureAuto"] = "Off"
        cam["ExposureTime"] = 50000

        while True:
            with lock: 
                img = cam.robust_get_frame()
            print(f"{cam_name}: {img.shape}")
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

if cam2 is not None:
    thread1 = Thread(target=get_frame, args=(cam1, "Camera 1"))
    thread2 = Thread(target=get_frame, args=(cam2, "Camera 2"))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

else:
    get_frame(cam1, "Camera 1")
