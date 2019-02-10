#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import time
from config import *


ascii_char = ASCII_CHAR
char_len = len(ascii_char)


def showImage(img, timeout=0):
    cv2.namedWindow('image')
    cv2.imshow('image', img)
    cv2.waitKey(timeout * 1000)
    cv2.destroyAllWindows()


#
def auto_thumb(img):
    height, width = img.shape[:2]
    if width >= D_WIDTH:
        height = height / (width / D_WIDTH) * 0.5
        width = D_WIDTH
    else:
        height = height / 2
    return cv2.resize(img, (int(width), int(height)))


def toChar_print(img, w_thumb=1, h_thumb=1):
    height, width = img.shape[:2]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if w_thumb == h_thumb == 1:
        img_gray_resize = auto_thumb(img_gray)
    else:
        img_gray_resize = cv2.resize(
            img_gray, (int(width / w_thumb), int(height / h_thumb)))
    text = ''
    for row in img_gray_resize:
        for pixel in row:
            text += ascii_char[int(pixel / 256 * char_len)]
        text += '\n'

    os.system('cls')
    print(text)


if __name__ == '__main__':
    print('------------建议按分辨率将宽度缩小至100+,高缩小倍数为宽2倍(默认宽度为%s)-------------' % D_WIDTH)
    print('当前路径：%s' % os.path.abspath('.'))
    while True:
        file_path = input('请输入图片或视频路径：')
        if os.path.isfile(file_path):
            break
        print('路径错误:目标不是文件')

    img = cv2.imread(file_path)
    if img is not None:
        print('当前图片尺寸为宽：%s 高：%s' % (img.shape[1], img.shape[0]))
        flag = input('是否缩小比例(y/n)?\n:')
        if flag.lower() == 'y':
            print('缩小倍数：')
            w_thumb = float(input('宽：'))
            h_thumb = float(input('高：'))
            toChar_print(img, w_thumb, h_thumb)
        else:
            toChar_print(img)
    else:
        print('文件非图片,尝试打开为视频...')
        video = cv2.VideoCapture(file_path)
        if video.isOpened():
            while True:
                flag, frame = video.read()
                if flag:
                    toChar_print(frame, VIDEO_W_THUMB, VIDEO_H_THUMB)
                time.sleep(VIDEO_FLASH_TIME)
        else:
            print('非支持的文件...')
