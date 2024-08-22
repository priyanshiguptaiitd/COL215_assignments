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
    
    xdata,ydata_peff,ydata_t = list(),list(),list()
    
    with open("comparison_single_tc_spitr.txt","r") as file:
        fdata = file.readlines()
        for i in range(0,len(fdata),3):
            g = int(fdata[i].split()[-1])
            t =  float(fdata[i+1].split()[-1])
            p_eff = float(fdata[i+2].split()[-1])
            xdata.append(g)
            ydata_t.append(t)
            ydata_peff.append(p_eff)
    print(xdata,ydata_peff)

    print("hi")
    # model = np.poly1d(np.polyfit(xdata,ydata_t,2))
    # polyline = np.linspace(0,2000,10)
    # # # plt.subplot(2,1,1)
    # plt.plot(xdata,ydata_t)
    # plt.plot(polyline,model(polyline))
    plt.plot(xdata,ydata_peff,color = 'g')
    
    xdata,ydata_peff,ydata_t = list(),list(),list()
    
    with open("comparison_single_tc_mpitr.txt","r") as file:
        fdata = file.readlines()
        for i in range(0,len(fdata),3):
            g = int(fdata[i].split()[-1])
            t =  float(fdata[i+1].split()[-1])
            p_eff = float(fdata[i+2].split()[-1])
            xdata.append(g)
            ydata_t.append(t)
            ydata_peff.append(p_eff)
    
    plt.plot(xdata,ydata_peff,color = 'b')
    
    
    
    plt.show()
if(__name__ == "__main__"):
    bhola()