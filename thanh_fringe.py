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
path = "your_path/patterns"

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

# # # Way 1_________________________________________________________________________________________________
# # # ======================================================================================================

# Create different phases
pha = [array_1d]
for p in range(1,cyc_no):
    # calculate value
    value = np.roll(pha[p-1],shift)
    pha.append(value)

# Create a 1080x1920x3 black images
pattern_dict = {}
for k in range(cyc_no):
    # calculate value
    value = np.zeros((im_h,im_w,3), dtype=np.uint8)
    pattern_dict[k] = value

# Paste Sine array to every pixel column
for c in range(cyc_no):
    j = 0
    for i in range(len(pattern_dict[c][0,:])):
        pattern_dict[c][:,i,0] = 255*pha[c][j]
        pattern_dict[c][:,i,1] = 255*pha[c][j]
        pattern_dict[c][:,i,2] = 255*pha[c][j]
        j = j+1
        if j == len(pha[0]):
            j = 0
            continue
    img_path = path + "/pat" + str(c) + '.jpg'
    cv.imwrite(img_path, pattern_dict[c])

# for i in range(cyc_no):
#     cv.imshow("test", pattern_dict[i])
#     cv.waitKey()

# # Test visualization Sine wave
time = np.linspace(0,1,num=len(pha[0]))
plot.plot(time, pha[0], color='r', label = r'${0}$')
plot.plot(time, pha[1], color='g', label = r'$\frac{\pi}{2}$')
plot.plot(time, pha[2], color='b', label = r'$\pi$')
plot.plot(time, pha[3], color='y', label = r'$\frac{3\pi}{2}$')
plot.title('Intensity phase for each cycle diagram')
plot.xlabel('Phase')
plot.ylabel('Intensity')
plot.grid(True, which='both')
plot.axhline(y=0, color='k')
plot.legend()
plot.show()

# # Create GIF
# # # https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
fp_in = "your_path/patterns/pat*.jpg"
fp_out = "your_path/graphics/phase_shift.gif"
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))] 
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=1000/cyc_no, loop=0)