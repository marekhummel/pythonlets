from typing import List, Tuple

Color = Tuple[int, int, int]


def create_ppm_file(image: List[List[Color]], path: str, width: int, height: int):
    with open(path, mode="w") as f:
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")

        for y in range(height):
            for x in range(width):
                r, g, b = image[y][x]
                f.write(f"{r} {g} {b}\n")
