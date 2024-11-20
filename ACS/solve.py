from z3 import *
import zlib

s = Solver()

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))


cmp = [0xf34a, 0x3aa8, 0xfc90, 0x415d, 0xc87b, 0xc88a, 0x234c, 0xb629, 0xfe48, 0x8d12, 0xd395, 0x2437, 0x2544, 0x19c2, 0xf1fa, 0x7a41, 0x8aa3, 0x7f8d, 0xe70, 0x8fe7, 0xe71e, 0x8f5e]

key_round_arr = [] 

# INIT KEY of SPECK
ori_key = 0x1110
ori_key_2 = 0x1918

for _ in range(11):
    key = ori_key
    key_2 = ori_key_2
    key_round_arr.append(key_2)
    for i in range(21):
        key = rol(key, 9, 16)
        key = (key + key_2) ^ i 
        key &= 0xFFFF
        key_2 = rol(key_2, 2, 16)
        key_2 &= 0xFFFF
        key_2 ^= key
        key_round_arr.append(key_2)

    ## PACK 2 ori_key 
    seg = (ori_key_2 << 16) | ori_key  
    ## reimplement bswap and crc32 new two key
    bswap = ((seg & 0xFF000000) >> 24) | \
            ((seg & 0x00FF0000) >> 8)  | \
            ((seg & 0x0000FF00) << 8)  | \
            ((seg & 0x000000FF) << 24)

    data = (bswap).to_bytes(4, byteorder='little')
    checksum = zlib.crc32(data)
    ori_key_2 = (checksum >> 16) & 0xffff
    ori_key = checksum & 0xffff

print(len(key_round_arr))

data = [BitVec(f'data_{i}', 64) for i in range(44)]

for i in range(len(data)):
    s.add(data[i] >= 0x20)
    s.add(data[i] <= 0x7f)
doxbi = 0

## reimplement SPECK encrypt
for i in range(0, 44, 4):
    two_shit = ( data[i] << 8 ) | data[i + 1]
    next_two = ( data[i + 2] << 8 ) | data[i + 3] 
    cnt = 0
    tmp = 0
    tmp2 = 0
    two_shit = rol(two_shit, 9, 16)
    two_shit += next_two
    two_shit ^= key_round_arr[cnt]
    cnt += 1
    next_two = rol(next_two, 2, 16)
    next_two ^= two_shit
    two_shit = rol(two_shit, 9, 16)
    two_shit += next_two
    two_shit ^= key_round_arr[cnt]
    cnt += 1
    next_two = rol(next_two, 2, 16)
    next_two ^= two_shit
    while cnt < 22:
        two_shit = rol(two_shit, 9, 16)
        v37 = next_two + two_shit
        v37 = (key_round_arr[cnt] ^ v37) & 0xFFFF  
        next_two = rol(next_two, 2, 16)
        v38 = v37 ^ next_two
        v37 = rol(v37, 9, 16)
        v39 = v38 + v37
        v39 = (key_round_arr[cnt + 1] ^ v39) & 0xFFFF
        v38 = rol(v38, 2, 16)
        v40 = v39 ^ v38
        v39 = rol(v39, 9, 16)
        v41 = v40 + v39
        v41 = (key_round_arr[cnt + 2] ^ v41) & 0xFFFF
        v40 = rol(v40, 2, 16)
        v42 = v41 ^ v40
        v41 = rol(v41, 9, 16)
        two_shit = v42 + v41
        two_shit = (key_round_arr[cnt + 3] ^ two_shit) & 0xFFFF
        v42 = rol(v42, 2, 16)
        next_two = two_shit ^ v42
        cnt += 4
    key_round_arr = key_round_arr[22:]
    s.add(two_shit == cmp[doxbi])
    s.add(next_two == cmp[doxbi + 1])
    doxbi += 2

print(s.check())
## GGWP
if s.check() == sat:
    model = s.model()
    flag = [chr(model[data[i]].as_long()) for i in range(44)]
    print("".join(flag))