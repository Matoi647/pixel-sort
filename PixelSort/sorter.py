import numpy as np
import cv2

class Sorter:
    """
    Image Sorter
    :param image: Input image, ndarray
    :param algorithm: Sorting algorithm
    :param step: Comparision times or swap times of pixels for each frame
    :param sort_by_col: Sort by column instead of row
    :param split_rgb: Split image into RGB channels and sort each channel separately
    :param reverse: Sort pixel values in descending order
    """
    def __init__(self, image, algorithm, step=5, sort_by_col=False, split_rgb=False, reverse=False):
        self.img = np.copy(image)
        self.sort_func = algorithm
        self.step = step
        self.sort_by_col = sort_by_col
        if self.sort_by_col:
            self.img = cv2.transpose(self.img)
        self.split_rgb = split_rgb
        self.is_sorted = []

        ndim = self.img.ndim
        height = self.img.shape[0]
        width = self.img.shape[1]
        n_channels = self.img.shape[2] if ndim==3 else 1
        is_rgb = ndim > 2
        
        self.img_channels = []
        self.row_sorter_list = []
        if is_rgb and self.split_rgb:  # split and sort each RGB channel
            self.is_sorted = np.zeros((n_channels, height), dtype=bool)
            self.img_channels = np.split(self.img, n_channels, axis=2)
            self.row_sorter_list = []
            for c in range(n_channels):
                channel_row_sorter_list = []
                for row in range(height):
                    channel_row_sorter_list.append(
                        algorithm(self.img_channels[c][row], 
                                  step=step, 
                                  is_rgb=False, 
                                  reverse=reverse))
                self.row_sorter_list.append(channel_row_sorter_list)
        else:
            self.is_sorted = np.zeros(height, dtype=bool)
            for row in range(height):
                self.row_sorter_list.append(
                    algorithm(self.img[row], 
                              step=step, 
                              is_rgb=is_rgb,
                              reverse=reverse))

    def __call__(self):
        if self.split_rgb:  # split and sort each RGB channel
            n_channels = self.img.shape[2] if self.img.ndim==3 else 1
            for c in range(n_channels):
                for row, sorter in enumerate(self.row_sorter_list[c]):
                    if not self.is_sorted[c][row]:
                        try:
                            next_channel_row = next(sorter)
                        except StopIteration:
                            next_channel_row = self.img_channels[c][row]
                            self.is_sorted[c][row] = True
                            # print(f'channel={c},row={row} sort completed')
                        self.img_channels[c][row] = next_channel_row

                        # if np.all(self.is_sorted):
                        #     print('image sort completed.')
            res = np.dstack(tuple(self.img_channels))
            if self.sort_by_col:
                return cv2.transpose(res)
            else:
                return res
        else:
            for row, sorter in enumerate(self.row_sorter_list):
                if not self.is_sorted[row]:
                    next_img_row = []
                    try:
                        next_img_row = next(sorter)
                    except StopIteration:
                        next_img_row = self.img[row]
                        self.is_sorted[row] = True
                        # print(f'row={row} sort completed')
                    self.img[row] = next_img_row

                    # if np.all(self.is_sorted):
                    #     print('image sort completed.')
            if self.sort_by_col:
                return cv2.transpose(self.img)
            else:
                return self.img