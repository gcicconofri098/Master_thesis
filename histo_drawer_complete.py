import ROOT
import os

histo_file = ROOT.TFile.Open("figures_analysis_complete/histograms.root", "READ") 

selection_steps_full = ['no_cut', 'nfatjets_request', 'genjet_request', 'pt_window', 'eta_cut', 'cleaning', 'softdrop_request']
selection_steps_flash = ['no_cut', 'pt_window', 'eta_cut', 'cleaning','softdrop_request']
selection_steps_ph2 = ['no_cut', 'nfatjets_request', 'genjet_request', 'pt_window', 'eta_cut','softdrop_request']


processes = ["QCD1_full", "QCD2_full", "QCD3_full", "QCD4_full", "QCD5_full", "QCD6_full", "QCD7_full", "QCD8_full", "signal_full", "QCD6_flash", "QCD7_flash", "QCD8_flash", "signal_flash", "QCD_ph2", "signal_ph2"] 



dict_discr_hist_tot = {}
dict_discr_hist1 = {}
dict_discr_hist2 = {}

dict_softdrop_hist_tot = {}
dict_softdrop_hist1 = {}
dict_softdrop_hist2 = {}


for i in processes:
    dict_discr_hist1[i] = {}
    dict_discr_hist2[i] = {}
    dict_discr_hist_tot[i] = {}

    dict_softdrop_hist1[i] = {}
    dict_softdrop_hist2[i] = {}
    dict_softdrop_hist_tot[i] = {}


    dict_discr_hist_tot[i]['no_cut'] = histo_file.Get("discr_histo_tot_" + str(i)+ "_no_cut")
    dict_discr_hist1[i]['no_cut'] = histo_file.Get("discr_histo1_" + str(i)+ "_no_cut")
    dict_discr_hist2[i]['no_cut'] = histo_file.Get("discr_histo2_" + str(i)+ "_no_cut")

    dict_softdrop_hist_tot[i]['no_cut'] = histo_file.Get("soft_histo_tot_" + str(i)+ "_no_cut")
    dict_softdrop_hist1[i]['no_cut'] = histo_file.Get("soft_histo1_" + str(i)+ "_no_cut")
    dict_softdrop_hist2[i]['no_cut'] = histo_file.Get("soft_histo2_" + str(i)+ "_no_cut")

    if str(i) != 'QCD6_flash' and str(i) != 'QCD7_flash' and str(i) != 'QCD8_flash' and str(i)!= 'signal_flash':

        dict_discr_hist_tot[i]['nfatjets_request'] = histo_file.Get("discr_histo_tot_" + str(i)+ "_nfatjets_request")
        dict_discr_hist1[i]['nfatjets_request'] = histo_file.Get("discr_histo1_" + str(i)+ "_nfatjets_request")
        dict_discr_hist2[i]['nfatjets_request'] = histo_file.Get("discr_histo2_" + str(i)+ "_nfatjets_request")

        dict_softdrop_hist_tot[i]['nfatjets_request'] = histo_file.Get("soft_histo_tot_" + str(i)+ "_nfatjets_request")
        dict_softdrop_hist1[i]['nfatjets_request'] = histo_file.Get("soft_histo1_" + str(i)+ "_nfatjets_request")
        dict_softdrop_hist2[i]['nfatjets_request'] = histo_file.Get("soft_histo2_" + str(i)+ "_nfatjets_request")


        dict_discr_hist_tot[i]['genjet_request'] = histo_file.Get("discr_histo_tot_" + str(i)+ "_genjet_request")
        dict_discr_hist1[i]['genjet_request'] = histo_file.Get("discr_histo1_" + str(i)+ "_genjet_request")
        dict_discr_hist2[i]['genjet_request'] = histo_file.Get("discr_histo2_" + str(i)+ "_genjet_request")

        dict_softdrop_hist_tot[i]['genjet_request'] = histo_file.Get("soft_histo_tot_" + str(i)+ "_genjet_request")
        dict_softdrop_hist1[i]['genjet_request'] = histo_file.Get("soft_histo1_" + str(i)+ "_genjet_request")
        dict_softdrop_hist2[i]['genjet_request'] = histo_file.Get("soft_histo2_" + str(i)+ "_genjet_request")


    dict_discr_hist_tot[i]['pt_window'] = histo_file.Get("discr_histo_tot_" + str(i)+ "_pt_window")
    dict_discr_hist1[i]['pt_window'] = histo_file.Get("discr_histo1_" + str(i)+ "_pt_window")
    dict_discr_hist2[i]['pt_window'] = histo_file.Get("discr_histo2_" + str(i)+ "_pt_window")

    dict_softdrop_hist_tot[i]['pt_window'] = histo_file.Get("soft_histo_tot_" + str(i)+ "_pt_window")
    dict_softdrop_hist1[i]['pt_window'] = histo_file.Get("soft_histo1_" + str(i)+ "_pt_window")
    dict_softdrop_hist2[i]['pt_window'] = histo_file.Get("soft_histo2_" + str(i)+ "_pt_window")


    dict_discr_hist_tot[i]['eta_cut'] = histo_file.Get("discr_histo_tot_" + str(i)+ "_eta_cut")
    dict_discr_hist1[i]['eta_cut'] = histo_file.Get("discr_histo1_" + str(i)+ "_eta_cut")
    dict_discr_hist2[i]['eta_cut'] = histo_file.Get("discr_histo2_" + str(i)+ "_eta_cut")

    dict_softdrop_hist_tot[i]['eta_cut'] = histo_file.Get("soft_histo_tot_" + str(i)+ "_eta_cut")
    dict_softdrop_hist1[i]['eta_cut'] = histo_file.Get("soft_histo1_" + str(i)+ "_eta_cut")
    dict_softdrop_hist2[i]['eta_cut'] = histo_file.Get("soft_histo2_" + str(i)+ "_eta_cut")

    if str(i) != 'QCD_ph2' and str(i) != 'signal_ph2':

        dict_discr_hist_tot[i]['cleaning'] = histo_file.Get("discr_histo_tot_" + str(i)+ "_cleaning")
        dict_discr_hist1[i]['cleaning'] = histo_file.Get("discr_histo1_" + str(i)+ "_cleaning")
        dict_discr_hist2[i]['cleaning'] = histo_file.Get("discr_histo2_" + str(i)+ "_cleaning")

        dict_softdrop_hist_tot[i]['cleaning'] = histo_file.Get("soft_histo_tot_" + str(i)+ "_cleaning")
        dict_softdrop_hist1[i]['cleaning'] = histo_file.Get("soft_histo1_" + str(i)+ "_cleaning")
        dict_softdrop_hist2[i]['cleaning'] = histo_file.Get("soft_histo2_" + str(i)+ "_cleaning")
    
    
    dict_discr_hist_tot[i]['softdrop_request'] = histo_file.Get("discr_histo_tot_" + str(i)+ "_softdrop_request")
    dict_discr_hist1[i]['softdrop_request'] = histo_file.Get("discr_histo1_" + str(i)+ "_softdrop_request")
    dict_discr_hist2[i]['softdrop_request'] = histo_file.Get("discr_histo2_" + str(i)+ "_softdrop_request")

    dict_softdrop_hist_tot[i]['softdrop_request'] = histo_file.Get("soft_histo_tot_" + str(i)+ "_softdrop_request")
    dict_softdrop_hist1[i]['softdrop_request'] = histo_file.Get("soft_histo1_" + str(i)+ "_softdrop_request")
    dict_softdrop_hist2[i]['softdrop_request'] = histo_file.Get("soft_histo2_" + str(i)+ "_softdrop_request")


stacked_full = {}

print("stacking the histograms")

for j in selection_steps_full:
    
    stacked_full[j] = {}

    temp_full_tot = dict_discr_hist_tot['QCD1_full'][j].Clone()
    temp_full_tot.Add(dict_discr_hist_tot['QCD2_full'][j])
    temp_full_tot.Add(dict_discr_hist_tot['QCD3_full'][j])
    temp_full_tot.Add(dict_discr_hist_tot['QCD4_full'][j])
    temp_full_tot.Add(dict_discr_hist_tot['QCD5_full'][j])
    temp_full_tot.Add(dict_discr_hist_tot['QCD6_full'][j])
    temp_full_tot.Add(dict_discr_hist_tot['QCD7_full'][j])
    temp_full_tot.Add(dict_discr_hist_tot['QCD8_full'][j])

    stacked_full[j]['all_jets_discr'] = temp_full_tot


    temp_full_hist1 = dict_discr_hist1['QCD1_full'][j].Clone()
    temp_full_hist1.Add(dict_discr_hist1['QCD2_full'][j])
    temp_full_hist1.Add(dict_discr_hist1['QCD3_full'][j])
    temp_full_hist1.Add(dict_discr_hist1['QCD4_full'][j])
    temp_full_hist1.Add(dict_discr_hist1['QCD5_full'][j])
    temp_full_hist1.Add(dict_discr_hist1['QCD6_full'][j])
    temp_full_hist1.Add(dict_discr_hist1['QCD7_full'][j])
    temp_full_hist1.Add(dict_discr_hist1['QCD8_full'][j])

    stacked_full[j]['jet1_discr'] = temp_full_hist1


    temp_full_hist2 = dict_discr_hist2['QCD1_full'][j].Clone()
    temp_full_hist2.Add(dict_discr_hist2['QCD2_full'][j])
    temp_full_hist2.Add(dict_discr_hist2['QCD3_full'][j])
    temp_full_hist2.Add(dict_discr_hist2['QCD4_full'][j])
    temp_full_hist2.Add(dict_discr_hist2['QCD5_full'][j])
    temp_full_hist2.Add(dict_discr_hist2['QCD6_full'][j])
    temp_full_hist2.Add(dict_discr_hist2['QCD7_full'][j])
    temp_full_hist2.Add(dict_discr_hist2['QCD8_full'][j])

    stacked_full[j]['jet2_discr'] = temp_full_hist2




    temp_full_tot = dict_softdrop_hist_tot['QCD1_full'][j].Clone()
    temp_full_tot.Add(dict_softdrop_hist_tot['QCD2_full'][j])
    temp_full_tot.Add(dict_softdrop_hist_tot['QCD3_full'][j])
    temp_full_tot.Add(dict_softdrop_hist_tot['QCD4_full'][j])
    temp_full_tot.Add(dict_softdrop_hist_tot['QCD5_full'][j])
    temp_full_tot.Add(dict_softdrop_hist_tot['QCD6_full'][j])
    temp_full_tot.Add(dict_softdrop_hist_tot['QCD7_full'][j])
    temp_full_tot.Add(dict_softdrop_hist_tot['QCD8_full'][j])

    stacked_full[j]['all_jets_softdrop'] = temp_full_tot


    temp_full_hist1 = dict_softdrop_hist1['QCD1_full'][j].Clone()
    temp_full_hist1.Add(dict_softdrop_hist1['QCD2_full'][j])
    temp_full_hist1.Add(dict_softdrop_hist1['QCD3_full'][j])
    temp_full_hist1.Add(dict_softdrop_hist1['QCD4_full'][j])
    temp_full_hist1.Add(dict_softdrop_hist1['QCD5_full'][j])
    temp_full_hist1.Add(dict_softdrop_hist1['QCD6_full'][j])
    temp_full_hist1.Add(dict_softdrop_hist1['QCD7_full'][j])
    temp_full_hist1.Add(dict_softdrop_hist1['QCD8_full'][j])

    stacked_full[j]['jet1_softdrop'] = temp_full_hist1


    temp_full_hist2 = dict_softdrop_hist2['QCD1_full'][j].Clone()
    temp_full_hist2.Add(dict_softdrop_hist2['QCD2_full'][j])
    temp_full_hist2.Add(dict_softdrop_hist2['QCD3_full'][j])
    temp_full_hist2.Add(dict_softdrop_hist2['QCD4_full'][j])
    temp_full_hist2.Add(dict_softdrop_hist2['QCD5_full'][j])
    temp_full_hist2.Add(dict_softdrop_hist2['QCD6_full'][j])
    temp_full_hist2.Add(dict_softdrop_hist2['QCD7_full'][j])
    temp_full_hist2.Add(dict_softdrop_hist2['QCD8_full'][j])

    stacked_full[j]['jet2_softdrop'] = temp_full_hist2




stacked_flash = {}

for j in selection_steps_flash:


    stacked_flash[j] = {}

    temp_flash_tot = dict_discr_hist_tot['QCD6_flash'][j].Clone()
    temp_flash_tot.Add(dict_discr_hist_tot['QCD7_flash'][j])
    temp_flash_tot.Add(dict_discr_hist_tot['QCD8_flash'][j])

    stacked_flash[j]['all_jets_discr'] = temp_flash_tot


    temp_flash_hist1 = dict_discr_hist1['QCD6_flash'][j].Clone()
    temp_flash_hist1.Add(dict_discr_hist1['QCD7_flash'][j])
    temp_flash_hist1.Add(dict_discr_hist1['QCD8_flash'][j])

    stacked_flash[j]['jet1_discr'] = temp_flash_hist1


    temp_flash_hist2 = dict_discr_hist2['QCD6_flash'][j].Clone()
    temp_flash_hist2.Add(dict_discr_hist2['QCD7_flash'][j])
    temp_flash_hist2.Add(dict_discr_hist2['QCD8_flash'][j])

    stacked_flash[j]['jet2_discr'] = temp_flash_hist2


    temp_flash_tot = dict_softdrop_hist_tot['QCD6_flash'][j].Clone()
    temp_flash_tot.Add(dict_softdrop_hist_tot['QCD7_flash'][j])
    temp_flash_tot.Add(dict_softdrop_hist_tot['QCD8_flash'][j])

    stacked_flash[j]['all_jets_softdrop'] = temp_flash_tot


    temp_flash_hist1 = dict_softdrop_hist1['QCD6_flash'][j].Clone()
    temp_flash_hist1.Add(dict_softdrop_hist1['QCD7_flash'][j])
    temp_flash_hist1.Add(dict_softdrop_hist1['QCD8_flash'][j])

    stacked_flash[j]['jet1_softdrop'] = temp_flash_hist1


    temp_flash_hist2 = dict_softdrop_hist2['QCD6_flash'][j].Clone()
    temp_flash_hist2.Add(dict_softdrop_hist2['QCD7_flash'][j])
    temp_flash_hist2.Add(dict_softdrop_hist2['QCD8_flash'][j])

    stacked_flash[j]['jet2_softdrop'] = temp_flash_hist2





#! FULLSIM DISCRIMINATOR, ALL JETS

c1 = ROOT.TCanvas("c1", "Discriminator histograms for fullsim, all jets", 1500, 1000)


c1.Divide(4,2)

c1.cd(1)
ROOT.gPad.SetLogy()
stacked_full['no_cut']['all_jets_discr'].Draw("HIST")
stacked_full['no_cut']['all_jets_discr'].SetTitle("No Cut; Discriminator, all jets; Events")
#stacked_full["no_cut"]['all_jets_discr'].SetLineWidth(2)
stacked_full['no_cut']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_full["no_cut"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["no_cut"]['all_jets_discr'].Scale(1 / stacked_full["no_cut"]['all_jets_discr'].Integral())

dict_discr_hist_tot['signal_full']['no_cut'].Draw("SAME HIST")
dict_discr_hist_tot['signal_full']['no_cut'].SetLineWidth(2)
dict_discr_hist_tot['signal_full']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_full']['no_cut'].Scale(1 / dict_discr_hist_tot['signal_full']['no_cut'].Integral())

legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)
legend.SetHeader("Fullsim", "C")
legend.AddEntry(stacked_full["no_cut"]['all_jets_discr'], "QCD", "f")
legend.AddEntry(dict_discr_hist_tot['signal_full']['no_cut'], "signal", "l")
legend.Draw()


c1.cd(2)
ROOT.gPad.SetLogy()

stacked_full['nfatjets_request']['all_jets_discr'].Draw("HIST")
stacked_full['nfatjets_request']['all_jets_discr'].SetTitle("request on nFatJet; Discriminator, all jets; Events")
#stacked_full["nfatjets_request"]['all_jets_discr'].SetLineWidth(2)
stacked_full['nfatjets_request']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_full['nfatjets_request']['all_jets_discr'].Scale(1 / stacked_full['nfatjets_request']['all_jets_discr'].Integral())
stacked_full["nfatjets_request"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)

dict_discr_hist_tot['signal_full']['nfatjets_request'].Draw("SAME HIST")
dict_discr_hist_tot['signal_full']['nfatjets_request'].SetLineWidth(2)
dict_discr_hist_tot['signal_full']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_full']['nfatjets_request'].Scale(1 / dict_discr_hist_tot['signal_full']['nfatjets_request'].Integral())
legend.Draw()


c1.cd(3)
ROOT.gPad.SetLogy()

stacked_full['genjet_request']['all_jets_discr'].Draw("HIST")
stacked_full['genjet_request']['all_jets_discr'].SetTitle("request on GenJetAK8_pt; Discriminator all jets; Events")
#stacked_full["genjet_request"]['all_jets_discr'].SetLineWidth(2)
stacked_full['genjet_request']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_full["genjet_request"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["genjet_request"]['all_jets_discr'].Scale(1 / stacked_full["genjet_request"]['all_jets_discr'].Integral())


dict_discr_hist_tot['signal_full']['genjet_request'].Draw("SAME HIST")
dict_discr_hist_tot['signal_full']['genjet_request'].SetLineWidth(2)
dict_discr_hist_tot['signal_full']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_full']['genjet_request'].Scale(1 / dict_discr_hist_tot['signal_full']['genjet_request'].Integral())
legend.Draw()

c1.cd(4)
ROOT.gPad.SetLogy()

stacked_full['pt_window']['all_jets_discr'].Draw("HIST")
stacked_full['pt_window']['all_jets_discr'].SetTitle("Pt window; Discriminator all jets; Events")
#stacked_full["pt_window"]['all_jets_discr'].SetLineWidth(2)
stacked_full['pt_window']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_full["pt_window"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["pt_window"]['all_jets_discr'].Scale(1 / stacked_full["pt_window"]['all_jets_discr'].Integral())


dict_discr_hist_tot['signal_full']['pt_window'].Draw("SAME HIST")
dict_discr_hist_tot['signal_full']['pt_window'].SetLineWidth(2)
dict_discr_hist_tot['signal_full']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_full']['pt_window'].Scale(1 / dict_discr_hist_tot['signal_full']['pt_window'].Integral())
legend.Draw()

c1.cd(5)
ROOT.gPad.SetLogy()

stacked_full['eta_cut']['all_jets_discr'].Draw("HIST")
stacked_full['eta_cut']['all_jets_discr'].SetTitle("Eta cut; Discriminator all jets; Events")
#stacked_full["eta_cut"]['all_jets_discr'].SetLineWidth(2)
stacked_full['eta_cut']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_full["eta_cut"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["eta_cut"]['all_jets_discr'].Scale(1 / stacked_full["eta_cut"]['all_jets_discr'].Integral())


dict_discr_hist_tot['signal_full']['eta_cut'].Draw("SAME HIST")
dict_discr_hist_tot['signal_full']['eta_cut'].SetLineWidth(2)
dict_discr_hist_tot['signal_full']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_full']['eta_cut'].Scale(1 / dict_discr_hist_tot['signal_full']['eta_cut'].Integral())
legend.Draw()

c1.cd(6)
ROOT.gPad.SetLogy()

stacked_full['cleaning']['all_jets_discr'].Draw("HIST")
stacked_full['cleaning']['all_jets_discr'].SetTitle("Cleaning; Discriminator all jets; Events")
#stacked_full["cleaning"]['all_jets_discr'].SetLineWidth(2)
stacked_full['cleaning']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_full["cleaning"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["cleaning"]['all_jets_discr'].Scale(1 / stacked_full["cleaning"]['all_jets_discr'].Integral())


dict_discr_hist_tot['signal_full']['cleaning'].Draw("SAME HIST")
dict_discr_hist_tot['signal_full']['cleaning'].SetLineWidth(2)
dict_discr_hist_tot['signal_full']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_full']['cleaning'].Scale(1 / dict_discr_hist_tot['signal_full']['cleaning'].Integral())
legend.Draw()


#! FULLSIM DISCRIMINATOR, JET 1

c2 = ROOT.TCanvas("c2", "Discriminator histograms for fullsim discriminator, jet 1", 1500, 1000)

c2.Divide(4,2)
c2.cd(1)
ROOT.gPad.SetLogy()

stacked_full['no_cut']['jet1_discr'].Draw("HIST")
stacked_full['no_cut']['jet1_discr'].SetTitle("No Cut; Discriminator Jet1; Events ")
#stacked_full["no_cut"]['jet1_discr'].SetLineWidth(2)
stacked_full['no_cut']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_full['no_cut']['jet1_discr'].Scale(1 / stacked_full['no_cut']['jet1_discr'].Integral())
stacked_full["no_cut"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)

dict_discr_hist1['signal_full']['no_cut'].Draw("SAME HIST")
dict_discr_hist1['signal_full']['no_cut'].SetLineWidth(2)
dict_discr_hist1['signal_full']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_full']['no_cut'].Scale(1 / dict_discr_hist1['signal_full']['no_cut'].Integral())

legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)
legend2.SetHeader("Fullsim", "C")
legend2.AddEntry(stacked_full["no_cut"]['jet1_discr'], "QCD", "f")
legend2.AddEntry(dict_discr_hist1['signal_full']['no_cut'], "signal", "l")
legend2.Draw()


c2.cd(2)
ROOT.gPad.SetLogy()

stacked_full['nfatjets_request']['jet1_discr'].Draw("HIST")
stacked_full['nfatjets_request']['jet1_discr'].SetTitle("request on nFatJet; Discriminator Jet1; Events")
#stacked_full["nfatjets_request"]['jet1_discr'].SetLineWidth(2)
stacked_full['nfatjets_request']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_full["nfatjets_request"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["nfatjets_request"]['jet1_discr'].Scale(1 / stacked_full["nfatjets_request"]['jet1_discr'].Integral())


dict_discr_hist1['signal_full']['nfatjets_request'].Draw("SAME HIST")
dict_discr_hist1['signal_full']['nfatjets_request'].SetLineWidth(2)
dict_discr_hist1['signal_full']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_full']['nfatjets_request'].Scale(1 / dict_discr_hist1['signal_full']['nfatjets_request'].Integral())
legend2.Draw()
c2.cd(3)
ROOT.gPad.SetLogy()

stacked_full['genjet_request']['jet1_discr'].Draw("HIST")
stacked_full['genjet_request']['jet1_discr'].SetTitle("request on GenJetAK8_pt; Discriminator Jet1; Events")
#stacked_full["genjet_request"]['jet1_discr'].SetLineWidth(2)
stacked_full['genjet_request']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_full["genjet_request"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["genjet_request"]['jet1_discr'].Scale(1 / stacked_full["genjet_request"]['jet1_discr'].Integral())

dict_discr_hist1['signal_full']['genjet_request'].Draw("SAME HIST")
dict_discr_hist1['signal_full']['genjet_request'].SetLineWidth(2)
dict_discr_hist1['signal_full']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_full']['genjet_request'].Scale(1 / dict_discr_hist1['signal_full']['genjet_request'].Integral())
legend2.Draw()
c2.cd(4)
ROOT.gPad.SetLogy()

stacked_full['pt_window']['jet1_discr'].Draw("HIST")
stacked_full['pt_window']['jet1_discr'].SetTitle("Pt window; Discriminator Jet1; Events")
#stacked_full["pt_window"]['jet1_discr'].SetLineWidth(2)
stacked_full['pt_window']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_full["pt_window"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["pt_window"]['jet1_discr'].Scale(1 / stacked_full["pt_window"]['jet1_discr'].Integral())

dict_discr_hist1['signal_full']['pt_window'].Draw("SAME HIST")
dict_discr_hist1['signal_full']['pt_window'].SetLineWidth(2)
dict_discr_hist1['signal_full']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_full']['pt_window'].Scale(1 / dict_discr_hist1['signal_full']['pt_window'].Integral())
legend2.Draw()
c2.cd(5)
ROOT.gPad.SetLogy()

stacked_full['eta_cut']['jet1_discr'].Draw("HIST")
stacked_full['eta_cut']['jet1_discr'].SetTitle("Eta cut; Discriminator Jet1; Events")
#stacked_full["eta_cut"]['jet1_discr'].SetLineWidth(2)
stacked_full['eta_cut']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_full["eta_cut"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["eta_cut"]['jet1_discr'].Scale(1 / stacked_full["eta_cut"]['jet1_discr'].Integral())

dict_discr_hist1['signal_full']['eta_cut'].Draw("SAME HIST")
dict_discr_hist1['signal_full']['eta_cut'].SetLineWidth(2)
dict_discr_hist1['signal_full']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_full']['eta_cut'].Scale(1 / dict_discr_hist1['signal_full']['eta_cut'].Integral())
legend2.Draw()

c2.cd(6)
ROOT.gPad.SetLogy()

stacked_full['cleaning']['jet1_discr'].Draw("HIST")
stacked_full['cleaning']['jet1_discr'].SetTitle("Cleaning; Discriminator Jet1; Events")
#stacked_full["cleaning"]['jet1_discr'].SetLineWidth(2)
stacked_full['cleaning']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_full["cleaning"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["cleaning"]['jet1_discr'].Scale(1 / stacked_full["cleaning"]['jet1_discr'].Integral())

dict_discr_hist1['signal_full']['cleaning'].Draw("SAME HIST")
dict_discr_hist1['signal_full']['cleaning'].SetLineWidth(2)
dict_discr_hist1['signal_full']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_full']['cleaning'].Scale(1 / dict_discr_hist1['signal_full']['cleaning'].Integral())
legend2.Draw()


#! FULLSIM DISCRIMINATOR, JET 2

c3 = ROOT.TCanvas("c3", "Discriminator histograms for fullsim discriminator, jet 2", 1500, 1000)

c3.Divide(4,2)
c3.cd(1)
ROOT.gPad.SetLogy()

stacked_full['no_cut']['jet2_discr'].Draw("HIST")
stacked_full['no_cut']['jet2_discr'].SetTitle("No Cut; Discriminator Jet2; Events")
#stacked_full["no_cut"]['jet2_discr'].SetLineWidth(2)
stacked_full['no_cut']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_full["no_cut"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["no_cut"]['jet2_discr'].Scale(1 / stacked_full["no_cut"]['jet2_discr'].Integral())


dict_discr_hist2['signal_full']['no_cut'].Draw("SAME HIST")
dict_discr_hist2['signal_full']['no_cut'].SetLineWidth(2)
dict_discr_hist2['signal_full']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_full']['no_cut'].Scale(1 / dict_discr_hist2['signal_full']['no_cut'].Integral())

legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)
legend3.SetHeader("Fullsim", "C")
legend3.AddEntry(stacked_full["no_cut"]['jet2_discr'], "QCD", "f")
legend3.AddEntry(dict_discr_hist2['signal_full']['no_cut'], "signal", "l")
legend3.Draw()



c3.cd(2)
ROOT.gPad.SetLogy()

stacked_full['nfatjets_request']['jet2_discr'].Draw("HIST")
stacked_full['nfatjets_request']['jet2_discr'].SetTitle("request on nFatJet; Discriminator Jet2; Events")
#stacked_full["nfatjets_request"]['jet2_discr'].SetLineWidth(2)
stacked_full['nfatjets_request']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_full["nfatjets_request"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["nfatjets_request"]['jet2_discr'].Scale(1 / stacked_full["nfatjets_request"]['jet2_discr'].Integral())


dict_discr_hist2['signal_full']['nfatjets_request'].Draw("SAME HIST")
dict_discr_hist2['signal_full']['nfatjets_request'].SetLineWidth(2)
dict_discr_hist2['signal_full']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_full']['nfatjets_request'].Scale(1 / dict_discr_hist2['signal_full']['nfatjets_request'].Integral())

legend3.Draw()

c3.cd(3)
ROOT.gPad.SetLogy()

stacked_full['genjet_request']['jet2_discr'].Draw("HIST")
stacked_full['genjet_request']['jet2_discr'].SetTitle("request on GenJetAK8_pt; Discriminator Jet2; Events")
#stacked_full["genjet_request"]['jet2_discr'].SetLineWidth(2)
stacked_full['genjet_request']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_full["genjet_request"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["genjet_request"]['jet2_discr'].Scale(1 / stacked_full["genjet_request"]['jet2_discr'].Integral())


dict_discr_hist2['signal_full']['genjet_request'].Draw("SAME HIST")
dict_discr_hist2['signal_full']['genjet_request'].SetLineWidth(2)
dict_discr_hist2['signal_full']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_full']['genjet_request'].Scale(1 / dict_discr_hist2['signal_full']['genjet_request'].Integral())
legend3.Draw()

c3.cd(4)
ROOT.gPad.SetLogy()

stacked_full['pt_window']['jet2_discr'].Draw("HIST")
stacked_full['pt_window']['jet2_discr'].SetTitle("Pt window; Discriminator Jet2; Events")
#stacked_full["pt_window"]['jet2_discr'].SetLineWidth(2)
stacked_full['pt_window']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_full["pt_window"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["pt_window"]['jet2_discr'].Scale(1 / stacked_full["pt_window"]['jet2_discr'].Integral())


dict_discr_hist2['signal_full']['pt_window'].Draw("SAME HIST")
dict_discr_hist2['signal_full']['pt_window'].SetLineWidth(2)
dict_discr_hist2['signal_full']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_full']['pt_window'].Scale(1 / dict_discr_hist2['signal_full']['pt_window'].Integral())
legend3.Draw()

c3.cd(5)
ROOT.gPad.SetLogy()

stacked_full['eta_cut']['jet2_discr'].Draw("HIST")
stacked_full['eta_cut']['jet2_discr'].SetTitle("Eta cut; Discriminator Jet2; Events")
#stacked_full["eta_cut"]['jet2_discr'].SetLineWidth(2)
stacked_full['eta_cut']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_full["eta_cut"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["eta_cut"]['jet2_discr'].Scale(1 / stacked_full["eta_cut"]['jet2_discr'].Integral())


dict_discr_hist2['signal_full']['eta_cut'].Draw("SAME HIST")
dict_discr_hist2['signal_full']['eta_cut'].SetLineWidth(2)
dict_discr_hist2['signal_full']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_full']['eta_cut'].Scale(1 / dict_discr_hist2['signal_full']['eta_cut'].Integral())
legend3.Draw()

c3.cd(6)
ROOT.gPad.SetLogy()

stacked_full['cleaning']['jet2_discr'].Draw("HIST")
stacked_full['cleaning']['jet2_discr'].SetTitle("Cleaning; Discriminator Jet2; Events")
#stacked_full["cleaning"]['jet2_discr'].SetLineWidth(2)
stacked_full['cleaning']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_full["cleaning"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["cleaning"]['jet2_discr'].Scale(1 / stacked_full["cleaning"]['jet2_discr'].Integral())


dict_discr_hist2['signal_full']['cleaning'].Draw("SAME HIST")
dict_discr_hist2['signal_full']['cleaning'].SetLineWidth(2)
dict_discr_hist2['signal_full']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_full']['cleaning'].Scale(1 / dict_discr_hist2['signal_full']['cleaning'].Integral())
legend3.Draw()



#! FULLSIM SOFTDROP, ALL JETS

c4 = ROOT.TCanvas("c4", "Discriminator histograms for fullsim softdrop, all jets", 1500, 1000)

c4.Divide(4,2)

c4.cd(1)

stacked_full['no_cut']['all_jets_softdrop'].Draw("HIST")
stacked_full['no_cut']['all_jets_softdrop'].SetTitle("No Cut; Softdrop mass, all jets; Events")
#stacked_full["no_cut"]['all_jets_softdrop'].SetLineWidth(2)
stacked_full['no_cut']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["no_cut"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["no_cut"]['all_jets_softdrop'].Scale(1 / stacked_full["no_cut"]['all_jets_softdrop'].Integral())


dict_softdrop_hist_tot['signal_full']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_full']['no_cut'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_full']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_full']['no_cut'].Scale(1 / dict_softdrop_hist_tot['signal_full']['no_cut'].Integral())

legend4 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)
legend4.SetHeader("Fullsim", "C")
legend4.AddEntry(stacked_full["no_cut"]['all_jets_softdrop'], "QCD", "f")
legend4.AddEntry(dict_softdrop_hist_tot['signal_full']['no_cut'], "signal", "l")
legend4.Draw()


c4.cd(2)

stacked_full['nfatjets_request']['all_jets_softdrop'].Draw("HIST")
stacked_full['nfatjets_request']['all_jets_softdrop'].SetTitle("request on nFatJet; Softdrop mass, all jets; Events ")
#stacked_full["nfatjets_request"]['all_jets_softdrop'].SetLineWidth(2)
stacked_full['nfatjets_request']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["nfatjets_request"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["nfatjets_request"]['all_jets_softdrop'].Scale(1 / stacked_full["nfatjets_request"]['all_jets_softdrop'].Integral())


dict_softdrop_hist_tot['signal_full']['nfatjets_request'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_full']['nfatjets_request'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_full']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
legend4.Draw()
dict_softdrop_hist_tot['signal_full']['nfatjets_request'].Scale(1 / dict_softdrop_hist_tot['signal_full']['nfatjets_request'].Integral())

c4.cd(3)

stacked_full['genjet_request']['all_jets_softdrop'].Draw("HIST")
stacked_full['genjet_request']['all_jets_softdrop'].SetTitle("request on GenJetAK8_pt; Softdrop mass, all jets; Events")
#stacked_full["genjet_request"]['all_jets_softdrop'].SetLineWidth(2)
stacked_full['genjet_request']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["genjet_request"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["genjet_request"]['all_jets_softdrop'].Scale(1 / stacked_full["genjet_request"]['all_jets_softdrop'].Integral())


dict_softdrop_hist_tot['signal_full']['genjet_request'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_full']['genjet_request'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_full']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_full']['genjet_request'].Scale(1 / dict_softdrop_hist_tot['signal_full']['genjet_request'].Integral())
legend4.Draw()


c4.cd(4)

stacked_full['pt_window']['all_jets_softdrop'].Draw("HIST")
stacked_full['pt_window']['all_jets_softdrop'].SetTitle("Pt window; Softdrop mass, all jets; Events")
#stacked_full["pt_window"]['all_jets_softdrop'].SetLineWidth(2)
stacked_full['pt_window']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["pt_window"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["pt_window"]['all_jets_softdrop'].Scale(1 / stacked_full["pt_window"]['all_jets_softdrop'].Integral())


dict_softdrop_hist_tot['signal_full']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_full']['pt_window'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_full']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_full']['pt_window'].Scale(1 / dict_softdrop_hist_tot['signal_full']['pt_window'].Integral())
legend4.Draw()


c4.cd(5)

stacked_full['eta_cut']['all_jets_softdrop'].Draw("HIST")
stacked_full['eta_cut']['all_jets_softdrop'].SetTitle("Eta cut; Softdrop mass, all jets; Events")
#stacked_full["eta_cut"]['all_jets_softdrop'].SetLineWidth(2)
stacked_full['eta_cut']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["eta_cut"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["eta_cut"]['all_jets_softdrop'].Scale(1 / stacked_full["eta_cut"]['all_jets_softdrop'].Integral())


dict_softdrop_hist_tot['signal_full']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_full']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_full']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_full']['eta_cut'].Scale(1 / dict_softdrop_hist_tot['signal_full']['eta_cut'].Integral())
legend4.Draw()


c4.cd(6)

stacked_full['cleaning']['all_jets_softdrop'].Draw("HIST")
stacked_full['cleaning']['all_jets_softdrop'].SetTitle("Cleaning; Softdrop mass, all jets; Events")
#stacked_full["cleaning"]['all_jets_softdrop'].SetLineWidth(2)
stacked_full['cleaning']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["cleaning"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["cleaning"]['all_jets_softdrop'].Scale(1 / stacked_full["cleaning"]['all_jets_softdrop'].Integral())


dict_softdrop_hist_tot['signal_full']['cleaning'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_full']['cleaning'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_full']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_full']['cleaning'].Scale(1 / dict_softdrop_hist_tot['signal_full']['cleaning'].Integral())
legend4.Draw()



#! FULLSIM softdrop SOFTDROP, JET 1

c5 = ROOT.TCanvas("c5", "Softdrop histograms for fullsim softdrop, jet 1", 1500, 1000)

c5.Divide(4,2)

c5.cd(1)

stacked_full['no_cut']['jet1_softdrop'].Draw("HIST")
stacked_full['no_cut']['jet1_softdrop'].SetTitle("No Cut; Softdrop mass Jet1; Events")
#stacked_full["no_cut"]['jet1_softdrop'].SetLineWidth(2)
stacked_full['no_cut']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["no_cut"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["no_cut"]['jet1_softdrop'].Scale(1 / stacked_full["no_cut"]['jet1_softdrop'].Integral())


dict_softdrop_hist1['signal_full']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist1['signal_full']['no_cut'].SetLineWidth(2)
dict_softdrop_hist1['signal_full']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_full']['no_cut'].Scale(1 / dict_softdrop_hist1['signal_full']['no_cut'].Integral())

legend5 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)
legend5.SetHeader("Fullsim", "C")
legend5.AddEntry(stacked_full["no_cut"]['jet1_softdrop'], "QCD", "f")
legend5.AddEntry(dict_softdrop_hist1['signal_full']['no_cut'], "signal", "l")
legend5.Draw()


c5.cd(2)

stacked_full['nfatjets_request']['jet1_softdrop'].Draw("HIST")
stacked_full['nfatjets_request']['jet1_softdrop'].SetTitle("request on nFatJet; Softdrop mass Jet1; Events ")
#stacked_full["nfatjets_request"]['jet1_softdrop'].SetLineWidth(2)
stacked_full['nfatjets_request']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["nfatjets_request"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["nfatjets_request"]['jet1_softdrop'].Scale(1 / stacked_full["nfatjets_request"]['jet1_softdrop'].Integral())


dict_softdrop_hist1['signal_full']['nfatjets_request'].Draw("SAME HIST")
dict_softdrop_hist1['signal_full']['nfatjets_request'].SetLineWidth(2)
dict_softdrop_hist1['signal_full']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
legend5.Draw()
dict_softdrop_hist1['signal_full']['nfatjets_request'].Scale(1 / dict_softdrop_hist1['signal_full']['nfatjets_request'].Integral())

c5.cd(3)

stacked_full['genjet_request']['jet1_softdrop'].Draw("HIST")
stacked_full['genjet_request']['jet1_softdrop'].SetTitle("request on GenJetAK8_pt; Softdrop mass Jet1; Events")
#stacked_full["genjet_request"]['jet1_softdrop'].SetLineWidth(2)
stacked_full['genjet_request']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["genjet_request"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["genjet_request"]['jet1_softdrop'].Scale(1 / stacked_full["genjet_request"]['jet1_softdrop'].Integral())

dict_softdrop_hist1['signal_full']['genjet_request'].Draw("SAME HIST")
dict_softdrop_hist1['signal_full']['genjet_request'].SetLineWidth(2)
dict_softdrop_hist1['signal_full']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_full']['genjet_request'].Scale(1 / dict_softdrop_hist1['signal_full']['genjet_request'].Integral())
legend5.Draw()


c5.cd(4)

stacked_full['pt_window']['jet1_softdrop'].Draw("HIST")
stacked_full['pt_window']['jet1_softdrop'].SetTitle("Pt window; Softdrop mass Jet1; Events")
#stacked_full["pt_window"]['jet1_softdrop'].SetLineWidth(2)
stacked_full['pt_window']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["pt_window"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["pt_window"]['jet1_softdrop'].Scale(1 / stacked_full["pt_window"]['jet1_softdrop'].Integral())

dict_softdrop_hist1['signal_full']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist1['signal_full']['pt_window'].SetLineWidth(2)
dict_softdrop_hist1['signal_full']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_full']['pt_window'].Scale(1 / dict_softdrop_hist1['signal_full']['pt_window'].Integral())
legend5.Draw()


c5.cd(5)

stacked_full['eta_cut']['jet1_softdrop'].Draw("HIST")
stacked_full['eta_cut']['jet1_softdrop'].SetTitle("Eta cut; Softdrop mass Jet1; Events")
#stacked_full["eta_cut"]['jet1_softdrop'].SetLineWidth(2)
stacked_full['eta_cut']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["eta_cut"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["eta_cut"]['jet1_softdrop'].Scale(1 / stacked_full["eta_cut"]['jet1_softdrop'].Integral())

dict_softdrop_hist1['signal_full']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist1['signal_full']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist1['signal_full']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_full']['eta_cut'].Scale(1 / dict_softdrop_hist1['signal_full']['eta_cut'].Integral())
legend5.Draw()


c5.cd(6)

stacked_full['cleaning']['jet1_softdrop'].Draw("HIST")
stacked_full['cleaning']['jet1_softdrop'].SetTitle("Cleaning; Softdrop mass Jet1; Events")
#stacked_full["cleaning"]['jet1_softdrop'].SetLineWidth(2)
stacked_full['cleaning']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["cleaning"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["cleaning"]['jet1_softdrop'].Scale(1 / stacked_full["cleaning"]['jet1_softdrop'].Integral())

dict_softdrop_hist1['signal_full']['cleaning'].Draw("SAME HIST")
dict_softdrop_hist1['signal_full']['cleaning'].SetLineWidth(2)
dict_softdrop_hist1['signal_full']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_full']['cleaning'].Scale(1 / dict_softdrop_hist1['signal_full']['cleaning'].Integral())
legend5.Draw()




#! FULLSIM SOFTDROP, JET 2

c6 = ROOT.TCanvas("c6", "Discriminator histograms for fullsim softdrop, jet 2", 1500, 1000)

c6.Divide(4,2)

c6.cd(1)

stacked_full['no_cut']['jet2_softdrop'].Draw("HIST")
stacked_full['no_cut']['jet2_softdrop'].SetTitle("No Cut; Softdrop mass Jet2; Events")
#stacked_full["no_cut"]['jet2_softdrop'].SetLineWidth(2)
stacked_full['no_cut']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["no_cut"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["no_cut"]['jet2_softdrop'].Scale(1 / stacked_full["no_cut"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_full']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist2['signal_full']['no_cut'].SetLineWidth(2)
dict_softdrop_hist2['signal_full']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_full']['no_cut'].Scale(1 / dict_softdrop_hist2['signal_full']['no_cut'].Integral())

legend6 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)
legend6.SetHeader("Fullsim", "C")
legend6.AddEntry(stacked_full["no_cut"]['jet2_softdrop'], "QCD", "f")
legend6.AddEntry(dict_softdrop_hist2['signal_full']['no_cut'], "signal", "l")
legend6.Draw()


c6.cd(2)

stacked_full['nfatjets_request']['jet2_softdrop'].Draw("HIST")
stacked_full['nfatjets_request']['jet2_softdrop'].SetTitle("request on nFatJet; Softdrop mass Jet2; Events ")
#stacked_full["nfatjets_request"]['jet2_softdrop'].SetLineWidth(2)
stacked_full['nfatjets_request']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["nfatjets_request"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["nfatjets_request"]['jet2_softdrop'].Scale(1 / stacked_full["nfatjets_request"]['jet2_softdrop'].Integral())


dict_softdrop_hist2['signal_full']['nfatjets_request'].Draw("SAME HIST")
dict_softdrop_hist2['signal_full']['nfatjets_request'].SetLineWidth(2)
dict_softdrop_hist2['signal_full']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_full']['nfatjets_request'].Scale(1 / dict_softdrop_hist2['signal_full']['nfatjets_request'].Integral())

legend6.Draw()

c6.cd(3)

stacked_full['genjet_request']['jet2_softdrop'].Draw("HIST")
stacked_full['genjet_request']['jet2_softdrop'].SetTitle("request on GenJetAK8_pt; Softdrop mass Jet2; Events")
#stacked_full["genjet_request"]['jet2_softdrop'].SetLineWidth(2)
stacked_full['genjet_request']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["genjet_request"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["genjet_request"]['jet2_softdrop'].Scale(1 / stacked_full["genjet_request"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_full']['genjet_request'].Draw("SAME HIST")
dict_softdrop_hist2['signal_full']['genjet_request'].SetLineWidth(2)
dict_softdrop_hist2['signal_full']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_full']['genjet_request'].Scale(1 / dict_softdrop_hist2['signal_full']['no_cut'].Integral())
legend6.Draw()

c6.cd(4)

stacked_full['pt_window']['jet2_softdrop'].Draw("HIST")
stacked_full['pt_window']['jet2_softdrop'].SetTitle("Pt window; Softdrop mass Jet2; Events")
#stacked_full["pt_window"]['jet2_softdrop'].SetLineWidth(2)
stacked_full['pt_window']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["pt_window"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["pt_window"]['jet2_softdrop'].Scale(1 / stacked_full["pt_window"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_full']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist2['signal_full']['pt_window'].SetLineWidth(2)
dict_softdrop_hist2['signal_full']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_full']['pt_window'].Scale(1 / dict_softdrop_hist2['signal_full']['pt_window'].Integral())
legend6.Draw()

c6.cd(5)

stacked_full['eta_cut']['jet2_softdrop'].Draw("HIST")
stacked_full['eta_cut']['jet2_softdrop'].SetTitle("Eta cut; Softdrop mass Jet2; Events")
#stacked_full["eta_cut"]['jet2_softdrop'].SetLineWidth(2)
stacked_full['eta_cut']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["eta_cut"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["eta_cut"]['jet2_softdrop'].Scale(1 / stacked_full["eta_cut"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_full']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist2['signal_full']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist2['signal_full']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_full']['eta_cut'].Scale(1 / dict_softdrop_hist2['signal_full']['eta_cut'].Integral())
legend6.Draw()

c6.cd(6)

stacked_full['cleaning']['jet2_softdrop'].Draw("HIST")
stacked_full['cleaning']['jet2_softdrop'].SetTitle("Cleaning; Softdrop mass Jet2; Events")
#stacked_full["cleaning"]['jet2_softdrop'].SetLineWidth(2)
stacked_full['cleaning']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_full["cleaning"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_full["cleaning"]['jet2_softdrop'].Scale(1 / stacked_full["cleaning"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_full']['cleaning'].Draw("SAME HIST")
dict_softdrop_hist2['signal_full']['cleaning'].SetLineWidth(2)
dict_softdrop_hist2['signal_full']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_full']['cleaning'].Scale(1 / dict_softdrop_hist2['signal_full']['cleaning'].Integral())
legend6.Draw()


#TODO FLASHSIM BEGINS HERE



#! FLASHSIM DISCRIMINATOR, ALL JETS

c7 = ROOT.TCanvas("c7", "Discriminator histograms for flashsim, all jets", 1500, 1000)

c7.Divide(4,2)
c7.cd(1)
ROOT.gPad.SetLogy()

stacked_flash['no_cut']['all_jets_discr'].Draw("HIST")
stacked_flash['no_cut']['all_jets_discr'].SetTitle("No Cut; Discriminator, all jets; Events")
#stacked_flash["no_cut"]['all_jets_discr'].SetLineWidth(2)
stacked_flash['no_cut']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["no_cut"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["no_cut"]['all_jets_discr'].Scale(1 / stacked_flash["no_cut"]['all_jets_discr'].Integral())


dict_discr_hist_tot['signal_flash']['no_cut'].Draw("SAME HIST")
dict_discr_hist_tot['signal_flash']['no_cut'].SetLineWidth(2)
dict_discr_hist_tot['signal_flash']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_flash']['no_cut'].Scale(1 / dict_discr_hist_tot['signal_flash']['no_cut'].Integral())

legend7 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend7.SetHeader("Flashim", "C")
legend7.AddEntry(stacked_flash["no_cut"]['all_jets_discr'], "QCD", "f")
legend7.AddEntry(dict_discr_hist_tot['signal_full']['no_cut'], "signal", "l")
legend7.Draw()


c7.cd(4)
ROOT.gPad.SetLogy()

stacked_flash['pt_window']['all_jets_discr'].Draw("HIST")
stacked_flash['pt_window']['all_jets_discr'].SetTitle("Pt window; Discriminator, all jets; Events")
#stacked_flash["pt_window"]['all_jets_discr'].SetLineWidth(2)
stacked_flash['pt_window']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["pt_window"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["pt_window"]['all_jets_discr'].Scale(1 / stacked_flash["pt_window"]['all_jets_discr'].Integral())


dict_discr_hist_tot['signal_flash']['pt_window'].Draw("SAME HIST")
dict_discr_hist_tot['signal_flash']['pt_window'].SetLineWidth(2)
dict_discr_hist_tot['signal_flash']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_flash']['pt_window'].Scale(1 / dict_discr_hist_tot['signal_flash']['pt_window'].Integral())
legend7.Draw()


c7.cd(5)
ROOT.gPad.SetLogy()

stacked_flash['eta_cut']['all_jets_discr'].Draw("HIST")
stacked_flash['eta_cut']['all_jets_discr'].SetTitle("Eta cut; Discriminator, all jets; Events")
#stacked_flash["eta_cut"]['all_jets_discr'].SetLineWidth(2)
stacked_flash['eta_cut']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["eta_cut"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["eta_cut"]['all_jets_discr'].Scale(1 / stacked_flash["eta_cut"]['all_jets_discr'].Integral())


dict_discr_hist_tot['signal_flash']['eta_cut'].Draw("SAME HIST")
dict_discr_hist_tot['signal_flash']['eta_cut'].SetLineWidth(2)
dict_discr_hist_tot['signal_flash']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_flash']['eta_cut'].Scale(1 / dict_discr_hist_tot['signal_flash']['eta_cut'].Integral())
legend7.Draw()

c7.cd(6)
ROOT.gPad.SetLogy()

stacked_flash['cleaning']['all_jets_discr'].Draw("HIST")
stacked_flash['cleaning']['all_jets_discr'].SetTitle("Cleaning; Discriminator, all jets; Events")
#stacked_flash["cleaning"]['all_jets_discr'].SetLineWidth(2)
stacked_flash['cleaning']['all_jets_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["cleaning"]['all_jets_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["cleaning"]['all_jets_discr'].Scale(1 / stacked_flash["cleaning"]['all_jets_discr'].Integral())


dict_discr_hist_tot['signal_flash']['cleaning'].Draw("SAME HIST")
dict_discr_hist_tot['signal_flash']['cleaning'].SetLineWidth(2)
dict_discr_hist_tot['signal_flash']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_flash']['cleaning'].Scale(1 / dict_discr_hist_tot['signal_flash']['cleaning'].Integral())
legend7.Draw()



#! FLASHSIM DISCRIMINATOR, JET 1

c8 = ROOT.TCanvas("c8", "Discriminator histograms for flashsim discriminator, jet 1", 1500, 1000)

c8.Divide(4,2)
c8.cd(1)
ROOT.gPad.SetLogy()

stacked_flash['no_cut']['jet1_discr'].Draw("HIST")
stacked_flash['no_cut']['jet1_discr'].SetTitle("No Cut; Discriminator Jet1; Events")
#stacked_flash["no_cut"]['jet1_discr'].SetLineWidth(2)
stacked_flash['no_cut']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["no_cut"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["no_cut"]['jet1_discr'].Scale(1 / stacked_flash["no_cut"]['jet1_discr'].Integral())

dict_discr_hist1['signal_flash']['no_cut'].Draw("SAME HIST")
dict_discr_hist1['signal_flash']['no_cut'].SetLineWidth(2)
dict_discr_hist1['signal_flash']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_flash']['no_cut'].Scale(1 / dict_discr_hist1['signal_flash']['no_cut'].Integral())

legend8 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend8.SetHeader("Run2 Flashsim", "C")
legend8.AddEntry(stacked_flash["no_cut"]['jet1_discr'], "QCD", "f")
legend8.AddEntry(dict_discr_hist1['signal_full']['no_cut'], "signal", "l")
legend8.Draw()

c8.cd(4)
ROOT.gPad.SetLogy()

stacked_flash['pt_window']['jet1_discr'].Draw("HIST")
stacked_flash['pt_window']['jet1_discr'].SetTitle("Pt window; Discriminator Jet1; Events")
#stacked_flash["pt_window"]['jet1_discr'].SetLineWidth(2)
stacked_flash['pt_window']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["pt_window"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["pt_window"]['jet1_discr'].Scale(1 / stacked_flash["pt_window"]['jet1_discr'].Integral())


dict_discr_hist1['signal_flash']['pt_window'].Draw("SAME HIST")
dict_discr_hist1['signal_flash']['pt_window'].SetLineWidth(2)
dict_discr_hist1['signal_flash']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_flash']['pt_window'].Scale(1 / dict_discr_hist1['signal_flash']['pt_window'].Integral())
legend8.Draw()

c8.cd(5)
ROOT.gPad.SetLogy()

stacked_flash['eta_cut']['jet1_discr'].Draw("HIST")
stacked_flash['eta_cut']['jet1_discr'].SetTitle("Eta cut; Discriminator Jet1; Events")
#stacked_flash["eta_cut"]['jet1_discr'].SetLineWidth(2)
stacked_flash['eta_cut']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["eta_cut"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["eta_cut"]['jet1_discr'].Scale(1 / stacked_flash["eta_cut"]['jet1_discr'].Integral())

dict_discr_hist1['signal_flash']['eta_cut'].Draw("SAME HIST")
dict_discr_hist1['signal_flash']['eta_cut'].SetLineWidth(2)
dict_discr_hist1['signal_flash']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_flash']['eta_cut'].Scale(1 / dict_discr_hist1['signal_flash']['eta_cut'].Integral())
legend8.Draw()

c8.cd(6)
ROOT.gPad.SetLogy()

stacked_flash['cleaning']['jet1_discr'].Draw("HIST")
stacked_flash['cleaning']['jet1_discr'].SetTitle("Cleaning; Discriminator Jet1; Events")
#stacked_flash["cleaning"]['jet1_discr'].SetLineWidth(2)
stacked_flash['cleaning']['jet1_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["cleaning"]['jet1_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["cleaning"]['jet1_discr'].Scale(1 / stacked_flash["cleaning"]['jet1_discr'].Integral())

dict_discr_hist1['signal_flash']['cleaning'].Draw("SAME HIST")
dict_discr_hist1['signal_flash']['cleaning'].SetLineWidth(2)
dict_discr_hist1['signal_flash']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_flash']['cleaning'].Scale(1 / dict_discr_hist1['signal_flash']['cleaning'].Integral())
legend8.Draw()



#! FLASHSIM DISCRIMINATOR, JET 2

c9 = ROOT.TCanvas("c9", "Discriminator histograms for flashsim discriminator, jet 2", 1500, 1000)

c9.Divide(4,2)
c9.cd(1)
ROOT.gPad.SetLogy()

stacked_flash['no_cut']['jet2_discr'].Draw("HIST")
stacked_flash['no_cut']['jet2_discr'].SetTitle("No Cut; Discriminator Jet 2; Events")
#stacked_flash["no_cut"]['jet2_discr'].SetLineWidth(2)
stacked_flash['no_cut']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["no_cut"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["no_cut"]['jet2_discr'].Scale(1 / stacked_flash["no_cut"]['jet2_discr'].Integral())


dict_discr_hist2['signal_flash']['no_cut'].Draw("SAME HIST")
dict_discr_hist2['signal_flash']['no_cut'].SetLineWidth(2)
dict_discr_hist2['signal_flash']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_flash']['no_cut'].Scale(1 / dict_discr_hist2['signal_flash']['no_cut'].Integral())

legend9 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend9.SetHeader("Run2 Flashsim", "C")
legend9.AddEntry(stacked_flash["no_cut"]['jet2_discr'], "QCD", "f")
legend9.AddEntry(dict_discr_hist2['signal_full']['no_cut'], "signal", "l")
legend9.Draw()


c9.cd(4)
ROOT.gPad.SetLogy()

stacked_flash['pt_window']['jet2_discr'].Draw("HIST")
stacked_flash['pt_window']['jet2_discr'].SetTitle("Pt window; Discriminator Jet 2; Events")
#stacked_flash["pt_window"]['jet2_discr'].SetLineWidth(2)
stacked_flash['pt_window']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["pt_window"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["pt_window"]['jet2_discr'].Scale(1 / stacked_flash["pt_window"]['jet2_discr'].Integral())


dict_discr_hist2['signal_flash']['pt_window'].Draw("SAME HIST")
dict_discr_hist2['signal_flash']['pt_window'].SetLineWidth(2)
dict_discr_hist2['signal_flash']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_flash']['pt_window'].Scale(1 / dict_discr_hist2['signal_flash']['pt_window'].Integral())
legend9.Draw()


c9.cd(5)
ROOT.gPad.SetLogy()

stacked_flash['eta_cut']['jet2_discr'].Draw("HIST")
stacked_flash['eta_cut']['jet2_discr'].SetTitle("Eta cut; Discriminator Jet 2; Events")
#stacked_flash["eta_cut"]['jet2_discr'].SetLineWidth(2)
stacked_flash['eta_cut']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["eta_cut"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["eta_cut"]['jet2_discr'].Scale(1 / stacked_flash["eta_cut"]['jet2_discr'].Integral())

dict_discr_hist2['signal_flash']['eta_cut'].Draw("SAME HIST")
dict_discr_hist2['signal_flash']['eta_cut'].SetLineWidth(2)
dict_discr_hist2['signal_flash']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_flash']['eta_cut'].Scale(1 / dict_discr_hist2['signal_flash']['eta_cut'].Integral())
legend9.Draw()

c9.cd(6)
ROOT.gPad.SetLogy()

stacked_flash['cleaning']['jet2_discr'].Draw("HIST")
stacked_flash['cleaning']['jet2_discr'].SetTitle("Cleaning; Discriminator Jet 2; Events")
#stacked_flash["cleaning"]['jet2_discr'].SetLineWidth(2)
stacked_flash['cleaning']['jet2_discr'].SetLineColor(ROOT.kCyan)
stacked_flash["cleaning"]['jet2_discr'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["cleaning"]['jet2_discr'].Scale(1 / stacked_flash["cleaning"]['jet2_discr'].Integral())

dict_discr_hist2['signal_flash']['cleaning'].Draw("SAME HIST")
dict_discr_hist2['signal_flash']['cleaning'].SetLineWidth(2)
dict_discr_hist2['signal_flash']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_flash']['cleaning'].Scale(1 / dict_discr_hist2['signal_flash']['cleaning'].Integral())
legend9.Draw()



#! FLASHSIM SOFTDROP, ALL JETS

c10 = ROOT.TCanvas("c10", "Discriminator histograms for flashsim softdrop, all jets", 1500, 1000)

c10.Divide(4,2)
c10.cd(1)

stacked_flash['no_cut']['all_jets_softdrop'].Draw("HIST")
stacked_flash['no_cut']['all_jets_softdrop'].SetTitle("No Cut; Softdrop mass, all jets; Events")
#stacked_flash["no_cut"]['all_jets_softdrop'].SetLineWidth(2)
stacked_flash['no_cut']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["no_cut"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["no_cut"]['all_jets_softdrop'].Scale(1 / stacked_flash["no_cut"]['all_jets_softdrop'].Integral())

dict_softdrop_hist_tot['signal_flash']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_flash']['no_cut'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_flash']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_flash']['no_cut'].Scale(1 / dict_softdrop_hist_tot['signal_flash']['no_cut'].Integral())

legend10 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend10.SetHeader("Run2 Flashsim", "C")
legend10.AddEntry(stacked_flash["no_cut"]['all_jets_softdrop'], "QCD", "f")
legend10.AddEntry(dict_softdrop_hist_tot['signal_full']['no_cut'], "signal", "l")
legend10.Draw()


c10.cd(4)

stacked_flash['pt_window']['all_jets_softdrop'].Draw("HIST")
stacked_flash['pt_window']['all_jets_softdrop'].SetTitle("Pt window; Softdrop mass, all jets; Events")
#stacked_flash["pt_window"]['all_jets_softdrop'].SetLineWidth(2)
stacked_flash['pt_window']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["pt_window"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["pt_window"]['all_jets_softdrop'].Scale(1 / stacked_flash["pt_window"]['all_jets_softdrop'].Integral())

dict_softdrop_hist_tot['signal_flash']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_flash']['pt_window'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_flash']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_flash']['pt_window'].Scale(1 / dict_softdrop_hist_tot['signal_flash']['pt_window'].Integral())
legend10.Draw()

c10.cd(5)

stacked_flash['eta_cut']['all_jets_softdrop'].Draw("HIST")
stacked_flash['eta_cut']['all_jets_softdrop'].SetTitle("Eta cut; Softdrop mass, all jets; Events")
#stacked_flash["eta_cut"]['all_jets_softdrop'].SetLineWidth(2)
stacked_flash['eta_cut']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["eta_cut"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["eta_cut"]['all_jets_softdrop'].Scale(1 / stacked_flash["eta_cut"]['all_jets_softdrop'].Integral())

dict_softdrop_hist_tot['signal_flash']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_flash']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_flash']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_flash']['eta_cut'].Scale(1 / dict_softdrop_hist_tot['signal_flash']['eta_cut'].Integral())
legend10.Draw()

c10.cd(6)

stacked_flash['cleaning']['all_jets_softdrop'].Draw("HIST")
stacked_flash['cleaning']['all_jets_softdrop'].SetTitle("Cleaning; Softdrop mass, all jets; Events")
#stacked_flash["cleaning"]['all_jets_softdrop'].SetLineWidth(2)
stacked_flash['cleaning']['all_jets_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["cleaning"]['all_jets_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["cleaning"]['all_jets_softdrop'].Scale(1 / stacked_flash["cleaning"]['all_jets_softdrop'].Integral())

dict_softdrop_hist_tot['signal_flash']['cleaning'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_flash']['cleaning'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_flash']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_flash']['cleaning'].Scale(1 / dict_softdrop_hist_tot['signal_flash']['cleaning'].Integral())
legend10.Draw()


#! FLASHSIM softdrop SOFTDROP, JET 1

c11 = ROOT.TCanvas("c11", "Softdrop histograms for flashsim softdrop, jet 1", 1500, 1000)

c11.Divide(4,2)

c11.cd(1)

stacked_flash['no_cut']['jet1_softdrop'].Draw("HIST")
stacked_flash['no_cut']['jet1_softdrop'].SetTitle("No Cut; Softdrop mass Jet1; Events")
#stacked_flash["no_cut"]['jet1_softdrop'].SetLineWidth(2)
stacked_flash['no_cut']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["no_cut"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["no_cut"]['jet1_softdrop'].Scale(1 / stacked_flash["no_cut"]['jet1_softdrop'].Integral())

dict_softdrop_hist1['signal_flash']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist1['signal_flash']['no_cut'].SetLineWidth(2)
dict_softdrop_hist1['signal_flash']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_flash']['no_cut'].Scale(1 / dict_softdrop_hist1['signal_flash']['no_cut'].Integral())

legend11 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend11.SetHeader("Run2 Flashsim", "C")
legend11.AddEntry(stacked_flash["no_cut"]['jet1_softdrop'], "QCD", "f")
legend11.AddEntry(dict_softdrop_hist1['signal_full']['no_cut'], "signal", "l")
legend11.Draw()


c11.cd(4)

stacked_flash['pt_window']['jet1_softdrop'].Draw("HIST")
stacked_flash['pt_window']['jet1_softdrop'].SetTitle("Pt window; Softdrop mass Jet1; Events")
#stacked_flash["pt_window"]['jet1_softdrop'].SetLineWidth(2)
stacked_flash['pt_window']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["pt_window"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["pt_window"]['jet1_softdrop'].Scale(1 / stacked_flash["pt_window"]['jet1_softdrop'].Integral())

dict_softdrop_hist1['signal_flash']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist1['signal_flash']['pt_window'].SetLineWidth(2)
dict_softdrop_hist1['signal_flash']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_flash']['pt_window'].Scale(1 / dict_softdrop_hist1['signal_flash']['pt_window'].Integral())
legend11.Draw()

c11.cd(5)

stacked_flash['eta_cut']['jet1_softdrop'].Draw("HIST")
stacked_flash['eta_cut']['jet1_softdrop'].SetTitle("Eta cut; Softdrop mass Jet1; Events")
#stacked_flash["eta_cut"]['jet1_softdrop'].SetLineWidth(2)
stacked_flash['eta_cut']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["eta_cut"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["eta_cut"]['jet1_softdrop'].Scale(1 / stacked_flash["eta_cut"]['jet1_softdrop'].Integral())

dict_softdrop_hist1['signal_flash']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist1['signal_flash']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist1['signal_flash']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_flash']['eta_cut'].Scale(1 / dict_softdrop_hist1['signal_flash']['eta_cut'].Integral())
legend11.Draw()

c11.cd(6)

stacked_flash['cleaning']['jet1_softdrop'].Draw("HIST")
stacked_flash['cleaning']['jet1_softdrop'].SetTitle("Cleaning; Softdrop mass Jet1; Events")
#stacked_flash["cleaning"]['jet1_softdrop'].SetLineWidth(2)
stacked_flash['cleaning']['jet1_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["cleaning"]['jet1_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["cleaning"]['jet1_softdrop'].Scale(1 / stacked_flash["cleaning"]['jet1_softdrop'].Integral())

dict_softdrop_hist1['signal_flash']['cleaning'].Draw("SAME HIST")
dict_softdrop_hist1['signal_flash']['cleaning'].SetLineWidth(2)
dict_softdrop_hist1['signal_flash']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_flash']['cleaning'].Scale(1 / dict_softdrop_hist1['signal_flash']['cleaning'].Integral())
legend11.Draw()


#! FLASHSIM SOFTDROP, JET 2

c12 = ROOT.TCanvas("c12", "Discriminator histograms for flashsim softdrop, jet 2", 1500, 1000)

c12.Divide(4,2)

c12.cd(1)

stacked_flash['no_cut']['jet2_softdrop'].Draw("HIST")
stacked_flash['no_cut']['jet2_softdrop'].SetTitle("No Cut; Softdrop mass Jet2; Events")
#stacked_flash["no_cut"]['jet2_softdrop'].SetLineWidth(2)
stacked_flash['no_cut']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["no_cut"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["no_cut"]['jet2_softdrop'].Scale(1 / stacked_flash["no_cut"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_flash']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist2['signal_flash']['no_cut'].SetLineWidth(2)
dict_softdrop_hist2['signal_flash']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_flash']['no_cut'].Scale(1 / dict_softdrop_hist2['signal_flash']['no_cut'].Integral())

legend12 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend12.SetHeader("Run2 Flashsim", "C")
legend12.AddEntry(stacked_flash["no_cut"]['jet2_softdrop'], "QCD", "f")
legend12.AddEntry(dict_softdrop_hist2['signal_full']['no_cut'], "signal", "l")
legend12.Draw()


c12.cd(4)

stacked_flash['pt_window']['jet2_softdrop'].Draw("HIST")
stacked_flash['pt_window']['jet2_softdrop'].SetTitle("Pt window; Softdrop mass Jet2; Events")
#stacked_flash["pt_window"]['jet2_softdrop'].SetLineWidth(2)
stacked_flash['pt_window']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["pt_window"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["pt_window"]['jet2_softdrop'].Scale(1 / stacked_flash["pt_window"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_flash']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist2['signal_flash']['pt_window'].SetLineWidth(2)
dict_softdrop_hist2['signal_flash']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_flash']['pt_window'].Scale(1 / dict_softdrop_hist2['signal_flash']['pt_window'].Integral())
legend12.Draw()

c12.cd(5)

stacked_flash['eta_cut']['jet2_softdrop'].Draw("HIST")
stacked_flash['eta_cut']['jet2_softdrop'].SetTitle("Eta cut; Softdrop mass Jet2; Events")
#stacked_flash["eta_cut"]['jet2_softdrop'].SetLineWidth(2)
stacked_flash['eta_cut']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["eta_cut"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["eta_cut"]['jet2_softdrop'].Scale(1 / stacked_flash["eta_cut"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_flash']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist2['signal_flash']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist2['signal_flash']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_flash']['eta_cut'].Scale(1 / dict_softdrop_hist2['signal_flash']['eta_cut'].Integral())
legend12.Draw()

c12.cd(6)

stacked_flash['cleaning']['jet2_softdrop'].Draw("HIST")
stacked_flash['cleaning']['jet2_softdrop'].SetTitle("Cleaning; Softdrop mass Jet2; Events")
#stacked_flash["cleaning"]['jet2_softdrop'].SetLineWidth(2)
stacked_flash['cleaning']['jet2_softdrop'].SetLineColor(ROOT.kCyan)
stacked_flash["cleaning"]['jet2_softdrop'].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
stacked_flash["cleaning"]['jet2_softdrop'].Scale(1 / stacked_flash["cleaning"]['jet2_softdrop'].Integral())

dict_softdrop_hist2['signal_flash']['cleaning'].Draw("SAME HIST")
dict_softdrop_hist2['signal_flash']['cleaning'].SetLineWidth(2)
dict_softdrop_hist2['signal_flash']['cleaning'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_flash']['cleaning'].Scale(1 / dict_softdrop_hist2['signal_flash']['cleaning'].Integral())
legend12.Draw()

#TODO PHASE2 BEGINS HERE

#! PHASE 2 DISCRIMINATOR, ALL JETS

c13 = ROOT.TCanvas("c13", "Discriminator histograms for phase 2, all jets", 1500, 1000)

c13.Divide(4,2)
c13.cd(1)
ROOT.gPad.SetLogy()

dict_discr_hist_tot['QCD_ph2']['no_cut'].Draw("HIST")
dict_discr_hist_tot['QCD_ph2']['no_cut'].SetTitle("No Cut; Discriminator, all jets; Events")
#dict_discr_hist_tot['QCD_ph2']["no_cut"].SetLineWidth(2)
dict_discr_hist_tot['QCD_ph2']['no_cut'].SetLineColor(ROOT.kCyan)
dict_discr_hist_tot['QCD_ph2']["no_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist_tot['QCD_ph2']["no_cut"].Scale(1 / dict_discr_hist_tot['QCD_ph2']["no_cut"].Integral())

dict_discr_hist_tot['signal_ph2']['no_cut'].Draw("SAME HIST")
dict_discr_hist_tot['signal_ph2']['no_cut'].SetLineWidth(2)
dict_discr_hist_tot['signal_ph2']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_ph2']["no_cut"].Scale(1 / dict_discr_hist_tot['signal_ph2']["no_cut"].Integral())

legend13 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend13.SetHeader("Phase2 fullsim", "C")
legend13.AddEntry(dict_discr_hist_tot['QCD_ph2']['no_cut'], "QCD", "f")
legend13.AddEntry(dict_discr_hist_tot['signal_full']['no_cut'], "signal", "l")
legend13.Draw()


c13.cd(2)
ROOT.gPad.SetLogy()

dict_discr_hist_tot['QCD_ph2']['nfatjets_request'].Draw("HIST")
dict_discr_hist_tot['QCD_ph2']['nfatjets_request'].SetTitle("request on nFatJet; Discriminator, all jets; Events ")
#dict_discr_hist_tot['QCD_ph2']["nfatjets_request"].SetLineWidth(2)
dict_discr_hist_tot['QCD_ph2']['nfatjets_request'].SetLineColor(ROOT.kCyan)
dict_discr_hist_tot['QCD_ph2']["nfatjets_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist_tot['QCD_ph2']["nfatjets_request"].Scale(1 / dict_discr_hist_tot['QCD_ph2']["nfatjets_request"].Integral())


dict_discr_hist_tot['signal_ph2']['nfatjets_request'].Draw("SAME HIST")
dict_discr_hist_tot['signal_ph2']['nfatjets_request'].SetLineWidth(2)
dict_discr_hist_tot['signal_ph2']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_ph2']["nfatjets_request"].Scale(1 / dict_discr_hist_tot['signal_ph2']["nfatjets_request"].Integral())
legend13.Draw()

c13.cd(3)
ROOT.gPad.SetLogy()

dict_discr_hist_tot['QCD_ph2']['genjet_request'].Draw("HIST")
dict_discr_hist_tot['QCD_ph2']['genjet_request'].SetTitle("request on GenJetAK8_pt; Discriminator, all jets; Events")
#dict_discr_hist_tot['QCD_ph2']["genjet_request"].SetLineWidth(2)
dict_discr_hist_tot['QCD_ph2']['genjet_request'].SetLineColor(ROOT.kCyan)
dict_discr_hist_tot['QCD_ph2']["genjet_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist_tot['QCD_ph2']["genjet_request"].Scale(1 / dict_discr_hist_tot['QCD_ph2']["genjet_request"].Integral())

dict_discr_hist_tot['signal_ph2']['genjet_request'].Draw("SAME HIST")
dict_discr_hist_tot['signal_ph2']['genjet_request'].SetLineWidth(2)
dict_discr_hist_tot['signal_ph2']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_ph2']["genjet_request"].Scale(1 / dict_discr_hist_tot['signal_ph2']["genjet_request"].Integral())
legend13.Draw()

c13.cd(4)
ROOT.gPad.SetLogy()

dict_discr_hist_tot['QCD_ph2']['pt_window'].Draw("HIST")
dict_discr_hist_tot['QCD_ph2']['pt_window'].SetTitle("Pt window; Discriminator, all jets; Events")
#dict_discr_hist_tot['QCD_ph2']["pt_window"].SetLineWidth(2)
dict_discr_hist_tot['QCD_ph2']['pt_window'].SetLineColor(ROOT.kCyan)
dict_discr_hist_tot['QCD_ph2']["pt_window"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist_tot['QCD_ph2']["pt_window"].Scale(1 / dict_discr_hist_tot['QCD_ph2']["pt_window"].Integral())

dict_discr_hist_tot['signal_ph2']['pt_window'].Draw("SAME HIST")
dict_discr_hist_tot['signal_ph2']['pt_window'].SetLineWidth(2)
dict_discr_hist_tot['signal_ph2']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_ph2']["pt_window"].Scale(1 / dict_discr_hist_tot['signal_ph2']["pt_window"].Integral())
legend13.Draw()

c13.cd(5)
ROOT.gPad.SetLogy()

dict_discr_hist_tot['QCD_ph2']['eta_cut'].Draw("HIST")
dict_discr_hist_tot['QCD_ph2']['eta_cut'].SetTitle("Eta cut; Discriminator, all jets; Events")
#dict_discr_hist_tot['QCD_ph2']["eta_cut"].SetLineWidth(2)
dict_discr_hist_tot['QCD_ph2']['eta_cut'].SetLineColor(ROOT.kCyan)
dict_discr_hist_tot['QCD_ph2']["eta_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist_tot['QCD_ph2']["eta_cut"].Scale(1 / dict_discr_hist_tot['QCD_ph2']["eta_cut"].Integral())

dict_discr_hist_tot['signal_ph2']['eta_cut'].Draw("SAME HIST")
dict_discr_hist_tot['signal_ph2']['eta_cut'].SetLineWidth(2)
dict_discr_hist_tot['signal_ph2']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist_tot['signal_ph2']["eta_cut"].Scale(1 / dict_discr_hist_tot['signal_ph2']["eta_cut"].Integral())
legend13.Draw()


#! PHASE 2 DISCRIMINATOR, JET 1

c14 = ROOT.TCanvas("c14", "Discriminator histograms for phase 2 discriminator, jet 1", 1500, 1000)

c14.Divide(4,2)
c14.cd(1)
ROOT.gPad.SetLogy()

dict_discr_hist1['QCD_ph2']['no_cut'].Draw("HIST")
dict_discr_hist1['QCD_ph2']['no_cut'].SetTitle("No Cut; Discriminator Jet1; Events")
#dict_discr_hist1['QCD_ph2']["no_cut"].SetLineWidth(2)
dict_discr_hist1['QCD_ph2']['no_cut'].SetLineColor(ROOT.kCyan)
dict_discr_hist1['QCD_ph2']["no_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist1['QCD_ph2']["no_cut"].Scale(1 / dict_discr_hist1['QCD_ph2']["no_cut"].Integral())

dict_discr_hist1['signal_ph2']['no_cut'].Draw("SAME HIST")
dict_discr_hist1['signal_ph2']['no_cut'].SetLineWidth(2)
dict_discr_hist1['signal_ph2']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_ph2']["no_cut"].Scale(1 / dict_discr_hist1['signal_ph2']["no_cut"].Integral())

legend14 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend14.SetHeader("Phase2 fullsim", "C")
legend14.AddEntry(dict_discr_hist1['QCD_ph2']['no_cut'], "QCD", "f")
legend14.AddEntry(dict_discr_hist1['signal_full']['no_cut'], "signal", "l")
legend14.Draw()

c14.cd(2)
ROOT.gPad.SetLogy()

dict_discr_hist1['QCD_ph2']['nfatjets_request'].Draw("HIST")
dict_discr_hist1['QCD_ph2']['nfatjets_request'].SetTitle("request on nFatJet; Discriminator Jet1; Events ")
#dict_discr_hist1['QCD_ph2']["nfatjets_request"].SetLineWidth(2)
dict_discr_hist1['QCD_ph2']['nfatjets_request'].SetLineColor(ROOT.kCyan)
dict_discr_hist1['QCD_ph2']["nfatjets_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist1['QCD_ph2']["nfatjets_request"].Scale(1 / dict_discr_hist1['QCD_ph2']["nfatjets_request"].Integral())

dict_discr_hist1['signal_ph2']['nfatjets_request'].Draw("SAME HIST")
dict_discr_hist1['signal_ph2']['nfatjets_request'].SetLineWidth(2)
dict_discr_hist1['signal_ph2']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_ph2']["nfatjets_request"].Scale(1 / dict_discr_hist1['signal_ph2']["nfatjets_request"].Integral())
legend14.Draw()

c14.cd(3)
ROOT.gPad.SetLogy()

dict_discr_hist1['QCD_ph2']['genjet_request'].Draw("HIST")
dict_discr_hist1['QCD_ph2']['genjet_request'].SetTitle("request on GenJetAK8_pt; Discriminator Jet1; Events")
#dict_discr_hist1['QCD_ph2']["genjet_request"].SetLineWidth(2)
dict_discr_hist1['QCD_ph2']['genjet_request'].SetLineColor(ROOT.kCyan)
dict_discr_hist1['QCD_ph2']["genjet_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist1['QCD_ph2']["genjet_request"].Scale(1 / dict_discr_hist1['QCD_ph2']["genjet_request"].Integral())

dict_discr_hist1['signal_ph2']['genjet_request'].Draw("SAME HIST")
dict_discr_hist1['signal_ph2']['genjet_request'].SetLineWidth(2)
dict_discr_hist1['signal_ph2']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_ph2']["genjet_request"].Scale(1 / dict_discr_hist1['signal_ph2']["genjet_request"].Integral())
legend14.Draw()

c14.cd(4)
ROOT.gPad.SetLogy()

dict_discr_hist1['QCD_ph2']['pt_window'].Draw("HIST")
dict_discr_hist1['QCD_ph2']['pt_window'].SetTitle("Pt window; Discriminator Jet1; Events")
#dict_discr_hist1['QCD_ph2']["pt_window"].SetLineWidth(2)
dict_discr_hist1['QCD_ph2']['pt_window'].SetLineColor(ROOT.kCyan)
dict_discr_hist1['QCD_ph2']["pt_window"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist1['QCD_ph2']["pt_window"].Scale(1 / dict_discr_hist1['QCD_ph2']["pt_window"].Integral())

dict_discr_hist1['signal_ph2']['pt_window'].Draw("SAME HIST")
dict_discr_hist1['signal_ph2']['pt_window'].SetLineWidth(2)
dict_discr_hist1['signal_ph2']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_ph2']["pt_window"].Scale(1 / dict_discr_hist1['signal_ph2']["pt_window"].Integral())
legend14.Draw()

c14.cd(5)
ROOT.gPad.SetLogy()

dict_discr_hist1['QCD_ph2']['eta_cut'].Draw("HIST")
dict_discr_hist1['QCD_ph2']['eta_cut'].SetTitle("Eta cut; Discriminator Jet1; Events")
#dict_discr_hist1['QCD_ph2']["eta_cut"].SetLineWidth(2)
dict_discr_hist1['QCD_ph2']['eta_cut'].SetLineColor(ROOT.kCyan)
dict_discr_hist1['QCD_ph2']["eta_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist1['QCD_ph2']["eta_cut"].Scale(1 / dict_discr_hist1['QCD_ph2']["eta_cut"].Integral())

dict_discr_hist1['signal_ph2']['eta_cut'].Draw("SAME HIST")
dict_discr_hist1['signal_ph2']['eta_cut'].SetLineWidth(2)
dict_discr_hist1['signal_ph2']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist1['signal_ph2']["eta_cut"].Scale(1 / dict_discr_hist1['signal_ph2']["eta_cut"].Integral())
legend14.Draw()



#! PHASE 2 DISCRIMINATOR, JET 2

c15 = ROOT.TCanvas("c15", "Discriminator histograms for phase 2 discriminator, jet 2", 1500, 1000)

c15.Divide(4,2)
c15.cd(1)
ROOT.gPad.SetLogy()

dict_discr_hist2['QCD_ph2']['no_cut'].Draw("HIST")
dict_discr_hist2['QCD_ph2']['no_cut'].SetTitle("No Cut; Discriminator Jet2; Events")
#dict_discr_hist2['QCD_ph2']["no_cut"].SetLineWidth(2)
dict_discr_hist2['QCD_ph2']['no_cut'].SetLineColor(ROOT.kCyan)
dict_discr_hist2['QCD_ph2']["no_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist2['QCD_ph2']["no_cut"].Scale(1 / dict_discr_hist2['QCD_ph2']["no_cut"].Integral())

dict_discr_hist2['signal_ph2']['no_cut'].Draw("SAME HIST")
dict_discr_hist2['signal_ph2']['no_cut'].SetLineWidth(2)
dict_discr_hist2['signal_ph2']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_ph2']["no_cut"].Scale(1 / dict_discr_hist2['signal_ph2']["no_cut"].Integral())

legend15 = ROOT.TLegend(0.52, 0.70, 0.82, 0.88)
legend15.SetHeader("Phase2 fullsim", "C")
legend15.AddEntry(dict_discr_hist_tot['QCD_ph2']['no_cut'], "QCD", "f")
legend15.AddEntry(dict_discr_hist_tot['signal_full']['no_cut'], "signal", "l")
legend15.Draw()

c15.cd(2)
ROOT.gPad.SetLogy()

dict_discr_hist2['QCD_ph2']['nfatjets_request'].Draw("HIST")
dict_discr_hist2['QCD_ph2']['nfatjets_request'].SetTitle("request on nFatJet; Discriminator Jet2; Events ")
#dict_discr_hist2['QCD_ph2']["nfatjets_request"].SetLineWidth(2)
dict_discr_hist2['QCD_ph2']['nfatjets_request'].SetLineColor(ROOT.kCyan)
dict_discr_hist2['QCD_ph2']["nfatjets_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist2['QCD_ph2']["nfatjets_request"].Scale(1 / dict_discr_hist2['QCD_ph2']["nfatjets_request"].Integral())

dict_discr_hist2['signal_ph2']['nfatjets_request'].Draw("SAME HIST")
dict_discr_hist2['signal_ph2']['nfatjets_request'].SetLineWidth(2)
dict_discr_hist2['signal_ph2']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_ph2']["nfatjets_request"].Scale(1 / dict_discr_hist2['signal_ph2']["nfatjets_request"].Integral())
legend15.Draw()

c15.cd(3)
ROOT.gPad.SetLogy()

dict_discr_hist2['QCD_ph2']['genjet_request'].Draw("HIST")
dict_discr_hist2['QCD_ph2']['genjet_request'].SetTitle("request on GenJetAK8_pt; Discriminator Jet2; Events")
#dict_discr_hist2['QCD_ph2']["genjet_request"].SetLineWidth(2)
dict_discr_hist2['QCD_ph2']['genjet_request'].SetLineColor(ROOT.kCyan)
dict_discr_hist2['QCD_ph2']["genjet_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist2['QCD_ph2']["genjet_request"].Scale(1 / dict_discr_hist2['QCD_ph2']["genjet_request"].Integral())

dict_discr_hist2['signal_ph2']['genjet_request'].Draw("SAME HIST")
dict_discr_hist2['signal_ph2']['genjet_request'].SetLineWidth(2)
dict_discr_hist2['signal_ph2']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_ph2']["genjet_request"].Scale(1 / dict_discr_hist2['signal_ph2']["genjet_request"].Integral())
legend15.Draw()

c15.cd(4)
ROOT.gPad.SetLogy()

dict_discr_hist2['QCD_ph2']['pt_window'].Draw("HIST")
dict_discr_hist2['QCD_ph2']['pt_window'].SetTitle("Pt window; Discriminator Jet2; Events")
#dict_discr_hist2['QCD_ph2']["pt_window"].SetLineWidth(2)
dict_discr_hist2['QCD_ph2']['pt_window'].SetLineColor(ROOT.kCyan)
dict_discr_hist2['QCD_ph2']["pt_window"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist2['QCD_ph2']["pt_window"].Scale(1 / dict_discr_hist2['QCD_ph2']["pt_window"].Integral())

dict_discr_hist2['signal_ph2']['pt_window'].Draw("SAME HIST")
dict_discr_hist2['signal_ph2']['pt_window'].SetLineWidth(2)
dict_discr_hist2['signal_ph2']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_ph2']["pt_window"].Scale(1 / dict_discr_hist2['signal_ph2']["pt_window"].Integral())
legend15.Draw()

c15.cd(5)
ROOT.gPad.SetLogy()

dict_discr_hist2['QCD_ph2']['eta_cut'].Draw("HIST")
dict_discr_hist2['QCD_ph2']['eta_cut'].SetTitle("Eta cut; Discriminator Jet2; Events")
#dict_discr_hist2['QCD_ph2']["eta_cut"].SetLineWidth(2)
dict_discr_hist2['QCD_ph2']['eta_cut'].SetLineColor(ROOT.kCyan)
dict_discr_hist2['QCD_ph2']["eta_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_discr_hist2['QCD_ph2']["eta_cut"].Scale(1 / dict_discr_hist2['QCD_ph2']["eta_cut"].Integral())

dict_discr_hist2['signal_ph2']['eta_cut'].Draw("SAME HIST")
dict_discr_hist2['signal_ph2']['eta_cut'].SetLineWidth(2)
dict_discr_hist2['signal_ph2']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_discr_hist2['signal_ph2']["eta_cut"].Scale(1 / dict_discr_hist2['signal_ph2']["eta_cut"].Integral())
legend15.Draw()



#! phase 2 SOFTDROP, ALL JETS

c16 = ROOT.TCanvas("c16", "Discriminator histograms for phase 2 softdrop, all jets", 1500, 1000)

c16.Divide(4,2)

c16.cd(1)

dict_softdrop_hist_tot['QCD_ph2']['no_cut'].Draw("HIST")
dict_softdrop_hist_tot['QCD_ph2']['no_cut'].SetTitle("No Cut; Softdrop mass, all jets; Events")
#dict_softdrop_hist_tot['QCD_ph2']["no_cut"].SetLineWidth(2)
dict_softdrop_hist_tot['QCD_ph2']['no_cut'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist_tot['QCD_ph2']["no_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist_tot['QCD_ph2']["no_cut"].Scale(1 / dict_softdrop_hist_tot['QCD_ph2']["no_cut"].Integral())

dict_softdrop_hist_tot['signal_ph2']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_ph2']['no_cut'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_ph2']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_ph2']["no_cut"].Scale(1 / dict_softdrop_hist_tot['signal_ph2']["no_cut"].Integral())

legend16 = ROOT.TLegend(0.52, 0.70, 0.85, 0.88)
legend16.SetHeader("Phase2 fullsim", "C")
legend16.AddEntry(dict_softdrop_hist_tot['QCD_ph2']['no_cut'], "QCD", "f")
legend16.AddEntry(dict_softdrop_hist_tot['signal_full']['no_cut'], "signal", "l")
legend16.Draw()

c16.cd(2)

dict_softdrop_hist_tot['QCD_ph2']['nfatjets_request'].Draw("HIST")
dict_softdrop_hist_tot['QCD_ph2']['nfatjets_request'].SetTitle("request on nFatJet; Softdrop mass, all jets; Events ")
#dict_softdrop_hist_tot['QCD_ph2']["nfatjets_request"].SetLineWidth(2)
dict_softdrop_hist_tot['QCD_ph2']['nfatjets_request'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist_tot['QCD_ph2']["nfatjets_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist_tot['QCD_ph2']["nfatjets_request"].Scale(1 / dict_softdrop_hist_tot['QCD_ph2']["nfatjets_request"].Integral())

dict_softdrop_hist_tot['signal_ph2']['nfatjets_request'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_ph2']['nfatjets_request'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_ph2']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_ph2']["nfatjets_request"].Scale(1 / dict_softdrop_hist_tot['signal_ph2']["nfatjets_request"].Integral())
legend16.Draw()

c16.cd(3)

dict_softdrop_hist_tot['QCD_ph2']['genjet_request'].Draw("HIST")
dict_softdrop_hist_tot['QCD_ph2']['genjet_request'].SetTitle("request on GenJetAK8_pt; Softdrop mass, all jets; Events")
#dict_softdrop_hist_tot['QCD_ph2']["genjet_request"].SetLineWidth(2)
dict_softdrop_hist_tot['QCD_ph2']['genjet_request'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist_tot['QCD_ph2']["genjet_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist_tot['QCD_ph2']["genjet_request"].Scale(1 / dict_softdrop_hist_tot['QCD_ph2']["genjet_request"].Integral())

dict_softdrop_hist_tot['signal_ph2']['genjet_request'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_ph2']['genjet_request'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_ph2']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_ph2']["genjet_request"].Scale(1 / dict_softdrop_hist_tot['signal_ph2']["genjet_request"].Integral())
legend16.Draw()

c16.cd(4)

dict_softdrop_hist_tot['QCD_ph2']['pt_window'].Draw("HIST")
dict_softdrop_hist_tot['QCD_ph2']['pt_window'].SetTitle("Pt window; Softdrop mass, all jets; Events")
#dict_softdrop_hist_tot['QCD_ph2']["pt_window"].SetLineWidth(2)
dict_softdrop_hist_tot['QCD_ph2']['pt_window'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist_tot['QCD_ph2']["pt_window"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist_tot['QCD_ph2']["pt_window"].Scale(1 / dict_softdrop_hist_tot['QCD_ph2']["pt_window"].Integral())

dict_softdrop_hist_tot['signal_ph2']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_ph2']['pt_window'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_ph2']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_ph2']["pt_window"].Scale(1 / dict_softdrop_hist_tot['signal_ph2']["pt_window"].Integral())
legend16.Draw()

c16.cd(5)

dict_softdrop_hist_tot['QCD_ph2']['eta_cut'].Draw("HIST")
dict_softdrop_hist_tot['QCD_ph2']['eta_cut'].SetTitle("Eta cut; Softdrop mass, all jets; Events")
#dict_softdrop_hist_tot['QCD_ph2']["eta_cut"].SetLineWidth(2)
dict_softdrop_hist_tot['QCD_ph2']['eta_cut'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist_tot['QCD_ph2']["eta_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist_tot['QCD_ph2']["eta_cut"].Scale(1 / dict_softdrop_hist_tot['QCD_ph2']["eta_cut"].Integral())

dict_softdrop_hist_tot['signal_ph2']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist_tot['signal_ph2']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist_tot['signal_ph2']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist_tot['signal_ph2']["eta_cut"].Scale(1 / dict_softdrop_hist_tot['signal_ph2']["eta_cut"].Integral())
legend16.Draw()

#! phase 2 softdrop SOFTDROP, JET 1

c17 = ROOT.TCanvas("c17", "Softdrop histograms for phase 2 softdrop, jet 1", 1500, 1000)

c17.Divide(4,2)

c17.cd(1)

dict_softdrop_hist1['QCD_ph2']['no_cut'].Draw("HIST")
dict_softdrop_hist1['QCD_ph2']['no_cut'].SetTitle("No Cut; Softdrop mass Jet1; Events")
#dict_softdrop_hist1['QCD_ph2']["no_cut"].SetLineWidth(2)
dict_softdrop_hist1['QCD_ph2']['no_cut'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist1['QCD_ph2']["no_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist1['QCD_ph2']["no_cut"].Scale(1 / dict_softdrop_hist1['QCD_ph2']["no_cut"].Integral())

dict_softdrop_hist1['signal_ph2']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist1['signal_ph2']['no_cut'].SetLineWidth(2)
dict_softdrop_hist1['signal_ph2']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_ph2']["no_cut"].Scale(1 / dict_softdrop_hist1['signal_ph2']["no_cut"].Integral())

legend17 = ROOT.TLegend(0.52, 0.70, 0.85, 0.88)
legend17.SetHeader("Phase2 fullsim", "C")
legend17.AddEntry(dict_softdrop_hist1['QCD_ph2']['no_cut'], "QCD", "f")
legend17.AddEntry(dict_softdrop_hist1['signal_full']['no_cut'], "signal", "l")
legend17.Draw()

c17.cd(2)

dict_softdrop_hist1['QCD_ph2']['nfatjets_request'].Draw("HIST")
dict_softdrop_hist1['QCD_ph2']['nfatjets_request'].SetTitle("request on nFatJet; Softdrop mass Jet1; Events ")
#dict_softdrop_hist1['QCD_ph2']["nfatjets_request"].SetLineWidth(2)
dict_softdrop_hist1['QCD_ph2']['nfatjets_request'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist1['QCD_ph2']["nfatjets_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist1['QCD_ph2']["nfatjets_request"].Scale(1 / dict_softdrop_hist1['QCD_ph2']["nfatjets_request"].Integral())

dict_softdrop_hist1['signal_ph2']['nfatjets_request'].Draw("SAME HIST")
dict_softdrop_hist1['signal_ph2']['nfatjets_request'].SetLineWidth(2)
dict_softdrop_hist1['signal_ph2']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_ph2']["nfatjets_request"].Scale(1 / dict_softdrop_hist1['signal_ph2']["nfatjets_request"].Integral())
legend17.Draw()

c17.cd(3)

dict_softdrop_hist1['QCD_ph2']['genjet_request'].Draw("HIST")
dict_softdrop_hist1['QCD_ph2']['genjet_request'].SetTitle("request on GenJetAK8_pt; Softdrop mass Jet1; Events")
#dict_softdrop_hist1['QCD_ph2']["genjet_request"].SetLineWidth(2)
dict_softdrop_hist1['QCD_ph2']['genjet_request'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist1['QCD_ph2']["genjet_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist1['QCD_ph2']["genjet_request"].Scale(1 / dict_softdrop_hist1['QCD_ph2']["genjet_request"].Integral())

dict_softdrop_hist1['signal_ph2']['genjet_request'].Draw("SAME HIST")
dict_softdrop_hist1['signal_ph2']['genjet_request'].SetLineWidth(2)
dict_softdrop_hist1['signal_ph2']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_ph2']["genjet_request"].Scale(1 / dict_softdrop_hist1['signal_ph2']["genjet_request"].Integral())
legend17.Draw()

c17.cd(4)

dict_softdrop_hist1['QCD_ph2']['pt_window'].Draw("HIST")
dict_softdrop_hist1['QCD_ph2']['pt_window'].SetTitle("Pt window; Softdrop mass Jet1; Events")
#dict_softdrop_hist1['QCD_ph2']["pt_window"].SetLineWidth(2)
dict_softdrop_hist1['QCD_ph2']['pt_window'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist1['QCD_ph2']["pt_window"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist1['QCD_ph2']["pt_window"].Scale(1 / dict_softdrop_hist1['QCD_ph2']["pt_window"].Integral())

dict_softdrop_hist1['signal_ph2']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist1['signal_ph2']['pt_window'].SetLineWidth(2)
dict_softdrop_hist1['signal_ph2']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_ph2']["pt_window"].Scale(1 / dict_softdrop_hist1['signal_ph2']["pt_window"].Integral())
legend17.Draw()

c17.cd(5)

dict_softdrop_hist1['QCD_ph2']['eta_cut'].Draw("HIST")
dict_softdrop_hist1['QCD_ph2']['eta_cut'].SetTitle("Eta cut; Softdrop mass Jet1; Events")
#dict_softdrop_hist1['QCD_ph2']["eta_cut"].SetLineWidth(2)
dict_softdrop_hist1['QCD_ph2']['eta_cut'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist1['QCD_ph2']["eta_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist1['QCD_ph2']["eta_cut"].Scale(1 / dict_softdrop_hist1['QCD_ph2']["eta_cut"].Integral())

dict_softdrop_hist1['signal_ph2']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist1['signal_ph2']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist1['signal_ph2']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist1['signal_ph2']["eta_cut"].Scale(1 / dict_softdrop_hist1['signal_ph2']["eta_cut"].Integral())
legend17.Draw()

#! phase 2 SOFTDROP, JET 2

c18 = ROOT.TCanvas("c18", "Discriminator histograms for phase 2 softdrop, jet 2", 1500, 1000)

c18.Divide(4,2)

c18.cd(1)

dict_softdrop_hist2['QCD_ph2']['no_cut'].Draw("HIST")
dict_softdrop_hist2['QCD_ph2']['no_cut'].SetTitle("No Cut; Softdrop mass Jet2; Events")
#dict_softdrop_hist2['QCD_ph2']["no_cut"].SetLineWidth(2)
dict_softdrop_hist2['QCD_ph2']['no_cut'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist2['QCD_ph2']["no_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist2['QCD_ph2']["no_cut"].Scale(1 / dict_softdrop_hist2['QCD_ph2']["no_cut"].Integral())

dict_softdrop_hist2['signal_ph2']['no_cut'].Draw("SAME HIST")
dict_softdrop_hist2['signal_ph2']['no_cut'].SetLineWidth(2)
dict_softdrop_hist2['signal_ph2']['no_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_ph2']["no_cut"].Scale(1 / dict_softdrop_hist2['signal_ph2']["no_cut"].Integral())

legend18 = ROOT.TLegend(0.52, 0.70, 0.85, 0.88)
legend18.SetHeader("Phase2 fullsim", "C")
legend18.AddEntry(dict_softdrop_hist2['QCD_ph2']['no_cut'], "QCD", "f")
legend18.AddEntry(dict_softdrop_hist2['signal_full']['no_cut'], "signal", "l")
legend18.Draw()

c18.cd(2)

dict_softdrop_hist2['QCD_ph2']['nfatjets_request'].Draw("HIST")
dict_softdrop_hist2['QCD_ph2']['nfatjets_request'].SetTitle("request on nFatJet; Softdrop mass Jet2; Events ")
#dict_softdrop_hist2['QCD_ph2']["nfatjets_request"].SetLineWidth(2)
dict_softdrop_hist2['QCD_ph2']['nfatjets_request'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist2['QCD_ph2']["nfatjets_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist2['QCD_ph2']["nfatjets_request"].Scale(1 / dict_softdrop_hist2['QCD_ph2']["nfatjets_request"].Integral())

dict_softdrop_hist2['signal_ph2']['nfatjets_request'].Draw("SAME HIST")
dict_softdrop_hist2['signal_ph2']['nfatjets_request'].SetLineWidth(2)
dict_softdrop_hist2['signal_ph2']['nfatjets_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_ph2']["nfatjets_request"].Scale(1 / dict_softdrop_hist2['signal_ph2']["nfatjets_request"].Integral())
legend18.Draw()

c18.cd(3)

dict_softdrop_hist2['QCD_ph2']['genjet_request'].Draw("HIST")
dict_softdrop_hist2['QCD_ph2']['genjet_request'].SetTitle("request on GenJetAK8_pt; Softdrop mass Jet2; Events")
#dict_softdrop_hist2['QCD_ph2']["genjet_request"].SetLineWidth(2)
dict_softdrop_hist2['QCD_ph2']['genjet_request'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist2['QCD_ph2']["genjet_request"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist2['QCD_ph2']["genjet_request"].Scale(1 / dict_softdrop_hist2['QCD_ph2']["genjet_request"].Integral())

dict_softdrop_hist2['signal_ph2']['genjet_request'].Draw("SAME HIST")
dict_softdrop_hist2['signal_ph2']['genjet_request'].SetLineWidth(2)
dict_softdrop_hist2['signal_ph2']['genjet_request'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_ph2']["genjet_request"].Scale(1 / dict_softdrop_hist2['signal_ph2']["genjet_request"].Integral())
legend18.Draw()

c18.cd(4)

dict_softdrop_hist2['QCD_ph2']['pt_window'].Draw("HIST")
dict_softdrop_hist2['QCD_ph2']['pt_window'].SetTitle("Pt window; Softdrop mass Jet2; Events")
#dict_softdrop_hist2['QCD_ph2']["pt_window"].SetLineWidth(2)
dict_softdrop_hist2['QCD_ph2']['pt_window'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist2['QCD_ph2']["pt_window"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist2['QCD_ph2']["pt_window"].Scale(1 / dict_softdrop_hist2['QCD_ph2']["pt_window"].Integral())

dict_softdrop_hist2['signal_ph2']['pt_window'].Draw("SAME HIST")
dict_softdrop_hist2['signal_ph2']['pt_window'].SetLineWidth(2)
dict_softdrop_hist2['signal_ph2']['pt_window'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_ph2']["pt_window"].Scale(1 / dict_softdrop_hist2['signal_ph2']["pt_window"].Integral())
legend18.Draw()

c18.cd(5)

dict_softdrop_hist2['QCD_ph2']['eta_cut'].Draw("HIST")
dict_softdrop_hist2['QCD_ph2']['eta_cut'].SetTitle("Eta cut; Softdrop mass Jet2; Events")
#dict_softdrop_hist2['QCD_ph2']["eta_cut"].SetLineWidth(2)
dict_softdrop_hist2['QCD_ph2']['eta_cut'].SetLineColor(ROOT.kCyan)
dict_softdrop_hist2['QCD_ph2']["eta_cut"].SetFillColorAlpha(ROOT.kCyan - 6, 0.8)
dict_softdrop_hist2['QCD_ph2']["eta_cut"].Scale(1 / dict_softdrop_hist2['QCD_ph2']["eta_cut"].Integral())

dict_softdrop_hist2['signal_ph2']['eta_cut'].Draw("SAME HIST")
dict_softdrop_hist2['signal_ph2']['eta_cut'].SetLineWidth(2)
dict_softdrop_hist2['signal_ph2']['eta_cut'].SetLineColor(ROOT.kRed + 2)
dict_softdrop_hist2['signal_ph2']["eta_cut"].Scale(1 / dict_softdrop_hist2['signal_ph2']["eta_cut"].Integral())
legend18.Draw()



c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_full_alljets.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_full_jet1.pdf")
c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_full_jet2.pdf")

c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_full_alljets.pdf")
c5.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_full_jet1.pdf")
c6.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_full_jet2.pdf")

c7.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_flash_alljets.pdf")
c8.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_flash_jet1.pdf")
c9.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_flash_jet2.pdf")

c10.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_flash_alljets.pdf")
c11.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_flash_jet1.pdf")
c12.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_flash_jet2.pdf")


c13.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_ph2_alljets.pdf")
c14.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_ph2_jet1.pdf")
c15.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/discr_ph2_jet2.pdf")

c16.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_ph2_alljets.pdf")
c17.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_ph2_jet1.pdf")
c18.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_analysis_complete/softdrop_ph2_jet2.pdf")

