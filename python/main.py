from finite_fields import FieldElement
from secp256k1 import S256Point, PrivateKey
from point import Point
from signature import Signature
from serialization import endoe_base58
from script import Script

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
s1 = 5003
s2 = 2021**5
s3 = 0x12345deadbeef


# corresponding public key
p1 = PrivateKey(s1)
p2 = PrivateKey(s2)
p3 = PrivateKey(s3)

# signature
r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

# sig = Signature(r, s)
# print(sig.der().hex())


# print(p1.point.sec().hex())
# print()
# print(p2.point.sec().hex())
# print()
# print(p3.point.sec().hex())

# conver hex value to Base58
h1 = '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'
# print(endoe_base58(bytes.fromhex(h1)))

# find addresss for above private keys
# print(p1.point.address(compressed=False, testnet=True))
# print(p2.point.address(compressed=True, testnet=True))
# print(p3.point.address(compressed=True, testnet=False))

# find WIF for private key
# print(p1.wif(compressed=True, testnet=True))
# print(p2.wif(compressed=False, testnet=True))

z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
sec = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e\
4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34')
sig = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f4048\
76325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fd\
dbdce6feab601')

script_pubkey = Script([sec, 0xac])
script_sig = Script([sig])
combined_script = script_sig + script_pubkey
print(combined_script.evaluate(z))