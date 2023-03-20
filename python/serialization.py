import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def hash160(s):
  return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def hash256(s):
  '''two rounds of sha256'''
  return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def endoe_base58(s):
  count = 0
  for c in s:
    if c == 0:
      count += 1
    else:
      break
  num = int.from_bytes(s, 'big')
  prefix = '1' * count
  result = ''
  while num > 0:
    num, mod = divmod(num, 58)
    result = BASE58_ALPHABET[mod] + result
  return prefix + result

def encode_base58_checksum(b):
  return endoe_base58(b + hash256(b)[:4])

def decode_base58(s):
    '''Decode a Base58 string into an integer'''
    # Convert the string to an integer
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder='big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {}'.format(s))
    return combined[1:-4]