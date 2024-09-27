from pixelmesure import PixelDistanceMeasurement

pxratio = 0.0831 # 1 pikselin kaç mm ye denk geldiği oran 

image_path = "/home/gedik/Desktop/den_last/MVS-Camera-Calibration/imageCalib/Result1/Image_20240913144706801_caliResult1.png" # görselin yolu

measurement = PixelDistanceMeasurement(image_path,pxratio)# objeyi oluştur
measurement.run()# çalıştır