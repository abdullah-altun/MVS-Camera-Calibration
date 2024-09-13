import numpy as np
import cv2 as cv
import pickle
import glob
import os

with open('cameraMatrix.pkl', 'rb') as f:
    cameraMatrix = pickle.load(f)

with open('dist.pkl', 'rb') as f:
    dist = pickle.load(f)

if not(os.path.exists("imageCalib")):
    os.mkdir("imageCalib")
if not(os.path.exists("imageCalib/Result1")):
    os.mkdir("imageCalib/Result1")
if not(os.path.exists("imageCalib/Result2")):
    os.mkdir("imageCalib/Result2")

for imagePath in glob.glob("images/camera1/**"):
    img = cv.imread(imagePath)
    name = imagePath.split("\\")[-1]
    h,  w = img.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

    dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite(f'imageCalib/Result1/{name[:-4]}_caliResult1.png', dst)

    mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
    dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite(f'imageCalib/Result2/{name[:-4]}_caliResult2.png', dst)
