from finite_fields import FieldElement
from secp256k1 import S256Point, PrivateKey
from point import Point
from signature import Signature

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
s1 = 5001
s2 = 2019**5
s3 = 0xdeadbeef54321


# corresponding public key
p1 = PrivateKey(s1)
p2 = PrivateKey(s2)
p3 = PrivateKey(s3)

# signature
r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

sig = Signature(r, s)
print(sig.der().hex())


# print(p1.point.sec().hex())
# print()
# print(p2.point.sec().hex())
# print()
# print(p3.point.sec().hex())