from tools import *

try:
    with open("Lab2.TaskII.B.txt", "r") as f:
        data = f.readlines()
        header = data[0][:54]
        data_without_header = list(map(lambda x: x[54:], data))
        data_without_header = list(map(lambda x: hex_to_ascii(x), data_without_header))
except FileNotFoundError:
    exit("File not found")
