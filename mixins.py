from receptive_field import calc as rf_calc
from featsize import calc as feat_calc


def calc(input_size, model, which=None):
    rfs = rf_calc(model, which)
    feats = feat_calc(input_size, model, which)

    out = []
    for i in range(len(feats)):
        mode, idx, feat = feats[i]
        _, _, rf = rfs[i]

        out.append((mode, idx, feat, rf))

    return out


def output_result(result):
    # assert isinstance(result, iter)

    with open('mix_feat_rf.txt', mode='w+') as fp:
        for mode, idx, feat, rf in result:
            fp.write(F'【{idx}】{mode} layer feat -> {feat} and rf -> {rf} \n')
            fp.flush
    print('success')


if __name__ == "__main__":
    from model import input_size, model, which
    import os
    import sys

    res = calc(input_size, model, which)
    output_result(res)
    
    if sys.platform == 'win32':
        print('aaa')
        os.system('start mix_feat_rf.txt')