def get_ksize(ksize, dilation=1):
    if dilation < 2:
        return ksize
    else:
        return (ksize - 1) * dilation + 1