import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

data = pd.read_csv("./analysis_regular_percent.csv")

categories = ["ED","EG","G","D","P"]
label = ["Far right","Far left", "Left","Right","Political video"]
colours = ["#00008a","#a30000","#fc0000","#006eff","#555555"]

Y= []
Y_reduce=[]
X = np.array(data["X"][:-7])
xs = np.linspace(0,100,2000)
tab_plot=[]

for i in range(0,len(categories)):
    Y.append(np.array(data[categories[i]][:-7]))
    Y_reduce.append(Y[i].reshape(-1, 14).mean(axis=1))
    X_reduce = np.array(range(0,len(Y_reduce[i])))*14
    model = make_interp_spline(X_reduce, Y_reduce[i])
    ys = model(xs)
    tab_plot.append(plt.plot(xs,ys,colours[i],label=label[i]))


plt.axvline(x=35,color="#fcdf00",label="Beginning of autoplay")
plt.xlabel("Number of videos watched",fontsize=18)
plt.ylabel("Percentage of video recommended",fontsize=18)
plt.title("Recommended videos when training bot with 35 far right videos",fontsize=22)
plt.rcParams.update({'font.size': 15})
plt.legend()
plt.show()