    psd_gd,anneal_rotuine_time = sma.anneal_routine(supress_time_out = True)
    print(f"Total Annealing Routine Time: {anneal_rotuine_time:.6f} seconds\n")
    Parse_Output(sma.final_packed_data,FP_SINGLE_OUT,is_pseudo_copy = True)
