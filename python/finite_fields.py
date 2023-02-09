class FieldElement:
  def __init__(self, num, prime):
    if num >= prime or num < 0:
      error = 'Num {} not in field range 0 to {}'.format(num, prime - 1)
      raise ValueError(error)
    
    self.num = num
    self.prime = prime
  
  # Output meaningful string when print class object
  def __repr__(self):
    return 'FieldElement_{}({})'.format(self.prime, self.num)
  
  def __eq__(self, other):
    if other is None:
      return False
    return self.num == other.num and self.prime == other.prime
  
  def __ne__(self, other):
    if self.num != other.num or self.prime != other.prime:
      return True
    return False
  
  def __add__(self, other):
    if self.prime != other.prime:
        raise TypeError('Cannot add two numbers in different Fields')
    num = (self.num + other.num) % self.prime 
    return self.__class__(num, self.prime)

  def __sub__(self, other):
    if self.prime != other.prime:
        raise TypeError('Cannot add two numbers in different Fields')
    num = (self.num - other.num) % self.prime 
    return self.__class__(num, self.prime)
  
  def __mul__(self, other):
    if self.prime != other.prime:
        raise TypeError('Cannot multiply two numbers in different Fields')
    num = (self.num * other.num) % self.prime
    return self.__class__(num, self.prime)
  
  def __rmul__(self, coefficient):
    num = (self.num * coefficient) % self.prime
    return self.__class__(num=num, prime=self.prime)

  def __pow__(self, exponent):
    n = exponent % (self.prime - 1)
    num = pow(self.num, n, self.prime)
    return self.__class__(num, self.prime)

  def __truediv__(self, other):
    if self.prime != other.prime:
      raise TypeError('Cannot divide two numbers in different Fields')

    num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
    return self.__class__(num, self.prime)

a = FieldElement(2, 31)
b = FieldElement(2, 31)
c = FieldElement(15, 31)
