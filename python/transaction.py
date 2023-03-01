from python.helper import read_varint
from python.serialization import hash256
from helper import little_endian_to_int, int_to_little_endian


class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet
    
    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        
        return 'tx: {}\nversion: {}\ntx_ins: {}\ntx_outs: {}\nlocktime: {}\n'.format(
            self.id(),
            self.version,
            tx_ins,
            tx_outs,
            self.locktime,
        )
    
    def id(self):
        '''Human-readable hexadecimal of the transaction hash'''
        return self.hash().hex()
    
    def hash(self):
        '''Binary hash of the legacy transaction'''
        return hash256(self.serialize())[::-1]

    @classmethod
    def parse(cls, stream, testnet=False):
        serialized_version = stream.read(4)
        version = little_endian_to_int(serialized_version)
        num_inputs = read_varint(stream)
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(stream))
        num_outputs = read_varint(stream)
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxOut.parse(stream))
        locktime = little_endian_to_int(stream.read(4))
        return cls(version, None, None, None, testnet=testnet)
    
class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence
    
    def __repr__(self):
        return '{}:{}'.format(self.prev_tx.hex(), self.prev_index)
    
    @classmethod
    def parse(cls, stream):
        '''Takes a byte stream and parses the tx_ins at the start.
        Returns a TxIn object
        '''
        prev_tx = stream.read(32)[::-1]
        prev_index = little_endian_to_int(stream.read(4))
        script_sig = Script.parse(stream)
        sequence = little_endian_to_int(stream.read(4))
        return cls(prev_tx, prev_index, script_sig, sequence)

class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey
    
    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)
    
    @classmethod
    def parse(cls, stream):
        '''Takes a byte stream and parses the tx_outs at the start.
        Returns a TxOut object
        '''
        amount = little_endian_to_int(stream.read(8))
        script_pubkey = Script.parse(stream)
        return cls(amount, script_pubkey)