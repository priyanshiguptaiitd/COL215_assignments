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
def single_pack_iter(rec_data,cols,rows):
    # Docstring - Function Description (Medium)
    """ Runs a single Iteration of Packing Algorithm (On the initial guesses of Columns and Rows)
        If a successful packing is found then the algorithm returns that otherwise we increase the 
        Number of Columns to 1.5 times the original till a packing is found
        
        (Note that if we ensure that our rows are more than the max height of gates then this process will
        terminate after finite steps since a feasible upper bound on the number of columns is the sum of widths 
        of all the gates (Which is what the V0 algorithm uses))

    Args:
        rec_data (List of Rec objects): The Gates as Rec Objects in a list 
        cols (Integer): Guess on initial cols
        rows (Integer): Guess on initial rows

    Returns:
        max_peff_rect - The Rec Object List with updated states of packing coordinates 
        [cells_packed,max_peff_rows,max_peff_cols] - Total Area Covered by gate, Maximum Rows Utilised , Maximum Columns Utilised
        True - (Earlier A failsafe to check if the ouput is being produced or not)
    """
    
    max_peff_cols, max_peff_rows, max_peff_rect = 0, 0, None

    for i in count(0,1):
        PBP_out = Pack_by_Pixel_v2(rec_data,cols,rows,supress_time_out = True)
        packed_recs,pack_data,check_pack = PBP_out[0]
        
        if(check_pack is None):
            cols = int(DIM_INC_FAILTC*cols)

        else:
            cells_packed,max_peff_cols, max_peff_rows =  pack_data[0], pack_data[2], pack_data[1] 
            max_packeff = round(pack_data[0]/(pack_data[1]*pack_data[2]),8)
            max_peff_rect  = packed_recs                
            break
        
    return max_peff_rect,[cells_packed,max_peff_rows,max_peff_cols],True

@ time_it
def multi_pack_iter(rec_data,cols,rows,rec_tot_area,w_max,h_max):
    # Docstring - Function Description (Long)
    """ Runs a Iterations of Packing Algorithm (On the initial guesses of Columns and Rows)
        If a successful packing is found then the algorithm returns that otherwise we increase the 
        Number of Columns to 1.5 times the original till a packing is found ( Refer the docstring of single_pack_iter
        for a proof of working)
        
        Once a packing is found the time taken to produce the proof is noted. Now if the packing efficiency of 
        the current packing exceed PACK_EFF_BOUND or the time taken exceeds TC_RUNTIME_BOUND then the code exits 
        with the single produced packing.
        
        (Note that since for higher frequency of gates our packing efficiency exceed PACK_EFF_BOUND on the first try itself
        (At the initial guesses itself), there is not much difference in this implementation VS the single_pack_iter)
        
        If the case is otherwise, using the current tc_total_runtime an estimate is made on the number of iterations that can be run
        on Packing Algorithm at different inputs such that we don't exceed TC_RUNTIME_BOUND. If the number of iterations are lesser than 
        MAX_IT_BOUND then we take testing_iterations otherwise we take MAX_IT_BOUND.
        
        We generate multiple widths at a step of DIM_DELTA_PEFF percentage of original width (on both incrreasing and decreasing side)
        If the new_width is higher then we let the number of rows be max_peff_rows (The one from first successful test iteration)
        otherwise we increase it in accordance to the decrease in width (Care is taken about the rec_total-area constraint as well as
        maximum width and height of gates (acting as lower bound for our cols and rows))
        
        On Testcases with smaller gate frequency , this implementation tends to perform better than single_pack_itr
        for packing efficiency ( With a time tradeoff of ~20 times). Depending upon cost of manufacture vs time tradeoff
        One can choose which algorithm to implement

    Args:
        rec_data (List of Rec objects): The Gates as Rec Objects in a list 
        cols (Integer): Guess on initial cols
        rows (Integer): Guess on initial rows
        rec_tot_area (_type_): Total Area that gates will cover
        w_max (_type_): Maximum Width of the Gates (Lower Bound on Columns)
        h_max (_type_): Maximum Height of the Gates (Lower Bound on Rows)

    Returns:
        _type_: _description_
    """
    
    tc_total_runtime, max_packeff = 0, 0
    max_peff_cols, max_peff_rows, max_peff_rect =  0, 0, None
    its_took = 0
    
    for i in count(0,1):
        PBP_out = Pack_by_Pixel_v2(rec_data,cols,rows,supress_time_out=True)
        packed_recs,pack_data,check_pack = PBP_out[0]
        tc_runtime = PBP_out[1]
        tc_total_runtime += tc_runtime
        
        if(check_pack is None):
            cols = int(DIM_INC_FAILTC*cols)
            its_took += 1
        else:
            cells_packed,max_peff_cols, max_peff_rows =  pack_data[0], pack_data[2], pack_data[1] 
            max_packeff = round(pack_data[0]/(pack_data[1]*pack_data[2]),8)
            max_peff_rect  = packed_recs
            its_took += 1                
            break
        
    if(max_packeff > PACK_EFF_BOUND or round(tc_total_runtime,8) > TC_RUNTIME_BOUND):
        print(f"Iterations took = {its_took}")
        
        return max_peff_rect,[cells_packed,max_peff_rows,max_peff_cols],True
    else:
        if(tc_runtime < 0.1): max_iterations = MAX_IT_BOUND
        else: max_iterations = min(round((TC_RUNTIME_BOUND-tc_total_runtime)//tc_total_runtime),MAX_IT_BOUND)
            
        if(max_iterations%2==1): max_iterations += 1
        
        cols_rows_iter = set()
        
        
        for i in range(1,max_iterations//2+1):
            cols_l = int(max_peff_cols*(1+DIM_DELTA_PEFF*i))
            cols_r = int(max_peff_cols*(1-DIM_DELTA_PEFF*i))
            if(w_max <= cols_l):
                cols_rows_iter.add((cols_l,max_peff_rows))
            if(w_max <= cols_r and h_max <= int(ALPHA_MARGIN_DIM*rec_tot_area/cols_r)):
                cols_rows_iter.add((cols_r,int(ALPHA_MARGIN_DIM*rec_tot_area/cols_r)))
        
        for t in cols_rows_iter:
            its_took += 1
            PBP_out = Pack_by_Pixel_v2(rec_data,t[0],t[1],supress_time_out=True)
            packed_recs, pack_data, check_pack = PBP_out[0]
            tc_runtime = PBP_out[1]
    
            if(check_pack is not None):
                curr_packeff = round(pack_data[0]/(pack_data[1]*pack_data[2]),8)
                 
                if(curr_packeff > max_packeff):
                    cells_packed, max_peff_cols, max_peff_rows =  pack_data[0], pack_data[2], pack_data[1] 
                    max_packeff, max_peff_rect = curr_packeff, packed_recs                          
                
                if(max_packeff > PACK_EFF_BOUND):
                    
                    print(f"Iterations took = {its_took}")
                    return max_peff_rect,[cells_packed,max_peff_rows,max_peff_cols],True
        
        print(f"Iterations took = {its_took}")
        
        return max_peff_rect,[cells_packed,max_peff_rows,max_peff_cols],True
    
@ time_it_no_out
def test_single_case_sp(fpath_in,fpath_out):
    """ Checks single test case using single packing iteration
        Displays additional data and writes the output to given fpath_out 

    Args:
        fpath_in (FilePath): Passed to IO_Parser to read rectangle Data
        fpath_out (FilePath): Passed to IO_Parser to write rectangle Data
    """
    
    rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(fpath_in)
    avg_asp,w_avg,h_avg= Rec_Data_Analysis(rec_data)
    rec_freq = len(rec_data)
    
    alpha_margin = ALPHA_MARGIN_DIM

    print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} " )
    print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(alpha_margin*(rec_tot_area**0.5))} across {rec_freq} gates")
    
    icols = int(alpha_margin*(rec_tot_area**0.5))
    irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1 
    
    if(icols < mw): icols = int(1.5*mw)
    if(irows < mh): irows = int(1.5*mh)
    
    SPI_out = single_pack_iter(rec_data,icols,irows,supress_time_out = True)
    packed_recs,pack_data,pack_check= SPI_out[0]
    tc_runtime = SPI_out[1] 

    with open("comparison_single_tc_sp.txt","a") as file:
        file.write(f"Gate Freq : {rec_freq}\n")
        file.write(f"Runtime : {tc_runtime :.8f}\n")
        file.write(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}\n")

    print(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used")
    print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
    parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Output(packed_recs),fpath_out)

@ time_it_no_out
def test_multi_cases_sp(gatefreq,tc_freq):
    """ Checks multiple test cases of a given gate_frequency
        The Paths used are local to the creators machine and hence were used 
        for rigorous testing against select gate frequencies to benchmark the code
        and to improve on design decisions 

    Args:
        fpath_in (FilePath): Passed to IO_Parser to read rectangle Data
        fpath_out (FilePath): Passed to IO_Parser to write rectangle Data
    """
    assert gatefreq in [10,25,50,100,250,500,1000], "Please give a valid test case size"
    assert tc_freq > 0, "Please give non zero number of test cases"
    
    success_packs,fail_packs,tc_runtime_avg, pack_eff_avg = 0,0,0,0
    multi_tc_report_fpath = FP_MULTI_CASES_OUT(gate_freq=gatefreq)
    
    for tc in range(1,tc_freq+1):
        rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(FP_MULTI_CASES_IN(tc,gatefreq))
        avg_asp,w_avg,h_avg = Rec_Data_Analysis(rec_data)
        rec_freq = len(rec_data)
        
        alpha_margin = ALPHA_MARGIN_DIM   
        # print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} ")
        # print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(1.1*(rec_tot_area**0.5))} across {rec_freq} gates")
        
        icols = int(alpha_margin*(rec_tot_area**0.5))
        irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1
        
        if(icols < mw): icols = int(1.5*mw)
        if(irows < mh): irows = int(1.5*mh)
            
        # PBP_out = Pack_by_Pixel_v2(rec_data,icols,irows,supress_time_out=False) 
        # packed_recs,pack_data,check_pack = PBP_out[0]
        # tc_runtime = PBP_out[1]
        SPI_out = multi_pack_iter(rec_data,icols,irows,rec_tot_area,supress_time_out=True)
        packed_recs,pack_data,pack_check= SPI_out[0]
        tc_runtime = SPI_out[1]
        
        tc_runtime_avg += round(tc_runtime,8)
        
        if(pack_check is not None):
            success_packs += 1
            # print(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used")
            # print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
            parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Output(packed_recs),FP_MULTI_CASES_OUT(tc,gatefreq))
            pack_eff_avg += round(pack_data[0]/(pack_data[1]*pack_data[2]),8)
        else:    
            fail_packs += 1
        
        with open(multi_tc_report_fpath,"a") as file:
            file.write(f"Test Case {tc} \n")
            if(pack_check is not None):
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
def testing_at_25_sp():
    """Tests code at 25 frequency interval of gates (from [25,1000]) using Single Pack Iteration
       Used for graph analysis of the impact of number of gates on runtime 
       and packing efficiency
    """
    
    with open("report_tc_analysis.txt","w") as file:
        pass
    for g in range(25,2001,25):
        write_single_case(g,FP_SINGLE_CASE_IN)
        
        rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(FP_SINGLE_CASE_IN)
        avg_asp,w_avg,h_avg= Rec_Data_Analysis(rec_data)
        rec_freq = len(rec_data)
        
        alpha_margin = ALPHA_MARGIN_DIM
        
        print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} " )
        print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(alpha_margin*(rec_tot_area**0.5))} across {rec_freq} gates")
        
        icols = int(alpha_margin*(rec_tot_area**0.5))
        irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1 
        # PBP_out = Pack_by_Pixel_v2(rec_data,icols,irows,supress_time_out=False) 
        # packed_recs,pack_data,check_pack = PBP_out[0]
        # tc_runtime = PBP_out[1]
        
        SPI_out = single_pack_iter(rec_data,icols,irows,rec_tot_area,supress_time_out=True)
        packed_recs,pack_data,pack_check= SPI_out[0]
        tc_runtime = SPI_out[1]
        
        if(pack_check is not None):
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
def test_single_case_mp(fpath_in,fpath_out):
    """ Checks single test case using multiple packing iteration
        Displays additional data and writes the output to given fpath_out 

    Args:
        fpath_in (FilePath): Passed to IO_Parser to read rectangle Data
        fpath_out (FilePath): Passed to IO_Parser to write rectangle Data
    """
    
    rec_data,rec_tot_area,maxw,maxh,ws,hs = parse_Input_Rectangles(fpath_in)
    avg_asp,w_avg,h_avg= Rec_Data_Analysis(rec_data)
    rec_freq = len(rec_data)
    
    alpha_margin = ALPHA_MARGIN_DIM
    
    print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} " )
    print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(alpha_margin*(rec_tot_area**0.5))} across {rec_freq} gates")
    
    icols = int(alpha_margin*(rec_tot_area**0.5))
    irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1 
    if(icols < maxw): icols = int(1.5*maxw)
    if(irows < maxh): irows = int(1.5*maxh)
    
    
    MPI_out = multi_pack_iter(rec_data,icols,irows,rec_tot_area,maxw,maxh,supress_time_out=True)
    packed_recs,pack_data,pack_check= MPI_out[0]
    tc_runtime = MPI_out[1] 
    
    with open("comparison_single_tc_mp.txt","a") as file:
        file.write(f"Gate Freq : {rec_freq}\n")
        file.write(f"Runtime : {tc_runtime:.8f}\n")
        file.write(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}\n")

    
    print(f"Packing Efficiency : {pack_data[0]/(pack_data[1]*pack_data[2]) : .8f}, {pack_data[2]} cols and  {pack_data[1]} rows were used")
    print(f"Total area of Gates used and total area of Image: {rec_tot_area} , {pack_data[1]*pack_data[2]}")
    parse_Output_Rectangles(pack_data[2],pack_data[1],parse_Rec_Data_Output(packed_recs),fpath_out)

@ time_it_no_out
def test_multi_cases_mp(gatefreq,tc_freq):
    """ Checks single test case using multiple packing iteration
        Displays additional data and writes the output to given fpath_out 

    Args:
        fpath_in (FilePath): Passed to IO_Parser to read rectangle Data
        fpath_out (FilePath): Passed to IO_Parser to write rectangle Data
    """
    
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
        
        alpha_margin = ALPHA_MARGIN_DIM    
        # print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} ")
        # print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(1.1*(rec_tot_area**0.5))} across {rec_freq} gates")
        
        icols = int(alpha_margin*(rec_tot_area**0.5))
        irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1
        if(icols < maxw): icols = int(1.5*maxw)
        if(irows < maxh): irows = int(1.5*maxh)
        
        
        MPI_out = multi_pack_iter(rec_data,icols,irows,rec_tot_area,maxw,maxh,supress_time_out=True)
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
def testing_at_25_mp():
    """Tests code at 25 frequency interval of gates (from [25,1000]) using Single Pack Iteration
       Used for graph analysis of the impact of number of gates on runtime 
       and packing efficiency
    """
    
    with open("report_tc_analysis.txt","w") as file:
        pass
    for g in range(25,2001,25):
        write_single_case(g,FP_SINGLE_CASE_IN)
        
        rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(FP_SINGLE_CASE_IN)
        avg_asp,w_avg,h_avg= Rec_Data_Analysis(rec_data)
        rec_freq = len(rec_data)
        
        alpha_margin = ALPHA_MARGIN_DIM
        
        print(f"Average Aspect Ratio : {avg_asp :.4f}, Average Width : {w_avg :.4f}, Average Height : {h_avg :.4f} " )
        print(f"Total Cell Area : {rec_tot_area} , Approx Width / height of Diagram : {int(alpha_margin*(rec_tot_area**0.5))} across {rec_freq} gates")
        
        icols = int(alpha_margin*(rec_tot_area**0.5))
        irows = int(alpha_margin*(rec_tot_area**0.5)) if (int(alpha_margin*(rec_tot_area**0.5)) > rec_tot_area//icols + 1) else rec_tot_area//icols + 1 
        # PBP_out = Pack_by_Pixel_v2(rec_data,icols,irows,supress_time_out=False) 
        # packed_recs,pack_data,check_pack = PBP_out[0]
        # tc_runtime = PBP_out[1]
        
        MPI_out = multi_pack_iter(rec_data,icols,irows,rec_tot_area,supress_time_out=True)
        packed_recs,pack_data,pack_check= MPI_out[0]
        tc_runtime = MPI_out[1]
        
        if(pack_check is not None):
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
def testing_mp_sp():
    """
    For testing the difference between multi pack iteration and single pack iteration
    """
    for g in range(5,1001,5):
        write_single_case(g, FP_SINGLE_CASE_IN,"normal_hi",supress_time_out = False)
        test_single_case_sp(FP_SINGLE_CASE_IN, FP_SINGLE_CASE_OUT, supress_time_out = False)
        test_single_case_mp(FP_SINGLE_CASE_IN, FP_SINGLE_CASE_OUT, supress_time_out = False)        


if(__name__ == "__main__"):
    # supress_time_out is kwarg to timer wrapper that supresses it outputing the runtime of a function call
      
    # write_single_case(150,FP_SINGLE_CASE_IN,"normal_hi",supress_time_out = False)
    write_multi_cases(1000,100,"normal_lo",supress_time_out = False)
    # test_multi_cases_sp(50,100,supress_time_out = False)
    test_multi_cases_mp(1000,100,supress_time_out = False)
    # testing_mp_sp(supress_time_out=True)
    
    # test_single_case_mp(FP_SINGLE_CASE_IN,FP_SINGLE_CASE_OUT,supress_time_out = False)
    # test_single_case_sp(FP_SINGLE_CASE_IN,FP_SINGLE_CASE_OUT,supress_time_out = False)
    # remove_multi_cases(1000,250,supress_time_out = False)
    # testing_at_25_sp()
    
    # for gf in [10]:
    #     remove_multi_cases(gf,100,supress_time_out = False)
    # pass