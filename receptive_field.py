''' Receptive field calculation tools '''

from functools import reduce
from model import model
from utils import get_ksize


def calc_rf(f_p: int, k_c: int, s_p_list: list):
    ''' calc specific layer receptive field '''
    return f_p + (k_c - 1)*reduce(lambda s,x: s*x, s_p_list)


def calc(model, which=None):
    assert isinstance(model, list)
    assert len(model) > 0

    stride_list = [m[-1][1] for m in model]
    receptive_fields = []

    if which is None:
        for idx, m in enumerate(model, 1):
            mode = m[0]
            layer = m[1]
            ksize = get_ksize(layer[0], dilation=layer[-1])
            if idx == 1:
                receptive_fields.append((mode, idx, (layer[0], layer[0])))
                continue

            rf = calc_rf(receptive_fields[-1][-1][0], ksize, stride_list[:idx-1])
            receptive_fields.append((mode, idx, (rf, rf)))
    elif which is "multi_ksize":
        for idx, m in enumerate(model, 1):
            mode = m[0]
            layer = m[1]

            if isinstance(layer[-1], (tuple, list)):
                ksize1 = get_ksize(layer[0][0], dilation=layer[-1][0])
                ksize2 = get_ksize(layer[0][1], dilation=layer[-1][1])
            else:
                ksize1 = get_ksize(layer[0][0], dilation=layer[-1])
                ksize2 = get_ksize(layer[0][1], dilation=layer[-1])

            if idx == 1:
                receptive_fields.append((mode, idx, (layer[0][0], layer[0][1])))
                continue

            rf1 = calc_rf(receptive_fields[-1][-1][0], ksize1, stride_list[:idx-1])
            rf2 = calc_rf(receptive_fields[-1][-1][1], ksize2, stride_list[:idx-1])
            receptive_fields.append((mode, idx, (rf1, rf2)))

    return receptive_fields


def output_result(result):
    assert len(result)
    assert isinstance(result, list)

    with open('receptive.txt', mode='w+') as fp:
        for mode, idx, rf in result:
            fp.write(F"[{idx}] {mode} layer's rf -> {rf}")
            fp.flush()


if __name__ == '__main__':
    # res = main(model)
    # if isinstance(res, list):
    #     with open('receptive fields.txt', mode='w+') as fp:
    #         fp.write(str(dict(enumerate(res, 1))))
    #         fp.flush()
    # else:
    #     print(res)
    from model import which, model
    res = calc(model, which)
    output_result(res)