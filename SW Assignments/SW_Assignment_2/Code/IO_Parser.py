from gates_pins import *

def parse_Input_Gates(fpath):
    g_data = Gate_Data() 
    with open(fpath,'r') as file:
        cgate,cwire = 1,1
        for l in file.readlines():
            rdata = (l.strip()).split()
            # Breaks if encounters empty line , Hopefully doesnt
            if(len(rdata)==0):
                break
            if(rdata[0].startswith('g')):
                g_data.set_gate(cgate,int(rdata[1]),int(rdata[2]))
                cgate += 1
            elif(rdata[0]=='pins'):
                gindex = int(rdata[1][1:])
                pin_freq = (len(rdata)-2)//2
                for i in range(1,pin_freq+1):
                    g_data.get_gate(gindex).set_pin(i,int(rdata[2*i]),int(rdata[2*i+1]))
            elif(rdata[0]=='wire'):
                gp1 = rdata[1].split('.')
                gp2 = rdata[2].split('.')
                g1,p1 = int(gp1[0][1:]),int(gp1[1][1:])
                g2,p2 = int(gp2[0][1:]),int(gp2[1][1:])
                g_data.set_wire(cwire,g1,p1,g2,p2)
                cwire += 1
    return g_data

def parse_Output_Gates(g_data : Gate_Data,fpath):
    optimal_w, optimal_h = g_data.get_bbox()
    rec_data = g_data.get_gate_data() 
    with open(fpath,'w') as file:
        lines_output = list()
        lines_output.append(f"bounding_box {optimal_w} {optimal_h} \n")
        for rdata in rec_data:
            lines_output.append(f"g{rdata[0]} {rdata[1]} {rdata[2]} \n")
        file.writelines(lines_output)
    

