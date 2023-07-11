import ROOT
import os
import numpy as np

module_path_1 = os.path.join(os.path.dirname(__file__), "utils.h")
module_path_2 = os.path.join(os.path.dirname(__file__), "fatjets_utils.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")



ROOT.gInterpreter.ProcessLine(f'#include "{module_path_1}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_2}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')



ROOT.gStyle.SetOptStat(0)

ROOT.EnableImplicitMT(10)


fullsim_path = "/scratchnvme/cicco/signal_RunIISummer20UL16/212C7FC6-48EC-574D-B7E9-617A974C308E.root"

flashsim_path = (
    "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/212C7FC6-48EC-574D-B7E9-617A974C308E.root"
)

df_full = ROOT.RDataFrame("Events", fullsim_path)

df_flash = ROOT.RDataFrame("Events", flashsim_path)

full_pre = df_full.Count().GetValue()

flash_pre = df_flash.Count().GetValue()

#! FLASHSIM

df_flash = df_flash.Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")

df_flash = (
    df_flash.Filter("nFatJet>=2")# && FatJet_pt[0] >300 && FatJet_pt[1] >300")
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

df_flash = (
    df_flash.Define(
            "GenPart_IsLastB",
            "(abs(GenPart_pdgId) >=500 && abs(GenPart_pdgId) < 600) | (abs(GenPart_pdgId) >=5000 && abs(GenPart_pdgId) < 6000) && (GenPart_statusFlags &(1<<13))!=0",
        )
        .Define("GenPart_IsLastB_m", "Take(GenPart_IsLastB, GenPart_genPartIdxMother)")
        .Define(
            "GenPart_parent_IsNotLastB",
            "(GenPart_genPartIdxMother == -1 | GenPart_IsLastB_m ==0)",
        )
        .Define("GenPart_IsGoodB", "GenPart_IsLastB && GenPart_parent_IsNotLastB")
        .Define("GenPart_eta_goodb", "GenPart_eta[GenPart_IsGoodB]")
        .Define("GenPart_phi_goodb", "GenPart_phi[GenPart_IsGoodB]")
        .Define(
            "GenJetAK8_nbFlavour",
            "count_nHadrons(GenPart_eta_goodb, GenPart_phi_goodb, GenJetAK8_eta, GenJetAK8_phi)",
        )
        
        .Define("mask_0", "GenJetAK8_nbFlavour == 0")
        .Define("discriminator_0", "FatJet_particleNetMD_XbbvsQCD[mask_0]")

        .Define("mask_1", "GenJetAK8_nbFlavour == 1")
        .Define("discriminator_1", "FatJet_particleNetMD_XbbvsQCD[mask_1]")

        .Define("mask_2", "GenJetAK8_nbFlavour == 2")
        .Define("discriminator_2", "FatJet_particleNetMD_XbbvsQCD[mask_2]")

        
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


df_full = (
    df_full.Filter("nFatJet>=2") # && FatJet_pt[0] > 300 && FatJet_pt[1] >300")
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

df_full = (
    df_full.Define(
            "GenPart_IsLastB",
            "(abs(GenPart_pdgId) >=500 && abs(GenPart_pdgId) < 600) | (abs(GenPart_pdgId) >=5000 && abs(GenPart_pdgId) < 6000) && (GenPart_statusFlags &(1<<13))!=0",
        )
        .Define("GenPart_IsLastB_m", "Take(GenPart_IsLastB, GenPart_genPartIdxMother)")
        .Define(
            "GenPart_parent_IsNotLastB",
            "(GenPart_genPartIdxMother == -1 | GenPart_IsLastB_m ==0)",
        )
        .Define("GenPart_IsGoodB", "GenPart_IsLastB && GenPart_parent_IsNotLastB")
        .Define("GenPart_eta_goodb", "GenPart_eta[GenPart_IsGoodB]")
        .Define("GenPart_phi_goodb", "GenPart_phi[GenPart_IsGoodB]")
        .Define(
            "GenJetAK8_nbFlavour",
            "count_nHadrons(GenPart_eta_goodb, GenPart_phi_goodb, GenJetAK8_eta, GenJetAK8_phi)",
        )
        .Define("matched_genjet_nb", "Take(GenJetAK8_nbFlavour, FatJet_genJetAK8Idx)")
        .Define("mask_0", "matched_genjet_nb == 0")
        .Define("discriminator_0", "new_discriminator[mask_0]")

        .Define("mask_1", "matched_genjet_nb == 1")
        .Define("discriminator_1", "new_discriminator[mask_1]")

        .Define("mask_2", "matched_genjet_nb == 2")
        .Define("discriminator_2", "new_discriminator[mask_2]")
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


full_post = df_full.Count().GetValue()

flash_post = df_flash.Count().GetValue()

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


hist_full_pt = df_full.Histo1D(
    ("full", "fullsim sample; Pt; Events", 25, 240, 1000), "Pt_sel_jets"
)
h_full_pt = hist_full_pt.GetValue()

hist_flash_pt = df_flash.Histo1D(
    ("flash", "flashsim sample; Pt; Events", 25, 240, 1000), "Pt_sel_jets"
)
h_flash_pt = hist_flash_pt.GetValue()

hist_flash_pt_post = df_flash.Histo1D(
    ("flash", "flashsim sample; Pt; Events", 25, 240, 1000), "Post_calib_sel_jets"
)
h_flash_pt_post = hist_flash_pt_post.GetValue()



hist_full_softdrop = df_full.Histo1D(
    ("full", "fullsim sample; softdrop; Events", 25, 50, 330), "Softdrop_sel_jets"
)
h_full_softdrop = hist_full_softdrop.GetValue()

hist_flash_softdrop = df_flash.Histo1D(
    ("flash", "flashsim sample; softdrop; Events", 25, 50, 330), "Softdrop_sel_jets"
)
h_flash_softdrop = hist_flash_softdrop.GetValue()


hist_full_discr = df_full.Histo1D(
    ("full", "fullsim sample; discriminator; Events", 25, 0, 1), "new_discriminator"
)
h_full_discr = hist_full_discr.GetValue()


hist_flash_discr = df_flash.Histo1D(
    ("flash", "flashsim sample; discriminator; Events", 25, 0, 1), "new_discriminator"
)
h_flash_discr = hist_flash_discr.GetValue()



hist_full_nb = df_full.Histo1D(
    ("full", "fullsim sample; Pt; Events", 10, 0, 5), "GenJetAK8_nbFlavour"
)
h_full_nb = hist_full_nb.GetValue()

hist_flash_nb = df_flash.Histo1D(
    ("flash", "flashsim sample; Pt; Events", 10, 0, 5), "GenJetAK8_nbFlavour"
)
h_flash_nb = hist_flash_nb.GetValue()




hist_full_0 = df_full.Histo1D(
    ("full", "fullsim sample; 0; Events", 10, 0, 1),"discriminator_0"
)
h_full_0 = hist_full_0.GetValue()

# hist_flash_0 = df_flash.Histo1D(
#     ("flash", "flashsim sample; 0; Events", 10, 0, 1),"discriminator_0"
# )
# h_flash_0 = hist_flash_0.GetValue()


hist_full_1 = df_full.Histo1D(
    ("full", "fullsim sample; 1; Events", 10, 0, 1),"discriminator_1"
)
h_full_1 = hist_full_1.GetValue()

# hist_flash_1 = df_flash.Histo1D(
#     ("flash", "flashsim sample; 1; Events", 10, 0, 1),"discriminator_1"
# )
# h_flash_1 = hist_flash_1.GetValue()

hist_full_2 = df_full.Histo1D(
    ("full", "fullsim sample; 2; Events", 10, 0, 1),"discriminator_2"
)
h_full_2 = hist_full_2.GetValue()

# hist_flash_2 = df_flash.Histo1D(
#     ("flash", "flashsim sample; 2; Events", 10, 0, 1),"discriminator_2"
# )
# h_flash_2 = hist_flash_2.GetValue()




c1 = ROOT.TCanvas("c1", "Confrontation betweeen full and flash", 800, 700)

legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_flash_pt.Draw("HIST")
h_flash_pt.SetTitle("Pt distribution")
h_flash_pt.SetLineColor(ROOT.kBlue + 1)
legend.AddEntry(h_flash_pt, "flashsim", "l")
h_flash_pt.SetLineWidth(2)
h_flash_pt.Scale(1 / h_flash_pt.Integral())

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

legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_flash_softdrop.Draw("HIST")
h_flash_softdrop.SetTitle("Softdrop distribution")
h_flash_softdrop.SetLineColor(ROOT.kBlue + 1)
legend2.AddEntry(h_flash_softdrop, "flashsim", "l")
h_flash_softdrop.Scale(1 / h_flash_softdrop.Integral())


h_full_softdrop.Draw("SAME HIST")
h_full_softdrop.SetLineColor(ROOT.kRed + 1)
legend2.AddEntry(h_full_softdrop, "fullsim", "l")
h_full_softdrop.Scale(1 / h_full_softdrop.Integral())

legend2.Draw()

c3 = ROOT.TCanvas("c3", "Confrontation betweeen full and flash", 800, 700)

legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_flash_discr.Draw("HIST")
h_flash_discr.SetTitle("Discriminator distribution")
h_flash_discr.SetLineColor(ROOT.kBlue + 1)
legend3.AddEntry(h_flash_discr, "flashsim", "l")
h_flash_discr.Scale(1 / h_flash_discr.Integral())


h_full_discr.Draw("SAME HIST")
h_full_discr.SetLineColor(ROOT.kRed + 1)
legend3.AddEntry(h_full_discr, "fullsim", "l")
h_full_discr.Scale(1 / h_full_discr.Integral())
c3.SetLogy()
legend3.Draw()

c4 = ROOT.TCanvas("c4", "Confrontation betweeen full and flash", 800, 700)

legend4 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_flash_nb.Draw("HIST")
h_flash_nb.SetTitle("b distribution")
h_flash_nb.SetMaximum(10000)
h_flash_nb.SetLineColor(ROOT.kBlue + 1)
legend4.AddEntry(h_flash_nb, "flashsim", "l")
h_flash_nb.Scale(1 / h_flash_nb.Integral())


h_full_nb.Draw("SAME HIST")
h_full_nb.SetLineColor(ROOT.kRed + 1)
legend4.AddEntry(h_full_nb, "fullsim", "l")
h_full_nb.Scale(1 / h_full_nb.Integral())

legend4.Draw()


c5 = ROOT.TCanvas("c5", "Confrontation betweeen full and flash", 800, 700)

legend5 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

# h_flash_0.Draw("HIST")
# h_flash_0.SetTitle("b distribution")
# h_flash_0.SetLineColor(ROOT.kBlue + 1)
# legend5.AddEntry(h_flash_0, "flashsim 0", "l")
# #h_flash_0.Scale(1 / h_flash_0.Integral())

# h_flash_1.Draw("SAME HIST")
# h_flash_1.SetLineColor(ROOT.kRed + 1)
# legend5.AddEntry(h_flash_1, "flashsim 1", "l")
# #h_flash_1.Scale(1 / h_flash_1.Integral())

# h_flash_2.Draw("SAME HIST")
# h_flash_2.SetLineColor(ROOT.kBlack)
# legend5.AddEntry(h_flash_2, "flashsim 2", "l")
# #h_flash_2.Scale(1 / h_flash_2.Integral())


h_full_0.Draw("HIST")
h_full_0.SetLineColor(ROOT.kBlue + 1)
h_full_0.SetLineStyle(9)
h_full_0.SetMaximum(0.6)
legend5.AddEntry(h_full_0, "fullsim 0", "l")
h_full_0.Scale(1 / h_full_0.Integral())

h_full_1.Draw("SAME HIST")
h_full_1.SetLineColor(ROOT.kRed + 1)
legend5.AddEntry(h_full_1, "fullsim 1 ", "l")
h_full_1.SetLineStyle(9)

h_full_1.Scale(1 / h_full_1.Integral())

h_full_2.Draw("SAME HIST")
h_full_2.SetLineColor(ROOT.kBlack )
h_full_2.SetLineStyle(9)
legend5.AddEntry(h_full_2, "fullsim 2", "l")
h_full_2.Scale(1 / h_full_2.Integral())

c5.SetLogy()


legend5.Draw()



c1.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/sig_flash_vs_full_pt_calibrated.pdf"
)

# c2.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/sig_flash_vs_full_soft.pdf"
# )

# c3.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/sig_flash_vs_full_discr.pdf"
# )


# c4.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/sig_flash_vs_full_nb.pdf"
# )

# c5.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/sig_flash_vs_full_nb_discr.pdf"
# )