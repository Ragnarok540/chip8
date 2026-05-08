
# Bitwise AND
a =         0b10011100
b =         0b00110100
c = a & b # 0b00010100

print(bin(a))
print(bin(b))
print(bin(c))
print('----------')

# Bitwise OR
a =         0b10011100
b =         0b00110100
c = a | b # 0b10111100

print(bin(a))
print(bin(b))
print(bin(c))
print('----------')

# Bitwise XOR
a =         0b10011100
b =         0b00110100
c = a ^ b # 0b10101000

print(bin(a))
print(bin(b))
print(bin(c))
print('----------')

# Bitwise NOT
a =          0b10011100
b =          0b11111111
c = ~a & b # 0b01100011

print(bin(a))
print(bin(c))
print('----------')

# Left Shift
a =          0b00100111
b = a << 1 # 0b01001110
c = a << 2 # 0b10011100

print(bin(a))
print(bin(b))
print(bin(c))
print('----------')

# Right Shift
a =          0b100111
b = a >> 1 # 0b010011
c = a >> 2 # 0b001001

print(bin(a))
print(bin(b))
print(bin(c))
