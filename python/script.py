from helper import int_to_little_endian, little_endian_to_int, read_varint, encode_varint
from serialization import hash160, hash256
from logging import getLogger
from op import (
    OP_CODE_FUNCTIONS,
    OP_CODE_NAMES,
)


LOGGER = getLogger(__name__)

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

class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    def __add__(self, other):
        return Script(self.cmds + other.cmds)
    
    def __repr__(self):
        result = []
        for cmd in self.cmds:
            if type(cmd) == int:
                if OP_CODE_NAMES.get(cmd):
                    name = OP_CODE_NAMES.get(cmd)
                else:
                    name = 'OP_[{}]'.format(cmd)
                result.append(name)
            else:
                result.append(cmd.hex())
        return ' '.join(result)

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
    
    def evaluate(self, z):
        cmds = self.cmds[:]
        stack = []
        altstack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if type(cmd) == int:
                operation = OP_CODE_FUNCTIONS[cmd]
                if cmd in (99, 100):  # <4>
                    if not operation(stack, cmds):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (107, 108):  # <5>
                    if not operation(stack, altstack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (172, 173, 174, 175):  # <6>
                    if not operation(stack, z):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                else:
                    if not operation(stack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
            
            else:
                stack.append(cmd)
        
        if len(stack) == 0:
            return False
        if stack.pop() == b'':
            return False
        return True


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
    
    def serialize(self):
        # get the raw serialization (no prepended length)
        result = self.raw_serialize()
        # get the length of the whole thing
        total = len(result)
        # encode_varint the total length of the result and prepend
        return encode_varint(total) + result
    
def p2pkh_script(h160):
    '''Takes a hash160 and returns the p2pkh ScriptPubKey''' 
    return Script([0x76, 0xa9, h160, 0x88, 0xac])