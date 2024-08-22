import matplotlib.pyplot as plt
import numpy as np

xdata = []
ydata_t = []
ydata_peff = []

def hola():
    with open("report_tc_analysis.txt","r") as file:
        fdata = file.readlines()
        for i in range(0,len(fdata),3):
            g = int(fdata[i].split()[-1])
            t =  float(fdata[i+1].split()[-1])
            p_eff = float(fdata[i+2].split()[-1])
            if(g not in [1350,1375,1400,1425,1800] and (g < 900 or  g > 1025)):
                xdata.append(g)
                ydata_t.append(t)
                ydata_peff.append(p_eff)

    model = np.poly1d(np.polyfit(xdata,ydata_t,2))

    polyline = np.linspace(0,2000,10)
    
    print("hi")
    

    # # plt.subplot(2,1,1)
    plt.plot(xdata,ydata_t)
    plt.plot(polyline,model(polyline))

    # plt.subplot(2,1,2)
    # plt.plot(xdata,ydata_peff)
    plt.show()


def bhola():
    
    xdata_sp,ydata_peff_sp,ydata_t_sp = list(),list(),list()
    
    with open("comparison_single_tc_sp.txt","r") as file:
        fdata = file.readlines()
        for i in range(0,len(fdata),3):
            g = int(fdata[i].split()[-1])
            t =  float(fdata[i+1].split()[-1])
            p_eff = float(fdata[i+2].split()[-1])
            xdata_sp.append(g)
            ydata_t_sp.append(t)
            ydata_peff_sp.append(p_eff)

    print("hi")
    # model = np.poly1d(np.polyfit(xdata,ydata_t,2))
    # polyline = np.linspace(0,2000,10)
    # # # plt.subplot(2,1,1)
    # plt.plot(xdata,ydata_t)
    # plt.plot(polyline,model(polyline))
    
    
    xdata_mp,ydata_peff_mp,ydata_t_mp = list(),list(),list()
    
    with open("comparison_single_tc_mp.txt","r") as file:
        fdata = file.readlines()
        for i in range(0,len(fdata),3):
            g = int(fdata[i].split()[-1])
            t =  float(fdata[i+1].split()[-1])
            p_eff = float(fdata[i+2].split()[-1])
            xdata_mp.append(g)
            ydata_t_mp.append(t)
            ydata_peff_mp.append(p_eff)
    
    plt.subplot(1,2,1)
    plt.xticks(np.arange(0, 10001, 200))
    plt.plot(xdata_sp,ydata_t_sp,color = 'g',label = "Single-Iteration Method")
    plt.plot(xdata_mp,ydata_t_mp,color = 'b',label = "Multi-Iteration Method")
    plt.xlabel("Number of Gates [Generated using Normal Distribution with Mean = 50 , SD = 25]")
    plt.ylabel("Packing Efficiency")
    plt.legend(loc="lower right")
    plt.title("Run Time of Multi-Iteration & Single-Iteration VS Number of Gates")
    
    
    
    plt.subplot(1,2,2)
    plt.xticks(np.arange(0, 10001, 200))
    plt.plot(xdata_sp,ydata_peff_sp,color = 'g',label = "Single-Iteration Method")
    plt.plot(xdata_mp,ydata_peff_mp,color = 'b',label = "Multi-Iteration Method")
    plt.xlabel("Number of Gates [Generated using Normal Distribution with Mean = 50 , SD = 25]")
    plt.ylabel("Packing Efficiency")
    plt.legend(loc="lower right")
    plt.title("Packing Efficiency of Multi-Iteration & Single-Iteration VS Number of Gates")
    plt.show()
if(__name__ == "__main__"):
    bhola()