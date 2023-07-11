import ROOT
import os
import numpy as np
from decimal import *


getcontext().prec = 2


module_path_1 = os.path.join(os.path.dirname(__file__), "utils.h")
module_path_2 = os.path.join(os.path.dirname(__file__), "fatjets_utils.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")



ROOT.gInterpreter.ProcessLine(f'#include "{module_path_1}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_2}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')

ROOT.gStyle.SetPaintTextFormat("1.2f")


ROOT.gStyle.SetOptStat(0)

ROOT.EnableImplicitMT(10)

#TODO Background data

# fullsim_path = "/scratchnvme/cicco/QCD7/5FAA3FD1-66D9-8547-AB56-825E6E5F3AF7.root"

# flashsim_path = (
#     "/scratchnvme/cicco/QCD7_good_flash/5FAA3FD1-66D9-8547-AB56-825E6E5F3AF7.root"
# )

# phase2_path = "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg.root"

#TODO Signal data

fullsim_path = "/scratchnvme/cicco/signal_RunIISummer20UL16/212C7FC6-48EC-574D-B7E9-617A974C308E.root"

flashsim_path = "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/212C7FC6-48EC-574D-B7E9-617A974C308E.root"

phase2_path = "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1.root"


df_full = ROOT.RDataFrame("Events", fullsim_path)

df_flash = ROOT.RDataFrame("Events", flashsim_path)

df_phase2 = ROOT.RDataFrame("MJets", phase2_path)

full_pre = df_full.Count().GetValue()

flash_pre = df_flash.Count().GetValue()

phase2_pre = df_phase2.Count().GetValue()

#! FLASHSIM

df_flash = df_flash.Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")

df_flash = df_flash.Filter("nFatJet>=2")



df_flash = (
    df_flash.Define("matching_index", "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
    .Define("Matched_Gen_pt", "Take(GenJetAK8_pt, matching_index)")
)



df_flash = (
    df_flash
    .Define("Pt_ratio_pre", "FatJet_pt/Matched_Gen_pt")
    .Define("Pt_ratio_post", "Post_calibration_pt/Matched_Gen_pt")
)


df_flash = (
    df_flash# && FatJet_pt[0] >300 && FatJet_pt[1] >300")
    .Define("FatJet_Selection", "FatJet_pt > 300")
    .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
    .Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[FatJet_Selection]")
    .Define("Pt_sel_jets", "FatJet_pt[FatJet_Selection]")
    .Define("Post_calib_sel_jets", "Post_calibration_pt[FatJet_Selection]")
)

df_flash = (
    df_flash.Define(
        "sorted_FatJet_deepTagMD_HbbvsQCD",
        "Reverse(Argsort(new_discriminator))",
    )
    .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
    .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
    .Define("Jet1_discriminator", "new_discriminator[Jet1_index]")
    .Define("Jet2_discriminator", "new_discriminator[Jet2_index]")
    )

# df_flash = df_flash.Filter(
#     "new_discriminator[Jet1_index]> 0.86" 
# )


# df_flash = (
#     df_flash
#     .Define(
#         # mu = 13, e = 11
#         "FatJet_Selection",
#         "FatJet_pt > 300 && abs(FatJet_eta) < 2.4 && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Electron_pt, Electron_eta, Electron_phi, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Muon_pt, Muon_eta, Muon_phi, Muon_pfRelIso03_all, 13)",
#     )
#     .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
#     # .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
#     # .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
#     # .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
#     # .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
#     .Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[FatJet_Selection]")
#     .Define("Eta_sel_jets", "FatJet_eta[FatJet_Selection]")
#     .Define("Phi_sel_jets", "FatJet_phi[FatJet_Selection]")
#     .Define("Pt_sel_jets", "FatJet_pt[FatJet_Selection]")
# )
# df_flash = df_flash.Filter("new_discriminator.size()>=2")

# df_flash = (
#     df_flash
#     .Define(
#         "sorted_FatJet_deepTagMD_HbbvsQCD",
#         "Reverse(Argsort(new_discriminator))",
#     )
#     .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
#     .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
# )
# df_flash = df_flash.Filter(
#     "Softdrop_sel_jets[Jet1_index]> 50 && Softdrop_sel_jets[Jet2_index]> 50"
# )
# df_flash = (
#     df_flash
#     .Define("Jet1_Selected_jet_softdrop", "Softdrop_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jet_softdrop", "Softdrop_sel_jets[Jet2_index]")
#     .Define(
#         "Jet1_Selected_jets_discriminator", "new_discriminator[Jet1_index]"
#     )
#     .Define(
#         "Jet2_Selected_jets_discriminator", "new_discriminator[Jet2_index]"
#     )
#     .Define("Jet1_Selected_jets_eta", "Eta_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_eta", "Eta_sel_jets[Jet2_index]")
#     .Define("Jet1_Selected_jets_phi", "Phi_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_phi", "Phi_sel_jets[Jet2_index]")
#     .Define(
#         "Sum_selected_jets",
#         "Jet1_Selected_jet_softdrop + Jet2_Selected_jet_softdrop",
#     )
#     .Define("Jet1_Selected_jets_pt", "Pt_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_pt", "Pt_sel_jets[Jet2_index]")

# )

# df_flash = df_flash.Filter("new_discriminator[Jet1_index]>0.86").Filter("MET_pt <100")


# #! VETO ON VBF

# df_flash = (
#     df_flash
#     .Define(
#         "VBF_jet_preselection",
#         "jet_isolation(Jet_eta, Jet_phi, Eta_sel_jets, Phi_sel_jets) && Jet_pt >25 && abs(Jet_eta) <4.7",
#     )
#     .Define("Candidate_jets_pt", "Jet_pt[VBF_jet_preselection]")
#     .Define("Candidate_jets_mass", "Jet_mass[VBF_jet_preselection]")
#     .Define("Candidate_jets_eta", "Jet_eta[VBF_jet_preselection]")
#     .Define("Candidate_jets_phi", "Jet_phi[VBF_jet_preselection]")
# )

# df_flash = (
#     df_flash
#     .Define("Muon_preselection", "Muon_pt >5")
#     .Define("Candidate_muon_pt", "Muon_pt[Muon_preselection]")
#     .Define("Candidate_muon_eta", "Muon_eta[Muon_preselection]")
#     .Define("Candidate_muon_phi", "Muon_phi[Muon_preselection]")
# )
# df_flash = (
#     df_flash
#     .Define("Electron_preselection", "Electron_pt >7")
#     .Define("Candidate_el_pt", "Electron_pt[Electron_preselection]")
#     .Define("Candidate_el_eta", "Electron_eta[Electron_preselection]")
#     .Define("Candidate_el_phi", "Electron_phi[Electron_preselection]")
# )

# df_flash = (
#     df_flash
#     .Define(
#         "Good_VBF_candidates",
#         "part_isolation(Candidate_jets_eta, Candidate_jets_phi, Candidate_muon_eta, Candidate_muon_phi, Candidate_el_eta, Candidate_el_phi)",
#     )
#     .Define("Good_VBF_jets_eta", "Candidate_jets_eta[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_mass", "Candidate_jets_mass[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_pt", "Candidate_jets_pt[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_phi", "Candidate_jets_phi[Good_VBF_candidates]")
# )
# df_flash = (
#     df_flash
#     .Define("sorted_VBF_jets_pt", "Reverse(Argsort(Good_VBF_jets_pt))")
#     .Define("VBF_Jet1_index", "sorted_VBF_jets_pt[0]")
#     .Define("VBF_Jet2_index", "sorted_VBF_jets_pt[1]")
# )
# df_flash = (
#     df_flash
#     .Define("VBF_Jet1_eta", "Good_VBF_jets_eta[VBF_Jet1_index]")
#     .Define("VBF_Jet2_eta", "Good_VBF_jets_eta[VBF_Jet2_index]")
#     .Define("VBF_Jet1_mass", "Good_VBF_jets_mass[VBF_Jet1_index]")
#     .Define("VBF_Jet2_mass", "Good_VBF_jets_mass[VBF_Jet2_index]")
#     .Define("VBF_Jet1_pt", "Good_VBF_jets_pt[VBF_Jet1_index]")
#     .Define("VBF_Jet2_pt", "Good_VBF_jets_pt[VBF_Jet2_index]")
#     .Define("VBF_Jet1_phi", "Good_VBF_jets_phi[VBF_Jet1_index]")
#     .Define("VBF_Jet2_phi", "Good_VBF_jets_phi[VBF_Jet2_index]")
# )

# df_flash = (
#     df_flash
#     .Define(
#         "Delta_eta",
#         "VBF_Jet1_eta - VBF_Jet2_eta",
#     )
#     .Define(
#         "Jet_invariant_mass",
#         "invariant_mass(VBF_Jet1_pt, VBF_Jet1_eta, VBF_Jet1_phi, VBF_Jet1_mass, VBF_Jet2_pt, VBF_Jet2_eta, VBF_Jet2_phi, VBF_Jet2_mass)",
#     )
# )

# df_flash = (
#     df_flash
#     .Define(
#         "VBF_events", "nJet >=2 && abs(Delta_eta) >4.0 && Jet_invariant_mass > 500"
#     )
#     .Filter("!VBF_events")
# )

#! FULLSIM

df_full = df_full.Filter("nFatJet>=2")


df_full = (
    df_full.Filter("!FatJet_genJetAK8Idx.empty()")
    .Define(
        "good_jets",
        "FatJet_genJetAK8Idx>=0",
    )
    .Define("new_index", "FatJet_genJetAK8Idx[good_jets]")
)


df_full = (
    df_full
    .Define("Matched_GenJet_pt", "Take(GenJetAK8_pt, new_index)")
    .Define("Matched_FatJet_pt", "FatJet_pt[good_jets]")
    .Define("Pt_ratio", "Matched_FatJet_pt/Matched_GenJet_pt"))






df_full = (
    df_full # && FatJet_pt[0] > 300 && FatJet_pt[1] >300")
    .Define("FatJet_Selection", "FatJet_pt > 300")
    .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
    .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
    .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
    .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
    # .Define(
    #     "new_discriminator",
    #     "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)",
    # )
    .Define("new_discriminator", "FatJet_particleNetMD_Xbb/(1-FatJet_particleNetMD_Xcc- FatJet_particleNetMD_Xqq)")
    .Define("Pt_sel_jets", "FatJet_pt[FatJet_Selection]")
)


df_full = (
    df_full.Define(
        "sorted_FatJet_deepTagMD_HbbvsQCD",
        "Reverse(Argsort(new_discriminator))",
    )
    .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
    .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
    .Define("Jet1_discriminator", "new_discriminator[Jet1_index]")
    .Define("Jet2_discriminator", "new_discriminator[Jet2_index]")

)


# df_full = df_full.Filter(
#     "new_discriminator[Jet1_index]> 0.86" 
# )

# df_full = (
#     df_full
#     .Define(
#         # mu = 13, e = 11
#         "FatJet_Selection",
#         "FatJet_pt > 300 && abs(FatJet_eta) < 2.4 && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Electron_pt, Electron_eta, Electron_phi, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Muon_pt, Muon_eta, Muon_phi, Muon_pfRelIso03_all, 13)",
#     )
#     .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
#     .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
#     .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
#     .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
#     .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
#     #.Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[FatJet_Selection]")
#     .Define("Eta_sel_jets", "FatJet_eta[FatJet_Selection]")
#     .Define("Phi_sel_jets", "FatJet_phi[FatJet_Selection]")
#     .Define("Pt_sel_jets", "FatJet_pt[FatJet_Selection]")
# )
# df_full = df_full.Filter("new_discriminator.size()>=2")

# df_full = (
#     df_full
#     .Define(
#         "sorted_FatJet_deepTagMD_HbbvsQCD",
#         "Reverse(Argsort(new_discriminator))",
#     )
#     .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
#     .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
# )
# df_full = df_full.Filter(
#     "Softdrop_sel_jets[Jet1_index]> 50 && Softdrop_sel_jets[Jet2_index]> 50"
# )
# df_full = (
#     df_full
#     .Define("Jet1_Selected_jet_softdrop", "Softdrop_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jet_softdrop", "Softdrop_sel_jets[Jet2_index]")
#     .Define(
#         "Jet1_Selected_jets_discriminator", "new_discriminator[Jet1_index]"
#     )
#     .Define(
#         "Jet2_Selected_jets_discriminator", "new_discriminator[Jet2_index]"
#     )
#     .Define("Jet1_Selected_jets_eta", "Eta_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_eta", "Eta_sel_jets[Jet2_index]")
#     .Define("Jet1_Selected_jets_phi", "Phi_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_phi", "Phi_sel_jets[Jet2_index]")
#     .Define(
#         "Sum_selected_jets",
#         "Jet1_Selected_jet_softdrop + Jet2_Selected_jet_softdrop",
#     )
#     .Define("Jet1_Selected_jets_pt", "Pt_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_pt", "Pt_sel_jets[Jet2_index]")

# )

# df_full = df_full.Filter("new_discriminator[Jet1_index]>0.86").Filter("MET_pt <100")

# #! VETO ON VBF

# df_full = (
#     df_full
#     .Define(
#         "VBF_jet_preselection",
#         "jet_isolation(Jet_eta, Jet_phi, Eta_sel_jets, Phi_sel_jets) && Jet_pt >25 && abs(Jet_eta) <4.7",
#     )
#     .Define("Candidate_jets_pt", "Jet_pt[VBF_jet_preselection]")
#     .Define("Candidate_jets_mass", "Jet_mass[VBF_jet_preselection]")
#     .Define("Candidate_jets_eta", "Jet_eta[VBF_jet_preselection]")
#     .Define("Candidate_jets_phi", "Jet_phi[VBF_jet_preselection]")
# )

# df_full = (
#     df_full
#     .Define("Muon_preselection", "Muon_pt >5")
#     .Define("Candidate_muon_pt", "Muon_pt[Muon_preselection]")
#     .Define("Candidate_muon_eta", "Muon_eta[Muon_preselection]")
#     .Define("Candidate_muon_phi", "Muon_phi[Muon_preselection]")
# )
# df_full = (
#     df_full
#     .Define("Electron_preselection", "Electron_pt >7")
#     .Define("Candidate_el_pt", "Electron_pt[Electron_preselection]")
#     .Define("Candidate_el_eta", "Electron_eta[Electron_preselection]")
#     .Define("Candidate_el_phi", "Electron_phi[Electron_preselection]")
# )

# df_full = (
#     df_full
#     .Define(
#         "Good_VBF_candidates",
#         "part_isolation(Candidate_jets_eta, Candidate_jets_phi, Candidate_muon_eta, Candidate_muon_phi, Candidate_el_eta, Candidate_el_phi)",
#     )
#     .Define("Good_VBF_jets_eta", "Candidate_jets_eta[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_mass", "Candidate_jets_mass[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_pt", "Candidate_jets_pt[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_phi", "Candidate_jets_phi[Good_VBF_candidates]")
# )
# df_full = (
#     df_full
#     .Define("sorted_VBF_jets_pt", "Reverse(Argsort(Good_VBF_jets_pt))")
#     .Define("VBF_Jet1_index", "sorted_VBF_jets_pt[0]")
#     .Define("VBF_Jet2_index", "sorted_VBF_jets_pt[1]")
# )
# df_full = (
#     df_full
#     .Define("VBF_Jet1_eta", "Good_VBF_jets_eta[VBF_Jet1_index]")
#     .Define("VBF_Jet2_eta", "Good_VBF_jets_eta[VBF_Jet2_index]")
#     .Define("VBF_Jet1_mass", "Good_VBF_jets_mass[VBF_Jet1_index]")
#     .Define("VBF_Jet2_mass", "Good_VBF_jets_mass[VBF_Jet2_index]")
#     .Define("VBF_Jet1_pt", "Good_VBF_jets_pt[VBF_Jet1_index]")
#     .Define("VBF_Jet2_pt", "Good_VBF_jets_pt[VBF_Jet2_index]")
#     .Define("VBF_Jet1_phi", "Good_VBF_jets_phi[VBF_Jet1_index]")
#     .Define("VBF_Jet2_phi", "Good_VBF_jets_phi[VBF_Jet2_index]")
# )

# df_full = (
#     df_full
#     .Define(
#         "Delta_eta",
#         "VBF_Jet1_eta - VBF_Jet2_eta",
#     )
#     .Define(
#         "Jet_invariant_mass",
#         "invariant_mass(VBF_Jet1_pt, VBF_Jet1_eta, VBF_Jet1_phi, VBF_Jet1_mass, VBF_Jet2_pt, VBF_Jet2_eta, VBF_Jet2_phi, VBF_Jet2_mass)",
#     )
# )


# df_full = (
#     df_full
#     .Define(
#         "VBF_events", "nJet >=2 && abs(Delta_eta) >4.0 && Jet_invariant_mass > 500"
#     )
#     .Filter("!VBF_events")
# )


#! PHASE 2


#! N.B. QUANDO VAI A SELEZIONAR GLI EVENTI DI FASE2, VANNO CAMBIATI I NOMI ALLE VARIABILI  

df_phase2 = df_phase2.Define("Post_calibration_pt", "calibrate_pt(Mfatjet_eta, Mfatjet_pt)")

df_phase2 = (
    df_phase2
    .Define("Pt_ratio_pre", "Mfatjet_pt/MgenjetAK8_pt")
    .Define("Pt_ratio_post", "Post_calibration_pt/MgenjetAK8_pt")
)


# df_phase2 = (
#     df_phase2# && FatJet_pt[0] >300 && FatJet_pt[1] >300")
#     .Define("FatJet_Selection", "FatJet_pt > 300")
#     .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
#     .Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[FatJet_Selection]")
#     .Define("Pt_sel_jets", "FatJet_pt[FatJet_Selection]")
#     .Define("Post_calib_sel_jets", "Post_calibration_pt[FatJet_Selection]")
# )

# df_phase2 = (
#     df_phase2.Define(
#         "sorted_FatJet_deepTagMD_HbbvsQCD",
#         "Reverse(Argsort(new_discriminator))",
#     )
#     .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
#     .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
#     .Define("Jet1_discriminator", "new_discriminator[Jet1_index]")
#     .Define("Jet2_discriminator", "new_discriminator[Jet2_index]")
#     )

# df_phase2 = df_phase2.Filter(
#     "new_discriminator[Jet1_index]> 0.86" 
# )


# df_phase2 = (
#     df_phase2
#     .Define(
#         # mu = 13, e = 11
#         "FatJet_Selection",
#         "FatJet_pt > 300 && abs(FatJet_eta) < 2.4 && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Electron_pt, Electron_eta, Electron_phi, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Muon_pt, Muon_eta, Muon_phi, Muon_pfRelIso03_all, 13)",
#     )
#     .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
#     # .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
#     # .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
#     # .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
#     # .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
#     .Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[FatJet_Selection]")
#     .Define("Eta_sel_jets", "FatJet_eta[FatJet_Selection]")
#     .Define("Phi_sel_jets", "FatJet_phi[FatJet_Selection]")
#     .Define("Pt_sel_jets", "FatJet_pt[FatJet_Selection]")
# )
# df_phase2 = df_phase2.Filter("new_discriminator.size()>=2")

# df_phase2 = (
#     df_phase2
#     .Define(
#         "sorted_FatJet_deepTagMD_HbbvsQCD",
#         "Reverse(Argsort(new_discriminator))",
#     )
#     .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
#     .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
# )
# df_phase2 = df_phase2.Filter(
#     "Softdrop_sel_jets[Jet1_index]> 50 && Softdrop_sel_jets[Jet2_index]> 50"
# )
# df_phase2 = (
#     df_phase2
#     .Define("Jet1_Selected_jet_softdrop", "Softdrop_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jet_softdrop", "Softdrop_sel_jets[Jet2_index]")
#     .Define(
#         "Jet1_Selected_jets_discriminator", "new_discriminator[Jet1_index]"
#     )
#     .Define(
#         "Jet2_Selected_jets_discriminator", "new_discriminator[Jet2_index]"
#     )
#     .Define("Jet1_Selected_jets_eta", "Eta_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_eta", "Eta_sel_jets[Jet2_index]")
#     .Define("Jet1_Selected_jets_phi", "Phi_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_phi", "Phi_sel_jets[Jet2_index]")
#     .Define(
#         "Sum_selected_jets",
#         "Jet1_Selected_jet_softdrop + Jet2_Selected_jet_softdrop",
#     )
#     .Define("Jet1_Selected_jets_pt", "Pt_sel_jets[Jet1_index]")
#     .Define("Jet2_Selected_jets_pt", "Pt_sel_jets[Jet2_index]")

# )

# df_phase2 = df_phase2.Filter("new_discriminator[Jet1_index]>0.86").Filter("MET_pt <100")


# #! VETO ON VBF

# df_phase2 = (
#     df_phase2
#     .Define(
#         "VBF_jet_preselection",
#         "jet_isolation(Jet_eta, Jet_phi, Eta_sel_jets, Phi_sel_jets) && Jet_pt >25 && abs(Jet_eta) <4.7",
#     )
#     .Define("Candidate_jets_pt", "Jet_pt[VBF_jet_preselection]")
#     .Define("Candidate_jets_mass", "Jet_mass[VBF_jet_preselection]")
#     .Define("Candidate_jets_eta", "Jet_eta[VBF_jet_preselection]")
#     .Define("Candidate_jets_phi", "Jet_phi[VBF_jet_preselection]")
# )

# df_phase2 = (
#     df_phase2
#     .Define("Muon_preselection", "Muon_pt >5")
#     .Define("Candidate_muon_pt", "Muon_pt[Muon_preselection]")
#     .Define("Candidate_muon_eta", "Muon_eta[Muon_preselection]")
#     .Define("Candidate_muon_phi", "Muon_phi[Muon_preselection]")
# )
# df_phase2 = (
#     df_phase2
#     .Define("Electron_preselection", "Electron_pt >7")
#     .Define("Candidate_el_pt", "Electron_pt[Electron_preselection]")
#     .Define("Candidate_el_eta", "Electron_eta[Electron_preselection]")
#     .Define("Candidate_el_phi", "Electron_phi[Electron_preselection]")
# )

# df_phase2 = (
#     df_phase2
#     .Define(
#         "Good_VBF_candidates",
#         "part_isolation(Candidate_jets_eta, Candidate_jets_phi, Candidate_muon_eta, Candidate_muon_phi, Candidate_el_eta, Candidate_el_phi)",
#     )
#     .Define("Good_VBF_jets_eta", "Candidate_jets_eta[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_mass", "Candidate_jets_mass[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_pt", "Candidate_jets_pt[Good_VBF_candidates]")
#     .Define("Good_VBF_jets_phi", "Candidate_jets_phi[Good_VBF_candidates]")
# )
# df_phase2 = (
#     df_phase2
#     .Define("sorted_VBF_jets_pt", "Reverse(Argsort(Good_VBF_jets_pt))")
#     .Define("VBF_Jet1_index", "sorted_VBF_jets_pt[0]")
#     .Define("VBF_Jet2_index", "sorted_VBF_jets_pt[1]")
# )
# df_phase2 = (
#     df_phase2
#     .Define("VBF_Jet1_eta", "Good_VBF_jets_eta[VBF_Jet1_index]")
#     .Define("VBF_Jet2_eta", "Good_VBF_jets_eta[VBF_Jet2_index]")
#     .Define("VBF_Jet1_mass", "Good_VBF_jets_mass[VBF_Jet1_index]")
#     .Define("VBF_Jet2_mass", "Good_VBF_jets_mass[VBF_Jet2_index]")
#     .Define("VBF_Jet1_pt", "Good_VBF_jets_pt[VBF_Jet1_index]")
#     .Define("VBF_Jet2_pt", "Good_VBF_jets_pt[VBF_Jet2_index]")
#     .Define("VBF_Jet1_phi", "Good_VBF_jets_phi[VBF_Jet1_index]")
#     .Define("VBF_Jet2_phi", "Good_VBF_jets_phi[VBF_Jet2_index]")
# )

# df_phase2 = (
#     df_phase2
#     .Define(
#         "Delta_eta",
#         "VBF_Jet1_eta - VBF_Jet2_eta",
#     )
#     .Define(
#         "Jet_invariant_mass",
#         "invariant_mass(VBF_Jet1_pt, VBF_Jet1_eta, VBF_Jet1_phi, VBF_Jet1_mass, VBF_Jet2_pt, VBF_Jet2_eta, VBF_Jet2_phi, VBF_Jet2_mass)",
#     )
# )

# df_phase2 = (
#     df_phase2
#     .Define(
#         "VBF_events", "nJet >=2 && abs(Delta_eta) >4.0 && Jet_invariant_mass > 500"
#     )
#     .Filter("!VBF_events")
# )


#! ENDING OF SELECTION


full_post = df_full.Count().GetValue()

flash_post = df_flash.Count().GetValue()

phase2_post = df_phase2.Count().GetValue()

print(
    "fullsim events pre and post selection: pre {}, post {}, fraction {}".format(
        full_pre, full_post, full_post / full_pre
    )
)

print(
    "flashsim events pre and post selection: pre {}, post {}, fraction {}".format(
        flash_pre, flash_post, flash_post / flash_pre
    )
)

print(
    "phase2 events pre and post selection: pre {}, post {}, fraction {}".format(
        phase2_pre, phase2_post, phase2_post / phase2_pre
    )
)

#! PT

hist_full_pt = df_full.Histo1D(
    ("full", "fullsim sample; Pt; Events", 25, 240, 1000), "Matched_FatJet_pt"
)
h_full_pt = hist_full_pt.GetValue()

hist_flash_pt_pre = df_flash.Histo1D(
    ("flash", "flashsim sample; Pt; Events", 25, 240, 1000), "FatJet_pt"
)
h_flash_pt_pre = hist_flash_pt_pre.GetValue()

hist_flash_pt_post = df_flash.Histo1D(
    ("flash", "flashsim sample; Pt; Events", 25, 240, 1000), "Post_calibration_pt"
)
h_flash_pt_post = hist_flash_pt_post.GetValue()


hist_phase2_pt_pre = df_phase2.Histo1D(
    ("phase2", "Phase 2 sample; Pt; Events", 25, 240, 1000), "Mfatjet_pt"
)
h_phase2_pt_pre = hist_phase2_pt_pre.GetValue()

hist_phase2_pt_post = df_phase2.Histo1D(
    ("phase2", "Phase 2 sample; Pt; Events", 25, 240, 1000), "Post_calibration_pt"
)
h_phase2_pt_post = hist_phase2_pt_post.GetValue()


#! PT RATIO


hist_pt_ratio_full = df_full.Histo1D(
    ("pt_ratio_full", "pt Ratio for Fullsim; reco/gen; Events", 50, 0, 2), "Pt_ratio"
)

h_full_pt_ratio = hist_pt_ratio_full.GetValue()




hist_pt_ratio_flash_pre = df_flash.Histo1D(
    ("pt_ratio_flash_pre", "pt Ratio for Flashsim pre calibration; reco/gen; Events", 50, 0, 2), "Pt_ratio_pre"
)

h_flash_pt_ratio_pre = hist_pt_ratio_flash_pre.GetValue()


hist_pt_ratio_flash_post = df_flash.Histo1D(
    ("pt_ratio_flash_post", "pt Ratio for Flashsim poat calibration; reco/gen; Events", 50, 0, 2), "Pt_ratio_post"
)

h_flash_pt_ratio_post = hist_pt_ratio_flash_post.GetValue()




hist_pt_ratio_phase2_pre = df_phase2.Histo1D(
    ("pt_ratio_phase2_pre", "pt Ratio for Phase 2 pre calibration; reco/gen; Events", 50, 0, 2), "Pt_ratio_pre"
)

h_pt_ratio_phase2_pre = hist_pt_ratio_phase2_pre.GetValue()


hist_pt_ratio_phase2_post = df_phase2.Histo1D(
    ("pt_ratio_phase2_post", "pt Ratio for Phase 2 poat calibration; reco/gen; Events", 50, 0, 2), "Pt_ratio_post"
)

h_pt_ratio_phase2_post  = hist_pt_ratio_phase2_post.GetValue()



#! CANVASES

c1 = ROOT.TCanvas("c1", "Confrontation betweeen full and flash", 800, 700)

legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_flash_pt_pre.Draw("HIST")
h_flash_pt_pre.SetTitle("Pt distribution  for signal")
h_flash_pt_pre.SetLineColor(ROOT.kBlue + 1)
legend.AddEntry(h_flash_pt_pre, "flashsim", "l")
h_flash_pt_pre.SetLineWidth(2)
h_flash_pt_pre.Scale(1 / h_flash_pt_pre.Integral())

h_flash_pt_post.Draw("HIST SAME")
h_flash_pt_post.SetTitle("Pt distribution")
h_flash_pt_post.SetLineColor(ROOT.kBlack )
legend.AddEntry(h_flash_pt_post, "flashsim post calibration", "l")
h_flash_pt_post.Scale(1 / h_flash_pt_post.Integral())
h_flash_pt_post.SetLineWidth(2)


h_full_pt.Draw("SAME HIST")
h_full_pt.SetLineColor(ROOT.kRed + 1)
legend.AddEntry(h_full_pt, "fullsim", "l")
h_full_pt.Scale(1 / h_full_pt.Integral())
h_full_pt.SetLineWidth(2)


legend.Draw()




c2 = ROOT.TCanvas("c2", "Confrontation betweeen full and flash", 800, 700)

legend2 = ROOT.TLegend(0.68, 0.70, 0.88, 0.88)

h_full_pt_ratio.Draw("HIST")


h_full_pt_ratio.SetTitle("Pt ratio for signal")
h_full_pt_ratio.SetLineColor(ROOT.kBlue + 1)
legend2.AddEntry(h_full_pt_ratio, "fullsim", "l")
h_full_pt_ratio.SetLineWidth(2)
h_full_pt_ratio.SetMaximum(0.4)
h_full_pt_ratio.SetLineStyle(2)

h_full_pt_ratio.Scale(1 / h_full_pt_ratio.Integral())



h_flash_pt_ratio_pre.Draw("HIST SAME")
h_flash_pt_ratio_pre.SetTitle("Pt distribution")
h_flash_pt_ratio_pre.SetLineColor(ROOT.kBlack)
legend2.AddEntry(h_flash_pt_ratio_pre, "flashsim pre calibration", "l")
h_flash_pt_ratio_pre.SetLineWidth(2)
h_flash_pt_ratio_pre.Scale(1 / h_flash_pt_ratio_pre.Integral())


h_flash_pt_ratio_post.Draw("SAME HIST")
h_flash_pt_ratio_post.SetLineColor(ROOT.kRed + 1)
legend2.AddEntry(h_flash_pt_ratio_post, "flashsim post calibration", "l")
h_flash_pt_ratio_post.SetLineWidth(2)
h_flash_pt_ratio_post.Scale(1 / h_flash_pt_ratio_post.Integral())




h_pt_ratio_phase2_pre.Draw("HIST SAME")
h_pt_ratio_phase2_pre.SetTitle("Pt distribution")
h_pt_ratio_phase2_pre.SetLineColor(ROOT.kBlack)
legend2.AddEntry(h_pt_ratio_phase2_pre, "phase 2 pre calibration", "l")
h_pt_ratio_phase2_pre.SetLineWidth(3)
h_pt_ratio_phase2_pre.Scale(1 / h_pt_ratio_phase2_pre.Integral())
h_pt_ratio_phase2_pre.SetLineStyle(2)



h_pt_ratio_phase2_post.Draw("SAME HIST")
h_pt_ratio_phase2_post.SetLineColor(ROOT.kRed + 1)
legend2.AddEntry(h_pt_ratio_phase2_post, "phase 2 post calibration", "l")
h_pt_ratio_phase2_post.SetLineWidth(3)
h_pt_ratio_phase2_post.Scale(1 / h_pt_ratio_phase2_post.Integral())
h_pt_ratio_phase2_post.SetLineStyle(2)


legend2.Draw()




#! MEAN AND RMS

full_mean = float("%.3f" % h_full_pt_ratio.GetMean())

full_rms = float("%.3f" % h_full_pt_ratio.GetRMS())


flash_mean_pre = float("%.3f" % h_flash_pt_ratio_pre.GetMean())

flash_rms_pre = float("%.3f" % h_flash_pt_ratio_pre.GetRMS())


flash_mean_post = float("%.3f" % h_flash_pt_ratio_post.GetMean())

flash_rms_post = float("%.3f" % h_flash_pt_ratio_post.GetRMS())


phase2_mean_pre = float("%.3f" % h_pt_ratio_phase2_pre.GetMean())

phase2_rms_pre = float("%.3f" % h_pt_ratio_phase2_pre.GetRMS())

phase2_mean_post = float("%.3f" % h_pt_ratio_phase2_post.GetMean())

phase2_rms_post = float("%.3f" % h_pt_ratio_phase2_post.GetRMS())



text_full_mean = ROOT.TLatex(0.04, 0.19, "fullsim mean: " + str(full_mean)) #0.19
text_full_mean.SetTextSize(0.022)
text_full_mean.Draw()


text_full_rms = ROOT.TLatex(0.04, 0.18, "fullsim RMS: " + str(full_rms)) #0.17
text_full_rms.SetTextSize(0.022)
text_full_rms.Draw()


text_flash_mean_pre = ROOT.TLatex(0.04, 0.16, "flashsim mean pre calibration: " + str(flash_mean_pre)) #0.15
text_flash_mean_pre.SetTextSize(0.022)
text_flash_mean_pre.Draw()

text_flash_rms_pre = ROOT.TLatex(0.04, 0.15, "flashsim RMS pre calibration: " + str(flash_rms_pre)) #0.13
text_flash_rms_pre.SetTextSize(0.022)
text_flash_rms_pre.Draw()


text_flash_mean_post = ROOT.TLatex(0.04, 0.13, "flashsim mean post calibration: " + str(flash_mean_post)) #0.11
text_flash_mean_post.SetTextSize(0.022)
text_flash_mean_post.Draw()

text_flash_rms_post = ROOT.TLatex(0.04, 0.12, "flashsim RMS post calibration: " + str(flash_rms_post)) #0.09
text_flash_rms_post.SetTextSize(0.022)
text_flash_rms_post.Draw()


text_phase2_mean_pre = ROOT.TLatex(0.04, 0.10, "phase2 mean pre calibration: " + str(phase2_mean_pre)) #0.15
text_phase2_mean_pre.SetTextSize(0.022)
text_phase2_mean_pre.Draw()

text_phase2_rms_pre = ROOT.TLatex(0.04, 0.09, "phase2 RMS pre calibration: " + str(phase2_rms_pre)) #0.13
text_phase2_rms_pre.SetTextSize(0.022)
text_phase2_rms_pre.Draw()


text_phase2_mean_post = ROOT.TLatex(0.04, 0.07, "phase2 mean post calibration: " + str(phase2_mean_post)) #0.11
text_phase2_mean_post.SetTextSize(0.022)
text_phase2_mean_post.Draw()

text_phase2_rms_post = ROOT.TLatex(0.04, 0.06, "phase2 RMS post calibration: " + str(phase2_rms_post)) #0.09
text_phase2_rms_post.SetTextSize(0.022)
text_phase2_rms_post.Draw()

c1.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/sig_flash_vs_full_pt_calibrated.pdf"
)

c2.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/sig_flash_vs_full_pt_ratio_calibrated.pdf"
)

