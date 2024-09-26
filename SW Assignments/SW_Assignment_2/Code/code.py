from oops import *
from utils import *

if(__name__ == "__main__"):
    gd = Parse_Input(FP_SINGLE_IN)
    gd.set_gate_env()
    sma = Simulated_Annealing(gd,1000,0.99,0.1)
    sma.gen_init_packing()
    # print(gd)
    Parse_Output(sma.gate_data,FP_SINGLE_OUT)
    print("Done")