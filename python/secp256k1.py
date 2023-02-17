from random import randint
from finite_fields import FieldElement
from signature import Signature
from point import Point
from serialization import hash160, encode_base58_checksum

P = 2**256 - 2**32 - 977  # prime
A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141  # group nG = 0

class S256Field(FieldElement):
  def __init__(self, num, prime=None):
    super().__init__(num, prime=P)
    
  def __repr__(self):
    return '{:x}'.format(self.num).zfill(64)
  
  def sqrt(self):
    return self**((P + 1) // 4)

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

  def sec(self, compressed=True):
    '''return sthe binay version of the SEC format'''
    if compressed:
      if self.y.num % 2 == 0:
        return b'\x02' + self.x.num.to_bytes(32, 'big')
      else:
        return b'\x03' + self.x.num.to_bytes(32, 'big')
    else:
      return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')
  
  def hash160(self, compressed=True):
    return hash160(self.sec(compressed))

  def address(self, compressed=True, testnet=False):
    '''returns the address string'''
    h160 = self.hash160(compressed)
    if testnet:
      prefix = b'\x6f'
    else:
      prefix = b'\x00'
    return encode_base58_checksum(prefix + h160)
  
  @classmethod
  def parse(self, sec_bin):
    '''returns a Point object from a SEC binary (not hex)'''
    if sec_bin[0] == 4:
      x = int.from_bytes(sec_bin[1:33], 'big')
      y = int.from_bytes(sec_bin[33:65], 'big')
      return S256Point(x=x, y=y)
    
    is_even = sec_bin[0] == 2
    x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
    # right side of the equation y^2 = x^3 + 7
    alpha = x**3 + S256Field(B)
    # solve for left side
    beta = alpha.sqrt()
    if beta.num % 2 == 0:
      even_beta = beta
      odd_beta = S256Field(P - beta.num)
    else:
      even_beta = S256Field(P - beta.num)
      odd_beta = beta

    if is_even:
      return S256Point(x, even_beta)
    else:
      return S256Point(x, odd_beta)

class PrivateKey:
  def __init__(self, secret):
    self.secret = secret
    self.point = secret * G
  
  def hex(self):
    return '{:x}'.format(self.secret).zfill(64)

  def sign(self, z):
    # Don't use this random in production because it's not random enough
    # use RFC6979 instead
    k = randint(0, N)
    r = (k * G).x.num
    k_inv = pow(k, N - 2, N)
    s = (z + r * self.secret) * k_inv % N
    if s > N/2:
      s = N - s
      return Signature(r, s)

G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)


