from oops import *
from utils import *

if(__name__ == "__main__"):
    gd = Parse_Input(FP_SINGLE_IN)
    gd.set_gate_env()
    sma = Simulated_Annealing(gd,10**(6),0.99,0.1)
    # sma.gen_init_packing()
    sma.anneal_to_pack()
    # sma.perturb_packing_swap()
    sma.wire_cost_function()
    Parse_Output(sma.gate_data,FP_SINGLE_OUT)
    # print(sma.gate_data.gates[18].pins)
    print("Done")