
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
import pyaudio
import wave

def play_audio():
    CHUNK = 1024
    wf = wave.open("14060.wav", 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate= wf.getframerate(),
                        output=True)
    data = wf.readframes(CHUNK)
    start=time.time()
    while time.time() - start < 3:
            stream.write(data)
            data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()


taozhi_sum = 118633