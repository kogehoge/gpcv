import cv2
import gtuner
import numpy as np
import os

def red_detect(img):
# HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 赤色のHSVの値域1
    hsv_min = np.array([0,200,100])
    hsv_max = np.array([1,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

# 赤色のHSVの値域2
    hsv_min = np.array([179,200,100])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1 + mask2


class GCVWorker:
    def __init__(self, width, height):
        if width != 1920 or height != 1080:
            print("WARNING: This GCV script is optimized for 1920x1080 resolution")

#　カレントディレクトリ設定
        os.chdir(os.path.dirname(__file__))
        self.gcvdata = bytearray([0x00])


    def __del__(self):
        del self.gcvdata


    def process(self, frame):
#　検出範囲　X:横軸　Y:縦軸　(原点は左上)
        X = 70
        Y = 50

#　検出dot数の下限　(ノイズに反応しないため)
        count_lower_limit = 3

        halfX = X // 2
        halfY = Y // 2

        x1 = 960 - halfX
        x2 = 960 + halfX

        y1 = 540 - halfY
        y2 = 540 + halfY

#　画像の切り出し
        detect_frame = frame[y1 : y2, x1: x2]

# 画像サイズ
        sizeX = halfX * 2 -1
        sizeY = halfY * 2 -1

#　赤色検出
        mask = red_detect(detect_frame)

# 画素値検出
        counter = 0
        total_x = 0
        #total_y = 0

        for y in range(sizeY):
            for x in range(sizeX):
                colorvalue = mask.item(y,x)
                if colorvalue != 0:
                    counter += 1
                    total_x += x
                    #total_y += y

#　平均計算
        if counter > count_lower_limit:
            average_x = total_x // counter
            #average_y = total_y // counter

            # 元のサイズへ換算
            center_x = average_x + x1
            #center_y += y1

# フレームに中心周囲を円で描く
            cv2.circle(frame, (center_x, 540), 30, (0, 200, 0),thickness=3, lineType=cv2.LINE_AA)

#dot数変換 to valorant
            center_x -= 960
            center_x /= 960
            center_x *= 2254
            #round(center_x)
            dot_to_red_x = int(center_x)

#dot数変換 to valorant
            #center_y -= 960
            #center_y /= 960
            #center_y *= 2254
            #round(center_y)
            #dot_to_red = int(center_y)
            #print(dot_to_red_y)

#バイトデータ変換
            gcvdata = bytearray()
            gcvdata.extend(dot_to_red_x.to_bytes(4, byteorder='big', signed=True))
            #gcvdata.extend(dot_to_red_y.to_bytes(4, byteorder='big', signed=True))
            return(None, gcvdata)

        else:
            return(None,None)