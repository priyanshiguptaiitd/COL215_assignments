from collections import defaultdict as def_dict
from random import randint as rint

def binary_len(n):
    blen = 0
    if(n==0):      # 0 is a Edge case
        return 1
    while n>0:
        n = n >> 1
        blen+=1
    return blen

if(__name__ == "__main__"):
    pass