from finite_fields import FieldElement
from secp256k1 import S256Point, PrivateKey
from point import Point

prime = 2**256 - 2**32 - 977
a = FieldElement(0 , prime)
b = FieldElement(7 , prime)
px = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
py = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
x = FieldElement(px, prime)
y = FieldElement(py, prime)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

G = S256Point(x, y)
G2 = Point(x, y, a, b)
G3 = S256Point(px, py)

# secrets
s1 = 5000
s2 = 2018**5
s3 = 0xdeadbeef12345

# corresponding public key
p1 = PrivateKey(s1)
p2 = PrivateKey(s2)
p3 = PrivateKey(s3)

print(p1.point.sec().hex())
print()
print(p2.point.sec().hex())
print()
print(p3.point.sec().hex())