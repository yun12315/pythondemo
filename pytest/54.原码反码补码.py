print(bin(18))
print(oct(18))
print(hex(18))

print(int("0b10010",2))
print(int("0x12",16))
print(int("0o12",8))

print(bin(18)[2:])
print(bin(18)[2:].zfill(8))
print(bin(18)[2:].zfill(8)[::-1])
print(int(bin(18)[2:].zfill(8)[::-1],2))
print(int(bin(18)[2:].zfill(8)[::-1],2) == 18)
