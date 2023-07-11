import ROOT 
import os
import array

files = {
    "QCD1": "/scratchnvme/cicco/QCD1/",
    "QCD2": "/scratchnvme/cicco/QCD2/",
    "QCD3": "/scratchnvme/cicco/QCD3/",
    "QCD4": "/scratchnvme/cicco/QCD4/",
    "QCD5": "/scratchnvme/cicco/QCD5/",
    "QCD6": "/scratchnvme/cicco/QCD6_good_flash/",
    "QCD7": "/scratchnvme/cicco/QCD7_good_flash/",
    "QCD8": "/scratchnvme/cicco/QCD8_good_flash/",
    "WJets1": "/scratchnvme/cicco/WJets1/",
    "WJets2": "/scratchnvme/cicco/WJets2/",
    "WJets3": "/scratchnvme/cicco/WJets3/",
    "ZJets1": "/scratchnvme/cicco/ZJets1/",
    "ZJets2": "/scratchnvme/cicco/ZJets2/",
    "ZJets3": "/scratchnvme/cicco/ZJets3/",
    "TTHad": "/scratchnvme/cicco/TTHad/",
    "TTSemilept": "/scratchnvme/cicco/TTSemilept/",
    "ST_tw_antitop": "/scratchnvme/cicco/ST_tw_antitop/",
    "ST_tw_top": "/scratchnvme/cicco/ST_tw_top/",
    "GGH": "/scratchnvme/cicco/GGH/",
    "VBFH": "/scratchnvme/cicco/VBFH/",
    "ttH": "/scratchnvme/cicco/ttH/",
    "WMinusH": "/scratchnvme/cicco/WMinusH/",
    "WPlusH": "/scratchnvme/cicco/WPlusH/",
    "ZH": "/scratchnvme/cicco/ZH/",
    "ggZH": "/scratchnvme/cicco/ggZH/",
    "WW": "/scratchnvme/cicco/WW/",
    "WZ": "/scratchnvme/cicco/WZ/",
    "ZZ": "/scratchnvme/cicco/ZZ/",
    "signal": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
}

#processes = list(files.keys())
processes = ['QCD8']#, 'QCD7' , 'QCD8', 'signal']


for i in processes:
    f = os.listdir(files.get(i))
    num = len(f)
    print(num)
    for j in range(0, num):
        file = ROOT.TFile.Open(str(files.get(i)) + str(f[j]), "READ")
        tree = file.Get("Events")
        print(f"file: {f[j]}")
        tree.Print("FatJet_particle*")

        #print(f"file{f[j]} has branch of type:{type(temp)}")