#ifndef UTILS_MASS_DECORRELATION
#define UTILS_MASS_DECORRELATION

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

    ROOT::VecOps::RVec<int> closest_id(genpart_size);

    for (int i = 0; i < genjet_size; i++)
    {
        int closest_idx = 0;

        float dr_0 = delta_R(genjetAK8_eta[i], genjetAK8_phi[i], genpart_eta[0], genpart_phi[0]);

        for (int j = 0; j < genpart_size; j++)
        {
            float dr = delta_R(genjetAK8_eta[i], genjetAK8_phi[i], genpart_eta[j], genpart_phi[j]);
            if (dr < dr_0)
            {
                dr_0 = dr;
                closest_idx = j;
            }
        }
        if (genpart_id[closest_idx] == 25) 
            closest_id[i] = 1;
        else 
            closest_id[i] = 0;
    }

    return closest_id;
}

#endif
