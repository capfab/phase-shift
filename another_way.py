import numpy as np
import cv2 as cv
import scipy.misc as smp
import matplotlib.pyplot as plot
import array as arr
import math
import os
from PIL import Image, ImageDraw
import glob

# Path
path = "F:/web/codes/Phase_shift/graphics"

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

def incr(lst, i):
    return [x+i for x in lst]

# Set initial parameters
im_h = 1080
im_w = 1920
# No. of stripes
stripe_no = 16
# No. of phases
cyc_no = 4
# Pixels per cycle
pixpcy = im_w/stripe_no
# Radian for increment
rad_inc = 360/pixpcy
# Pixels to shift after each phase
shift = int(pixpcy/cyc_no)
# Generate angles in radian
c = np.array(np.arange(0,360,rad_inc)) * np.pi / 180.
# Generate Sine values
d = np.sin(c)
# Shift Sine graph along y axis 1 unit
inc_array_1d = incr(d,1)
# Normalize Sine values to (0,1)
new_range = (0,1)
array_1d = np.array(normalize(inc_array_1d, new_range[0], new_range[1]))

# # Way 2_________________________________________________________________________________________________
# # ======================================================================================================

x0 = array_1d
x1 = np.roll(x0,shift)
x2 = np.roll(x1,shift)
x3 = np.roll(x2,shift)
# Create a 1080x1920x3 black images 
# Approach 1 ===================== NOT RECOMMENDED
for count in range(cyc_no):
    globals()[f"t_phase_shift_pattern{count}"] = np.zeros((im_h,im_w,3), dtype=np.uint8)
# Paste array to every pixel column
for c in range(cyc_no):
    if c == 0:
        i = 0
        j = 0
        while i<len(t_phase_shift_pattern0[0,:]):
            t_phase_shift_pattern0[:,i,0] = 255*x0[j]
            t_phase_shift_pattern0[:,i,1] = 255*x0[j]
            t_phase_shift_pattern0[:,i,2] = 255*x0[j]
            i = i+1
            j = j+1
            if j == len(x0):
                j = 0
                continue
        img_path = path + "/pat" + str(c) + '.bmp'
        cv.imwrite(img_path, t_phase_shift_pattern0)
    if c == 1:
        i = 0
        j = 0
        while i<len(t_phase_shift_pattern1[0,:]):
            t_phase_shift_pattern1[:,i,0] = 255*x1[j]
            t_phase_shift_pattern1[:,i,1] = 255*x1[j]
            t_phase_shift_pattern1[:,i,2] = 255*x1[j]
            i = i+1
            j = j+1
            if j == len(x1):
                j = 0
                continue
        img_path = path + "/pat" + str(c) + '.bmp'
        cv.imwrite(img_path, t_phase_shift_pattern1)
    if c == 2:
        i = 0
        j = 0
        while i<len(t_phase_shift_pattern2[0,:]):
            t_phase_shift_pattern2[:,i,0] = 255*x2[j]
            t_phase_shift_pattern2[:,i,1] = 255*x2[j]
            t_phase_shift_pattern2[:,i,2] = 255*x2[j]
            i = i+1
            j = j+1
            if j == len(x2):
                j = 0
                continue
        img_path = path + "/pat" + str(c) + '.bmp'
        cv.imwrite(img_path, t_phase_shift_pattern2)
    if c == 3:
        i = 0
        j = 0
        while i<len(t_phase_shift_pattern3[0,:]):
            t_phase_shift_pattern3[:,i,0] = 255*x3[j]
            t_phase_shift_pattern3[:,i,1] = 255*x3[j]
            t_phase_shift_pattern3[:,i,2] = 255*x3[j]
            i = i+1
            j = j+1
            if j == len(x3):
                j = 0
                continue
        img_path = path + "/pat" + str(c) + '.bmp'
        cv.imwrite(img_path, t_phase_shift_pattern3)
cv.imshow("phase 0", t_phase_shift_pattern0)
cv.imshow("phase 1", t_phase_shift_pattern1)
cv.imshow("phase 2", t_phase_shift_pattern2)
cv.imshow("phase 3", t_phase_shift_pattern3)
cv.waitKey(0)
