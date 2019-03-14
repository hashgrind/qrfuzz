# TODO: Improve in every conceivable way. :)

import qrcode
import os
import sys
import numpy as np
import hashlib


def setup_check(args):
    if 4 != len(args):
        print("Usage:", args[0], '<numImages> <bytesPerCode> <outputDir>')
        sys.exit(1)


def generate_image(bytez):
    return qrcode.make(bytez)


def get_bytes(qty):
    return np.random.bytes(qty)


def get_output_filename(out_dir, bytez):
    return os.path.join(out_dir, hashlib.sha256(bytez).hexdigest() + '.png')


setup_check(sys.argv)

num_images = int(sys.argv[1])
num_bytes = int(sys.argv[2])
output_dir = sys.argv[3]

for i in range(num_images):
    byte_data = get_bytes(num_bytes)
    img = generate_image(byte_data)
    output_file_name = get_output_filename(output_dir, byte_data)
    img.save(output_file_name)
