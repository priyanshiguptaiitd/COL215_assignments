from gates_pins import *

def parse_Input_Rectangles(fpath):
    
    rec_data,rec_total_area= list(),0
    max_width,max_height,width_sum,height_sum = 0,0,0,0 
    
    with open(fpath,'r') as file:
        c = 1
        for l in file.readlines():
            rdata = l.split()
            # Breaks if encounters empty line , Hopefully doesnt
            if(len(rdata)==0):
                break
            rec_data.append(Rect(c,int(rdata[1]),int(rdata[2])))
            c += 1
            height_sum+= int(rdata[2])
            width_sum += int(rdata[1])
            rec_total_area += int(rdata[1])*int(rdata[2])
            max_width = max_width if(max_width >= int(rdata[1])) else int(rdata[1])
            max_height = max_height if(max_height >= int(rdata[2])) else int(rdata[2])
            
    rec_data.sort(reverse=True,key= lambda t: (t.height,t.width))
    
    return rec_data,rec_total_area,max_width,max_height,width_sum,height_sum

def parse_Rec_Data_Readable(rec_data):
    rec_data_readable = [(rec.index,rec.width,rec.height) for rec in rec_data]
    return rec_data_readable

def parse_Rec_Data_Output(rec_data):
    rec_data_output = [(rec.index,rec.x,rec.y) for rec in rec_data]
    return rec_data_output

def parse_Output_Rectangles(optimal_w,optimal_h,rec_data,fpath):
     
    with open(fpath,'w') as file:
        lines_output = list()
        lines_output.append(f"bounding_box {optimal_w} {optimal_h} \n")
        c = 1
        for rdata in rec_data:
            lines_output.append(f"g{rdata[0]} {rdata[1]} {rdata[2]} \n")
        file.writelines(lines_output)
    
    return 1

