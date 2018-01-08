from ColorClassification import *
from FieldBoundaryRecognition import *
from FieldLineRecognition import *
import cv2

filename = "TCrossFieldLines"

def printCoord(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print "({}, {})".format(x, y)


img = cv2.imread("Images\\" + filename + ".jpg", cv2.IMREAD_COLOR)

cv2.namedWindow("Original image")
cv2.setMouseCallback("Original image", printCoord)

cv2.imshow('Original image', img)

CCimg = colorClassification(img)
cv2.imwrite('Images\\color_classification_' + filename + '.jpg', CCimg)
# cv2.imshow("Color classified image", CCimg)

FBimg = drawBoundaries(CCimg, filename)
#cv2.imshow("Field Boundaries Recognized", FBimg)

VSLimg = verticalScanLines(FBimg)
# cv2.imshow("Vertical Scan Line Image", VSLimg)

C1img = criterion1(VSLimg)
# cv2.imshow("Criterion 1 Image", C1img)

C2img = criterion2(C1img)
# cv2.imshow("Criterion 2 Image", C2img)

C3img = criterion3(C2img)
cv2.imshow("Criterion 3 Image", C3img)

cv2.imwrite('Images\\field_lines_3criterions_' + filename + '.jpg', C3img)

C4img = criterion4(C3img)
cv2.imshow("", C4img)

cv2.imshow("final", final_scanlines())
cv2.waitKey(0)
cv2.destroyAllWindows()