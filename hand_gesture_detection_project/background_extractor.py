

import numpy as np
import cv2
from matplotlib import pyplot as plt

if __name__ == '__main__':
    colored_birdview_bkg = cv2.imread('birdview/birdview_bkg.jpg')
    colored_side_bkg = cv2.imread('side/side_bkg.jpg')
    birdview_bkg = cv2.cvtColor(colored_birdview_bkg, cv2.COLOR_BGR2GRAY)
    side_bkg = cv2.cvtColor(colored_side_bkg, cv2.COLOR_BGR2GRAY)
    birdview_loc = 'birdview/birdview.mp4'
    side_loc = 'side/side.mp4'
    birdview = cv2.VideoCapture(birdview_loc)
    side = cv2.VideoCapture(side_loc)
    success = True
    k=1
    while (success is True):
        success, frame_birdview = birdview.read()
        success2, frame_side = side.read()
        success = success and success2
        if success:
            gray_birdview = cv2.cvtColor(frame_birdview, cv2.COLOR_BGR2GRAY)
            gray_side = cv2.cvtColor(frame_side, cv2.COLOR_BGR2GRAY)
            newbirdview = np.zeros((gray_birdview.shape[0], gray_birdview.shape[1]))
            newside = np.zeros((gray_side.shape[0], gray_side.shape[1]))
            T = 70; #80
            for i in range(0, newbirdview.shape[0]):
                for j in range(0, newbirdview.shape[1]):
                    #print("birdview", np.abs(gray_birdview[i, j] - birdview_bkg[i, j]))
                    if np.abs(int(gray_birdview[i, j]) - int(birdview_bkg[i, j])) > T:
                        newbirdview[i, j] = 1;
                    else:
                        newbirdview[i, j] = 0;
            for i in range(0, newside.shape[0]):
                for j in range(0, newside.shape[1]):
                    #print("side", np.abs(gray_side[i, j] - side_bkg[i, j]))
                    if np.abs(int(gray_side[i, j]) - int(side_bkg[i, j])) > T:
                        newside[i, j] = 1;
                    else:
                        newside[i, j] = 0;

            cv2.imwrite('birdview/birdview_frame('+str(k)+').jpg', newbirdview*255)
            cv2.imwrite('side/side_frame(' + str(k) + ').jpg', newside*255)
            k=k+1
    print("conversion done!")