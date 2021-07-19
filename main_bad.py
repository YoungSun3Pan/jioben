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
from pynput.keyboard import Controller, Key, Listener
from pynput import keyboard
import random,string


from pynput import keyboard,mouse

coodinates = {'头像': [(850,100)], '战斗选项区域': [(840, 260), (920, 630)], '头像区域': [(850, 70), (950, 150)], '驿站区域': [(410, 219), (650, 440)],
              '任务栏l2': [(808,268), (1004,289)], 'CA搜索图标': [(177, 206)], 'DHW搜索图标': [(300, 226)], '确认传送':[(273, 494)],
              'LG搜索图标': [(153, 226)], '昆仑仙境搜索图标': [(245, 222)], '搜索栏': [(425, 590)], '搜索结果': [(388, 323), (363, 355)],
              '自动寻路': [(520, 595)], '中心': [(508, 415)], 'HS搜索图标': [(246, 222)], 'CSJW搜索图标':[(275, 226)],
              'JW搜索图标':[(152, 310)], 'TG搜索图标':[(210, 222)], 'MW搜索图标':[(244, 222)], 'WZ搜索图标':[(242, 226)],
              'PS搜索图标':[(243, 226)], 'STL搜索图标':[(243, 226)], 'DF搜索图标':[(243, 226)], 'AL搜索图标':[(218, 226)],
              'HGS搜索图标':[(240, 226)], 'BJ搜索图标':[(240, 226)]}
images = {'鼠标': 'images/mymouse.png', '鼠标掩模': 'images/mymouse_mask_1.png', '战斗选项': 'images/fight_choice.png'}
speed_ratio = 200
# time.sleep(2)
# moveTo(1280, 720, duration = 0.11)
# time.sleep(5)
# moveRel(10, 0, duration = 0.1)
# mhxy = locateCenterOnScreen('./images/mhxy.png')
# moveTo(mhxy, duration = 0.11)
PAUSE = 0.5
#lt 840 70
#rb 977 134

class windows_control:
    '''
    LG = [CA2JN, JN2JY, JY2DHW, DHW2LG, LG2SJG, GIVE2DHLW]
    HS = [CA2HS, HS2CJG, GIVE2KDCS]
    MW = [CA2GJ, GJ2JW, JW2MW, MW2MWJ, GIVE2NMW]
    PS = [CA2GJ, GJ2JW, JW2PS, PS2PSD, GIVE2HSN]
    # PS = [GJ2JW, JW2PS, PS2PSD, GIVE2HSN]
    WZ = [CA2GJ, GJ2JW, JW2WZ, WZ2QKD, GIVE2ZYDX]
    TG1 = [CA2GJ, GJ2JW, JW2CSJW, CSJW2TG, TG2LXBDLJ, GIVE2LJ]
    # TG1 = [TG2LXBDLJ, GIVE2LJ]
    TG2 = [CA2GJ, GJ2JW, JW2CSJW, CSJW2TG, TG2LXBDYJ, GIVE2YJ]
    STL1 = [CA2GJ, GJ2JW, JW2STL, STL2SZD, GIVE2DDW]
    STL2 = [CA2GJ, GJ2JW, JW2STL, STL2DXD, GIVE2EDW]
    STL3 = [CA2GJ, GJ2JW, JW2STL, STL2LYD, GIVE2SDW]

    BJ = [CA2JN, JN2JY, JY2DHW, DHW2AL, AL2HGS, HGS2BJ, BJ2BJHS]
    '''
    def __init__(self):
        self.mouse_mask = cv2.imread(images['鼠标掩模'])
        self.mouse_img = cv2.imread(images['鼠标'])
        self.fight_choice_img = cv2.imread(images['战斗选项'])
        self.cur_pos = (0,0)
        self.count = 0
        # self.id = '狐小暖'
        self.id = '离缘'
        self.img_count = 0
        self.iffight = False
        self.cur_state = ('', 0)
        self.next_op = 'normal'
        # 54, 154  86, 167
        # 103, 150 138, 166
        self.hwnd = self.get_hwnd()
        self.windows = self.get_windows()

    def main(self):
        self.set_foreground()
        # img = self.get_current_screen()
        # cv2.imwrite('cor.png', img[151:167, 32:137, :])
        # t1 = threading.Thread(target=self.listen_to_fight)
        # t1.start()
        i_task = 0
        self.mission = self.TG1
        while i_task < len(self.mission):
            if self.iffight:
                time.sleep(0.5)
                continue
            task = self.mission[i_task]
            print(i_task, ':', task)
            try:
                self.exe_task(task)
            except FightExceptin as e:
                print('catch FightExceptin.')
                self.next_op = 'normal'
                continue
            i_task += 1

    def get_windows(self):
        return gw.getWindowsWithTitle(self.id)[0]

    def get_hwnd(self):
        hwnds = []
        _id = self.id
        def foo(hwnd, mouse):
            # 去掉下面这句就所有都输出了，但是我不需要那么多
            if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
                if GetWindowText(hwnd).find(_id) > 0:
                    mouse.append(hwnd)
        EnumWindows(foo, hwnds)
        return hwnds

    def set_foreground(self):
        SetForegroundWindow(self.hwnd)
        ShowWindow(self.hwnd, win32con.SW_RESTORE)
        SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW|win32con.SWP_NOSIZE)

    def get_current_screen(self):
        return cv2.cvtColor(np.array(
            screenshot(region=(*tuple(map(lambda x:x+1, self.windows.topleft)), *tuple(map(lambda x:x+1, self.windows.bottomright))))), cv2.COLOR_RGB2BGR)

    def find_mouse(self, src_img):
        pos = self.rect2point_mouse(inference(src_img))
        if pos is None:
            return None
        print('found mouse at ', pos)
        cv2.circle(src_img, pos, 3, (0,0,255), 2)
        cv2.imwrite('debug_mouse/debug_mount_%d.png'%self.img_count, src_img)
        self.img_count += 1
        return pos

    def if_fighting(self, img):
        return np.mean(img[796:800, 618:622, 0]) > 20

    def local_mouse_on_map(self, map_pos, img_pos, delta=2):
        moveTo(img_pos, duration=0.5)
        for i in range(10):
            print('=====================================')
            img = self.get_current_screen()
            pos = self.rect2point_mouse(inference(img))
            # 672-710, 439-473 = (-38, -34)
            # 747-710, 463-476 = (37, -13)
            if pos is None:
                moveTo(img_pos, duration=0.1)
                continue
            x1 = pos[0] - 38
            y1 = pos[1] - 34
            x3 = pos[0] + 37
            y3 = pos[1] - 10
            x4, y4 = x1, y3
            x2, y2 = x3, y1
            box = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
            res = crnnRecWithBox(np.array(img), [box])
            print(res)
            text = res[0]['text'].replace('B', '8')
            cv2.imwrite('tmp\\test_clear%d.png'%i, img)
            print(i, text, box.tolist())
            cv2.rectangle(img, (x1, y1), (x3, y3), (0,255,0), 2)
            cv2.imwrite('tmp\\test%d.png'%i, img)
            if text[:len(str(map_pos[0]))].isdigit() and text[-len(str(map_pos[1])):].isdigit():
                x = text[:len(str(map_pos[0]))]
                y = text[-len(str(map_pos[1])):]
            else:
                raise
            cur_pos = (int(x), int(y))
            print('cur_pos:', cur_pos)
            dis = (cur_pos[0]-map_pos[0])**2+(cur_pos[1]-map_pos[1])**2
            if dis <= delta:
                return cur_pos
            elif dis < 100:
                dxs = int(np.abs(map_pos[0] - cur_pos[0])/2)
                dys = int(np.abs(map_pos[1] - cur_pos[1]) / 2)
            else:
                dxs = dys = 1
            dx = dxs if map_pos[0] - cur_pos[0] > 0 else -dxs
            dy = -dys if map_pos[1] - cur_pos[1] > 0 else dys
            moveRel((dx, dy), duration=0.5)
        return None

    def copy_to(self, msg):
        for _ in range(5):
            if self.iffight:
                raise FightExceptin()
            press('backspace')
        for _ in range(5):
            if self.iffight:
                raise FightExceptin()
            press('delete')
        pyperclip.copy(msg)
        hotkey('ctrl', 'v')

    def click_YZ(self):
        moveTo(coodinates['头像'][0])
        sleep(0.2)
        rightClick()
        for _ in range(10):
            hotkey('alt', 'h')
            press('f9')
            img = self.get_current_screen()
            pos = self.rect2point_yz(inference_yz(img[267:550, 404:700, :]))
            if pos is None:
                hotkey('alt', 'h')
                press('f9')
                sleep(0.5)
                continue
            self.move_to(pos, 5)
            self.click()
            img = self.get_current_screen()
            if np.var(img[600, 800:810, 0]) < 25:
                break
            else:
                sleep(0.5)


    def move_to(self, value, delta=2):
        for i in range(10):
            if self.iffight:
                raise FightExceptin()
            moveTo(value, duration=0.1)
            screen = self.get_current_screen()
            pos = self.find_mouse(screen)
            if pos is not None:
                self.cur_pos = pos
                break
            else:
                moveTo((2000, 300), duration=1)


        for i in range(10):
            if self.iffight:
                raise FightExceptin()
            dx = value[0] - self.cur_pos[0]
            moveRel(dx, 0, duration=0.3)
            dy = value[1] - self.cur_pos[1]
            moveRel(0, dy, duration=0.3)

            screen = self.get_current_screen()
            pos = self.find_mouse(screen)
            if pos is not None:
                self.cur_pos = pos
            else:
                continue

            if np.abs(pos[0] - value[0]) <= delta and np.abs(pos[1] - value[1]) <= delta:
                print('delta:', (pos[0] - value[0]), (pos[1] - value[1]))
                break
            else:
                print('delta:', (pos[0] - value[0]), (pos[1] - value[1]))

    def correct(self):
        for i in range(10):
            if self.iffight:
                raise FightExceptin()
            moveTo((580, 300), duration=0.1)
            screen = self.get_current_screen()
            pos = self.find_mouse(screen)
            if pos is not None:
                self.cur_pos = pos
                break

    def move_npclst(self, value):
        cut = 2 * float(32) ** 2
        moveRel(value, duration=np.sqrt(cut) / speed_ratio)
        screen = self.get_current_screen()
        self.cur_pos = self.find_mouse(screen)

    def ocrTask(self):
        x1, y1 = coodinates['任务栏l2'][0]
        x3, y3 = coodinates['任务栏l2'][1]
        x4, y4 = x1, y3
        x2, y2 = x3, y1
        box = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        img = self.get_current_screen()
        result = crnnRecWithBox(np.array(img), [box])[0]['text']
        print(result)
        if '盘' in result:
            print('现在去盘丝岭。')
            self.mission = self.PS
        elif '天宫' in result:
            print('现在去天宫。')
            self.mission = self.TG1
        elif '龙宫' in result:
            print('现在去龙宫。')
            self.mission = self.LG
        elif '化' in result:
            print('现在去化生。')
            self.mission = self.HS
        elif '狮' in result:
            print('现在去狮驼岭。')
            self.mission = self.STL1
        elif '寨' in result:
            print('现在去魔王寨。')
            self.mission = self.MW
        elif '庄' in result:
            print('现在去五庄观。')
            self.mission = self.WZ
        else:
            self.mission = []
            print('不支持的门派')


    def give_to(self):
        keyDown('alt')
        keyDown('g')
        self.click()
        keyUp('g')
        keyUp('alt')

    def open_backpack(self):
        keyDown('alt')
        keyDown('e')
        keyUp('e')
        keyUp('alt')

    def click(self):
        click(duration=0.2)
        time.sleep(1)

    def rclick(self):
        rightClick()
        time.sleep(0.1)

    def search(self, value):
        press('Tab')
        self.move_to(coodinates['%s搜索图标'%value[0]][0])
        self.click()
        self.move_to(coodinates['自动寻路'][0])
        moveRel((-100, 0), duration=0.5)
        self.click()
        self.copy_to(value[1])
        if len(value) < 3:
            self.move_to(coodinates['搜索结果'][0])
        else:
            self.move_to(coodinates['搜索结果'][value[2]])
        self.click()
        self.move_to(coodinates['自动寻路'][0])
        self.click()
        self.move_to(coodinates['中心'][0])
        self.rclick()
        self.rclick()

    def exe_task(self, task):
        for i, act in enumerate(task):
            aType, value = act
            if aType == 'correct':
                self.correct()
            elif aType == 'move':
                self.move_to(value)
            elif aType == 'wait':
                for _ in range(value*10):
                    time.sleep(0.1)
                    if self.next_op[0] == 'rollback':
                        print('rollback:', value, self.next_op[1])
                        task[i] = [aType, value-self.next_op[1]]
                        raise FightExceptin()
                if value > 10:
                    print('wait done.')
            elif aType == 'Lclick':
                self.click()
            elif aType == 'Rclick':
                rightClick()
            elif aType == 'CLclick':
                keyDown('ctrl')
                self.click()
                keyUp('ctrl')
            elif aType == 'KLclick':
                mouseDown()
                time.sleep(value)
                mouseUp()
            elif aType == 'confirm':
                self.move_to(coodinates['确认传送'][0])
                self.click()
            elif aType == 'NPClst':
                self.move_npclst(value)
            elif aType == 'backpack':
                self.open_backpack()
            elif aType == 'click_yz':
                self.click_YZ()
            elif aType == 'ocrTask':
                self.ocrTask()
            elif aType == 'Tab':
                press('Tab')
            elif aType == 'give':
                self.give_to()
            elif aType == 'search':
                self.search(value)
            elif aType == 'mask':
                press('f9')
            else:
                print('wrong action type!(%s)'%aType)

    def rect2point_mouse(self, rects):
        if rects is None:
            return None

        if len(rects) == 1:
            x = (rects[0][0] + rects[0][2]) / 2 - 16.0
            y = (rects[0][1] + rects[0][3]) / 2 - 15.5
            return (int(x), int(y))
        print('detections: ', rects)
        score = 0
        x = (rects[0][0] + rects[0][2]) / 2 - 16.0
        y = (rects[0][1] + rects[0][3]) / 2 - 15.5
        for rect in rects:
            if rect[4] > score:
                x = (rect[0] + rect[2]) / 2 - 16.0
                y = (rect[1] + rect[3]) / 2 - 15.5
                score = rect[4]
        return (int(x), int(y))

    def rect2point_yz(self, rects):
        if rects is None:
            return None

        if len(rects) == 1:
            x = (rects[0][0] + rects[0][2]) / 2
            y = (rects[0][1] + rects[0][3]) / 2
            return (int(x)+404, int(y)+267)
        print('detections: ', rects)
        score = 0
        x = (rects[0][0] + rects[0][2]) / 2
        y = (rects[0][1] + rects[0][3]) / 2
        for rect in rects:
            if rect[4] > score:
                x = (rect[0] + rect[2]) / 2
                y = (rect[1] + rect[3]) / 2
                score = rect[4]
        return (int(x)+404, int(y)+267)

    def listen_to_fight(self):
        while True:
            screen = self.get_current_screen()
            if self.if_fighting(screen):
                if not self.iffight:
                    print('====================>fighting start')
                    time.sleep(3)
                    num = string.ascii_letters + string.digits
                    cv2.imwrite('fight_img\\'+''.join(random.sample(num, 10))+'.png', screen)
                    self.iffight = True
                    self.next_op = ('rollback', int(time.time()-self.cur_state[1]))
                    print('set next op:', time.time(), self.cur_state[1])
            else:
                if self.iffight:
                    print('====================>fighting finish')
                    self.iffight = False
            time.sleep(0.5)


def on_press(key):
    exit()

def start_listen():
    keyboard_listener=keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

if __name__ == '__main__':
    # start_listen()
    print(1)
    wc = windows_control()
    wc.main()