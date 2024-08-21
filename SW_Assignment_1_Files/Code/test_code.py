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
from itertools import count        

@ time_it
def multi_pack_iter(rec_data,cols,rows,rec_tot_area,w_max,h_max):
    
    tc_total_runtime,max_packeff,max_peff_cols,max_peff_rows,max_peff_rect = 0,0,0,0,None
    itstook = 0
    for i in count(0,1):
        PBP_out = Pack_by_Pixel_v2(rec_data,cols,rows,supress_time_out=True)
        packed_recs,pack_data,check_pack = PBP_out[0]
        tc_runtime = PBP_out[1]
        if(check_pack is None):
            cols = int(DIM_INC_FAILTC*cols)
            rows = int(ALPHA_MARGIN_DIM*rec_tot_area/cols)
            tc_total_runtime += tc_runtime
        else:
            tc_total_runtime += tc_runtime
            cells_packed,max_peff_cols, max_peff_rows =  pack_data[0], pack_data[2], pack_data[1] 
            max_packeff = round(pack_data[0]/(pack_data[1]*pack_data[2]),8)
            max_peff_rect  = packed_recs                
            break

    if(max_packeff > PACK_EFF_BOUND or round(tc_total_runtime,8) > TC_RUNTIME_BOUND):
        itstook += 1
        print(max_packeff,PACK_EFF_BOUND,round(tc_total_runtime,8),TC_RUNTIME_BOUND)
        print(f"Iterations took = {itstook}")
        return max_peff_rect,[cells_packed,max_peff_rows,max_peff_cols],True
    else:
        if(tc_runtime < 0.1):
            max_iterations = MAX_IT_BOUND
        else:
            max_iterations = min((TC_RUNTIME_BOUND-tc_total_runtime)//tc_total_runtime,MAX_IT_BOUND)
            
        print(f"Max iterations allowed : {max_iterations}")
        if(max_iterations%2==1):
            max_iterations -= 1
        
        cols_rows_iter = set()
        
        for i in range(1,max_iterations//2+1):
            cols_l = int(max_peff_cols*(1+DIM_DELTA_PEFF*i))
            cols_r = int(max_peff_cols*(1+DIM_DELTA_PEFF*i))
            if(w_max <= cols_l):
                cols_rows_iter.add((cols_l,max_peff_rows))
            if(w_max <= cols_r and h_max <= int(ALPHA_MARGIN_DIM*rec_tot_area/cols_r)):
                cols_rows_iter.add((cols_r,int(ALPHA_MARGIN_DIM*rec_tot_area/cols_r)))
        
        # print(cols_rows_iter)
        
        for t in cols_rows_iter:
            itstook += 1
            # print(f"Checking at {t[0]} {t[1]}")
            PBP_out = Pack_by_Pixel_v2(rec_data,t[0],t[1],supress_time_out=True)
            packed_recs,pack_data,check_pack = PBP_out[0]
            tc_runtime = PBP_out[1]
            if(check_pack is not None):
                curr_packeff = round(pack_data[0]/(pack_data[1]*pack_data[2]),8)
                # print(curr_packeff,max_packeff) 
                if(curr_packeff > max_packeff):
                    cells_packed,max_peff_cols, max_peff_rows =  pack_data[0], pack_data[2], pack_data[1] 
                    max_packeff = curr_packeff
                    max_peff_rect  = packed_recs                          
                if(max_packeff > PACK_EFF_BOUND):
                    print(f"Iterations took = {itstook}")
                    return max_peff_rect,[cells_packed,max_peff_rows,max_peff_cols],True
        
        print(f"Iterations took = {itstook}")
        return max_peff_rect,[cells_packed,max_peff_rows,max_peff_cols],True
    
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

@ time_it_no_out
def test_single_case_mpitr(fpath_in,fpath_out):
    rec_data,rec_tot_area,maxw,maxh,ws,hs = parse_Input_Rectangles(fpath_in)
    avg_asp,w_avg,h_avg= Rec_Data_Analysis(rec_data)
    rec_freq = len(rec_data)
    
    alpha_margin = ALPHA_MARGIN(rec_freq)
    
    print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} " )
    print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(alpha_margin*(rec_tot_area**0.5))} across {rec_freq} gates")
    
    icols = int(alpha_margin*(rec_tot_area**0.5))
    irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1 
    
    MPI_out = multi_pack_iter(rec_data,icols,irows,rec_tot_area,maxw,maxh,supress_time_out=False)
    packed_recs,pack_data,pack_check= MPI_out[0]
    tc_runtime = MPI_out[1] 
    
    print(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used")
    print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
    parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Output(packed_recs),fpath_out)

@ time_it_no_out
def test_multi_cases_mpitr(gatefreq,tc_freq):
    
    assert gatefreq in [10,25,50,100,250,500,1000], "Please give a valid test case size"
    assert tc_freq > 0, "Please give non zero number of test cases"
    
    success_packs,fail_packs,tc_runtime_avg, pack_eff_avg = 0,0,0,0
    multi_tc_report_fpath = FP_MULTI_CASES_OUT(gate_freq=gatefreq)
    
    with open(multi_tc_report_fpath,"w") as file:
        pass
    
    for tc in range(1,tc_freq+1):
        rec_data,rec_tot_area,maxw,maxh,ws,hs = parse_Input_Rectangles(FP_MULTI_CASES_IN(tc,gatefreq))
        avg_asp,w_avg,h_avg = Rec_Data_Analysis(rec_data)
        rec_freq = len(rec_data)
        
        alpha_margin = 1.1 if(rec_freq >= 100) else (1.3 if(rec_freq <= 20) else 1.2)    
        # print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} ")
        # print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(1.1*(rec_tot_area**0.5))} across {rec_freq} gates")
        
        icols = int(alpha_margin*(rec_tot_area**0.5))
        irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1
        
        MPI_out = multi_pack_iter(rec_data,icols,irows,rec_tot_area,maxw,maxh,supress_time_out=False)
        packed_recs,pack_data,pack_check = MPI_out[0]
        tc_runtime = MPI_out[1]
        
        tc_runtime_avg += round(tc_runtime,8)
        # print(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used")
        # print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
        parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Output(packed_recs),FP_MULTI_CASES_OUT(tc,gatefreq))
        pack_eff_avg += round(pack_data[0]/(pack_data[1]*pack_data[2]),8)
        
        with open(multi_tc_report_fpath,"a") as file:
            if(pack_check):
                success_packs += 1
                file.write(f"Test Case {tc} \n")
                file.write(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]} \n")
                file.write(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used \n")
                file.write(f"Time to run Code :{tc_runtime : .8f}\n")
            else:
                fail_packs += 1
                file.write(f"Test Case {tc} \n")
                file.write(f"Packing Failure !\n")
                file.write(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used \n")
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
def testing_at_25_mpitr():
    pass

if(__name__ == "__main__"): 
    # write_single_case(10,FP_SINGLE_CASE_IN,"normal_hi")
    # write_multi_cases(50,100)
    test_multi_cases(50,100)
    # test_multi_cases_mpitr(50,100)
    # test_single_case(FP_SINGLE_CASE_IN,FP_SINGLE_CASE_OUT)
    # test_single_case_mpitr(FP_SINGLE_CASE_IN,FP_SINGLE_CASE_OUT)
    # remove_multi_cases(100,20)
    # testing_at_25()
    pass