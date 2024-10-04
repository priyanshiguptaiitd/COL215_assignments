def seven_seg_decoder_hex(A, B, C, D):
    dec_out = [0] * 7

    dec_out[0] =  int((not A and not B and not D) or (not A and B and D) or (A and not C and not D)
                      or (A and not B and not C) or (not A and C) or (B and C) or (C and not D))
    dec_out[1] =  int((not A and not C and not D) or (not A and C and D) or (A and not C and D)
                      or (A and not B and not D) or (not A and not B))
    dec_out[2] =  int((not A and C and D) or (not A and not C) or (not A and B) or (not C and D)
                      or (A and not B))
    dec_out[3] =  int((not A and not B and not D) or (not B and C and D) or (B and not C and D)
                      or (B and C and not D) or (A and not C and not D))
    dec_out[4] =  int((not B and not C and not D) or (A and B) or (C and not D) or (A and C))
    dec_out[5] =  int ((not A and B and not C) or (B and C and not D) or (not C and not D)
                      or (A and not B) or (A and C))
    dec_out[6] =  int((not A and not B and C) or (not A and B and not C) or (C and not D)
                      or (A and not B) or (A and D))

    return dec_out

# Test the function - Works Fine
for A in [0,1]:
    for B in  [0,1]:
        for C in [0,1]:
            for D in [0,1]:
                print(f"(A,B,C,D) = ({A},{B},{C},{D}), Input = {8*A + 4*B + 2*C + D}")
                print("Output = ", seven_seg_decoder_hex(A, B, C, D))
                print()

