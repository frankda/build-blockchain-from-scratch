from finite_fields import FieldElement
from point import Point

P = 2**256 - 2**32 - 977
A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

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