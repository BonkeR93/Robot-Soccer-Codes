import numpy as np
import cv2

def colorClassification(img):
    # Load an color image in color
    img2 = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_green = np.array([35, 8, 0])
    upper_green = np.array([70, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if mask[i, j] > 0:
                img2[i, j] = [0, 255, 0]

    # cv2.imshow('Adding green', img2)
    lower_orange = np.array([0, 50, 50])
    upper_orange = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if mask[i, j] > 0 and (img2[i, j][0] == 0 and img2[i, j][1] == 0 and img2[i, j][2] == 0):
                img2[i, j] = [0, 140, 255]

    # cv2.imshow("Adding orange", img2)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([255, 100, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if mask[i, j] > 0 and (img2[i, j][0] == 0 and img2[i, j][1] == 0 and img2[i, j][2] == 0):
                img2[i, j] = [255, 255, 255]

    # cv2.imshow("Adding white", img2)

    lower_blue = np.array([110, 55, 55])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if mask[i, j] > 0 and (img2[i, j][0] == 0 and img2[i, j][1] == 0 and img2[i, j][2] == 0):
                img2[i, j] = [255, 0, 0]

    # cv2.imshow("Adding blue", img2)

    lower_cyan = np.array([80, 55, 55])
    upper_cyan = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if mask[i, j] > 0 and (img2[i, j][0] == 0 and img2[i, j][1] == 0 and img2[i, j][2] == 0):
                img2[i, j] = [255, 225, 0]

    # cv2.imshow("Adding cyan", img2)

    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if img2[i, j][0] == 0 and img2[i, j][1] == 0 and img2[i, j][2] == 0:
                img2[i, j] = [255, 255, 255]

    # remaining pixels: white

    return img2
