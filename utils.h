#ifndef UTILS_ANALYSIS
#define UTILS_ANALYSIS



auto invariant_mass(const float &pt_1, const float &eta_1, const float &phi_1, const float &mass_1, const float &pt_2, const float &eta_2, const float &phi_2, const float &mass_2){

    ROOT::Math::PtEtaPhiMVector v1(pt_1, eta_1, phi_1, mass_1);
    ROOT::Math::PtEtaPhiMVector v2(pt_2, eta_2, phi_2, mass_2);
    double inv_mass = (v1 + v2).M();

    return inv_mass;

}

auto delta_R(const float &jet1_eta, const float &jet1_phi, const float &jet2_eta, const float &jet2_phi){

        Double_t deta = jet1_eta - jet2_eta;
        Double_t dphi = TVector2::Phi_mpi_pi(jet1_phi - jet2_phi);

        float dr = TMath::Sqrt(deta * deta + dphi * dphi);
    
    return dr;
}


ROOT::VecOps::RVec<int> lepton_matching_index(ROOT::VecOps::RVec<float> &fatjet_eta, ROOT::VecOps::RVec<float> &fatjet_phi, ROOT::VecOps::RVec<float> &lepton_eta, ROOT::VecOps::RVec<float> &lepton_phi){

    int n_fatjets = fatjet_eta.size();
    int n_leptons = lepton_eta.size();

    ROOT::VecOps::RVec<int> matching_index(n_fatjets);

    float dr = 0.8;

    for(int i=0; i<n_fatjets; i ++){
        auto dr_max = dr;
        matching_index[i] = -1;
        for(int j=0; j<n_leptons; j++){
            auto temp_dr = delta_R(fatjet_eta[i], fatjet_phi[i], lepton_eta[j], lepton_phi[j]);
            if(temp_dr<dr_max){
                dr_max = temp_dr;
                matching_index[i] = j;
            }

        }
    }

    return matching_index;

}


ROOT::VecOps::RVec<bool> fatjet_lepton_isolation(ROOT::VecOps::RVec<float> &fatjet_eta, ROOT::VecOps::RVec<float> &fatjet_phi, ROOT::VecOps::RVec<float> &lepton_pt, ROOT::VecOps::RVec<float> &lepton_eta, ROOT::VecOps::RVec<float> &lepton_phi, ROOT::VecOps::RVec<float> &rel_iso, const int &type){

    ROOT::VecOps::RVec<int> matching_index = lepton_matching_index(fatjet_eta, fatjet_phi, lepton_eta, lepton_phi);

    int n_fatjets = fatjet_eta.size();

    ROOT::VecOps::RVec<bool> fatjet_isolation(n_fatjets);

    for(int i =0; i < n_fatjets; i++){

        if(matching_index[i] == -1)
            fatjet_isolation[i] = true;

        else if(type == 13) {
            int j = matching_index[i];
            if(lepton_pt[j]> 50 && abs(lepton_eta[j]) < 2.4 && rel_iso[j]<0.2)
                fatjet_isolation[i] = false;
            else
                fatjet_isolation[i] = true;

        }
        else if(type == 11) {
            int k = matching_index[i];
            if(lepton_pt[k]> 50 && abs(lepton_eta[k]) < 2.5 && rel_iso[k]<0.2)
                fatjet_isolation[i] = false;
            else
                fatjet_isolation[i] = true;

        }


    }

    return fatjet_isolation;

}


ROOT::VecOps::RVec<bool> jet_isolation(ROOT::VecOps::RVec<float> &jet_eta, ROOT::VecOps::RVec<float> &jet_phi, ROOT::VecOps::RVec<float> &fatjet_eta, ROOT::VecOps::RVec<float> &fatjet_phi){

    int n_jets = jet_eta.size();
    int n_fatjets = fatjet_eta.size();

    ROOT::VecOps::RVec<bool> jet_mask(n_jets);

    for(int i = 0; i <n_jets; i ++){
    
        jet_mask[i] = true;

        for(int j=0; j< n_fatjets; j++){
            auto dr  = delta_R(jet_eta[i], jet_phi[i], fatjet_eta[j], fatjet_phi[j]);

            if (dr<1.2) {

                jet_mask[i] = false;
                break;
            }
        }     
    }
    return jet_mask;
}





ROOT::VecOps::RVec<bool>  part_isolation(ROOT::VecOps::RVec<float> &jet_eta, ROOT::VecOps::RVec<float> &jet_phi,  ROOT::VecOps::RVec<float> &muon_eta, ROOT::VecOps::RVec<float> &muon_phi, ROOT::VecOps::RVec<float> &el_eta, ROOT::VecOps::RVec<float> &el_phi){

    int n_jets = jet_eta.size();
    int n_muons = muon_eta.size();
    int n_el = el_eta.size();   

    ROOT::VecOps::RVec<bool> res (n_jets);
    
    for(int i = 0; i< n_jets; i ++){
        if(n_muons== 0 && n_el ==0){
                res[i] = false;
            }
        else{
            for(int j=0; j<n_muons; j++){
                if (delta_R(jet_eta[i], jet_phi[i], muon_eta[j], muon_phi[j])<0.4)
                    res[i] = false;
                else
                    res[i]= true;             
                }
            for(int k=0; k<n_el; k++){
                if (delta_R(jet_eta[i], jet_phi[i], el_eta[k], el_phi[k])<0.4)
                    res[i] = false;
                else
                    res[i] = true;
                }
            }
        }
    
    return res;
}

ROOT::VecOps::RVec<bool> gen_jet_pt_checker(ROOT::VecOps::RVec<float> fatjet_pt, ROOT::VecOps::RVec<float> gen_pt,  ROOT::VecOps::RVec<int> matching_index) {

    int n_fatjets = fatjet_pt.size();
    int n_genjets = gen_pt.size();

    ROOT::VecOps::RVec<bool> res (n_fatjets);

    for(int i =0;i<n_fatjets;i++){
        int current_index = matching_index[i];
        if(current_index == -1)
            res[i] = false;
        else{
            if(gen_pt[current_index]>=250)
            res[i] = true;
            else
            res[i] = false;
        }
    }
    return res;
}



#endif