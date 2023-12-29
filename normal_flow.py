import math
import os

import cv2
import numpy as np
from matplotlib import pyplot as plt


def normal_flow(I0, I1):
    Gx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]]) / 8
    Gy = np.transpose(Gx)
    avg = np.array([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]]) / 9
    fx = cv2.filter2D(I1.astype(np.float32), -1, Gx)
    fy = cv2.filter2D(I1.astype(np.float32), -1, Gy)
    avg0 = cv2.filter2D(I0.astype(np.float32), -1, avg)
    avg1 = cv2.filter2D(I1.astype(np.float32), -1, avg)
    ft = avg1 - avg0
    x = fx/np.sqrt((np.square(fx) + np.square(fy)))
    x = np.nan_to_num(x)
    y = fy / np.sqrt((np.square(fx) + np.square(fy)))
    y = np.nan_to_num(y)
    magnitudes = ft / np.sqrt(np.square(fx) + np.square(fy))
    magnitudes = np.nan_to_num(magnitudes)
    x_dir = x*magnitudes
    y_dir = y*magnitudes
    cv2.normalize(x_dir, x_dir, 1, 0, cv2.NORM_L1)
    cv2.normalize(y_dir, y_dir, 1, 0, cv2.NORM_L1)
    total_x = np.sum(x_dir)
    total_y = np.sum(y_dir)
    # print(x[np.where(x>0)[0], np.where(x>0)[1]])
    # total_x = np.linalg.norm(x_dir)
    #total_y = np.linalg.norm(y_dir)
    # x_temp = x_dir[np.where(x_dir != 0)[0], np.where(x_dir != 0)[1]]
    # y_temp = y_dir[np.where(x_dir != 0)[0], np.where(x_dir != 0)[1]]
    # if x_temp.shape[0] > y_temp.shape[0]:
    #     y_temp = np.insert(y_temp, len(y_temp), [0]*(x_temp.shape[0]-y_temp.shape[0]))
    # elif y_temp.shape[0] > x_temp.shape[0]:
    #     x_temp = np.insert(x_temp, len(x_temp), [0]*(y_temp.shape[0]-x_temp.shape[0]))
    # print(x_dir[np.where(x_dir != 0)[0], np.where(x_dir != 0)[1]].shape)
    # print(y_dir[np.where(x_dir != 0)[0], np.where(x_dir != 0)[1]].shape)
    # print(x_temp.shape)
    # print(y_temp.shape)
    # print(total_x)
    print(total_y)
    plt.quiver(total_x, total_y, color='b', units='xy', scale=1)
    plt.axis('equal')
    plt.xticks(range(-1, 2))
    plt.yticks(range(-1, 2))
    plt.grid()
    plt.show()
    return total_y

if __name__ == '__main__':
    threshold = 0.2
    for i in range(1, len(os.listdir('side/')) - 2):
        img1 = cv2.imread('side//side_frame(' + str(i) + ').jpg', 0)
        img2 = cv2.imread('side//side_frame(' + str(i+1) + ').jpg', 0)
        y_vector = normal_flow(img1, img2)
        if y_vector > 0 and abs(y_vector) > threshold:
            print('the click operation should happened around Frame(' + str(i) + ')')
            break

        # plt.imshow(img1, cmap='copper')
        # plt.axis('off')
        # plt.show()