import cv2
import PIL
import numpy as np
from paddleocr import PaddleOCR
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
def get_input_box(img):
    #地图x y输入框像素值rgb：（176，184，200）
    map_bi_b = np.where(img[:,:,0]==200,1,0)
    map_bi_g = np.where(img[:,:,1]==184,1,0)
    map_bi_r = np.where(img[:,:,2]==176,1,0)

    map_bi = map_bi_b*map_bi_g*map_bi_r
    contours,hierarchy = cv2.findContours(map_bi.astype(np.uint8), 3, 1)
    centers = []
    for cnt  in contours:
        center = cv2.moments(cnt)
        cx = int(center['m10']/center['m00']) 
        cy = int(center['m01']/center['m00'])
        centers.append((cx,cy))


    if centers[0][0] < centers[1][0]:
        centers_x = centers[0]
        centers_y = centers[1]
    else:
        centers_x = centers[1]
        centers_y = centers[0]
    return centers_x, centers_y

def temmatchimg(target,template):
    #target,template 均为cv2图片类型
    theight, twidth = template.shape[:2]
    result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF)
    min_difference, _, min_loc, _ = cv2.minMaxLoc(result)
    loc = (min_loc[0] + twidth//2, min_loc[1] + theight//2)
    return loc, min_difference/(theight*twidth)


def get_position():
    return true


'''
template = cv2.imread("Template_imgs\close_map_tem.png")
targt = cv2.imread("Template_imgs\close.PNG")
temmatchimg(targt,template)
'''
img = cv2.imread("test\position.png")
img2 = cv2.imread("test\_room.png")
ocr = PaddleOCR(use_angle_cls=False, use_gpu=False)
result = ocr.ocr([img2,img], det=False, cls=True)
for line in result:
    print(line)