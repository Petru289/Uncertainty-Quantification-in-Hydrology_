import spotpy
import numpy as np
from scipy.optimize import fsolve, minimize
import matplotlib.pyplot as plt
from functions import c


results = spotpy.analyser.load_csv_results('HydrologyDREAM')
param_all = results[['parn', 'parD', 'parq', 'parLambda']]
param = param_all[-100:]
param = np.column_stack((param['parn'], param['parD'], param['parq'], param['parLambda']))


time = np.arange(1,101)
cmax = np.zeros(param.shape[0])

for i in range(len(cmax)):
    cmax[i] = np.max(c(100, time, 200, param[i,0], param[i,1], param[i,2], param[i,3]))

#Pick only those values of cmax that are within one standard deviation far from the mean: cmax \in (mean - std, mean + std)
mean = np.mean(cmax)
std =  np.std(cmax)
ind = np.abs(cmax - mean) < std
param = param[ind]


def getTfromConcentration(c, x, M, n, D, q, Lambda):
    func = lambda t: M / np.sqrt(4 * np.pi * D * t) * np.exp(- (x - q * t / n) ** 2 / (4 * D * t) - Lambda * t) - c
    #res = minimize(-func, 60)
    return fsolve(func, x0 = 60)

def getXfromConcentration(c, t, M, n, D, q ,Lambda):
    A = M / (np.sqrt(4 * np.pi * D * t))
    x1 = q * t / n - np.sqrt(- 4 * D * t * (np.log(c / A) + Lambda * t))
    x2 = q * t / n + np.sqrt(- 4 * D * t * (np.log(c / A) + Lambda * t))
    return [x1, x2]

#x where contaminant is detectable at day 36, i.e. earliest you can measure something -- gives farthest point (i.e. closest to the drinking well)
#we can do measurements in the allowed time interval only before the center of masse passed the sampling point
for i in range(param.shape[0]):
    tcrit = getTfromConcentration(2.5, 100, 200, param[i,0], param[i,1], param[i,2], param[i,3])[0]
    tdet = tcrit - 10
    print("tcrit - 10:")
    print(tdet)
    x_s = getXfromConcentration(10 ** (-5), 36, 200, param[i,0], param[i,1], param[i,2], param[i,3])
    print("x where contaminant is detectable (10^(-5)) at day 36:")
    print(x_s[1])
    conc1 = c(x_s[1], 36, 200, param[i,0], param[i,1], param[i,2], param[i,3]) #should give 10 ** (-5)
    conc2 = c(x_s[1], tdet, 200, param[i,0], param[i,1], param[i,2], param[i,3])
    print("Concentration on time t = 36:")
    print(conc1)
    print("Concentration on time tcrit - 10:")
    print(conc2)
    print("Max:")
    print(np.max(c(x_s[1], time, 200, param[i,0], param[i,1], param[i,2], param[i,3])))
    print("Day of maximum:")
    print(np.argmax(c(x_s[1], time, 200, param[i,0], param[i,1], param[i,2], param[i,3])))
    print(" ")

    #Divide the interval to obtain 5 points in total
    h = (tdet - 36) / 4
    obstimes = np.array([36, np.floor(36 + h), np.floor(36 + 2*h), np.floor(36 + 3*h), tdet])



#x where contaminant is 0.5 at day 36. We want the maximum to be attained at the half time between 36 and tcrit - 10,
#so that we can do measurements in that time interval when the before and after the center of mass passed the sampling point
#we can figure out from previous simulations that this approximately happens when contaminant is about 0.5 at day 36

    tcrit = getTfromConcentration(2.5, 100, 200, param[i,0], param[i,1], param[i,2], param[i,3])[0]
    tdet = tcrit - 10
    print("tcrit - 10:")
    print(tdet)
    x_s = getXfromConcentration(0.5, 36, 200, param[i,0], param[i,1], param[i,2], param[i,3])
    print("x where contaminant is 0.5 at day 36:")
    print(x_s[1])
    conc1 = c(x_s[1], 36, 200, param[i,0], param[i,1], param[i,2], param[i,3]) #should give 10 ** (-1)
    conc2 = c(x_s[1], tdet, 200, param[i,0], param[i,1], param[i,2], param[i,3])
    print("Concentration on time t = 36:")
    print(conc1)
    print("Concentration on time tcrit - 10:")
    print(conc2)
    print("Max:")
    print(np.max(c(x_s[1], time, 200, param[i,0], param[i,1], param[i,2], param[i,3])))
    print("Day of maximum:")
    print(np.argmax(c(x_s[1], time, 200, param[i,0], param[i,1], param[i,2], param[i,3])))
    print("Middle time between 36 and tcrit-10:")
    tmiddle = 36 + np.floor((tdet - 36) / 2)
    print(tmiddle)
    print(" ")

    #Divide the interval to obtain 5 points in total
    h = (tdet - 36) / 4
    obstimes = np.array([36, np.floor(36 + h), np.floor(36 + 2*h), np.floor(36 + 3*h), tdet])


#x where contaminant is 0.1 at day tcrit - 10. We want the maximum to be attained at approximately day 36,
#so that we can do measurements only after the center of mass passed the sampling point
#we can figure out from previous simulations that this approximately happens when contaminant is about 0.1 at day tcrit - 10
    tcrit = getTfromConcentration(2.5, 100, 200, param[i,0], param[i,1], param[i,2], param[i,3])[0]
    tdet = tcrit - 10
    print("tcrit - 10:")
    print(tdet)
    x_s = getXfromConcentration(0.1, tdet, 200, param[i,0], param[i,1], param[i,2], param[i,3])
    print("x where contaminant is 0.5 at day tcrit - 10:")
    print(x_s[0])
    conc1 = c(x_s[0], 36, 200, param[i,0], param[i,1], param[i,2], param[i,3]) 
    conc2 = c(x_s[0], tdet, 200, param[i,0], param[i,1], param[i,2], param[i,3]) #should give 0.5
    print("Concentration on time t = 36:")
    print(conc1)
    print("Concentration on time tcrit - 10:")
    print(conc2)
    print("Max:")
    print(np.max(c(x_s[0], time, 200, param[i,0], param[i,1], param[i,2], param[i,3])))
    print("Day of maximum:")
    print(np.argmax(c(x_s[0], time, 200, param[i,0], param[i,1], param[i,2], param[i,3])))
    print(" ")

    #Divide the interval to obtain 5 points in total
    h = (tdet - 36) / 4
    obstimes = np.array([36, np.floor(36 + h), np.floor(36 + 2*h), np.floor(36 + 3*h), tdet])
    


# for i in range(param.shape[0]):
#     concentration = c(100, time, 200, param[i,0], param[i,1], param[i,2], param[i,3])
#     plt.plot(time, concentration, alpha = 0.2, color = 'navy')

# plt.ylabel('concentration $[kg/m^3]$')
# plt.xlabel('time [days]')
# plt.show()


print(2)









