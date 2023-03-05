from python.helper import int_to_little_endian, little_endian_to_int, read_varint
from python.serialization import hash160, hash256

def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True

def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))
    return True

def op_hash256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True

OP_CODE_FUNCTIONS = {
    76: op_hash160,
    170: op_hash256,
    118: op_dup,
}

class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            cmds = []
        else:
            self.cmds = cmds

    def __add__(self, other):
        return Script(self.cmds + other.cmds)

    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            if type(cmd) == int:
                result += int_to_little_endian(cmd, 1)
            else:
                length = len(cmd)
                if length < 75:
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif length >= 0x100 and length < 520:
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError('too long')
                result += cmd
        return result

    @classmethod
    def parse(cls, stream):
        length = read_varint(stream)
        cmds = []
        count = 0
        while count < length:
            current = stream.read(1)
            count += 1
            current_byte = current[0]
            if current_byte >= 1 and current_byte <= 75:
                n = current_byte
                cmds.append(stream.read(n))
                count += n
            elif current_byte == 76:
                data_length = little_endian_to_int(stream.read(1))
                cmds.append(stream.read(data_length))
                count += data_length + 1
            elif current_byte == 77:
                data_length = little_endian_to_int(stream.read(2))
                cmds.append(stream.read(data_length))
                count += data_length + 2
            else:
                op_code = current_byte
                cmds.append(op_code)
        
        if count != length:
            raise SyntaxError('parsing script failed')
        
        return cls(cmds)