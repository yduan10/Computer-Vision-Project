import math
import os

import numpy as np
import cv2
from matplotlib import pyplot as plt


def getcnthull(mask_img):
    contours, hierarchy = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv2.contourArea(x))
    epsilon = 0.0085 * cv2.arcLength(contours, True)
    approx = cv2.approxPolyDP(contours, epsilon, True)
    hull = cv2.convexHull(approx)
    return approx, hull


def getdefects(contours):
    hull = cv2.convexHull(contours, returnPoints=False)
    defects = cv2.convexityDefects(contours, hull)
    return defects


if __name__ == '__main__':
    count = 0
    k = 1
    for i in range(1, len(os.listdir('birdview/')) - 1):
        img = cv2.imread('birdview//birdview_frame('+ str(i) + ').jpg', 0)
        kernel1 = np.ones((5, 5), np.uint8)
        kernel2 = np.ones((5, 5), np.uint8)
        kernel3 = np.ones((4, 4), np.uint8)
        img_birdview = cv2.dilate(cv2.erode(cv2.dilate(img, kernel1, iterations = 1), kernel2, iterations=3), kernel3, iterations = 2)
        birdview_contours, birdview_hull = getcnthull(img_birdview)
        #cv2.drawContours(img_birdview, [birdview_contours], -1, (255, 255, 255), 2)
        #cv2.drawContours(img_birdview, [birdview_hull], -1, (255, 255, 255), 2)
        birdview_defects = getdefects(birdview_contours)
        if birdview_defects is not None:
            cnt = 0
            for i in range(birdview_defects.shape[0]):
                s, e, f, d = birdview_defects[i][0]
                start = tuple(birdview_contours[s][0])
                #cv2.putText(img_birdview, 's',start, cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2,cv2.LINE_AA)
                end = tuple(birdview_contours[e][0])
                #cv2.putText(img_birdview, 'e',end, cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2,cv2.LINE_AA)
                far = tuple(birdview_contours[f][0])
                #cv2.putText(img_birdview, 'f',far, cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2,cv2.LINE_AA)
                a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                s = (a + b + c) / 2
                ar = math.sqrt(s * (s - a) * (s - b) * (s - c))
                d = (2 * ar) / a
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                if angle <= 90 and d > 230:
                    cnt += 1
                    cv2.circle(img_birdview, far, 6, [255, 255, 255], 10)
            cnt += 1
            if cnt > 0:
                cv2.putText(img, str(cnt), (1206, 681), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)#1206*681
            else:
                cv2.putText(img, str(0), (1206, 681), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # plt.figure("finger count img")
        # plt.imshow(img, cmap='gray')
        # plt.axis('off')
        # plt.show()
        cv2.imwrite('finger_counts//birdview_frame_with_finger_counts('+ str(k) + ').jpg', img)
        k += 1
        finger_count = 1 #changable
        if cnt == finger_count:
            count = count + 1;
    print('The total number of finger equals to ' + str(finger_count) + ' is: ', count)
    cv2.destroyAllWindows()
