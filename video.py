import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse
import os

from PixelSort.sorter import Sorter
from PixelSort.algorithm import *

np.random.seed(42)

def auto_scale(img, resolution=360):
    height, width = img.shape[0], img.shape[1]
    ratio = width / height
    new_height = min(height, resolution)
    new_width = int(ratio * new_height)
    return cv2.resize(img, (new_width, new_height))

def upsample(img, factor=3):
    height, width = img.shape[0], img.shape[1]
    res = cv2.resize(img, (int(width*factor), int(height*factor)), interpolation=cv2.INTER_NEAREST)
    return res

def main():
    parser = argparse.ArgumentParser(description='Visualize sorting algorithms on an image.')

    parser.add_argument('image_path', 
                        type=str, 
                        help='Path to the input image file')
    parser.add_argument('--resolution', 
                        type=int, 
                        default=360, 
                        help='Resample image to given resolution (image height)')
    parser.add_argument('--algorithm', 
                        type=str, 
                        choices=[
                            'bubble', 
                            'selection', 
                            'insertion', 
                            'quick',
                            'merge',
                            'heap',
                            'count'],
                        default='bubble', 
                        help='Sorting algorithm')
    parser.add_argument('--interval', 
                        type=int, 
                        default=10, 
                        help='Time interval between two frame (in miliseconds)')
    parser.add_argument('--step', 
                        type=int, 
                        default=1, 
                        help='Number of pixels swapped per frame')
    parser.add_argument('--sort_by_col', 
                        default=False, 
                        action='store_true', 
                        help='Sort by column instead of row')
    parser.add_argument('--split_rgb', 
                        default=False, 
                        action='store_true', 
                        help='Split image into RGB channels and sort each channel separately')
    parser.add_argument('--reverse', 
                        default=False, 
                        action='store_true', 
                        help='Sort pixel values in descending order')

    args = parser.parse_args()

    img = cv2.imread(args.image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = auto_scale(img, args.resolution)

    sort_algorithm = None
    if args.algorithm == 'bubble':
        sort_algorithm = bubble_sort
    elif args.algorithm == 'selection':
        sort_algorithm = selection_sort
    elif args.algorithm == 'insertion':
        sort_algorithm = insertion_sort
    elif args.algorithm == 'quick':
        sort_algorithm = quick_sort
    elif args.algorithm == 'merge':
        sort_algorithm = merge_sort
    elif args.algorithm == 'heap':
        sort_algorithm = heap_sort
    elif args.algorithm == 'count':
        sort_algorithm = counting_sort

    sorter = Sorter(img, 
                    sort_algorithm, 
                    step=args.step, 
                    sort_by_col=args.sort_by_col, 
                    split_rgb=args.split_rgb,
                    reverse=args.reverse)

    fps = 30
    upsample_factor = 3
    height, width = img.shape[0] * upsample_factor, img.shape[1] * upsample_factor
    image_name = os.path.splitext(os.path.basename(args.image_path))[0]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(f'assets\\{image_name}_{args.algorithm}.mp4', 
                                   fourcc, fps, (width, height))
    print('pixel sorting...')
    while not np.all(sorter.is_sorted):
        next_frame = sorter()
        next_frame = cv2.cvtColor(next_frame, cv2.COLOR_RGB2BGR)
        next_frame = upsample(next_frame, upsample_factor)
        output_video.write(next_frame)
    output_video.release()
    print('pixel sorting completed...')

if __name__ == '__main__':
    main()
