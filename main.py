import threading
from pyautogui import *
import time
import pygetwindow as gw
import cv2
import numpy as np
from win32gui import IsWindow, IsWindowEnabled, IsWindowVisible, GetWindowText, SetForegroundWindow, EnumWindows, SetWindowPos, ShowWindow
import win32con
import win32clipboard as w
import pyperclip
import win32api 
from pynput.keyboard import Controller, Key, Listener
from pynput import keyboard
import ctypes
import PIL
import pyautogui
import random,string
import wave
import pyaudio
from paddleocr import PaddleOCR
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from utils import get_input_box, temmatchimg
#import pdb;pdb.set_trace()
taozhi_sum = 118633
chilun_sum = [86593, 46263]
congwu = [187770,100213]
jiantou = [13510, 7206]
class windows_control:
    def __init__(self, windows_X=0, windows_Y=0):
        self.cur_pos = (0,0)
        self.windows_pos = (windows_X, windows_Y)
        self.count = 0
        self.id = '雷电模拟器'
        self.img_count = 0
        self.iffight = False
        self.cur_state = ('', 0)
        self.next_op = 'normal'
        self.hwnd = self.get_hwnd()
        self.windows = self.get_windows()
        self.widows_region = self.get_window_rect()
        self.ocr_model = PaddleOCR(use_angle_cls=False, use_gpu=False)
    def main(self):
        
        
        self.set_foreground() #设置线程到前景,并将窗口设置到指定位置
        self.init_pos()
        #img = self.get_cap_screen(self.get_window_rect())
        #cv2.imwrite("ttt\code.png",img)
        #self.Receiving_Darts() #接镖
        self.datangguojing2datangjingwai()

    def get_windows(self):
        return gw.getWindowsWithTitle(self.id)
    
    def get_hwnd(self):
        hwnds = []
        _id = self.id
        def foo(hwnd, mouse):
            # 去掉下面这句就所有都输出了，但是我不需要那么多
            
            if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
                if _id in GetWindowText(hwnd):
                    mouse.append(hwnd)
        EnumWindows(foo, hwnds)
        return hwnds[0]
    
    def set_foreground(self):
        SetForegroundWindow(self.hwnd)
        ShowWindow(self.hwnd, win32con.SW_RESTORE)
        #将窗口设置到指定位置
        SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, self.windows_pos[0], self.windows_pos[1], 0, 0, win32con.SWP_SHOWWINDOW|win32con.SWP_NOSIZE)

    def move_to(self, X, Y):
        button_coordinates={"delete":(200,89), 0:(200,164), 1:(-27,89),\
                            2:(51,89), 3:(126,89), 4:(-27,164),\
                            5:(51,164), 6:(126,164), 7:(-27,236),\
                            8:(51,236), 9:(126,236), "confirm":(200,236)
                            }
        button_go = (95,0) #相对于y输入框
        button_map =(109,74)
        count = 3 #最多尝试3次W
        ori_X, ori_Y = X, Y
        while True:
            self.click_left( X = button_map[0], Y = button_map[1])
            time.sleep(1)
            img = self.get_cap_screen(self.get_window_rect())
            try:
                center_x, center_y = get_input_box(img)
            except:
                count = count - 1
                if count <=0:
                    return False
                else:
                    continue
            point_x = []
            point_y = []
            if X==0:
                point_x.append(0)
            if Y==0:
                point_y.append(0)
            while X:
                num = X%10
                point_x.insert(0,num)
                X = X//10
            while Y:
                num = Y%10
                point_y.insert(0,num)
                Y = Y//10
            
            self.click_left(X=center_x[0],Y=center_x[1])
            for x_num in point_x:
                time.sleep(0.05)
                self.click_left(X=button_coordinates[x_num][0] + center_x[0],\
                                Y=button_coordinates[x_num][1] + center_x[1])
            time.sleep(0.05)
            self.click_left(X=button_coordinates["confirm"][0] + center_x[0],\
                            Y=button_coordinates["confirm"][1] + center_x[1])
            time.sleep(0.05)
            self.click_left(X=center_y[0],Y=center_y[1])
            for y_num in point_y:
                time.sleep(0.03)
                self.click_left(X=button_coordinates[y_num][0]+center_y[0],\
                                Y=button_coordinates[y_num][1]+center_y[1])
            time.sleep(0.05)                    
            self.click_left(X=button_coordinates["confirm"][0] + center_y[0],\
                            Y=button_coordinates["confirm"][1] + center_y[1])
            time.sleep(0.05)                    
            self.click_left(X=button_go[0] + center_y[0],\
                            Y=button_go[1] + center_y[1])

            #清空输入框
            time.sleep(0.5)
            self.click_left(X=center_x[0],Y=center_x[1])
            time.sleep(1)
            self.click_left(X=center_y[0],Y=center_y[1])
            time.sleep(0.5)
            self.click_left(X=center_y[0],Y=center_y[1])
            time.sleep(1)
            self.click_left(X=center_x[0],Y=center_x[1])

            tem_closs_button = cv2.imread("Template_imgs\close_map_tem.PNG")
            tem_closs_button_2 = cv2.imread("Template_imgs\close_map.PNG")
            tem_closs_button_3 = cv2.imread("Template_imgs\close_map_2.PNG")
            count_temmatch = 3#最多尝试3次
            while True:
                closs_button, different = temmatchimg(img, tem_closs_button)
                closs_button_2, different_2 = temmatchimg(img, tem_closs_button_2)
                closs_button_3, different_3 = temmatchimg(img, tem_closs_button_3)
                time.sleep(1)
                if different < 80:
                    break
                if different_2 < 80:
                    closs_button = closs_button_2
                    different = different_2
                    break
                if different_3 < 80:
                    closs_button = closs_button_3
                    different = different_3
                    break
                count_temmatch = count_temmatch-1
                if count_temmatch <= 0:
                    import pdb;pdb.set_trace() #debug
            self.click_left(X=closs_button[0], Y=closs_button[1])

            time.sleep(0.1)
            pred_position = self.get_position()[1]

            while True:
                time.sleep(3)
                pos = self.get_position()
                if pos:
                    cur_position = pos[1]
                    if np.abs(cur_position[0] - pred_position[0])>1 or \
                        np.abs(cur_position[1] - pred_position[1])>1:
                        pred_position = cur_position
                        continue
                    
                    elif np.abs(cur_position[0] -ori_X)<=1 and \
                            np.abs(cur_position[1] - ori_Y)<=1:
                        #到达终点
                        return True
                    else:
                        #如果停止了并且没到终点，则递归再走
                        return self.move_to(X=ori_X, Y=ori_Y)
            
            return True

    def init_pos(self):
        #将游戏初始化到起始位置
        return True
    
    def click_left(self, X, Y, num = 1):
        #在x，y点击鼠标左键，num为点击次数
        win32api.SetCursorPos([X,Y])
        for i in range(num):
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def Receiving_Darts(self):
        #接镖
        #旗子坐标：长安城（525，155）
        #出来后的坐标 长安城（528，147）
        '''
        self.click_left(849, 543)
        time.sleep(1)
        self.click_left(477, 401, num=2)
        time.sleep(1)
        self.click_left(794, 222)
        time.sleep(1)
        self.click_left(802, 78)
        time.sleep(1)
        
        self.click_left(519, 265)#移动 进入镖局
        time.sleep(3)
        self.click_left(678, 239)#移动
        time.sleep(3)
        self.click_left(545, 351)#移动
        time.sleep(3)
        '''
        self.click_left(590, 243)# 点击镖头，todo：可能会弹验证码
        time.sleep(1.5)
        import pdb;pdb.set_trace()
        if self.if_verification_code():
            time_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            img = self.get_cap_screen(self.get_window_rect())
            cv2.imwrite("vcode\_"+time_now+".png",img)
        time.sleep(1.5)
        self.click_left(780, 340)
        time.sleep(1.5)
        self.click_left(813, 300)
        time.sleep(1.5)
        img = self.get_cap_screen(( 20, 430,  915, 540))
        #name_task = () ocr
        time.sleep(1)
        self.click_left(752, 512)
        time.sleep(1)
        self.click_left(287, 443)#移动
        time.sleep(4)
        self.click_left(516, 468)#移动

        return 0 #todo返回押镖的名字或者索引

    def get_cap_screen(self, region = None):
        if region == None:
            cap_region = self.widows_region
        else:
            
            cap_region = list(region)
            cap_region[0] = cap_region[0] + self.windows_pos[0]
            cap_region[1] = cap_region[1] + self.windows_pos[1]
            cap_region[2] = cap_region[2] + self.windows_pos[0] - cap_region[0]
            cap_region[3] = cap_region[3] + self.windows_pos[1] - cap_region[1]
        img = np.array(screenshot( region=cap_region ))
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    def get_window_rect(self):
        #self.set_foreground()
        time.sleep(1)
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(self.hwnd),
            ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
            ctypes.byref(rect),
            ctypes.sizeof(rect)
            )
            return (rect.left, rect.top, rect.right, rect.bottom)

    def is_battle(self):
        img = self.get_cap_screen((18, 151, 23, 156))
        print (np.sum(img))
        if np.sum(img) not in jiantou:
            return True
        else:
            return False

    def play_audio(self):
        CHUNK = 1024
        wf = wave.open("14060.wav", 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels = wf.getnchannels(),
                            rate= wf.getframerate(),
                            output=True)
        data = wf.readframes(CHUNK)
        start=time.time()
        while time.time() - start < 2:
                stream.write(data)
                data = wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def collect_data_face(self):
        count = 0
        while os.path.exists('full_imgs\imgs_{}.png'.format(count)):
            count = count + 1

        while True:
            if self.is_battle():
                self.play_audio()
                img = self.get_cap_screen((270,150,720,350))
                (h , w, c)= img.shape
                offset = w//4 #4等分
                p1 = img[:, :offset, :]
                p2 = img[:, offset:2*offset, :]
                p3 = img[:, 2*offset:3*offset, :]
                p4 = img[:, 3*offset:4*offset, :]
                index=int(input("请输入1或2或3或4"))
                cv2.imwrite('full_imgs\imgs_{}.png'.format(count), img)
                persons = [p1, p2, p3, p4]
                index = index - 1
                cv2.imwrite('positive\imgs_{}.png'.format(count), persons[index])
                persons.pop(index)
                for i in range(3):
                    cv2.imwrite('negative\imgs_{}_{}.png'.format(count,i), persons[i])
                count = count + 1
                while self.is_battle():
                    time.sleep(1)
            else:
                time.sleep(1)

    def get_position(self):
        room_img = self.get_cap_screen((63,51,169,77))
        position_img = self.get_cap_screen((63,77,162,100))
        room = self.ocr_model.ocr(room_img, det=False, cls=True)[0]
        cv2.imwrite("roomimg.png", position_img)
        position = self.ocr_model.ocr(position_img, det=False, cls=True)[0]
        print(room[0],position[0][0])
        if room[1]<0.5 or position[1]<0.5:
            import pdb;pdb.set_trace()
            return False
        if (position[0][0] !='（' and position[0][0] !='(') or\
            (position[0][-1] !='）' and position[0][-1] !=')'):
            import pdb;pdb.set_trace()
            return False
        try:
            point_index = position[0].index(',')
        except:
            point_index = position[0].index('，')
        X = int(position[0][1:point_index])
        Y =  int(position[0][point_index+1 : -1])
        
        return room[0], (X,Y)

    def collect_data_boss(self):
        count = 0
        while os.path.exists('donghaiwan\imgs_{}.png'.format(count)):
            count = count + 1

        while True:
            img = self.get_cap_screen(self.get_window_rect())
            cv2.imwrite('donghaiwan\imgs_{}.png'.format(count), img)
            print(count)
            count = count + 1
            time.sleep(10)

    def if_verification_code(self):
        img = self.get_cap_screen(self.get_window_rect())
        tem_closs_button = cv2.imread("Template_imgs\_receiving_dart.PNG")
        count_temmatch = 3#最多尝试3次
        while True:
            closs_button, different = temmatchimg(img, tem_closs_button)
            time.sleep(1)
            import pdb;pdb.set_trace()
            if different < 0.01:
                break
            count_temmatch = count_temmatch-1
            if count_temmatch <= 0:
                print(1)
                import pdb;pdb.set_trace() #debug
        return False

    def give_darts(self, X, Y):
        self.click_left(X=444, Y=532)
        time.sleep(1)
        self.click_left(X=X, Y=Y)
        time.sleep(1)
        self.click_left(X=461, Y=357)
        time.sleep(1)
        self.click_left(X=783, Y=168)
        return True

    def changan2datangguojing(self):
        self.move_to(X=10, Y=3)
        time.sleep(2)
        self.click_left(X=80, Y=525)
        return True

    def changan2jiangnanyewai(self):
        self.move_to(X=541, Y=0)
        time.sleep(5)
        self.click_left(X=841, Y=487)
        return True

    def changan2datangguanfu(self):
        self.move_to(X=310, Y=273)
        self.click_left(X=406, Y=70)
        return True

    def jiangnanyewai2jianyecheng(self):
        self.move_to(X=147, Y=55)
        time.sleep(5)
        self.click_left(X=899, Y=301)
        return True

    def jianyecheng2longgong(self):
        self.move_to(X=107, Y=89)
        time.sleep(5)
        self.click_left(X=815, Y=293)
        time.sleep(1)
        self.click_left(X=773, Y=291)
        return True

    def longgong2longwang(self):
        self.move_to(X=110, Y=61)
        time.sleep(5)
        self.click_left(X=580, Y=230)
        time.sleep(2)
        self.give_darts(X=763, Y=163)
        return True

    def changan2huashengshi(self):
        self.move_to(X=507, Y=273)
        time.sleep(5)
        self.click_left(X=620, Y=64)
        return True
    
    def huangshengshi2kongduchanshi(self):
        self.move_to(X=90, Y=55)
        time.sleep(5)
        self.click_left(X=561, Y=249)
        time.sleep(2)
        #self.give_darts(402,210)
        return True

    def datangguanfu2chengyaojing(self):
        self.move_to(X=78, Y=46)
        time.sleep(5)
        self.click_left(X=407, Y=231)
        time.sleep(2)
        self.give_darts(350,188)
        return True

    def changan2qinqiong(self):
        self.move_to(X=88, Y=78)
        time.sleep(5)
        self.click_left(X=462, Y=159)
        time.sleep(2)
        self.click_left(X=502, Y=294)
        time.sleep(2)
        self.give_darts(284,124)
        return True

    def datangguojing2difu(self):
        self.move_to(X=48, Y=326)
        time.sleep(5)
        self.click_left(X=429, Y=101)
        time.sleep(2)
        return True

    def difu2dizangwang(self):
        self.move_to(X=32, Y=66)
        time.sleep(15)
        self.click_left(X=393, Y=236)
        time.sleep(2)
        self.click_left(X=448, Y=75)
        time.sleep(4)
        self.click_left(X=260, Y=83)
        time.sleep(4)
        self.give_darts(351,233)
        return True

    def datangguojing2putuoshan(self):
        self.move_to(X=221, Y=61)
        time.sleep(15)
        self.click_left(X=474, Y=285)
        time.sleep(2)
        self.click_left(X=778, Y=292)
        time.sleep(4)
        return True

    def putuoshan2guanyinjiejie(self):
        self.move_to(X=5, Y=61)
        time.sleep(5)
        self.click_left(X=54, Y=142)
        time.sleep(2)
        self.click_left(X=264, Y=128)
        time.sleep(6)
        self.click_left(X=269, Y=133)
        time.sleep(2)
        self.give_darts(X=252, Y=156)
        return True

    def datangguojing2datangjingwai(self):
        self.move_to(X=9, Y=77)
        time.sleep(5)
        self.click_left(X=23, Y=284)
        time.sleep(2)
        return True

    def datangjingwai2wuguanzhuang(self):
        self.move_to(X=631, Y=76)
        time.sleep(5)
        self.click_left(X=889, Y=210)
        time.sleep(2)
        return True
    
    def wuguanzhuang2zhenyuandaxian(self):
        self.move_to(X=55, Y=36)
        time.sleep(5)
        self.click_left(X=565, Y=238)
        time.sleep(2)
        self.give_darts(X=477, Y=265)
        return True
    
    def datangjingwai2pansiling(self):
        self.move_to(X=527, Y=113)
        time.sleep(5)
        self.click_left(X=455, Y=41)
        time.sleep(2)
        return True

    def pansiling2huashiniang(self):
        self.move_to(X=187, Y=126)
        time.sleep(5)
        self.click_left(X=828, Y=210)
        time.sleep(3)
        self.give_darts(X=542, Y=98)
        time.sleep(2)
        return True

    def pansiling2binbinguniang(self):
        self.move_to(X=187, Y=126)
        time.sleep(5)
        self.click_left(X=828, Y=210)
        time.sleep(3)
        self.click_left(X=365, Y=57)
        time.sleep(3)
        self.click_left(X=579, Y=55)
        time.sleep(3)
        self.give_darts(X=551, Y=176)
        return True
    
    def datangjingwai2mowangzai(self):
        self.move_to(X=54, Y=113)
        time.sleep(5)
        self.click_left(X=470, Y=49)
        time.sleep(3)
        return True

    def mowangzai2niumowang(self):
        self.move_to(X=92, Y=73)
        time.sleep(5)
        self.click_left(X=582, Y=232)
        time.sleep(2)
        self.give_darts(X=535, Y=235)
        return True

    def datangjingwai2shituoling(self):
        self.move_to(X=8, Y=48)
        time.sleep(5)
        self.click_left(X=9, Y=302)
        time.sleep(2)
        return True

    def shituoling2dadawang(self):
        self.move_to(X=116, Y=28)
        time.sleep(5)
        self.click_left(X=766, Y=201)
        time.sleep(2)
        self.give_darts(X=578, Y=120)
        return True

    def shituoling2erdawang(self):
        self.move_to(X=27, Y=84)
        time.sleep(5)
        self.click_left(X=515, Y=127)
        time.sleep(2)
        self.give_darts(X=517, Y=142)
        return True

    def shituoling2sandawang(self):
        self.move_to(X=13, Y=41)
        time.sleep(5)
        self.click_left(X=351, Y=237)
        time.sleep(2)
        self.give_darts(X=597, Y=156)
        return True

    def datangjingwai2changshoujiaowai(self):
        self.move_to(X=48, Y=16)
        time.sleep(5)
        self.click_left(X=561, Y=298)
        time.sleep(2)
        self.click_left(X=785, Y=293)
        time.sleep(2)
        return True

    def changshoujiaowai2tiangong(self):
        self.move_to(X=26, Y=58)
        time.sleep(5)
        self.click_left(X=372, Y=267)
        time.sleep(2)
        self.click_left(X=776, Y=295)
        time.sleep(2)
        return True 
    
    def tiangong2yangjian(self):
        self.move_to(X=151, Y=60)
        time.sleep(5)
        self.click_left(X=363, Y=206)
        time.sleep(3)
        self.give_darts(X=6, Y=137)
        return True 

    def tiangong2lijing(self):
        self.move_to(X=151, Y=60)
        time.sleep(5)
        self.click_left(X=363, Y=206)
        time.sleep(3)
        self.click_left(X=35, Y=278)
        time.sleep(5)
        self.click_left(X=202, Y=134)
        time.sleep(5)
        self.give_darts(X=202, Y=162)
        return True

    def changshoujiaowai2changshoucun(self):
        self.move_to(X=160, Y=161)
        time.sleep(5)
        self.click_left(X=472, Y=79)
        time.sleep(2)
        return True

    def changshoucun2fangcunshan(self):
        self.move_to(X=108, Y=205)
        time.sleep(5)
        self.click_left(X=482, Y=42)
        time.sleep(2)
        return True

    def fangcunshan2putizhushi(self):
        self.move_to(X=128, Y=136)
        time.sleep(5)
        self.click_left(X=566, Y=247)
        time.sleep(4)
        self.click_left(X=761, Y=114)
        time.sleep(4)
        self.give_darts(X=626, Y=199)
        return True          
if __name__ == '__main__':
    # start_listen()
    wc = windows_control()
    wc.main()