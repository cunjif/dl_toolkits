import numpy as np
from collections import namedtuple
from model import model, which, input_size
from utils import get_ksize

    
def calc_with_conv_pool(input_size: int, model: list)-> list:
    assert isinstance(model, list)
    assert len(model)

    outs = []
    for idx, layer in enumerate(model, 1):
        mode = layer[0]
        ksize, stride, padding = layer[1][:3]
        if len(layer[1]) == 4:
            ksize = get_ksize(ksize, layer[1][-1])
        input_size = int((input_size - ksize + 2 * padding) / stride + 1)
        outs.append((mode, idx, input_size))
    return outs

def calc_with_multi_ker_conv_pool(input_size: int, model: list)-> list:
    assert isinstance(model, list)
    assert len(model)

    outs = []
    for idx, layer in enumerate(model, 1):
        mode = layer[0]
        ksize, stride, padding = layer[1][:3]
        if len(layer[1]) == 4:
            if isinstance(ksize, (tuple, list)):
                ksize1 = get_ksize(ksize[0], layer[1][-1])
                ksize2 = get_ksize(ksize[1], layer[1][-1])
                input_size1 = int((input_size - ksize1 + 2 * padding) / stride + 1)
                input_size2 = int((input_size - ksize2 + 2 * padding) / stride + 1)
                outs.append((mode, idx, (input_size1, input_size2)))
            else:
                ksize = get_ksize(ksize, layer[1][-1])
                input_size = int((input_size - ksize + 2 * padding) / stride + 1)
                outs.append((mode, idx, (input_size, )))
        else:
            if isinstance(ksize, (tuple, list)):
                input_size1 = int((input_size - ksize[0] + 2 * padding) / stride + 1)
                input_size2 = int((input_size - ksize[1] + 2 * padding) / stride + 1)
                outs.append((mode, idx, (input_size1, input_size2)))
            else:
                input_size = int((input_size - ksize + 2 * padding) / stride + 1)
                outs.append((mode, idx, (input_size1, (input_size, ))))

    return outs


def calc(input_size, model, which=None):
    out = []
    if which is None:
        if len(input_size) == 2:
            result = zip(calc_with_conv_pool(input_size[0], model), calc_with_conv_pool(input_size[1], model))
            for (mode, idx, featsize1), (_, _, featsize2) in result:
                out.append((mode, idx, (featsize1, featsize2)))
                # print(F"{idx} {mode} layer's feature size -> {featsize1} x {featsize2}")
        elif len(input_size) == 1:
            result = calc_with_conv_pool(input_size[0], model)
            for mode, idx, featsize in result:
                out.append((mode, idx, (featsize, )))
                # print(F"{idx} {mode} layer's feature size -> {featsize} x {featsize}")
        else:
            raise Exception(F"Cant support input size {input_size} which length > 2")
    elif which is 'multi_ksize':
        pass
    
    return out

def output_results(result: list):
    assert len(result)
    assert isinstance(result, list)

    with open('featsizes.txt', mode='w+') as fp:
        for mode, idx, featsize in result:
            fp.write(F"[{idx}] {mode} layer's rf: {featsize}")
            fp.flush()


if __name__ == "__main__":
    calc(input_size, model, which)

        