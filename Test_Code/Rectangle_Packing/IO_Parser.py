from Rect import *
        
def parse_Input_Rectangles(fpath):
    
    rec_data,rec_total_area= list(),0
    max_width,max_height,width_sum,height_sum = 0,0,0,0 
    
    with open(fpath,'r') as file:
        c = 1
        for l in file.readlines():
            rdata = l.split()
            rec_data.append(Rect(c,int(rdata[1]),int(rdata[2])))
            c += 1
            height_sum+= int(rdata[2])
            width_sum += int(rdata[1])
            rec_total_area += int(rdata[1])*int(rdata[2])
            max_width,max_height = max(max_width,int(rdata[1])),max(max_height,int(rdata[1])) 
    
    rec_data.sort(reverse=True,key= lambda t: (t.height,t.width))
    
    return rec_data,rec_total_area,max_width,max_height,width_sum,height_sum

def parse_Rec_Data_Readable(rec_data):
    rec_data_readable = [(rec.index,rec.width,rec.height) for rec in rec_data]
    return rec_data_readable

def parse_Output_Rectangles(optimal_w,optimal_h,rec_data):
    
    with open(r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\SW_Assignment_1_Files\Output_Test_Cases\output.txt",'w') as file:
        lines_output = list()
        lines_output.append(f"bounding_box {optimal_w} {optimal_h} \n")
        c = 1
        for rdata in rec_data:
            lines_output.append(f"g{rdata[0]} {rdata[1]} {rdata[2]} \n")
        file.writelines(lines_output)
    
    return 1


if(__name__ == "__main__"):
    fp = r"C:\Users\YASH\OneDrive\Desktop\IIT D\Sem 3\Courses\COL215\Practical Work\SW Assignments\SW_Assignment_1\SW_Assignment_1_Files\Test_Cases\input.txt"
    rec_data,rec_tot_area,mw,mh,ws,hs = parse_Input_Rectangles(fp)
    rdv,cells_p,check_pack = Pack_by_Pixel(rec_data,7,6)
    if(check_pack is not None):
        print(parse_Rec_Data_Ouput(rdv),f"Packing Efficiency : {cells_p/(7*6) : .4f}")
        parse_Output_Rectangles(6,7,parse_Rec_Data_Ouput(rdv)) 
    
    
        
    
