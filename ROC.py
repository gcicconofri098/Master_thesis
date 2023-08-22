import matplotlib.pyplot as plt
import numpy as np

#efficiency =  np.array([1., 0.99889781, 0.99748071, 0.99559125, 0.9943316,  0.9914974, 0.98882066, 0.9844119,  0.98031806, 0.9727602,  0.96315541, 0.94678003, 0.91261219, 0.808849,   0. ])
#bckg_rej = np.array([0., 0.36426696, 0.4730878 , 0.54577745, 0.60342722 ,0.65196603, 0.69536713, 0.73469023, 0.77200962, 0.80789219, 0.84413062, 0.88163062, 0.9208168,  0.96411814, 1.        ])


efficiency_fullsim = open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/efficiency_fullsim_all_QCD.txt", "r") #1
rejection_fullsim = open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/rejection_fullsim_all_QCD.txt", "r")

efficiency_flashim = open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/efficiency_flashsim_all_QCD.txt", "r") #2
rejection_flashim = open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/rejection_flashsim_all_QCD.txt", "r")

efficiency_phase2 = open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/efficiency_phase2_QCD.txt", "r") #3
rejection_phase2 = open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/rejection_phase2_QCD.txt", "r")



efficiency_1 = np.array([])
bckg_rej_1 = np.array([])

efficiency_2 = np.array([])
bckg_rej_2 = np.array([])

efficiency_3 = np.array([])
bckg_rej_3 = np.array([])

# efficiency_4 = np.array([])
# bckg_rej_4 = np.array([])

for j in range(0, 15):
    line_e_1 = efficiency_fullsim.readline()
    line_r_1 = rejection_fullsim.readline()

    efficiency_1 = np.append(efficiency_1, float(line_e_1[:-1]))
    bckg_rej_1 = np.append(bckg_rej_1, float(line_r_1[:-1]))

    line_e_2 = efficiency_flashim.readline()
    line_r_2 = rejection_flashim.readline()

    efficiency_2 = np.append(efficiency_2, float(line_e_2[:-1]))
    bckg_rej_2 = np.append(bckg_rej_2, float(line_r_2[:-1]))

    line_e_3 = efficiency_phase2.readline()
    line_r_3 = rejection_phase2.readline()

    efficiency_3 = np.append(efficiency_3, float(line_e_3[:-1]))
    bckg_rej_3 = np.append(bckg_rej_3, float(line_r_3[:-1]))

#for j in range(0,30):
    
    # line_e_2 = efficiency_PN_fullsim.readline()
    # line_r_2 = rejection_PN_fullsim.readline()

    # efficiency_2 = np.append(efficiency_2, float(line_e_2[:-1]))
    # bckg_rej_2 = np.append(bckg_rej_2, float(line_r_2[:-1]))


efficiency_fullsim.close()
rejection_fullsim.close()

efficiency_flashim.close()
rejection_flashim.close()

efficiency_phase2.close()
rejection_phase2.close()

# efficiency_Xbb_vs_Xcc_Xqq.close()
# rejection_Xbb_vs_Xcc_Xqq.close()

new_efficiency_1 = np.delete(efficiency_1, -1)
new_bckg_rej_1 = np.delete(bckg_rej_1, -1)

bg_efficiency_1 = 1 - new_bckg_rej_1


new_efficiency_2 = np.delete(efficiency_2, -1)
new_bckg_rej_2 = np.delete(bckg_rej_2, -1)

bg_efficiency_2 = 1 - new_bckg_rej_2


new_efficiency_3 = np.delete(efficiency_3, -1)
new_bckg_rej_3 = np.delete(bckg_rej_3, -1)

bg_efficiency_3 = 1 - new_bckg_rej_3


# new_efficiency_4 = np.delete(efficiency_4, -1)
# new_bckg_rej_4 = np.delete(bckg_rej_4, -1)

# bg_efficiency_4 = 1 - new_bckg_rej_4

#! PLOT

#print("values for comparison @ T>0.857: efficiency = {}, background rejection: {}".format(efficiency[11], bg_efficiency[11]))

plt.plot(new_efficiency_1, bg_efficiency_1, label ='fullsim', color = 'seagreen', marker = '.' , markersize = 4)

plt.plot(new_efficiency_2, bg_efficiency_2, label ='flashsim', color = 'lightskyblue', marker = '.' , markersize = 4)

plt.plot(new_efficiency_3, bg_efficiency_3, label ='phase2', color = 'lightcoral', marker = '.' , markersize = 4)

#plt.plot(new_efficiency_4, bg_efficiency_4, label ='$T_{Xbb} / (1 - T_{Xcc} - T_{Xqq})$', color = 'g')


plt.plot(new_efficiency_1[7], bg_efficiency_1[7], marker = 's', linestyle= '', color='darkgreen', markersize=6)#, label='fullsim $T > 0.85$')
plt.plot(new_efficiency_2[7], bg_efficiency_2[7], marker = 's', linestyle= '', color='mediumblue', markersize=6)#, label='flashsim $T > 0.85$')
plt.plot(new_efficiency_3[7], bg_efficiency_3[7], marker = 's', linestyle= '', color='crimson', markersize=6)#, label='phase 2 $T > 0.85$')

plt.plot(new_efficiency_1[10], bg_efficiency_1[10], marker = 'P', linestyle= '', color='darkgreen', markersize=6)#, label='fullsim $T > 0.91$')
plt.plot(new_efficiency_2[10], bg_efficiency_2[10], marker = 'P', linestyle= '', color='mediumblue', markersize=6)#, label='flashsim $T > 0.91$')
plt.plot(new_efficiency_3[10], bg_efficiency_3[10], marker = 'P', linestyle= '', color='crimson', markersize=6)#, label='phase 2 $T > 0.91$')


# plt.plot(new_efficiency_2[27], bg_efficiency_2[27], marker = 's', linestyle= '', color='crimson', markersize=6)#, label='$T> 0.98$')

plt.plot(new_efficiency_1[12], bg_efficiency_1[12], marker = 'X', linestyle= '', color='darkgreen', markersize=6)#, label='fullsim $T> 0.96$')
plt.plot(new_efficiency_2[12], bg_efficiency_2[12], marker = 'X', linestyle= '', color='mediumblue', markersize=6)#, label='flashsim $T> 0.96$')
plt.plot(new_efficiency_3[12], bg_efficiency_3[12], marker = 'X', linestyle= '', color='crimson', markersize=6)#, label='phase 2 $T> 0.96$')

plt.plot(new_efficiency_1[0], bg_efficiency_1[0], marker = 'd', linestyle= '', color='darkgreen', markersize=6)#, label='fullsim $T> 0.7$')
plt.plot(new_efficiency_2[0], bg_efficiency_2[0], marker = 'd', linestyle= '', color='mediumblue', markersize=6)#, label='flashsim $T> 0.7$')
plt.plot(new_efficiency_3[0], bg_efficiency_3[0], marker = 'd', linestyle= '', color='crimson', markersize=6)#, label='phase 2 $T> 0.7$')

plt.plot(0,0, marker = 's', linestyle= '', color='black', markersize=6, label='$T > 0.85$')
plt.plot(0,0, marker = 'P', linestyle= '', color='black', markersize=6, label='$T > 0.91$')
plt.plot(0,0, marker = 'X', linestyle= '', color='black', markersize=6, label='$T > 0.96$')
plt.plot(0,0, marker = 'd', linestyle= '', color='black', markersize=6, label='$T > 0.7$')




plt.legend()

plt.xlabel('Signal efficiency')
plt.ylabel('background efficiency')
plt.yscale("log")
#plt.ylim(3e-3,1e-1)
plt.xlim(0.68,1)
#plt.grid()
plt.show()

plt.savefig('ROC_comp_weighted.png')