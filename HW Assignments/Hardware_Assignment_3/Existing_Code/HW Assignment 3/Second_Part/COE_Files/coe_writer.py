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
    
    fname = r"HW Assignments\HW Assignment 3\Second_Part\COE_Files" + f"\\{filename}"
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
    generate_coe_file(gen_data(256), "rom_01.coe",256)
    
    print("Done")
    pass