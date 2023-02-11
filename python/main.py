from finite_fields import FieldElement
from secp256k1 import S256Point
from point import Point

prime = 2**256 - 2**32 - 977
a = FieldElement(0 , prime)
b = FieldElement(7 , prime)
px = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
py = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
x = FieldElement(px, prime)
y = FieldElement(py, prime)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

G = Point(x, y, a, b)

G2 = S256Point(x, y)
G3 = S256Point(px, py)

print(n*G3)