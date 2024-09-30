import numpy as np
import cv2 as cv
import glob
import pickle

chessboardSize = (8,6)
frameSize = (3648,5472)


criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 19
objp = objp * size_of_chessboard_squares_mm

objpoints = []
imgpoints = []

def calibMatrix(images,cameName):
    workT = False
    for image in images:
        img = cv.imread(image)
        if img is None:
            print(f"Image {image} not found!")
        else:   
            print(f"Processing {image}")
        x,y,c = img.shape
        img = cv.resize(img, (x//3, y//3))

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

        if ret == True:
            workT = True
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (8, 6), (-1,-1), criteria)
            imgpoints.append(corners)

            cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
            cv.imshow('img', cv.resize(img,(1920,1080)))
            cv.waitKey()

    if workT == False:
        assert ValueError("Görüntü Matrisi Yok")

    cv.destroyAllWindows()
    ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

    pickle.dump((cameraMatrix, dist), open(f"calibMatrix/{cameName}_calibration.pkl", "wb" ))
    pickle.dump(cameraMatrix, open(f"calibMatrix/{cameName}_cameraMatrix.pkl", "wb" ))
    pickle.dump(dist, open(f"calibMatrix/{cameName}_dist.pkl", "wb" ))


    img = cv.imread(images[0])
    print(img.shape)
    h,  w = img.shape[:2]
    newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

    dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite(f'calibMatrix/{cameName}_caliResult1.png', dst)

    mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
    dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imwrite(f'calibMatrix/{cameName}_caliResult2.png', dst)

    mean_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error

    print("total error: {}".format(mean_error/len(objpoints)) )


images1 = glob.glob("images/camera1/0.png")

calibMatrix(images1,"camera1")
