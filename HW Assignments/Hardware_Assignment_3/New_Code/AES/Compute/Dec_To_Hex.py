def dec_to_hex(decimal_list):
    hex_list = [hex(num) for num in decimal_list]
    return hex_list


def xor_hex_lists(hex_list1, hex_list2):
    if len(hex_list1) != len(hex_list2):
        raise ValueError("Both lists must have the same length")
    
    xor_list = [hex(int(a, 16) ^ int(b, 16)) for a, b in zip(hex_list1, hex_list2)]
    return xor_list

# Example usage
decimal_list = [90, 245, 253, 134, 212, 243, 146, 128, 203, 155, 136, 100, 17, 136, 107, 222]
hex_output = dec_to_hex(decimal_list)
print(hex_output) 

hxl1 = ['0x5a', '0xf5', '0xfd', '0x86', '0xd4', '0xf3', '0x92', '0x80',
        '0xcb', '0x9b', '0x88', '0x64', '0x11', '0x88', '0x6b', '0xde']

hxl2 = ['0x54', '0x68', '0x31', '0x73', '0x49', '0x73', '0x41', '0x31',
        '0x36', '0x42', '0x79', '0x74', '0x65', '0x4b', '0x65', '0x79']

xor_output = xor_hex_lists(hxl1, hxl2)

print(xor_output)
