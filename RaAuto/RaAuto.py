from pprint import pprint
import os
import re
import time
from time import sleep

from pynput.mouse import Button, Controller as MouseCtrlr
from pynput.keyboard import Key, Controller as KeyCtrlr
import pyautogui as pag
import keyboard as keyboard


from matplotlib import pyplot as plt
from PIL import Image
import cv2 as cv
import numpy as np

import sys
sys.path.append('..')

from RaAuto.RaImage import *


globalWaitTime = 1
globalLimitTime = 20
globalWaitBeforeStart = 0.2


kb = KeyCtrlr()


class Pos:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __bool__(self):
        return True


def message(str):
    return pag.confirm(str)


def getWaitAndLimit(beforeStart = -1, limit = -1, wait = -1):
    if wait == -1:
        wait = globalWaitTime
    if limit == -1:
        limit = globalLimitTime
    if beforeStart == -1:
        beforeStart = globalWaitBeforeStart
        
    if (wait == 0):
        raise ValueError("Wait time cannot be 0. That would create an infinite loop.")
    
    return (beforeStart, limit, wait)


def waitForElement(path, beforeStart = -1, limit = -1, waitTime = -1, conf = 0.9, warn = True):
    timePassed = 0
    beforeStart, limit, waitTime = getWaitAndLimit(beforeStart, limit, waitTime)
    sleep(beforeStart)
    
    while timePassed < limit:
        try:
            x, y = pag.locateCenterOnScreen(path, confidence = conf)
            return Pos(x, y)
        except Exception as e:
            pass
            #print(str(e))
            
        sleep(waitTime)
        timePassed += waitTime
    
    if warn:
        message("Timed out waiting for element " + path)
    return False


def waitForElementDisappear(path, beforeStart = -1, limit = -1, waitTime = -1, conf = 0.9, warn = True):
    timePassed = 0
    beforeStart, limit, waitTime = getWaitAndLimit(beforeStart, limit, waitTime)
    sleep(beforeStart)
    
    while timePassed < limit:
        try:
            x, y = pag.locateCenterOnScreen(path, confidence = conf)
        except Exception as e:
            if (str(e) == "cannot unpack non-iterable NoneType object"):
                return True
            else:
                print(str(e))
            
        sleep(waitTime)
        timePassed += waitTime
    
    if warn:
        message("Timed out waiting for element disappear " + path)
    return False


def waitForOneOf(pathList, beforeStart = -1, limit = -1, waitTime = -1, conf = 0.9, warn = True):
    timePassed = 0
    beforeStart, limit, waitTime = getWaitAndLimit(beforeStart, limit, waitTime)
    sleep(beforeStart)
    
    while timePassed < limit:
        for path in pathList:
            pos = waitForElement(path, beforeStart = 0, limit = 0.01, waitTime = 0.01, conf = conf, warn = False)
            timePassed += 0.01
            if pos:
                return pos
            
        sleep(waitTime)
        timePassed += waitTime
        
    if warn:
        message("Timed out waiting for element list " + str(pathList))
        
    return False


def waitAndClickOneOf(pathList, relX = 0, relY = 0, beforeStart = -1, limit = -1, waitTime = -1, conf = 0.9, warn = True, button = "left"):
    pos = waitForOneOf(pathList, beforeStart = beforeStart, limit = limit, waitTime = waitTime, conf = conf, warn = warn)
    
    if pos:
        pos.x += relX
        pos.y += relY
        
        if button == "left":
            pag.leftClick(pos.x, pos.y)
        elif button == "right":
            pag.rightClick(pos.x, pos.y)
            
        return pos
    
    return False


def waitAndClickElement(path, relX = 0, relY = 0, beforeStart = -1, limit = -1, waitTime = -1, conf = 0.9, warn = True, button="left"):
    pos = waitForElement(path, beforeStart, limit, waitTime, conf, warn=warn)
    
    if pos:
        pos.x += relX
        pos.y += relY
        #print(f'Moving to {pos.x}, {pos.y}')
        
        if button == "left":
            pag.leftClick(pos.x, pos.y)
        elif button == "right":
            pag.rightClick(pos.x, pos.y)
        elif button == "double":
            pag.doubleClick(pos.x, pos.y)
        return pos
    else:
        return False
    

def waitAndClickXY(x, y, beforeStart = -1, waitTime = -1, button="left"):
    pos = Pos(x, y)
    return waitAndClick([pos], beforeStart = beforeStart, waitTime = waitTime, button=button)


def waitAndClick(positions, beforeStart = -1, waitTime = -1, button="left"):
    beforeStart, limit, waitTime = getWaitAndLimit(beforeStart = beforeStart, wait = waitTime)
    
    try:
        if type(positions) != list and type(positions) != tuple:
            positions = [positions]

        #print(f"Sleeping {beforeStart} before starting")
        sleep(beforeStart)
        for i, pos in enumerate(positions):
            if type(pos) == list or type(pos) == tuple:
                posObj = Pos(pos[0], pos[1])
            else:
                posObj = pos
            
            #print(text)
            if button == "left":
                pag.leftClick(posObj.x, posObj.y)
            elif button == "right":
                pag.rightClick(posObj.x, posObj.y)
            if i != len(positions) - 1:
                sleep(waitTime)
        
        return True
    except Exception as e:
        print("Faild at waitAndClick: " + str(e))
        return False
    

def typeSlowly(text, keyInterval):
    for ch in text:
        kb.type(ch)
        sleep(keyInterval)


def waitAndType(texts, beforeStart = -1, waitTime = -1, keyInterval=0):
    beforeStart, limit, waitTime = getWaitAndLimit(beforeStart = beforeStart, wait = waitTime)
    
    if keyInterval == True:
        keyInterval = 0.05
    
    try:
        if type(texts) == str:
            texts = [texts]

        sleep(beforeStart)
        for i, text in enumerate(texts):
            #print(text)
            if keyInterval <= 0:
                kb.type(text)
            else:
                typeSlowly(text, keyInterval)
                
            if i != len(texts) - 1:
                sleep(waitTime)
        
        return True
    except Exception as e:
        print("Faild at waitAndType: " + str(e))
        return False
    

def waitAndPress(key1, key2 = None, key3 = None, beforeStart = -1):
    beforeStart, limit, waitTime = getWaitAndLimit(beforeStart)
    
    sleep(beforeStart)
    
    try:
        if key2 and key3:
            keyboard.press_and_release(key1+"+"+key2+"+"+key3)
        elif key2:
            keyboard.press_and_release(key1+"+"+key2)
        else:
            keyboard.press_and_release(key1)
        return True
    except Exception as e:
        pag.confirm(f"Failed wait and press {str(key1)},{str(key2)},{str(key3)}")
        return False