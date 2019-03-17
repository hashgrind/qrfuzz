import qrcode
import numpy as np
import argparse
import matplotlib.pyplot as plt
from codecs import encode


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mode", help="byte generator mode", type=str,
                        choices=['random', 'window', 'input', 'incremental'])
    parser.add_argument("-rs", "--random-seed", help="the rng seed (random mode)", type=int)
    parser.add_argument("-rn", "--random-number", help="number of bytes (random mode)", type=int)
    parser.add_argument("-wn", "--window-size", help="width of the byte window (window mode)", type=int)
    parser.add_argument("-ws", "--window-start", help="starting int (window mode)", type=int)
    parser.add_argument("-we", "--window-end", help="ending int (window mode)", type=int)
    parser.add_argument("-ib", "--input-bytes", help="input bytes (input mode)", type=str)

    argz = parser.parse_args()

    if argz.mode is None:
        argz.mode = "random"
    else:
        argz.mode = argz.mode.lower()

    return argz


def generate_image(bytez):
    return qrcode.make(bytez)


args = get_args()

if args.random_seed is not None:
    np.random.seed(args.random_seed)

while True:
    byte_data = None
    if 'random' == args.mode:
        byte_data = np.random.bytes(args.random_number)

    if 'window' == args.mode:
        byte_data = np.arange(args.window_start, args.window_end).tobytes()

    if 'input' == args.mode:
        byte_data = encode(args.input_bytes.encode().decode('unicode-escape'), 'raw_unicode_escape')

    print(byte_data)

    img = generate_image(byte_data)
    plt.imshow(img)
    plt.show()

    if "window" == args.mode:
        args.window_start += 1
        args.window_end += 1
