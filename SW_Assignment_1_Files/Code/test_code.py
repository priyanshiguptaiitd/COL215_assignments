# Main Imports - Backbone of Solving the Problem Statement
# Rect Module - Implements Rect class, Ultimately being used to store gates data
# IO_Parser - For parsing Input and Ouput rectangle data as well as some intermediate pasrsing for debugging
# Pack_by_Pixels - Implementation of our Rectangle Packing Algorithm

from Rect import *
from IO_Parser import *
from Pack_by_Pixels import *
from project_constants import *

# Utility Imports - Helpful for rigorous implementation testing and report generation 
from txt_analysis import *
from testcase_gen import *
from code_timer import *
        
           
@ time_it_no_out
def test_single_case(fpath_in,fpath_out):
    
    rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(fpath_in)
    avg_asp,w_avg,h_avg= Rec_Data_Analysis(rec_data)
    rec_freq = len(rec_data)
    
    alpha_margin = ALPHA_MARGIN(rec_freq)
    print(mh)
    print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} " )
    print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(alpha_margin*(rec_tot_area**0.5))} across {rec_freq} gates")
    
    icols = int(alpha_margin*(rec_tot_area**0.5))
    irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1 
    PBP_out = Pack_by_Pixel_v2(rec_data,icols,irows,supress_time_out=False)
    packed_recs,pack_data,check_pack = PBP_out[0]
    tc_runtime = PBP_out[1]
     
    if(check_pack is not None):
        print(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used")
        print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
        parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Output(packed_recs),fpath_out)

@ time_it_no_out
def test_multi_cases(gatefreq,tc_freq):
    
    assert gatefreq in [10,25,50,100,250,500,1000], "Please give a valid test case size"
    assert tc_freq > 0, "Please give non zero number of test cases"
    
    success_packs,fail_packs,tc_runtime_avg, pack_eff_avg = 0,0,0,0
    multi_tc_report_fpath = FP_MULTI_CASES_OUT(gate_freq=gatefreq)
    
    with open(multi_tc_report_fpath,"w") as file:
        pass
    
    for tc in range(1,tc_freq+1):
        rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(FP_MULTI_CASES_IN(tc,gatefreq))
        avg_asp,w_avg,h_avg = Rec_Data_Analysis(rec_data)
        rec_freq = len(rec_data)
        
        alpha_margin = 1.1 if(rec_freq >= 100) else (1.3 if(rec_freq <= 20) else 1.2)    
        # print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} ")
        # print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(1.1*(rec_tot_area**0.5))} across {rec_freq} gates")
        
        icols = int(alpha_margin*(rec_tot_area**0.5))
        irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1
        PBP_out = Pack_by_Pixel_v2(rec_data,icols,irows,supress_time_out=False) 
        packed_recs,pack_data,check_pack = PBP_out[0]
        tc_runtime = PBP_out[1]
        tc_runtime_avg += round(tc_runtime,8)
        
        if(check_pack is not None):
            success_packs += 1
            # print(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used")
            # print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
            parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Output(packed_recs),FP_MULTI_CASES_OUT(tc,gatefreq))
            pack_eff_avg += round(pack_data[0]/(pack_data[1]*pack_data[2]),8)
        else:    
            fail_packs += 1
        
        with open(multi_tc_report_fpath,"a") as file:
            file.write(f"Test Case {tc} \n")
            if(check_pack is not None):
                file.write(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]} \n")
                file.write(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used \n")
                file.write(f"Time to run Code :{tc_runtime : .8f}\n")
            else:
                file.write(f"Packing Failure !!!\n")
                file.write(f"Time to run Code :{tc_runtime : .8f}\n")
            file.write(f"\n")            
    
    with open(multi_tc_report_fpath,"a") as file:
            file.write(f"Final Report of All Test Cases -\n")
            file.write(f"Total Number of Test Cases = {tc_freq}\n")
            file.write(f"No of failures = {fail_packs}\n")
            file.write(f"No of Succeses = {success_packs}\n")
            file.write(f"Average Packing Efficiency :{pack_eff_avg/tc_freq : .8f}\n")
            file.write(f"Average Time to run Code :{tc_runtime_avg/tc_freq : .8f}\n")
            file.write(f"\n")

@ time_it_no_out
def testing_at_25():
    with open("report_tc_analysis.txt","w") as file:
        pass
    for g in range(25,2001,25):
        write_single_case(g,FP_SINGLE_CASE_IN)
        
        rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(FP_SINGLE_CASE_IN)
        avg_asp,w_avg,h_avg= Rec_Data_Analysis(rec_data)
        rec_freq = len(rec_data)
        
        alpha_margin = 1.1 if(rec_freq >= 100) else (1.3 if(rec_freq <= 20) else 1.2)
        
        print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} " )
        print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(alpha_margin*(rec_tot_area**0.5))} across {rec_freq} gates")
        
        icols = int(alpha_margin*(rec_tot_area**0.5))
        irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1 
        PBP_out = Pack_by_Pixel_v2(rec_data,icols,irows,supress_time_out=False) 
        packed_recs,pack_data,check_pack = PBP_out[0]
        tc_runtime = PBP_out[1]
        
        if(check_pack is not None):
            with open("report_tc_analysis.txt","a") as file:
                file.write(f"No. of Gates : {rec_freq}\n")
                file.write(f"Time to Run Code : {tc_runtime : .6f}\n")
                file.write(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .6f}\n")
                print(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used")
                print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
                parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Output(packed_recs),FP_SINGLE_CASE_OUT)
        
        else:
            with open("report_tc_analysis.txt","a") as file:
                file.writeline(f"No. of Gates : {rec_freq}\n")
                file.writeline(f"Time to Run Code : NA\n")
                file.writeline(f"Packing Efficiency : NA\n")
                
    
if(__name__ == "__main__"): 
    write_single_case(500,FP_SINGLE_CASE_IN,"uniform")
    # test_multi_cases(250,100)
    test_single_case(FP_SINGLE_CASE_IN,FP_SINGLE_CASE_OUT)
    # write_multi_cases(250,100)
    # remove_multi_cases(100,20)
    # testing_at_25()
    pass