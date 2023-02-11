from finite_fields import FieldElement
from signature import Signature
from point import Point

P = 2**256 - 2**32 - 977  # prime
A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141  # group nG = 0

class S256Field(FieldElement):
  def __init__(self, num, prime=None):
    super().__init__(num, prime=P)
    
  def __repr__(self):
    return '{:x}'.format(self.num).zfill(64)
  

class S256Point(Point):
  def __init__(self, x, y, a=None, b=None):
    a, b = S256Field(A), S256Field(B)
    if type(x) == int:
      super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
    else:
      super().__init__(x=x, y=y, a=a, b=b)

  def __rmul__(self, coefficient):
    coef = coefficient % N
    return super().__rmul__(coefficient)

  # z is fingerprint derived from secret, used to create signature
  def verify(self, z, sig):
    s_inv = pow(sig.s, N - 2, N)  # Fermat’s little theorem
    u = z * s_inv % N
    v = sig.r * s_inv % N
    total = u * G + v * self  # uG + vP = R
    return total.x.num == sig.r

G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)