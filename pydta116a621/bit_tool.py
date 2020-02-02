def get_mask(bit_pos, bit_size):
    value = 0
    for i in range(bit_size):
        value <<= 1
        value |= 1
    for i in range(bit_pos):
        value <<= 1
    return value


def fill_field(old_field, bit_pos, bit_size, value):
    if(value > 2**bit_size):
        raise("Error, new value too big")
    new_field = (old_field & (~get_mask(bit_pos, bit_size))) | ( value << bit_pos)
    return new_field

def pick_value(field, bit_pos, bit_size):
    value = (field & get_mask(bit_pos, bit_size)) >> bit_pos
    return value

def bytes_to_list(bytes):
    bits = []
    for byte in bytes:
        v = byte
        for i in range(8):
            bits.append(v % 2)
            v = v // 2
    return bits


if __name__ == '__main__':
    print(bin(get_mask(0,0)))
    print(bin(get_mask(1,0)))
    print(bin(get_mask(0,1)))
    print(bin(get_mask(4,4)))
    print(bin(get_mask(2,2)))

    old_field = 0b11010100
    value = 0b0110
    bit_pos = 3
    bit_size = 4
    # 10110100
    print(bin(fill_field(old_field, bit_pos, bit_size, value)))

    print(bin(pick_value(old_field, bit_pos, bit_size)))



