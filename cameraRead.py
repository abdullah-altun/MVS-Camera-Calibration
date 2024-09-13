from hik_camera.hik_camera import HikCamera
import cv2
import os

class GetImages:
    def __init__(self,cap1,cap2,ips):
        self.cap1 = cap1
        self.cap2 = cap2
        self.ips = ips

        self.foldercrate()        
        
    def foldercrate(self):
        if not(os.path.exists("images")):
            os.mkdir("images")
        if not(os.path.exists("images/camera1")):
            os.mkdir("images/camera1")
        if not(os.path.exists("images/camera2")):
            os.mkdir("images/camera2")

    def view(self):
        num = 0

        with self.cap1:
            self.cap1["ExposureAuto"] = "Off"
            self.cap1["ExposureTime"] = 50000

            if cam2 is not None:
                with self.cap2:
                    self.cap2["ExposureAuto"] = "Off"
                    self.cap2["ExposureTime"] = 50000

                while True:
                    img1 = self.cap1.robust_get_frame()
                    img2 = self.cap2.robust_get_frame()
                    k = cv2.waitKey(1)
                    if k == 27:
                        break
                    elif k == ord("s"):
                        cv2.imwrite(f"images/camera2/{str(num)}.png",img1)
                        cv2.imwrite(f"images/camera1/{str(num)}.png",img2)
                        print("image saved!")
                        num += 1
                    
                    cv2.imshow("camera1",cv2.resize(img1,(1920,1080)))
                    cv2.imshow("camera2",cv2.resize(img2,(1920,1080)))

            else:
                while True:
                    img = self.cap1.robust_get_frame()
                    k = cv2.waitKey(1)
                    if k == ord("q"):
                        break
                    elif k == ord("s"):
                        cv2.imwrite(f"images/camera1/{str(num)}.png",img)
                        print("image saved!")
                        num += 1
                    cv2.imshow("camera1",cv2.resize(img,(1920,1080)))
    
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


getImage = GetImages(cam1,cam2,ips)
getImage.view()

    


