class VIPRand:
    def __init__(self, seed=0) -> None:
        self._rand_next= seed

    def rand(self):
        self._rand_next = (self._rand_next * 0x5851f42d4c957f2d + 1)&0xffffffffffffffff
        return (self._rand_next >>0x20) & 0x7fffffff

rando=VIPRand(1)
all_32_state=[]
all_256_state=[]
xor_keys=[]

def inverse_sbox(sbox):
    """Compute the inverse of a given S-box."""
    # Create an empty list for the inverse S-box
    inv_sbox = [0] * 256
    
    # Iterate over each value in the S-box
    for i in range(256):
        # Find the index in the S-box
        val = sbox[i]
        # Store the index in the inverse S-box
        inv_sbox[val] = i
    
    return inv_sbox
value1=[49664, 268435456, 2147614752, 9437184, 524352, 0, 4194564, 536870912, 102760448, 134217866, 0, 0, 16, 0, 1074018305, 16843776,]
value2=[0, 80, 8192, 0, 256, 136052736, 0, 16778752, 2097152, 0, 541081604, 8388610, 33, 268601344, 1073741824, 2248216712,]

p1=[[j for j in range(16) if value1[j]&(1<<i)>0][0] for i in range(32)]
p2=[[j for j in range(16) if value2[j]&(1<<i)>0][0] for i in range(32)]
flag=[p1[i]*16+p2[i] for i in range(32)][::-1]

w=0
arr=[i for i in range(32)]
flag_=[0 for i in range(256)]
arr_1=[i for i in range(256)]
for i in range(1337):
    for i in range(1000):
        a = rando.rand() % 0x20
        b = rando.rand() % 0x20
        if a != b:
            arr[a],arr[b]=arr[b],arr[a]
    all_32_state.append(arr[:])
    for i in range(10000):
        y = rando.rand() & 0xff
        x = rando.rand() & 0xff
        if y != x:
            arr_1[y],arr_1[x]=arr_1[x],arr_1[y]
    all_256_state.append(arr_1[:])
    xor_keys.append([rando.rand()&0xff for _ in range(32)])

for i in range(1336,-1,-1):
    for j in range(31,-1,-1):
        flag[j]^=xor_keys[i][j]&0xff
    arr_1=all_256_state[i][:]
    arr=all_32_state[i][:]

    for j in range(31,-1,-1):
        flag[j]=inverse_sbox(arr_1)[flag[j]]
    for j in range(31,-1,-1):
        flag_[arr[j]]=flag[j]
    for j in range(31,-1,-1):
        flag[arr[j]]=flag_[j]
print(bytes(flag))