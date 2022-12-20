import cv2
import gtuner
import numpy as np
import os
def red_detect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = np.array([0,200,100])
    hsv_max = np.array([1,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    hsv_min = np.array([179,200,100])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    return mask1 + mask2
class GCVWorker:
    def __init__(self, width, height):
        pass
    def __del__(self):
        del self.gcvdata
    def process(self, frame):
        X = 80
        Y = 50
        count_lower_limit = 1
        halfX = X // 2
        halfY = Y // 2
        x1 = 960 - halfX
        x2 = 960 + halfX
        y1 = 540 - halfY
        y2 = 540 + halfY
        detect_frame = frame[y1 : y2, x1: x2]
        sizeX = halfX * 2 -1
        sizeY = halfY * 2 -1
        mask = red_detect(detect_frame)
        counter = 0
        total_x = 0
        for y in range(sizeY):
            for x in range(sizeX):
                colorvalue = mask.item(y,x)
                if colorvalue != 0:
                    counter += 1
                    total_x += x
        if counter > count_lower_limit:
            average_x = total_x // counter
            center_x = average_x + x1
            center_x -= 960
            center_x /= 960
            center_x *= 2254
            dot_to_red_x = int(center_x)
            gcvdata = bytearray()
            gcvdata.extend(dot_to_red_x.to_bytes(4, byteorder='big', signed=True))
            return(None, gcvdata)
        else:
            return(None,None)

        