from io import BytesIO
from finite_fields import FieldElement
from transaction import Tx, TxIn, TxOut
from secp256k1 import S256Point, PrivateKey
from point import Point
from signature import Signature
from serialization import endoe_base58, decode_base58
from script import Script, p2pkh_script

prime = 2**256 - 2**32 - 977
a = FieldElement(0 , prime)
b = FieldElement(7 , prime)
px = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
py = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
x = FieldElement(px, prime)
y = FieldElement(py, prime)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

G = S256Point(x, y)
G2 = Point(x, y, a, b)
G3 = S256Point(px, py)

# secrets
s1 = 5003
s2 = 2021**5
s3 = 0x12345deadbeef


# corresponding public key
p1 = PrivateKey(s1)
p2 = PrivateKey(s2)
p3 = PrivateKey(s3)

# signature
r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

# sig = Signature(r, s)
# print(sig.der().hex())


# print(p1.point.sec().hex())
# print()
# print(p2.point.sec().hex())
# print()
# print(p3.point.sec().hex())

# conver hex value to Base58
h1 = '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'
# print(endoe_base58(bytes.fromhex(h1)))

# find addresss for above private keys
# print(p1.point.address(compressed=False, testnet=True))
# print(p2.point.address(compressed=True, testnet=True))
# print(p3.point.address(compressed=True, testnet=False))

# find WIF for private key
# print(p1.wif(compressed=True, testnet=True))
# print(p2.wif(compressed=False, testnet=True))

# --------
# z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
# sec = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e\
# 4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34')
# sig = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f4048\
# 76325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fd\
# dbdce6feab601')

# script_pubkey = Script([sec, 0xac])
# script_sig = Script([sig])
# combined_script = script_sig + script_pubkey
# print(combined_script.evaluate(z))

# --------
# Example of creating a ScriptSig that can unlock this ScriptPubKey 767695935687
'''
script_pubkey = Script([0x76, 0x76, 0x95, 0x93, 0x56, 0x87])
script_sig = Script([0x52])
combined_script = script_sig + script_pubkey
print(combined_script.evaluate(0))
'''

# --------
'''
script_pubkey = Script([0x6e, 0x87, 0x91, 0x69, 0xa7, 0x7c, 0xa7, 0x87])
c1 = '255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f576964746820\
32203020522f4865696768742033203020522f547970652034203020522f537562747970652035\
203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e67\
74682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8\
fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1ff\
fe017f46dc93a6b67e013b029aaa1db2560b45ca67d688c7f84b8c4c791fe02b3df614f86db169\
0901c56b45c1530afedfb76038e972722fe7ad728f0e4904e046c230570fe9d41398abe12ef5bc\
942be33542a4802d98b5d70f2a332ec37fac3514e74ddc0f2cc1a874cd0c78305a215664613097\
89606bd0bf3f98cda8044629a1'

c2 = '255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f576964746820\
32203020522f4865696768742033203020522f547970652034203020522f537562747970652035\
203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e67\
74682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8\
fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1ff\
fe017346dc9166b67e118f029ab621b2560ff9ca67cca8c7f85ba84c79030c2b3de218f86db3a9\
0901d5df45c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d23c570feb141398bb552ef5a0\
a82be331fea48037b8b5d71f0e332edf93ac3500eb4ddc0decc1a864790c782c76215660dd3097\
91d06bd0af3f98cda4bc4629b1'

collision1 = bytes.fromhex(c1) 
collision2 = bytes.fromhex(c2)
script_sig = Script([collision1, collision2])
combined_script = script_sig + script_pubkey
print(combined_script.evaluate(0))
'''

# --------
# raw_tx = ('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf830\ 3c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccf\ cf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8\ e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278\ afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88a\ c99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
# stream = BytesIO(bytes.fromhex(raw_tx))
# transaction = Tx.parse(stream)
# print(transaction.fee() >= 0)

# prev_tx = bytes.fromhex('0d6fe5213c0b3291f208cba8bfb59b7476dffacc4e5cb66f6eb20a080843a299')
# prev_index = 13
# tx_in = TxIn(prev_tx, prev_index)
# tx_outs = []

# change_amount = int(0.33*100000000)
# change_h160 = decode_base58('mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2')
# change_script = p2pkh_script(change_h160)
# change_output = TxOut(amount=change_amount, script_pubkey=change_script)

# target_amount = int(0.1*100000000)
# target_h160 = decode_base58('mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf')
# target_script = p2pkh_script(target_h160)
# target_output = TxOut(amount=target_amount, script_pubkey=target_script)

# tx_obj = Tx(1, [tx_in], [change_output, target_output], 0, True)
# print(tx_obj)

# --------
# Sign the transaction
