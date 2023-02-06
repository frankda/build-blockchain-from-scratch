class Point:
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        if self.x is None and self.y is None:
            return

        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError('({}, {}) is not on the curve'.format(x, y))
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b
    
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.a != other.a or self.b != other.b
    
    def __add__(self, other):
      if self.a != other.a or self.b != other.b:
        raise TypeError('Points {}, {} are not on the same curve'.format(self, other))
      
      if self.x is None:
        return other
      
      if other.x is None:
        return self
      
      if self.x == other.x and self.y != other.y:
        return self.__class__(None, None, self.a, self.b)
      
      if self.x != other.x:
        s = (other.y - self.y) / (other.x - self.x)
        x = s**2 - self.x - other.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.a, self.b)
      
      if self.x == other.x and self.y == other.y:
        s = (3 * self.x**2 + self.a) / (2 * self.y)
        x = s**2 - 2 * self.x
        y = s * (self.x - x) - self.y
        return self.__class__(x, y, self.a, self.b)
      
      if self == other and self.y == 0:
         return self.__class__(None, None, self.a, self.b)