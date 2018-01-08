import cv2

def drawBoundaries(img, file):

    if file == "CircleFieldLines":
        img = cv2.line(img, (282, 84), (0, 150), (0, 0, 255), 2)
        img = cv2.line(img, (282, 84), (639, 186), (0, 0, 255), 2)
    elif file == "TCrossFieldLines":
        img = cv2.line(img, (0, 179), (262, 122), (0, 0, 255), 2)
        img = cv2.line(img, (262, 122), (564, 189), (0, 0, 255), 2)

    return img
