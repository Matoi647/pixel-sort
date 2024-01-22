import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from src.sorter import Sorter
from src.algorithm import *

def auto_scale(img, resolution=240):
    height, width = img.shape[0], img.shape[1]
    ratio = width / height
    new_height = min(height, resolution)
    new_width = int(ratio * new_height)
    return cv2.resize(img, (new_width, new_height))

def upsample(img, factor=3):
    height, width = img.shape[0], img.shape[1]
    res = cv2.resize(img, (int(width*factor), int(height*factor)), interpolation=cv2.INTER_NEAREST)
    return res

img = cv2.imread('StarryNight.jpg')
# np.random.seed(42)
# img = np.random.randint(0, 256, size=(100, 100), dtype=np.uint8)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = auto_scale(img)

fig, ax = plt.subplots()
plt_imshow = ax.imshow(upsample(img))
def update(frame, sorter):
    next_frame = sorter()
    next_frame = upsample(next_frame)
    plt_imshow.set_array(next_frame)
    return (plt_imshow,)

sorter = Sorter(img, 
                counting_sort, 
                step=1, 
                sort_by_col=False, 
                split_rgb=False,
                reverse=True)
animation = FuncAnimation(fig, update, fargs=(sorter,), interval=10, blit=True)
plt.show()