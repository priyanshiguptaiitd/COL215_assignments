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
        f.write(f'memory_initialization_radix={n};\n')
        f.write('memory_initialization_vector=\n')
        for i in range(n):
            f.write('{:02X}'.format(data[i]))
            if i != len(data)-1:
                if(i%8 == 7):
                    f.write(',\n')
                else:
                    f.write(', ')
            else:
                f.write(';')
  
if(__name__ == "__main__"):                  
    generate_coe_file(gen_data(64), "rom.coe",64)
    
    print("Done")
    pass