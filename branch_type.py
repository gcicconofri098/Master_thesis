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

# processes = list(files.keys())
processes = ["signal"]
#! vanno controllati QCD6, 'QCD7' , 'QCD8', 'signal']


list_skip_QCD6 = [
    "0C61597A-3B75-4847-AB41-8C7836A3ABFD.root",
    "64C8D56A-0144-A344-AF48-EAE3EA799441.root",
    "740B4D56-6C96-FB44-B238-6EA51760412F.root",
    "B0B7A670-3CB0-C145-AEF8-9EFFC6C5945B.root",
    "B748163A-F39B-304C-B3C1-ECA559B3A883.root",
    "CE4D4D44-ED24-9949-9725-5CD1ED2301A1.root",
    "E73B04FA-B24E-104C-AA26-297EB416CE99.root",
    "EDF61A4D-119C-0144-B795-2D41733A7C3F.root",
    "58ECDC77-DB0B-8C46-BEE3-684B73591878.root",
    "7CBF439E-A1F7-E04B-A401-B928BCDF0BD1.root",
    "144A4B88-8FC9-0841-BC09-900E3DAE3DF3.root",
    "65A97A61-AF49-E941-B89C-DD988890D07D.root",
    "6842B510-2674-8148-AE6A-8DC7C51EE073.root",
    "9164ADC3-D6EE-F147-B7F5-6C815B7B7378.root",
    "F1EF8AB0-6FC5-F84A-97EA-02AE8F8389EC.root",
]

list_skip_QCD7 = [
    "591EBC4C-E20B-AF49-B865-DFDCD383D562.root",
    "5FAA3FD1-66D9-8547-AB56-825E6E5F3AF7.root",
    "796FF1A0-09E8-344A-B03F-BE3D5C9AA5AC.root",
    "95C33BA7-52EA-5448-B641-A6EF316BD045.root",
    "A93F7805-ED4E-BB48-9B3E-9DD930943A6A.root",
    "B3876AA9-202C-B941-905A-77B20AC770F1.root",
    "C9E2A2B3-C43A-3240-BC06-68711CB1B4BC.root",
    "FF3243AA-D860-164C-8B91-BFB42D370B77.root",
    "0732284C-A061-3B40-B8A2-57BCEDF87654.root",
    "623CA65F-FF71-1A47-B618-E2DB1DDB5B51.root",
    "8FEFECB2-A06C-D041-B43B-B15605F1FA29.root",
]
list_skip_QCD8 = [
    "47A52618-D9F3-0441-96DB-7550C7225D78.root",
    "13076D6D-BBE5-FA4A-BD32-FF0509C6FB74.root", 
    "B8FF2FFB-FAD8-4C41-B21A-7A840A282502.root",
    "0293F347-6724-E246-A0FD-75C0251D64B3.root",
    "FF6AE0D9-27EE-2242-B8D2-DAF3ECA7FBAA.root", 

]


list_skip_signal = [
    "47A52618-D9F3-0441-96DB-7550C7225D78.root",
    "13076D6D-BBE5-FA4A-BD32-FF0509C6FB74.root",
    "B8FF2FFB-FAD8-4C41-B21A-7A840A282502.root",
    "0293F347-6724-E246-A0FD-75C0251D64B3.root",
    "FF6AE0D9-27EE-2242-B8D2-DAF3ECA7FBAA.root"
]
for i in processes:
    f = os.listdir(files.get(i))
    num = len(f)
    print(num)
    for j in range(0, num):
        file = ROOT.TFile.Open(str(files.get(i)) + str(f[j]), "READ")
        tree = file.Get("Events")

        # if str(f[j]) == [f for f in list_skip_QCD6]:
        #     continue

        print(f"file: {f[j]}")
        tree.Print("FatJet_particle*")

        # print(f"file{f[j]} has branch of type:{type(temp)}")
