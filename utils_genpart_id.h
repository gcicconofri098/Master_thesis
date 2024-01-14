#ifndef UTILS_MASS_DECORRELATION
#define UTILS_MASS_DECORRELATION

#include <iostream>


auto delta_R(const float &jet1_eta, const float &jet1_phi, const float &jet2_eta, const float &jet2_phi)
{

    Double_t deta = jet1_eta - jet2_eta;
    Double_t dphi = TVector2::Phi_mpi_pi(jet1_phi - jet2_phi);

    float dr = TMath::Sqrt(deta * deta + dphi * dphi);

    return dr;
}

ROOT::VecOps::RVec<int> closest_genpart_id(ROOT::VecOps::RVec<float> &genpart_eta, ROOT::VecOps::RVec<float> &genpart_phi, ROOT::VecOps::RVec<int> &genpart_id, ROOT::VecOps::RVec<float> &genjetAK8_eta, ROOT::VecOps::RVec<float> &genjetAK8_phi)
{

    int genpart_size = genpart_eta.size();
    int genjet_size = genjetAK8_eta.size();

    ROOT::VecOps::RVec<int> is_h_within_0_8(genjet_size);

    for (int i = 0; i < genjet_size; i++)
    {
        float dr_0 = 0.8;
        is_h_within_0_8[i] = 0;

        for (int j = 0; j < genpart_size; j++)
        {
            float dr = delta_R(genjetAK8_eta[i], genjetAK8_phi[i], genpart_eta[j], genpart_phi[j]);
            if (dr < dr_0 && genpart_id[j] ==25)
            is_h_within_0_8[i] = 1;

        }
    }

    return is_h_within_0_8;
}



ROOT::VecOps::RVec<float> higgs_distance(ROOT::VecOps::RVec<float> &genpart_eta, ROOT::VecOps::RVec<float> &genpart_phi, ROOT::VecOps::RVec<float> &genpart_pt, ROOT::VecOps::RVec<int> &genpart_id, ROOT::VecOps::RVec<float> &genjetAK8_eta, ROOT::VecOps::RVec<float> &genjetAK8_phi, ROOT::VecOps::RVec<float> &genjetAK8_pt, ROOT::VecOps::RVec<float> &genjetAK8_mass)
{

    int genpart_size = genpart_eta.size();
    int genjet_size = genjetAK8_eta.size();

    
    ROOT::VecOps::RVec<float> res;
    for (int i = 0; i < genjet_size; i++)
    {
        //std::cout << "printing info on jet: " << i << std::endl;
        //std::cout << "pt is: " << genjetAK8_pt[i] << std::endl;
        //std::cout << "eta is: " << genjetAK8_eta[i] << std::endl;
        //std::cout << "phi is: " << genjetAK8_phi[i] << std::endl;
        //std::cout << "mass is: " << genjetAK8_mass[i] << std::endl;



        ROOT::VecOps::RVec<float> higgs_deltaR;
        for (int j = 0; j < genpart_size; j++){
            if (genpart_id[j] ==25){
                //if(i==0){
                //std::cout << "printing info on genpart: " << j << std::endl;
                //std::cout << "pt is: " << genpart_pt[j] << std::endl;
                //std::cout << "eta is: " << genpart_eta[j] << std::endl;
                //std::cout << "phi is: " << genpart_phi[j] << std::endl;  
        //}
                float dr = delta_R(genjetAK8_eta[i], genjetAK8_phi[i], genpart_eta[j], genpart_phi[j]);
                //std::cout << "Delta R is: " << dr << std::endl;
                higgs_deltaR.push_back(dr);
            }
        
        }
        float min_dr=ROOT::VecOps::Min(higgs_deltaR);

        std::cout << min_dr << std::endl;

        if (min_dr==0){
            min_dr=-1;
        }
        res.push_back(min_dr);
    }

    //std::cout << "finishing the evaluation"<< std::endl;
    
    return res;
}

#endif
