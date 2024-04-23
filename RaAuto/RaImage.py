from pprint import pprint
from time import sleep

from pynput.mouse import Button, Controller as MouseCtrlr
from pynput.keyboard import Key, Controller as KeyCtrlr
import pyautogui as pag
import keyboard as keyboard


from matplotlib import pyplot as plt
from PIL import Image
import cv2 as cv
import numpy as np
import pytesseract


def imshow(img, cmap=None, size=10):
    if type(img) == str:
        img = cv.imread(img)
    elif(not type(img) == np.ndarray):
        return
    
    fig = plt.figure(figsize=(size,size))
    ax = plt.Axes(fig, [0,0,1,1])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(img, cmap)

def get_inverted(image):
    return cv.bitwise_not(image)

# get grayscale image
def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

#thresholding
def thresholding(image, threshold=180):
    return cv.threshold(image, threshold, 255, cv.THRESH_BINARY)[1]
    #return cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
    
def thresholdingAdaptive(image):
    return cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)


def capture_and_ocr(x, y, width=300, height=22, lang='swe', resize_factor=2, save_as=None):
    # Capture screenshot
    screenshot = pag.screenshot(region=(x, y, width, height))

    # Enlarge the image by 50%
    width, height = screenshot.size
    new_width = int(width * resize_factor)
    new_height = int(height * resize_factor)
    if resize_factor != 1:
        enlarged_screenshot = screenshot.resize((new_width, new_height))
    else:
        enlarged_screenshot = screenshot

    enlarged_screenshot = enlarged_screenshot.convert('L')

    # Thresholding
    # enlarged_screenshot = np.array(enlarged_screenshot.convert('L'))
    # enlarged_screenshot = thresholding(enlarged_screenshot)
    # enlarged_screenshot = Image.fromarray(enlarged_screenshot)

    if save_as:
        enlarged_screenshot.save(save_as)

    # Perform OCR
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(enlarged_screenshot, lang=lang)

    return text