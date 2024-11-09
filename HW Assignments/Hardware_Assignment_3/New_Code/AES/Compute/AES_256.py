def galois_multiply(a, b):
    p = 0
    hi_bit_set = 0
    for i in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= 0x1b  # x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p & 0xFF

def galois_array(a,b):
    p = [galois_multiply(a[i], b[i]) for i in range(len(a))]
    
    xor_ans = 0
    
    for i in range(len(p)):
        xor_ans ^= p[i]
        
    return xor_ans
# Example usage:
r0 = [0x0e,0x0b,0x0d,0x09]
r1 = [0x09,0x0e,0x0b,0x0d]
r2 = [0x0d,0x09,0x0e,0x0b]
r3 = [0x0b,0x0d,0x09,0x0e]
  
c0 = [0x0f,0x03,0x84,0x63]
c1 = [0x04,0x8c,0x2e,0xa2]
c2 = [0x53,0x8e,0x07,0x89]
c3 = [0xfa,0x2e,0x6d,0x67]

print(f"Result: First Row")
print(f"Result: {galois_array(r0, c0):02x}")
print(f"Result: {galois_array(r0, c1):02x}")
print(f"Result: {galois_array(r0, c2):02x}")
print(f"Result: {galois_array(r0, c3):02x}")

print(f"Result: Second Row")
print(f"Result: {galois_array(r1, c0):02x}")
print(f"Result: {galois_array(r1, c1):02x}")
print(f"Result: {galois_array(r1, c2):02x}")
print(f"Result: {galois_array(r1, c3):02x}")

print(f"Result: Third Row")
print(f"Result: {galois_array(r2, c0):02x}")
print(f"Result: {galois_array(r2, c1):02x}")
print(f"Result: {galois_array(r2, c2):02x}")
print(f"Result: {galois_array(r2, c3):02x}")

print(f"Result: Fourth Row")
print(f"Result: {galois_array(r3, c0):02x}")
print(f"Result: {galois_array(r3, c1):02x}")
print(f"Result: {galois_array(r3, c2):02x}")
print(f"Result: {galois_array(r3, c3):02x}")

    