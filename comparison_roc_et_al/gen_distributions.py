import ROOT 
import os

ROOT.EnableImplicitMT()


module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")


#plt.rcParams['text.usetex'] = True

ROOT.gStyle.SetOptStat(0)


ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')



files = {
    "QCD6_flash": "/scratchnvme/cicco/QCD6_good_flash/",
    "QCD7_flash": "/scratchnvme/cicco/QCD7_good_flash/",
    "QCD8_flash": "/scratchnvme/cicco/QCD8_good_flash/",
    }

processes = list(files.keys())

df = {}
entries = {}

events_chain = {}
full_chain = {}

histos ={}

for i in processes:
    f = os.listdir(files.get(i))
    num = len(f)
    entries[i] = []

    print("creating the TChains")
    events_chain[i] = ROOT.TChain("Events")
    full_chain[i] = ROOT.TChain("FullSim")

    for j in range(0, num):
        entries[i].append(str(files.get(i)) + str(f[j]))

        print("adding files to the TChains")
        events_chain[i].Add(str(files.get(i)) + str(f[j]))
        full_chain[i].Add(str(files.get(i)) + str(f[j]))
    events_chain[i].AddFriend(full_chain[i])

    df[i] = ROOT.RDataFrame(events_chain[i])
        

for i in processes:
    df[i] = (df[i]
        .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
        .Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")
        .Define("HbbvsQCD_discriminator_lower_limited", "Where(FatJet_particleNetMD_XbbvsQCD>=0,  FatJet_particleNetMD_XbbvsQCD, 0)")
        .Define("HbbvsQCD_discriminator_limited", "Where(HbbvsQCD_discriminator_lower_limited<1, HbbvsQCD_discriminator_lower_limited, 0.9995) ")

        .Define("Selection", "Post_calibration_pt> 300 && Post_calibration_pt < 500 && abs(FatJet_eta) < 2.4")
        .Define("Selected_jets", "Post_calibration_pt[Selection]")        
        )
        #df[i] = df[i].Filter("!matching_index.empty()")
    df[i] = df[i].Filter("Selected_jets.size()>=2")



    df[i] = (df[i]

            .Define("new_discriminator", "HbbvsQCD_discriminator_limited[Selection]")
            .Define("FatJet_eta_sel", "FatJet_eta[Selection]")
            .Define("FatJet_phi_sel", "FatJet_phi[Selection]")
            .Define("Softdrop_sel_jets", "FatJet_msoftdrop[Selection]")
            .Define("Selected_pt", "Post_calibration_pt[Selection]")
    )

    df[i] = df[i].Filter("Softdrop_sel_jets.size()>=2")

    df[i] = (
            df[i]
            .Define("sorted_FatJet_deepTagMD_HbbvsQCD", "Reverse(Argsort(new_discriminator))")
            .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
            .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
        )
    df[i] = df[i].Filter("Softdrop_sel_jets[Jet1_index]> 40 && Softdrop_sel_jets[Jet2_index]> 40")

    df[i] = df[i].Filter("new_discriminator[Jet1_index]>0.995 && new_discriminator[Jet2_index]>0.98")

    df[i] = (df[i]
                .Define("jet1_discr", "new_discriminator[Jet1_index]")
                .Define("jet1_softdrop", "Softdrop_sel_jets[Jet1_index]")
                .Define("jet2_discr", "new_discriminator[Jet2_index]")
                .Define("jet2_softdrop", "Softdrop_sel_jets[Jet2_index]")
        )


    df[i] = (df[i]
            .Define("Selected_genjet_pt", "Take(GenJetAK8_pt, matching_index[Selection])")  
            .Define("Selected_genjet_eta", "Take(GenJetAK8_eta, matching_index[Selection])")        
            .Define("Selected_genjet_mass", "Take(GenJetAK8_mass, matching_index[Selection])")        
            .Define("Selected_genjet_phi", "Take(GenJetAK8_phi, matching_index[Selection])")        
            .Define("Matching_hadron_flavour", "Take(GenJetAK8_hadronFlavour, matching_index[Selection])")
            .Define("Matching_parton_flavour", "Take(GenJetAK8_partonFlavour, matching_index[Selection])")
    )
    histos[i] = {}

    histos[i]['Gen_pt'] = df[i].Histo1D((str(i), str(i) +"; Pt; Events", 80, 200, 1000), "Selected_genjet_pt").GetValue()
    histos[i]['Gen_eta'] = df[i].Histo1D((str(i), str(i) +"; Eta; Events", 50, -5, 5), "Selected_genjet_eta").GetValue()
    histos[i]['Gen_phi'] = df[i].Histo1D((str(i), str(i) +"; Phi; Events", 50, -3, 3), "Selected_genjet_phi").GetValue()
    histos[i]['Gen_mass'] = df[i].Histo1D((str(i), str(i) +"; Mass; Events", 40, 40, 300), "Selected_genjet_mass").GetValue()
    histos[i]['Gen_parton_flavour'] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 27, -5, 22), "Matching_parton_flavour").GetValue()
    histos[i]['Gen_hadron_flavour'] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 20, 0, 7), "Matching_hadron_flavour").GetValue()

variables = list(histos['QCD6_flash'].keys())
stacked_QCD = {}
for j in variables:
    
    stacked_QCD[j] = histos['QCD6_flash'][j].Clone()
    stacked_QCD[j].Add(histos['QCD7_flash'][j])
    stacked_QCD[j].Add(histos['QCD8_flash'][j])

c1 = ROOT.TCanvas("c1", "GenJetAK8_pt distribution", 4500, 3500)

stacked_QCD['Gen_pt'].Draw("HISTO")
stacked_QCD['Gen_pt'].SetTitle("Pt distribution for GenJetAK8")
stacked_QCD["Gen_pt"].SetLineWidth(2)


c2 = ROOT.TCanvas("c2", "GenJetAK8_eta distribution", 4500, 3500)

stacked_QCD['Gen_eta'].Draw("HISTO")
stacked_QCD['Gen_eta'].SetTitle("Eta distribution for GenJetAK8")
stacked_QCD["Gen_eta"].SetLineWidth(2)


c3 = ROOT.TCanvas("c3", "GenJetAK8_phi distribution", 4500, 3500)

stacked_QCD['Gen_phi'].Draw("HISTO")
stacked_QCD['Gen_phi'].SetTitle("Phi distribution for GenJetAK8")
stacked_QCD["Gen_phi"].SetLineWidth(2)


c4 = ROOT.TCanvas("c4", "GenJetAK8_mass distribution", 4500, 3500)

stacked_QCD['Gen_mass'].Draw("HISTO")
stacked_QCD['Gen_mass'].SetTitle("Mass distribution for GenJetAK8")
stacked_QCD["Gen_mass"].SetLineWidth(2)


c5 = ROOT.TCanvas("c5", "GenJetAK8_parton_flavour distribution", 4500, 3500)

stacked_QCD['Gen_parton_flavour'].Draw("HISTO")
stacked_QCD['Gen_parton_flavour'].SetTitle("Parton flavour distribution for GenJetAK8")
stacked_QCD["Gen_parton_flavour"].SetLineWidth(2)


c6 = ROOT.TCanvas("c6", "GenJetAK8_hadron_flavour distribution", 4500, 3500)

stacked_QCD['Gen_hadron_flavour'].Draw("HISTO")
stacked_QCD['Gen_hadron_flavour'].SetTitle("Hadron flavour distribution for GenJetAK8")
stacked_QCD["Gen_hadron_flavour"].SetLineWidth(2)


c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/gen_distributions/gen_pt.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/gen_distributions/gen_eta.pdf")
c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/gen_distributions/gen_phi.pdf")
c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/gen_distributions/gen_mass.pdf")
c5.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/gen_distributions/gen_parton_flavour.pdf")
c6.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/gen_distributions/gen_hadron_flavour.pdf")
