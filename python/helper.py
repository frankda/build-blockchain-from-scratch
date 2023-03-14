SIGHASH_ALL = 1

def little_endian_to_int(b):
    return int.from_bytes(b, 'little')

def int_to_little_endian(n, length):
    return n.to_bytes(length, 'little')

def read_varint(s):
    '''read_varint reads a variable integer from a stream'''
    i = s.read(1)[0]
    if i == 0xfd:
        # 0xfd means the next 2 bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        # 0xfe means the next 4 bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        # 0xff means the next 8 bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        # anything else is just the number
        return i
    
def encode_varint(i):
    '''encode_varint encodes a number as a variable integer'''
    if i < 0xfd:
        return int_to_little_endian(i, 1)
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise RuntimeError('integer too large: {}'.format(i))
    