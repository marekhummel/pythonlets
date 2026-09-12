# https://www.youtube.com/watch?v=fKLMM4V3bKE
# Using complex numbers to compute the area of a triangle.

from math import sqrt

A = (1, 2)
B = (6, 3)
C = (3, 7)


def distance(point_1, point_2):
    return sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)


side_ab = distance(A, B)
side_bc = distance(B, C)
side_ca = distance(C, A)
semi_perimeter = (side_ab + side_bc + side_ca) / 2
area_heron = sqrt(
    semi_perimeter
    * (semi_perimeter - side_ab)
    * (semi_perimeter - side_bc)
    * (semi_perimeter - side_ca)
)

print(f"AB = {side_ab:.3f}")
print(f"BC = {side_bc:.3f}")
print(f"CA = {side_ca:.3f}")
print(f"Area using Heron's formula = {area_heron:.3f}")

# Translate the triangle so that A becomes the origin.
z = complex(B[0] - A[0], B[1] - A[1])
w = complex(C[0] - A[0], C[1] - A[1])
area_complex = abs((z.conjugate() * w).imag) / 2

print(f"Area using complex numbers = {area_complex:.3f}")
