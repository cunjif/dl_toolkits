''' Receptive field calculation tools '''

from functools import reduce
from model import model


def calc_rf(f_p: int, k_c: int, s_p_list: list):
    ''' calc specific layer receptive field '''
    return f_p + (k_c - 1)*reduce(lambda s,x: s*x, s_p_list)


def main(models: list):
    if len(models) == 0:
        return 0
    
    if not isinstance(models[0], (list, tuple)):
        return models[0]

    stride_list = [m[-1] for m in models]

    receptive_fields = []
    for idx, model in enumerate(models, 1):
        if idx == 1:
            receptive_fields.append(model[0])
            continue
        receptive_fields.append(calc_rf(
            receptive_fields[-1], model[0], stride_list[:idx-1]))

    return receptive_fields


if __name__ == '__main__':
    res = main(model)
    if isinstance(res, list):
        with open('receptive fields.txt', mode='w+') as fp:
            fp.write(str(dict(enumerate(res, 1))))
            fp.flush()
    else:
        print(res)