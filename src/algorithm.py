import numpy as np

def cmp_pixel(a, b, is_rgb=True):
    res = 0
    if is_rgb:  # sort by average RGB value
        aa = int(a[0]) + int(a[1]) + int(a[1])
        bb = int(b[0]) + int(b[1]) + int(b[1])
        # sort by HSV, weight: V > H > S
        # aa = a[2] * 2**16 + a[0] * 2**8 + a[1]
        # bb = b[2] * 2**16 + b[0] * 2**8 + b[1]
        res = int(aa) - int(bb)
    else:       # sort single channel
        if isinstance(a, np.ndarray):
            res = int(a[0]) - int(b[0])
        else:
            res = int(a) - int(b)
    return res

def swap_pixel(a, b):
    tmp = np.copy(a)
    a = np.copy(b)
    b = tmp
    return a, b

def bubble_sort(arr, step=10, is_rgb=True, reverse=False):
    res = np.copy(arr)
    n = len(res)
    count = 0   # swap times
    step = step
    flag = -1 if reverse else 1
    for i in range(n - 1):
        for j in range(n - 1, i, -1):
            if flag * cmp_pixel(res[j-1], res[j], is_rgb=is_rgb) > 0:
                res[j-1], res[j] = swap_pixel(res[j-1], res[j])
                count += 1
                if count % step == 0:
                    yield res

def selection_sort(arr, step=1, is_rgb=True, reverse=False):
    res = np.copy(arr)
    n = len(res)
    count = 0   # swap times
    flag = -1 if reverse else 1
    for i in range(n):
        max_index = i
        for j in range(i + 1, n):
            if flag * cmp_pixel(res[j], res[max_index], is_rgb=is_rgb) < 0:
                max_index = j
                
        res[i], res[max_index] = swap_pixel(res[i], res[max_index])
        count += 1
        if count % step == 0:
            yield res

def insertion_sort(arr, step=10, is_rgb=True, reverse=False):
    res = np.copy(arr)
    n = len(res)
    count = 0   # swap times
    flag = -1 if reverse else 1
    for i in range(1, n):
        key = np.copy(res[i])
        j = i - 1

        while j >= 0 and flag * cmp_pixel(key, res[j], is_rgb=is_rgb) < 0:
            res[j + 1] = np.copy(res[j])
            j -= 1
            count += 1
            if count % step == 0:
                yield res

        res[j + 1] = np.copy(key)
        count += 1
        if count % step == 0:
            yield res

def quick_sort(arr, step=1, is_rgb=True, reverse=False):
    res = np.copy(arr)
    n = len(res)
    count = 0   # swap times
    flag = -1 if reverse else 1

    def quick_sort_aux(left, right):
        nonlocal count  # modify the value of the outer variable `count`
        if left >= right:
            return
        pivot = np.copy(res[right])
        i = left - 1
        for j in range(left, right):
            if flag * cmp_pixel(res[j], pivot, is_rgb=is_rgb) < 0:
                i += 1
                res[i], res[j] = swap_pixel(res[i], res[j])
                count += 1
                if count % step == 0:
                    yield res
        res[i+1], res[right] = swap_pixel(res[i+1], res[right])
        count += 1
        if count % step == 0:
            yield res
        pivot = i+1
        yield from quick_sort_aux(left, pivot-1)
        yield from quick_sort_aux(pivot+1, right)
    
    yield from quick_sort_aux(0, n-1)
