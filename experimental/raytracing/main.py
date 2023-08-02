# import numpy as np
import ppm

w, h = 256, 256
image = [[None for _ in range(w)] for _ in range(h)]

for j in range(h - 1, -1, -1):
    for i in range(w):
        r = int(i / (w - 1) * 255)
        g = int(j / (h - 1) * 255)
        b = int(0.25 * 255)
        image[j][i] = (r, g, b)

ppm.create_ppm_file(image, "test.ppm", w, h)
