IMIN = 0
IMAX = 2**8-1   # 8-bit data
import random

def gen_data(n = 16):
    assert n%8 == 0, "Data width must be a multiple of 8"
    data = []
    for i in range(n):
        data.append(random.randint(IMIN, IMAX))
    # print(data)
    return data

def generate_coe_file(data, filename,n = 16):
    
    assert n%8 == 0, "Data width must be a multiple of 8"
    
    fname = r"HW Assignments\HW Assignment 3\Local_Files_Yash\COE_Files" + f"\\{filename}"
    with open(fname, 'w') as f:
        f.write(f'memory_initialization_radix={16};\n')
        f.write('memory_initialization_vector=\n')
        for i in range(n):
            f.write('{:02X}'.format(data[i]))
            if i != len(data)-1:
                if(i%16 == 15):
                    f.write(',\n')
                else:
                    f.write(', ')
            else:
                f.write(';')
  
if(__name__ == "__main__"):                  
    # generate_coe_file(gen_data(256), "rom.coe",256)
    s = "54, 68, 31, 73, 49, 73, 41, 31, 36, 42, 79, 74, 65, 4b, 65, 79, e6, 25, 87, 3e, af, 56, c6, 0f, 99, 14, bf, 7b, fc, 5f, da, 02, 2b, 72, f0, 8e, 84, 24, 36, 81, 1d, 30, 89, fa, e1, 6f, 53, f8, 87, 9f, b1, 76, 03, bb, 87, f7, 1e, 8b, 0e, 0d, ff, e4, 5d, f5, e6, d3, 57, 60, e5, 68, d0, 97, fb, e3, de, 9a, 04, 07, 83, 6f, 33, 3f, ff, 92, d6, 57, 2f, 05, 2d, b4, f1, 9f, 29, b3, 72, f0, 7e, 7f, 73, 37, a8, 28, 5c, 32, 85, 9c, ad, ad, ac, 2f, df, 5d, 2b, e1, 3f, a6, 83, c9, 63, 94, 06, 55, ce, 39, aa, 7a, 11, 64, 71, 63, 7c, 0a, f2, aa, 1f, 9e, f4, ff, d1, a7, 5e, 85, c0, c3, fd, d9, 52, 52, 0f, 73, 4d, cc, fb, 8c, 9c, 6b, a5, 09, 5c, a8"
    print(len(s.strip().split(", ")))
    print("Done")
    pass