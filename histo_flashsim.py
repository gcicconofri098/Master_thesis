import ROOT
from decimal import *

ROOT.EnableImplicitMT()

getcontext().prec = 2

ROOT.gStyle.SetPaintTextFormat("1.3f")

integrated_luminosity = 59830

weights = {
    "QCD6": 1207 * integrated_luminosity,
    "QCD7": 119.9 * integrated_luminosity,
    "QCD8": 25.24 * integrated_luminosity,
    "signal": 0.01053 * integrated_luminosity,
}

h1= {}
h2= {}
h_tot = {}

histo_file = ROOT.TFile.Open("histograms_for_analysis_flashsim_discr_pres_0_83.root", "READ")


h1["QCD6"] = histo_file.Get("h1_QCD6")
h1["QCD7"] = histo_file.Get("h1_QCD7")
h1["QCD8"] = histo_file.Get("h1_QCD8")
h1['signal'] = histo_file.Get("h1_signal")

h2["QCD6"] = histo_file.Get("h2_QCD6")
h2["QCD7"] = histo_file.Get("h2_QCD7")
h2["QCD8"] = histo_file.Get("h2_QCD8")
h2['signal'] = histo_file.Get("h2_signal")

h2_2_signal = histo_file.Get("h2_2_signal")

print("entries", h2_2_signal.GetEntries())


processes = list(h1.keys())


for i in processes:
    #* the value to normalize at the same integrated luminosity of the AN is 2.27
    #print(type(h1[i]))
    h1[i].Scale(weights[i]*2.27)
    h2[i].Scale(weights[i]*2.27)

h2_2_signal.Scale(weights['signal']*2.27)

preselection_signal = 71.98 *2.27
print(preselection_signal)

hist_QCD = h1["QCD6"].Clone()
hist_QCD.Add(h1["QCD7"])
hist_QCD.Add(h1["QCD8"])

hist_QCD_2 = h1["QCD6"].Clone()
hist_QCD_2.Add(h1["QCD7"])
hist_QCD_2.Add(h1["QCD8"])


hist_2 = h2_2_signal.Clone()
hist_2.Reset()



#TODO JET1 

c1 = ROOT.TCanvas("c1", "Stacked contributions for jet1 after preselection", 800, 700)

legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)



hist_QCD.Draw("HIST")
hist_QCD.SetTitle("Distribution of Jet1 discriminator; Softdrop; Events")
# hist_QCD.SetLineColor(ROOT.kBlue+1)
hist_QCD.SetFillColorAlpha(ROOT.kAzure + 6, 0.8)
legend.AddEntry(hist_QCD, "QCD", "f")


h1['signal'].Draw("SAME HIST")
h1['signal'].SetLineColor(ROOT.kRed+4)
h1['signal'].Scale(10000)
legend.AddEntry(h1['signal'], "signal x 10000", "l")

legend.Draw()

#TODO JET2


c2 = ROOT.TCanvas("c2", "Stacked contributions for jet1 after preselection", 800, 700)

legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)



hist_QCD_2.Draw("HIST")
hist_QCD_2.SetTitle("Distribution of Jet2 discriminator; Softdrop mass; Events")
# hist_QCD_2.SetLineColor(ROOT.kBlue+1)
hist_QCD_2.SetFillColorAlpha(ROOT.kAzure + 6, 0.8)
legend2.AddEntry(hist_QCD_2, "QCD", "f")


h2['signal'].Draw("SAME HIST")
h2['signal'].SetLineColor(ROOT.kRed+4)
h2['signal'].Scale(10000)

legend2.AddEntry(h2['signal'], "signal x 10000", "l")

legend2.Draw()

#TODO EFFICIENCY MAP

for binx in reversed(range(1, 16)):
    for biny in reversed(range(1, 16)):
        if binx >= biny:
            stacked_sig = h2_2_signal.Integral(binx, 15, biny, 15)
            print("stacked signal: ", stacked_sig)

            if stacked_sig > 0:
                new_bin_cont = Decimal(stacked_sig) / Decimal(preselection_signal)
                temp = Decimal(new_bin_cont)
                print(temp)
                hist_2.SetBinContent(binx, biny, temp)
            else:
                hist_2.SetBinContent(binx, biny, 0)


c3 = ROOT.TCanvas("c3", "plot", 4500, 3500)
c3.SetGrid()
h2_2_signal.Draw("text COLZ")
h2_2_signal.SetTitle("Distribution of signal for flashsim")
#h2_2['signal'].Scale(1/(h2_2['signal'].Integral()))


c4 = ROOT.TCanvas("c4", "Efficiency plot", 4500, 3500)
c4.SetGrid()
hist_2.Draw("text COLZ")
hist_2.SetTitle("Signal efficiency for flashsim")




c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/flashsim_stacked_QCD_jet1_softdrop_discr_0_73.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/flashsim_stacked_QCD_jet2_softdrop_discr_0_73.pdf")
c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/flashsim_discr_distr_discr_0_73.pdf")
c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/flashsim_efficiency_discr_0_73.pdf")
