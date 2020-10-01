#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@func:
@author: Ziwang Zhao
@file: demo.py
@time: 2020/10/1
"""
import cv2
import numpy as np


def pic_to_sketch(img, ksize=25, sigmaX=100, sigmaY=100):
    '''The picture is changed to a sketch. You can change the parameter value to get better results.'''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    # ksize must be positive and odd numbers, or zero
    blur = cv2.GaussianBlur(inv, ksize=(ksize, ksize), sigmaX=sigmaX, sigmaY=sigmaY)
    sketch_img = cv2.divide(gray, 255 - blur, scale=255)
    return sketch_img


def left_right(img_path):
    '''Left and right splicing of original image and sketch'''
    img = cv2.imread(img_path)
    sketch_img = pic_to_sketch(img)
    sketch_img = cv2.cvtColor(sketch_img, cv2.COLOR_GRAY2BGR)
    w, h = img.shape[0], img.shape[1]
    result = np.concatenate((img[:, :int(h / 2), :], sketch_img[:, int(h / 2):, :]), axis=1)
    cv2.imwrite('left_right-' + img_path, result)


def up_down(img_path):
    '''Up and down splicing of original image and sketch'''
    img = cv2.imread(img_path)
    sketch_img = pic_to_sketch(img)
    sketch_img = cv2.cvtColor(sketch_img, cv2.COLOR_GRAY2BGR)
    w, h = img.shape[0], img.shape[1]
    result = np.concatenate((img[:int(w / 2), :, :], sketch_img[int(w / 2):, :, :]), axis=0)
    cv2.imwrite('up_down-' + img_path, result)


def video_to_sketch(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter('sketch-' + video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    ret, frame = cap.read()
    while ret:
        sketch_img = pic_to_sketch(frame)
        video_writer.write(cv2.cvtColor(sketch_img, cv2.COLOR_GRAY2BGR))
        ret, frame = cap.read()
    video_writer.release()


if __name__ == '__main__':
    img_path = 'Surrey.jpg'
    img = cv2.imread(img_path)
    sketch = pic_to_sketch(img)
    cv2.imwrite('sketch-' + img_path, sketch)

    left_right(img_path)

    up_down(img_path)

    video_to_sketch('video.mp4')
    print('Finish.')
