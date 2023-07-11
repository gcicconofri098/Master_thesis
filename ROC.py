import matplotlib.pyplot as plt
import numpy as np

#efficiency =  np.array([1., 0.99889781, 0.99748071, 0.99559125, 0.9943316,  0.9914974, 0.98882066, 0.9844119,  0.98031806, 0.9727602,  0.96315541, 0.94678003, 0.91261219, 0.808849,   0. ])
#bckg_rej = np.array([0., 0.36426696, 0.4730878 , 0.54577745, 0.60342722 ,0.65196603, 0.69536713, 0.73469023, 0.77200962, 0.80789219, 0.84413062, 0.88163062, 0.9208168,  0.96411814, 1.        ])


efficiency_HbbvsQCD = open("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/efficiency_flashsim.txt", "r") #1
rejection_HbbvsQCD = open("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/rejection_flashsim.txt", "r")

# efficiency_PN_HbbvsQCD = open("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/efficiency_PN_HbbvsQCD.txt", "r") #2
# rejection_PN_HbbvsQCD = open("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/rejection_PN_HbbvsQCD.txt", "r")


# efficiency_Xbb_vs_QCD =open("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/efficiency_Xbb_vs_QCD.txt", "r") #3
# rejection_Xbb_vs_QCD = open("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/rejection_Xbb_vs_QCD.txt", "r")

# efficiency_Xbb_vs_Xcc_Xqq = open("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/efficiency_Xbb_vs_Xcc_Xqq.txt", "r") #4
# rejection_Xbb_vs_Xcc_Xqq = open("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/rejection_Xbb_vs_Xcc_Xqq.txt", "r")



efficiency_1 = np.array([])
bckg_rej_1 = np.array([])

# efficiency_2 = np.array([])
# bckg_rej_2 = np.array([])

# efficiency_3 = np.array([])
# bckg_rej_3 = np.array([])

# efficiency_4 = np.array([])
# bckg_rej_4 = np.array([])

for j in range(0, 15):
    line_e_1 = efficiency_HbbvsQCD.readline()
    line_r_1 = rejection_HbbvsQCD.readline()

    efficiency_1 = np.append(efficiency_1, float(line_e_1[:-1]))
    bckg_rej_1 = np.append(bckg_rej_1, float(line_r_1[:-1]))

    # line_e_3 = efficiency_Xbb_vs_QCD.readline()
    # line_r_3 = rejection_Xbb_vs_QCD.readline()

    # efficiency_3 = np.append(efficiency_3, float(line_e_3[:-1]))
    # bckg_rej_3 = np.append(bckg_rej_3, float(line_r_3[:-1]))

    # # line_e_4 = efficiency_Xbb_vs_Xcc_Xqq.readline()
    # line_r_4 = rejection_Xbb_vs_Xcc_Xqq.readline()

    # efficiency_4 = np.append(efficiency_4, float(line_e_4[:-1]))
    # bckg_rej_4 = np.append(bckg_rej_4, float(line_r_4[:-1]))

#for j in range(0,30):
    
    # line_e_2 = efficiency_PN_HbbvsQCD.readline()
    # line_r_2 = rejection_PN_HbbvsQCD.readline()

    # efficiency_2 = np.append(efficiency_2, float(line_e_2[:-1]))
    # bckg_rej_2 = np.append(bckg_rej_2, float(line_r_2[:-1]))


efficiency_HbbvsQCD.close()
rejection_HbbvsQCD.close()

# efficiency_PN_HbbvsQCD.close()
# rejection_PN_HbbvsQCD.close()

# efficiency_Xbb_vs_QCD.close()
# rejection_Xbb_vs_QCD.close()

# efficiency_Xbb_vs_Xcc_Xqq.close()
# rejection_Xbb_vs_Xcc_Xqq.close()

new_efficiency_1 = np.delete(efficiency_1, -1)
new_bckg_rej_1 = np.delete(bckg_rej_1, -1)

bg_efficiency_1 = 1 - new_bckg_rej_1


# new_efficiency_2 = np.delete(efficiency_2, -1)
# new_bckg_rej_2 = np.delete(bckg_rej_2, -1)

# bg_efficiency_2 = 1 - new_bckg_rej_2


# new_efficiency_3 = np.delete(efficiency_3, -1)
# new_bckg_rej_3 = np.delete(bckg_rej_3, -1)

# bg_efficiency_3 = 1 - new_bckg_rej_3


# new_efficiency_4 = np.delete(efficiency_4, -1)
# new_bckg_rej_4 = np.delete(bckg_rej_4, -1)

# bg_efficiency_4 = 1 - new_bckg_rej_4

#! PLOT

#print("values for comparison @ T>0.857: efficiency = {}, background rejection: {}".format(efficiency[11], bg_efficiency[11]))

plt.plot(new_efficiency_1, bg_efficiency_1, label ='FatJet_deepTagMD_HbbvsQCD', color = 'r')

#plt.plot(new_efficiency_2, bg_efficiency_2, label ='FatJet_particleNet_HbbvsQCD', color = 'b')

#plt.plot(new_efficiency_3, bg_efficiency_3, label ='$T_{Xbb}/(T_{Xbb} + T_{QCD})$', color = 'orange')

#plt.plot(new_efficiency_4, bg_efficiency_4, label ='$T_{Xbb} / (1 - T_{Xcc} - T_{Xqq})$', color = 'g')


plt.plot(new_efficiency_1[7], bg_efficiency_1[7], marker = 's', linestyle= '', color='c', markersize=6, label='$T > 0.85$')
# plt.plot(new_efficiency_2[19], bg_efficiency_2[19], marker = 's', linestyle= '', color='c', markersize=6)
# plt.plot(new_efficiency_4[13], bg_efficiency_4[13], marker = 's', linestyle= '', color='c', markersize=6)

plt.plot(new_efficiency_1[10], bg_efficiency_1[10], marker = 's', linestyle= '', color='r', markersize=6, label='$T > 0.91$')
# plt.plot(new_efficiency_2[26], bg_efficiency_2[26], marker = 's', linestyle= '', color='r', markersize=6)
# plt.plot(new_efficiency_4[17], bg_efficiency_4[17], marker = 's', linestyle= '', color='r', markersize=6)


# plt.plot(new_efficiency_2[27], bg_efficiency_2[27], marker = 's', linestyle= '', color='b', markersize=6, label='$T> 0.98$')

plt.plot(new_efficiency_1[0], bg_efficiency_1[0], marker = 's', linestyle= '', color='g', markersize=6, label='$T> 0.7$')
# plt.plot(new_efficiency_2[10], bg_efficiency_2[10], marker = 's', linestyle= '', color='g', markersize=6)
# plt.plot(new_efficiency_4[7], bg_efficiency_4[7], marker = 's', linestyle= '', color='g', markersize=6)



plt.legend()

plt.xlabel('Signal efficiency')
plt.ylabel('background efficiency')
plt.yscale("log")
#plt.ylim(3e-3,1e-1)
#plt.xlim(0.,1)
#plt.grid()
plt.show()

plt.savefig('ROC_flash.png')