"""
Name : Brian Kwong and Trycia Vong
"""

from tools import *
import statistics


def process_header(header: str) -> bytes:
    header_binary = b""
    for i in range(0, len(header), 2):
        header_binary += int(header[i : i + 2], 16).to_bytes(1)
    return header_binary


def top_ten_duplicates(img_blocks: list):
    images = []
    for i in range(len(img_blocks)):
        block_freq = {}
        for block in img_blocks[i]:
            if block in block_freq:
                block_freq[block] += 1
            else:
                block_freq[block] = 1
        # Find the top 10 most frequent blocks for each image
        block_freq = dict(
            sorted(block_freq.items(), key=lambda x: (x[1], x[0]), reverse=True)
        )
        images.append([i, list(block_freq.values())[:10]])
    images = list(map(lambda x: [x[0], statistics.mean(x[1])], images))
    # Get the top average of the top 10 most frequent blocks
    images = sorted(images, key=lambda x: x[1], reverse=True)
    return images[:10]


try:
    with open("Lab2.TaskII.B.txt", "r") as f:
        data = f.readlines()
        header = data[0][:54]
        header = process_header(header)
        data_without_header = list(map(lambda x: x[54:], data))
        data_without_header = list(map(lambda x: hex_to_ascii(x), data_without_header))
        img_blocks = list(
            map(
                lambda x: [x[i : i + 16] for i in range(0, len(x), 16)],
                data_without_header,
            )
        )
        top_10_img = top_ten_duplicates(img_blocks)
        print(top_10_img)
        for img in top_10_img:
            with open("./output/{}.bmp".format(img[0]), "wb") as f:
                f.write(header + data_without_header[img[0]])
except FileNotFoundError:
    exit("File not found")
