#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RMath/Vector4D.hxx"
#include <string>
#include <vector>
#include <cmath>
#include <regex>
#include <unordered_map>
#include <iostream>
#include <fstream>
//normalisation of the events: we take the product between the integrated luminosity and the cross-section of the event, divided by the number of simulated events
/*
const float integrated_luminosity = 59830 //taken from the article, 2018 data




std::map<std::string events_weight = { //non so se questa cosa ha senso in questo modo
    {"QCD_HT100to200", 27990000/79857456 * integrated_luminosity},
    {"QCD_HT200to300", 1712000/61542214 * integrated_luminosity},
    {"QCD_HT300to500", 347700/56214199 * integrated_luminosity},
    {"QCD_HT500to700", 32100/61097673 * integrated_luminosity},
    {"QCD_HT700to1000", 6831/47314826 * integrated_luminosity},
    {"QCD_HT1000to1500", 1207/ 15230975 * integrated_luminosity},
    {"QCD_HT1500to2000", 119.9/11887406 * integrated_luminosity},
    {"QCD_HT2000toInf", 25.24/5710430 * integrated_luminosity},
    {"WJetsToQQ_HT400to600", 315.2/9335298* integrated_luminosity},
    {"WJetsToQQ_HT600to800", 68.58/13633226 * integrated_luminosity},
    {"WJetsToQQ_HT800toInf", 34.69/ 13581343 * integrated_luminosity},
    {"ZJetsToQQ_HT400to600", 145.3/13930474 * integrated_luminosity},
    {"ZJetsToQQ_HT600to800", 34.29/12029507 * integrated_luminosity},
    {"ZJetsToQQ_HT800toInf", 18.57/9681521 * integrated_luminosity},
    {"TTToHadronic", 370.04/334206000 * integrated_luminosity},
    {"TTToLeptonic", 369.49/476408000 * integrated_luminosity},
    {"ST_tW_antitop", 35.85/7749000 * integrated_luminosity},
    {"ST_tW_top", 35.85/7956000 * integrated_luminosity},
    {"ggHTobb", 9.60/14250000 *integrated_luminosity},
    {"VBFHTobb", 2.20/7598000 * integrated_luminosity},
    {"WminusH_HToBB", 0.331/9995915 * integrated_luminosity},
    {"WplusH_HToBB", 0.210/9513933 * integrated_luminosity},
    {"ZH_HToBB", 0.310/9989262 * integrated_luminosity},
    {"ggZH_HToBB", 0.050/4928000 * integrated_luminosity},
    {"WW_TuneCP5", 118.7/15679000 * integrated_luminosity},
    {"WZ_TuneCP5", 47.2/7940000 * integrated_luminosity},
    {"ZZ_TuneCP5", 16.52/3526000 * integrated_luminosity},
    {"GluGluHHTo4B", 10.53/400000 *integrated_luminosity}
}
*/

auto rdata_creator(){

    ROOT::RDataFrame QCD1("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/60000/01CD88A2-878C-6446-9D9C-70BFF7D9E19C.root", {"Events"});

    ROOT::RDataFrame QCD2("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2830000/01597A4E-6C68-B94C-90AA-45D8FAAB3E1E.root", {"Events"});

    ROOT::RDataFrame QCD3("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2820000/0BADC302-9E0D-D04B-B1AC-537CC5540912.root", {"Events"});

    ROOT::RDataFrame QCD4("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2820000/018FEA95-9E8E-214A-A020-7F55DC78B203.root", {"Events"});

    ROOT::RDataFrame QCD5("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2820000/150F2AD2-0267-AE4F-90F9-D8191F29DC95.root", {"Events"});

    ROOT::RDataFrame QCD6("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2820000/723E5B2D-0AF1-0D44-9D3F-3CE358680F9D.root", {"Events"});

    ROOT::RDataFrame QCD7("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2820000/4BFB898A-D75F-424E-9796-39C2DB42F6F2.root", {"Events"});

    ROOT::RDataFrame QCD8("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2820000/43A4A5EB-37B1-CA49-AF30-752C43FC828F.root", {"Events"});

    ROOT::RDataFrame WJets1("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/WJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/100000/3233BD62-0A6C-1A4B-BB9B-14CC03C2AE1D.root", {"Events"});

    ROOT::RDataFrame WJets2("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/WJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/100000/04CF847A-DA06-4849-82F3-34F4A86B4241.root", {"Events"});

    ROOT::RDataFrame WJets3("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2550000/0760B6BD-F18E-084D-8E42-AD9F8A467F71.root", {"Events"});

    ROOT::RDataFrame ZJets1("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2550000/B4FB8465-14B1-0449-9C14-DD2CD637D2DE.root", {"Events"});

    ROOT::RDataFrame ZJets2("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2540000/22CD330D-3CD3-C642-923B-18EA67086FE3.root", {"Events"});

    ROOT::RDataFrame ZJets3("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/30000/05B8CD6E-B303-A544-A285-5F2FFB47D5DC.root", {"Events"});

    ROOT::RDataFrame TTHad("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/130000/0307C1DA-E49C-AB4B-9179-C70BE232321E.root", {"Events"});

    ROOT::RDataFrame TTSemilept("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/120000/0520A050-AF68-EF43-AA5B-5AA77C74ED73.root", {"Events"});

    ROOT::RDataFrame ST_tw_antitop("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/230000/6371B801-DE75-5B4B-A781-98523A058E30.root", {"Events"});

    ROOT::RDataFrame ST_tw_top("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/100000/60FB6FDE-25EA-6C4E-80E5-96ED7EF8C294.root", {"Events"});

    ROOT::RDataFrame GGH("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/GluGluHToBB_M-125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/100000/010C2B15-1748-D34C-AE93-66E0864A2E54.root", {"Events"});

    ROOT::RDataFrame VBFH("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/VBFHToBB_M-125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/230000/04A5B8B1-C004-9247-97F8-EE9274C7DB51.root", {"Events"});

    ROOT::RDataFrame WMinusH("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/WminusH_HToBB_WToQQ_M-125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2820000/7A64C23A-88F1-3948-8DBE-5CC68396199B.root", {"Events"});

    ROOT::RDataFrame WPlusH("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/WplusH_HToBB_WToQQ_M-125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2830000/16EFFFE4-67DB-364F-90DD-A082DCF9CC81.root", {"Events"});

    ROOT::RDataFrame ZH("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/ZH_HToBB_ZToQQ_M-125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2820000/FC08EB31-9A28-0842-A01F-F6E482777701.root", {"Events"});

    ROOT::RDataFrame ggZH("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/ggZH_HToBB_ZToQQ_M-125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/50000/055A8936-10B9-D041-AD4C-4D8A3762F95E.root", {"Events"});

    ROOT::RDataFrame WW("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/WW_TuneCP5_13TeV-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/120000/A9859A3B-138E-0B45-A60E-A26B2E7CE4FD.root", {"Events"});

    ROOT::RDataFrame WZ("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/WZ_TuneCP5_13TeV-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/130000/0D38D325-67C1-2748-8678-C0C48FD151C4.root", {"Events"});

    ROOT::RDataFrame ZZ("root://xrd-cms-global.cern.ch///store/mc/RunIISummer20UL18NanoAODv9/ZZ_TuneCP5_13TeV-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/40000/29E7B7EF-D0FD-7343-9437-5C4F253A7B49.root", {"Events"});

    ROOT::RDataFrame signal("root://xrd-cms-global.cern.ch///store/mc/RunIIAutumn18NanoAODv5/GluGluToHHTo4B_node_SM_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NANOAODSIM/Nano1June2019_102X_upgrade2018_realistic_v19-v1/130000/4A33603E-8E8E-9C40-8086-C3345E752BE0.root", {"Events"});


    std::cout << "All dataframes created" <<std::endl;

    auto data_names = {"QCD1", "QCD2", "QCD3", "QCD4", "QCD5", "QCD6", "QCD7", "QCD8", "WJets1", "WJets2", "WJets3", "ZJets1", "ZJets2", "ZJets3", "TTHad", "TTSemilept", "ST_tw_antitop", "ST_tw_top", "GGH", "VBFH", "WMinusH", "WPlusH", "ZH", , "ggZH", "WW", "WZ", "ZZ", "signal"};

}


auto hist(rdata_names) {

    auto c1 = new TCanvas("c1", "Histogram", 800, 700);

    auto legend = new TLegend(0.62, 0.70, 0.82, 0.88);

    auto hs = new THStack("hs","Stacked 1D histograms");

    for(auto name : name_list){    
        if(name == signal){

            auto h2 = name.Histo1D({"Title","", 100, -4, 4}, "FatJet_msoftdrop");
            legend->AddEntry(h2, "name", "l");
        }
        auto h1 = name.Histo1D({"Title","", 100, -4, 4}, "FatJet_msoftdrop");

        hs->Add(h1);

        legend->AddEntry(h1, "name", "l");
    
    }

    hs->DrawClone();
    h2->Draw("SAME");
    legend->Draw("SAME");

}

int main() {

    ROOT::EnableImplicitMT();

    rdata_creator();

    event_selection(data_names);




}
