import qrcode
import numpy as np
import argparse
import matplotlib.pyplot as plt
from codecs import encode
import sys
import math


class RandomByteGenerator:
    def __init__(self, args):
        self.args = args

        if self.args.random_seed is not None:
            np.random.seed(self.args.random_seed)

    def get_bytes(self):
        return np.random.bytes(self.args.random_number)

    def iteration_end(self):
        pass


class WindowByteGenerator:
    def __init__(self, args):
        self.args = args

    def get_bytes(self):
        return np.arange(args.window_start, args.window_end).tobytes()

    def iteration_end(self):
        self.args.window_start += 1
        self.args.window_end += 1


class InputByteGenerator:
    def __init__(self, args):
        self.args = args

    def get_bytes(self):
        return byte_string_to_bytes(self.args.input_bytes)

    def iteration_end(self):
        pass


class NullByteGenerator:
    def __init__(self, args):
        self.args = args

        self.null_data = None
        self.null_bytes = bytes(1)
        if self.args.null_bytes is not None:
            self.null_bytes = byte_string_to_bytes(self.args.null_bytes)

        if self.null_data is None:
            self.null_data = byte_string_to_bytes(self.args.null_input)

    def get_bytes(self):
        return self.null_data

    def iteration_end(self):
        if 'end' == self.args.null_mode:
            self.null_data += self.null_bytes
        elif 'start' == self.args.null_mode:
            self.null_data = self.null_bytes + self.null_data
        elif 'center' == self.args.null_mode:
            self.null_data = self.null_bytes + self.null_data + self.null_bytes
        elif 'spread' == args.null_mode:
            null_insertion_point = np.random.randint(0, len(self.null_data))
            self.null_data = self.null_data[:null_insertion_point] + self.null_bytes + self.null_data[
                                                                                       null_insertion_point:]


class IncrementalByteGenerator:
    def __init__(self, args):
        self.args = args

        self.incremental_byte = None
        if self.args.incremental_start is not None:
            self.incremental_byte = int.from_bytes(byte_string_to_bytes(self.args.incremental_start), sys.byteorder)
        self.incremental_multiple = 1
        if self.args.incremental_multiple is not None:
            self.incremental_multiple = self.args.incremental_multiple

    def get_bytes(self):
        return self.incremental_byte.to_bytes(self.incremental_multiple * math.ceil(self.incremental_byte / 255), sys.byteorder)

    def iteration_end(self):
        self.incremental_byte += 1


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mode", help="byte generator mode", type=str,
                        choices=['random', 'window', 'input', 'null', 'incremental'])
    parser.add_argument("-rs", "--random-seed", help="the rng seed (random mode)", type=int)
    parser.add_argument("-rn", "--random-number", help="number of bytes (random mode)", type=int)
    parser.add_argument("-wn", "--window-size", help="width of the byte window (window mode)", type=int)
    parser.add_argument("-ws", "--window-start", help="starting int (window mode)", type=int)
    parser.add_argument("-we", "--window-end", help="ending int (window mode)", type=int)
    parser.add_argument("-ib", "--input-bytes", help="input bytes (input mode)", type=str)
    parser.add_argument("-ni", "--null-input", help="starting bytes (null mode)", type=str)
    parser.add_argument("-nm", "--null-mode", help="null mode", type=str, choices=['start', 'end', 'center', 'spread'])
    parser.add_argument("-nb", "--null-bytes", help="null bytes (null mode)", type=str)
    parser.add_argument("-is", "--incremental-start", help="starting bytes (incremental mode)", type=str)
    parser.add_argument("-im", "--incremental-multiple", help="byte multiple (incremental mode)", type=int)

    argz = parser.parse_args()

    if argz.mode is None:
        argz.mode = "random"
    else:
        argz.mode = argz.mode.lower()

    return argz


def generate_image(bytez):
    return qrcode.make(bytez)


def show_image(image):
    plt.imshow(image)
    plt.show()


def byte_string_to_bytes(byte_string):
    return encode(byte_string.encode().decode('unicode-escape'), 'raw_unicode_escape')


args = get_args()


byte_generator = None
if 'random' == args.mode:
    byte_generator = RandomByteGenerator(args)
elif 'window' == args.mode:
    byte_generator = WindowByteGenerator(args)
elif 'input' == args.mode:
    byte_generator = InputByteGenerator(args)
elif 'null' == args.mode:
    byte_generator = NullByteGenerator(args)
elif 'incremental' == args.mode:
    byte_generator = IncrementalByteGenerator(args)

while True:
    byte_data = byte_generator.get_bytes()

    print(byte_data)

    img = generate_image(byte_data)
    show_image(img)

    byte_generator.iteration_end()
