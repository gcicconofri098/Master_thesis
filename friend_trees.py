import ROOT
import os

files = {
    "QCD6_flash": "/scratchnvme/cicco/QCD6_good_flash_friend_trees/",
    "QCD7_flash": "/scratchnvme/cicco/QCD7_good_flash_friend_trees/",
    "QCD8_flash": "/scratchnvme/cicco/QCD8_good_flash_friend_trees/",
    "signal_flash": "/scratchnvme/cicco/signal_RunIISummer20UL16_good_flash_friend_trees/",
    }

entries1 = {}
events = {}

processes = ['QCD6_flash']

#processes = list(files.keys())
for i in processes:

    f = os.listdir(files.get(i))
    num = len(f)
    entries1[i] = []
    events[i] = []

    # new_dir = str(files.get(i))[:-1] + "_friend_trees"
    # print("creating or entering new dir")
    # if os.path.isdir(new_dir) is False:
    #     os.makedirs(new_dir)

    for j in range(1, 2):
        print(f"opening file {str(files.get(i)) + str(f[j])}")
        file = ROOT.TFile.Open(str(files.get(i)) + str(f[j]), "UPDATE")

        events_tree = file.Get("Events")
        #events.ResetBit(ROOT.TTree.EStatusBits.kEntriesReshuffled)
        full_tree = file.Get("FullSim")
        #full.ResetBit(ROOT.TTree.EStatusBits.kEntriesReshuffled)
        events_tree.AddFriend(full_tree, "FullSim")
        print("done AddFriend")
        #file.Write()
        #print("written file")
        file.Close()
        print("closed file")

