#ifndef UTILS_HAS_HIGGS_NBD
#define UTILS_HAS_HIGGS_NBD


auto has_H_within_0_8(ROOT::VecOps::RVec<float> &genpart_eta, ROOT::VecOps::RVec<float> &genpart_phi, ROOT::VecOps::RVec<int> &genpart_id, ROOT::VecOps::RVec<float> &genjetAK8_eta, ROOT::VecOps::RVec<float> &genjetAK8_phi){

    int genpart_size = genpart_eta.size();
    int genjet_size = genjetAK8_eta.size();

    ROOT::VecOps::RVec<int> is_h_within_0_8(genjet_size);

    for (int i = 0; i < genjet_size; i++)
    {
        float dr_0 = 0.8;
        is_h_within_0_8[i] = 0;

        for (int j = 0; j < genpart_size; j++)
        {
            Double_t deta = genjetAK8_eta[i] - genpart_eta[j];
            Double_t dphi = TVector2::Phi_mpi_pi(genjetAK8_phi[i] - genpart_phi[j]);
            float dr = TMath::Sqrt(deta * deta + dphi * dphi);
            if (dr < dr_0 && genpart_id[j] ==25)
            is_h_within_0_8[i] = 1;

        }
    }

    return is_h_within_0_8;
}

#endif