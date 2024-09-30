from hik_camera.hik_camera import HikCamera
import cv2
import os
import numpy as np
import pickle

ips = HikCamera.get_all_ips()
print("Camera IP adresleri:",ips)

class GetImages:
    def __init__(self,ip,cameraName):
        self.cap = HikCamera(ip=ip)
        self.Exposure = 10000
        self.cameraName = cameraName

        self.running = True
        self.workT = 0
        self.calibCounter = 10

        self.folderCrater()
        self.view()

    def folderCrater(self):
        if not os.path.exists("CameraCalib"):
            os.mkdir("CameraCalib")
        if not os.path.exists("CameraCalib/camera1"):
            os.mkdir("CameraCalib/camera1")
        if not os.path.exists("CameraCalib/camera2"):
            os.mkdir("CameraCalib/camera2")
        
    def view(self):
        chessboardSize = (9,6)
        frameSize = (3648,5472)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
        objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

        size_of_chessboard_squares_mm = 19
        objp = objp * size_of_chessboard_squares_mm
        
        objpoints = []
        imgpoints = []   
        idx = 0
        while self.running:
            with self.cap:
                self.cap["ExposureAuto"] = "Off"
                self.cap["ExposureTime"] = self.Exposure

                img = self.cap.robust_get_frame()
                gray = img.copy()
                # gray = cv2.resize(gray,(1920,1080))
                
                ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
                cv2.imshow("image",cv2.resize(gray,(1920,1080)))
                print(f"Adim {idx}")
                idx += 1
                if ret == True:
                    print(f"{self.cameraName} {self.workT} kalibre ediliyor...")
                    self.workT += 1
                    objpoints.append(objp)
                    corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
                    imgpoints.append(corners)
                    cv2.drawChessboardCorners(gray, chessboardSize, corners2, ret)
                    
                    cv2.imshow('image', cv2.resize(gray,(1920,1080)))
                    cv2.waitKey(1000)

                k = cv2.waitKey(1)
                if k == 27:
                    break
                elif k == ord("s"):
                    print("Kaydet..")
                    cv2.imwrite("den.png",gray)
                elif self.workT > self.calibCounter:
                    break

        # ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)
        # pickle.dump((cameraMatrix, dist), open(f"CameraCalib/{self.cameraName}/calibration.pkl", "wb" ))
        # pickle.dump(cameraMatrix, open(f"CameraCalib/{self.cameraName}/cameraMatrix.pkl", "wb" ))
        # pickle.dump(dist, open(f"CameraCalib/{self.cameraName}/dist.pkl", "wb" ))



 
if len(ips) == 0:
    raise ValueError("Camera bulunamadi...")
elif len(ips) == 1:
    print("Sadece 1 kamera bulundu...")
    getImage = GetImages(ips[0])

elif len(ips) >= 2:
    print("2 Camera bulundu...")
    print("Camera1 işlem yapılıyor")
    getImage = GetImages(ips[0],"camera1")
    print("Camera2 işlem yapılıyor")
    getImage = GetImages(ips[1],"camera2")
    




