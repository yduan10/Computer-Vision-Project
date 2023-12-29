import math
import os

import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import peak_local_max


# def gaussdiff(sigma, x, y):
#     diff = (x / (2 * math.pi * pow(sigma, 4))) * math.exp(-(pow(x, 2) + pow(y, 2)) / (2 * pow(sigma, 2)))
#     return diff
#
# def gaussDeriv2D(sigma):
#     step = math.ceil(3 * sigma)
#     Gx = np.ones((2 * step + 1, 2 * step + 1))
#     for b in range(-step, step+1):
#         for a in range(-step, step+1):
#             diff = gaussdiff(sigma, a, b)
#             Gx[b + step, a + step] = diff
#     Gy = np.transpose(Gx)
#     return Gx, Gy
#
# def feature_points(img, sigma1, sigma2, win_size):
#     Gx, Gy = gaussDeriv2D(sigma1)
#     Ix = cv2.filter2D(img.astype('float32'), -1, Gx, borderType=cv2.BORDER_CONSTANT)
#     Iy = cv2.filter2D(img.astype('float32'), -1, Gy, borderType=cv2.BORDER_CONSTANT)
#     Ix2 = Ix ** 2
#     Iy2 = Iy ** 2
#     IxIy = Ix * Iy
#     H = np.multiply(cv2.getGaussianKernel(2*math.ceil(3*sigma2)+1, sigma2), (cv2.getGaussianKernel(2*math.ceil(3*sigma2)+1, sigma2)).T)
#     gIx2 = cv2.filter2D(Ix2, -1, H, borderType=cv2.BORDER_CONSTANT)
#     gIy2 = cv2.filter2D(Iy2, -1, H, borderType=cv2.BORDER_CONSTANT)
#     gIxIy = cv2.filter2D(IxIy, -1, H, borderType=cv2.BORDER_CONSTANT)
#     R = gIx2 * gIy2 - gIxIy ** 2 + 0.05 * (gIx2 + gIy2) ** 2
#     R[R < 1000000] = 0
#     coordinates = peak_local_max(R, min_distance=1)
#     good_features = []
#     for [x,y] in coordinates:
#         if((x >= int(math.floor(win_size/2)) and x <= (719 - int(math.floor(win_size/2)) - 1)) and (y >= int(math.floor(win_size/2)) and y <= (1279 - int(math.floor(win_size/2)) - 1))):
#             good_features.append([x,y])
#     coor = []
#     for x, y in good_features:
#        coor.append([[x, y]])
#     return coor

img = cv2.imread('birdview//birdview_frame(' + str(1) + ').jpg', 0)
p0 = cv2.goodFeaturesToTrack(img, maxCorners=70, qualityLevel=0.001, minDistance=5)
#p0 = np.array(feature_points(img, 0.9, 1, 31))
print(p0)
feature_points_x = []
feature_points_y = []
for i in range(1, len(os.listdir('birdview/'))-2):
    img1 = cv2.imread('birdview//birdview_frame(' + str(i) + ').jpg', 0)
    img2 = cv2.imread('birdview//birdview_frame(' + str(i + 1) + ').jpg', 0)
    p1, isFound, err = cv2.calcOpticalFlowPyrLK(img1, img2, p0, None, winSize=(31, 31), maxLevel=10, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.03), flags=cv2.OPTFLOW_LK_GET_MIN_EIGENVALS, minEigThreshold=0.00025)
    aa = isFound > 0
    points = p1[aa[:, 0], :]
    p0 = points
    for i in range(0, len(points)):
        feature_points_x.append(((points[i])[0])[0])
        feature_points_y.append(((points[i])[0])[1])
plt.imshow(img, cmap='copper')
plt.scatter(feature_points_x, feature_points_y, s=5, marker='+', color='red')
#plt.gca().invert_yaxis()
plt.gca().invert_xaxis()
plt.axis('off')
plt.show()