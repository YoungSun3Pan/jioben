import os,time
import pyautogui as pag
from ctypes import *
gdi32 = windll.gdi32
user32 = windll.user32
hdc = user32.GetDC(None)
while True:
    x,y = pag.position() #返回鼠标的坐标
    pixel = gdi32.GetPixel(hdc, x, y)#获取像素值
    posStr="Position:"+str(x).rjust(4)+','+str(y).rjust(4)
    r = pixel & 0x0000ff
    g = (pixel & 0x00ff00) >> 8
    b = pixel >> 16
    print (posStr)#打印坐标
    print (r,g,b)
    time.sleep(3)