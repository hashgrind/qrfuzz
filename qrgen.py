import qrcode
import numpy as np
import argparse
import matplotlib.pyplot as plt
from codecs import encode


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mode", help="generation mode (random, incremental, input)", type=str)
    parser.add_argument("-s", "--size", help="number of bytes", type=int)
    parser.add_argument("-e", "--seed", help="the rng seed", type=int)
    parser.add_argument("-b", "--bytes", help="input bytes", type=str)

    argz = parser.parse_args()

    if argz.mode is None:
        argz.mode = "random"
    else:
        argz.mode = argz.mode.lower()

    return argz


def generate_image(bytez):
    return qrcode.make(bytez)


def get_bytes(qty, mode, start, end, bytez):
    if 'random' == mode:
        return np.random.bytes(qty)

    if 'incremental' == mode:
        return np.arange(start, end).tobytes()

    if 'input' == mode:
        return encode(bytez.encode().decode('unicode-escape'), 'raw_unicode_escape')

    return None


args = get_args()

if args.seed is not None:
    np.random.seed(args.seed)

byte_start = 0
byte_end = 0
if "incremental" == args.mode:
    byte_end = args.size - 1

while True:
    byte_data = get_bytes(qty=args.size, mode=args.mode, start=byte_start, end=byte_end, bytez=args.bytes)

    print(byte_data)

    img = generate_image(byte_data)
    plt.imshow(img)
    plt.show()

    if "incremental" == args.mode:
        byte_start += 1
        byte_end += 1
