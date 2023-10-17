#ifndef UTILS_CALIBRATORS
#define UTILS_CALIBRATORS

auto calibrate_pt(
                const ROOT::VecOps::RVec<float> &AK8_eta,
                const ROOT::VecOps::RVec<float> &AK8_pt) {

        auto size_outer = AK8_eta.size();
        ROOT::VecOps::RVec<float> calibrated_pt (size_outer);

        for (int i = 0; i < size_outer; i++) {
            float scale = 1.0;
            float eta = AK8_eta[i];
            float pt = AK8_pt[i];
            if (fabs(eta) > 1.0 && fabs(eta) <= 0.8 && pt > 200.0 && pt <= 250.0) scale = 1.08;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 200.0 && pt <= 250.0) scale = 1.06;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 200.0 && pt <= 250.0) scale = 1.21;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 200.0 && pt <= 250.0) scale = 1.20;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 200.0 && pt <= 250.0) scale = 0.870;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 250.0 && pt <= 300.0) scale = 1.07;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 250.0 && pt <= 300.0) scale = 1.05;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 250.0 && pt <= 300.0) scale = 1.21;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 250.0 && pt <= 300.0) scale = 1.17;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 250.0 && pt <= 300.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 300.0 && pt <= 350.0) scale = 1.07;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 300.0 && pt <= 350.0) scale = 1.05;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 300.0 && pt <= 350.0) scale = 1.21;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 300.0 && pt <= 350.0) scale = 1.15;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 300.0 && pt <= 350.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 350.0 && pt <= 400.0) scale = 1.07;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 350.0 && pt <= 400.0) scale = 1.05;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 350.0 && pt <= 400.0) scale = 1.20;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 350.0 && pt <= 400.0) scale = 1.13;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 350.0 && pt <= 400.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 400.0 && pt <= 450.0) scale = 1.07;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 400.0 && pt <= 450.0) scale = 1.04;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 400.0 && pt <= 450.0) scale = 1.20;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 400.0 && pt <= 450.0) scale = 1.09;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 400.0 && pt <= 450.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 450.0 && pt <= 500.0) scale = 1.07;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 450.0 && pt <= 500.0) scale = 1.04;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 450.0 && pt <= 500.0) scale = 1.20;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 450.0 && pt <= 500.0) scale = 1.06;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 450.0 && pt <= 500.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 500.0 && pt <= 600.0) scale = 1.06;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 500.0 && pt <= 600.0) scale = 1.04;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 500.0 && pt <= 600.0) scale = 1.18;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 500.0 && pt <= 600.0) scale = 1.00;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 500.0 && pt <= 600.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 600.0 && pt <= 700.0) scale = 1.06;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 600.0 && pt <= 700.0) scale = 1.04;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 600.0 && pt <= 700.0) scale = 1.16;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 600.0 && pt <= 700.0) scale = 0.990;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 600.0 && pt <= 700.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 700.0 && pt <= 800.0) scale = 1.06;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 700.0 && pt <= 800.0) scale = 1.03;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 700.0 && pt <= 800.0) scale = 1.12;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 700.0 && pt <= 800.0) scale = 0.901;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 700.0 && pt <= 800.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 800.0 && pt <= 900.0) scale = 1.05;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 800.0 && pt <= 900.0) scale = 1.03;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 800.0 && pt <= 900.0) scale = 1.12;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 800.0 && pt <= 900.0) scale = 0.840;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 800.0 && pt <= 900.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 900.0 && pt <= 1000.0) scale = 1.05;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 900.0 && pt <= 1000.0) scale = 1.03;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 900.0 && pt <= 1000.0) scale = 1.08;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 900.0 && pt <= 1000.0) scale = 0.781;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 900.0 && pt <= 1000.0) scale = 1.0;
            if (fabs(eta) > 0.0 && fabs(eta) <= 0.8 && pt > 1000.0 && pt <= 3000.0) scale = 1.05;
            if (fabs(eta) > 0.8 && fabs(eta) <= 1.6 && pt > 1000.0 && pt <= 3000.0) scale = 1.02;
            if (fabs(eta) > 1.6 && fabs(eta) <= 2.4 && pt > 1000.0 && pt <= 3000.0) scale = 0.990;
            if (fabs(eta) > 2.4 && fabs(eta) <= 3.8 && pt > 1000.0 && pt <= 3000.0) scale = 0.704;
            if (fabs(eta) > 3.8 && fabs(eta) <= 5.0 && pt > 1000.0 && pt <= 3000.0) scale = 1.0;

            calibrated_pt[i] = pt*scale;
                }

        return calibrated_pt;
    }





auto calibrate_pt_double_n_bins(
                const ROOT::VecOps::RVec<float> &AK8_eta,
                const ROOT::VecOps::RVec<float> &AK8_pt) {

        auto size_outer = AK8_eta.size();
        ROOT::VecOps::RVec<float> calibrated_pt (size_outer);

        for (int i = 0; i < size_outer; i++) {
            float scale = 1.0;
            float eta = AK8_eta[i];
            float pt = AK8_pt[i];

            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 200.0 && pt < 225.0) scale = 1.08;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 200.0 && pt < 225.0) scale = 1.08;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 200.0 && pt < 225.0) scale = 1.07;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 200.0 && pt < 225.0) scale = 1.04;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 200.0 && pt < 225.0) scale = 1.21;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 200.0 && pt < 225.0) scale = 1.20;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 200.0 && pt < 225.0) scale = 1.20;
            if (fabs(eta) >= 3.1 && fabs(eta) < 3.8 && pt >= 200.0 && pt < 225.0) scale = 1.34;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 225.0 && pt < 250.0) scale = 1.08;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 225.0 && pt < 250.0) scale = 1.07;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 225.0 && pt < 250.0) scale = 1.07;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 225.0 && pt < 250.0) scale = 1.04;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 225.0 && pt < 250.0) scale = 1.21;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 225.0 && pt < 250.0) scale = 1.21;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 225.0 && pt < 250.0) scale = 1.20;
            if (fabs(eta) >= 3.1 && fabs(eta) < 3.8 && pt >= 225.0 && pt < 250.0) scale = 1.30;

            if (fabs(eta) >= 3.8 && fabs(eta) < 4.4 && pt >= 225.0 && pt < 250.0) scale = 0.87;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 250.0 && pt < 275.0) scale = 1.08;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 250.0 && pt < 275.0) scale = 1.07;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 250.0 && pt < 275.0) scale = 1.07;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 250.0 && pt < 275.0) scale = 1.04;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 250.0 && pt < 275.0) scale = 1.22;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 250.0 && pt < 275.0) scale = 1.20;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 250.0 && pt < 275.0) scale = 1.18;
            if (fabs(eta) >= 3.1 && fabs(eta) < 3.8 && pt >= 250.0 && pt < 275.0) scale = 1.16;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 275.0 && pt < 300.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 275.0 && pt < 300.0) scale = 1.07;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 275.0 && pt < 300.0) scale = 1.07;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 275.0 && pt < 300.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 275.0 && pt < 300.0) scale = 1.22;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 275.0 && pt < 300.0) scale = 1.20;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 275.0 && pt < 300.0) scale = 1.16;
            if (fabs(eta) >= 3.1 && fabs(eta) < 3.8 && pt >= 275.0 && pt < 300.0) scale = 1.15;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 300.0 && pt < 325.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 300.0 && pt < 325.0) scale = 1.07;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 300.0 && pt < 325.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 300.0 && pt < 325.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 300.0 && pt < 325.0) scale = 1.22;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 300.0 && pt < 325.0) scale = 1.20;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 300.0 && pt < 325.0) scale = 1.16;
            if (fabs(eta) >= 3.1 && fabs(eta) < 3.8 && pt >= 300.0 && pt < 325.0) scale = 1.19;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 325.0 && pt < 350.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 325.0 && pt < 350.0) scale = 1.07;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 325.0 && pt < 350.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 325.0 && pt < 350.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 325.0 && pt < 350.0) scale = 1.22;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 325.0 && pt < 350.0) scale = 1.19;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 325.0 && pt < 350.0) scale = 1.14;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 350.0 && pt < 375.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 350.0 && pt < 375.0) scale = 1.07;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 350.0 && pt < 375.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 350.0 && pt < 375.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 350.0 && pt < 375.0) scale = 1.21;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 350.0 && pt < 375.0) scale = 1.20;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 350.0 && pt < 375.0) scale = 1.13;
            if (fabs(eta) >= 3.1 && fabs(eta) < 3.8 && pt >= 350.0 && pt < 375.0) scale = 1.18;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 375.0 && pt < 400.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 375.0 && pt < 400.0) scale = 1.07;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 375.0 && pt < 400.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 375.0 && pt < 400.0) scale = 1.04;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 375.0 && pt < 400.0) scale = 1.22;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 375.0 && pt < 400.0) scale = 1.18;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 375.0 && pt < 400.0) scale = 1.12;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 400.0 && pt < 425.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 400.0 && pt < 425.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 400.0 && pt < 425.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 400.0 && pt < 425.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 400.0 && pt < 425.0) scale = 1.20;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 400.0 && pt < 425.0) scale = 1.18;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 400.0 && pt < 425.0) scale = 1.09;
            if (fabs(eta) >= 3.1 && fabs(eta) < 3.8 && pt >= 400.0 && pt < 425.0) scale = 0.952;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 425.0 && pt < 450.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 425.0 && pt < 450.0) scale = 1.07;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 425.0 && pt < 450.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 425.0 && pt < 450.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 425.0 && pt < 450.0) scale = 1.21;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 425.0 && pt < 450.0) scale = 1.18;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 425.0 && pt < 450.0) scale = 1.09;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 450.0 && pt < 475.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 450.0 && pt < 475.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 450.0 && pt < 475.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 450.0 && pt < 475.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 450.0 && pt < 475.0) scale = 1.21;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 450.0 && pt < 475.0) scale = 1.18;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 450.0 && pt < 475.0) scale = 1.05;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 475.0 && pt < 500.0) scale = 1.07;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 475.0 && pt < 500.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 475.0 && pt < 500.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 475.0 && pt < 500.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 475.0 && pt < 500.0) scale = 1.20;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 475.0 && pt < 500.0) scale = 1.17;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 475.0 && pt < 500.0) scale = 1.07;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 500.0 && pt < 550.0) scale = 1.06;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 500.0 && pt < 550.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 500.0 && pt < 550.0) scale = 1.06;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 500.0 && pt < 550.0) scale = 1.03;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 500.0 && pt < 550.0) scale = 1.19;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 500.0 && pt < 550.0) scale = 1.14;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 500.0 && pt < 550.0) scale = 1.02;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 550.0 && pt < 600.0) scale = 1.06;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 550.0 && pt < 600.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 550.0 && pt < 600.0) scale = 1.05;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 550.0 && pt < 600.0) scale = 1.02;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 550.0 && pt < 600.0) scale = 1.18;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 550.0 && pt < 600.0) scale = 1.14;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 550.0 && pt < 600.0) scale = 0.971;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 600.0 && pt < 650.0) scale = 1.06;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 600.0 && pt < 650.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 600.0 && pt < 650.0) scale = 1.05;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 600.0 && pt < 650.0) scale = 1.02;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 600.0 && pt < 650.0) scale = 1.18;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 600.0 && pt < 650.0) scale = 1.12;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 600.0 && pt < 650.0) scale = 0.99;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 650.0 && pt < 700.0) scale = 1.06;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 650.0 && pt < 700.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 650.0 && pt < 700.0) scale = 1.05;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 650.0 && pt < 700.0) scale = 1.02;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 650.0 && pt < 700.0) scale = 1.17;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 650.0 && pt < 700.0) scale = 1.07;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 650.0 && pt < 700.0) scale = 0.99;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 700.0 && pt < 750.0) scale = 1.06;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 700.0 && pt < 750.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 700.0 && pt < 750.0) scale = 1.05;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 700.0 && pt < 750.0) scale = 1.01;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 700.0 && pt < 750.0) scale = 1.13;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 700.0 && pt < 750.0) scale = 1.05;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 700.0 && pt < 750.0) scale = 0.917;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 750.0 && pt < 800.0) scale = 1.06;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 750.0 && pt < 800.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 750.0 && pt < 800.0) scale = 1.05;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 750.0 && pt < 800.0) scale = 1.02;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 750.0 && pt < 800.0) scale = 1.13;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 750.0 && pt < 800.0) scale = 1.04;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 750.0 && pt < 800.0) scale = 0.877;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 800.0 && pt < 850.0) scale = 1.06;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 800.0 && pt < 850.0) scale = 1.06;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 800.0 && pt < 850.0) scale = 1.05;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 800.0 && pt < 850.0) scale = 1.02;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 800.0 && pt < 850.0) scale = 1.15;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 800.0 && pt < 850.0) scale = 1.01;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 800.0 && pt < 850.0) scale = 0.87;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 850.0 && pt < 900.0) scale = 1.05;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 850.0 && pt < 900.0) scale = 1.05;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 850.0 && pt < 900.0) scale = 1.04;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 850.0 && pt < 900.0) scale = 1.01;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 850.0 && pt < 900.0) scale = 1.13;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 850.0 && pt < 900.0) scale = 1.03;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 850.0 && pt < 900.0) scale = 0.714;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 900.0 && pt < 950.0) scale = 1.05;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 900.0 && pt < 950.0) scale = 1.05;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 900.0 && pt < 950.0) scale = 1.04;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 900.0 && pt < 950.0) scale = 1.00;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 900.0 && pt < 950.0) scale = 1.10;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 900.0 && pt < 950.0) scale = 0.952;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 900.0 && pt < 950.0) scale = 0.87;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 950.0 && pt < 1000.0) scale = 1.06;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 950.0 && pt < 1000.0) scale = 1.05;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 950.0 && pt < 1000.0) scale = 1.04;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 950.0 && pt < 1000.0) scale = 1.00;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 950.0 && pt < 1000.0) scale = 1.10;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 950.0 && pt < 1000.0) scale = 0.84;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 950.0 && pt < 1000.0) scale = 0.741;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 1000.0 && pt < 2000.0) scale = 1.05;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 1000.0 && pt < 2000.0) scale = 1.05;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 1000.0 && pt < 2000.0) scale = 1.04;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 1000.0 && pt < 2000.0) scale = 0.99;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 1000.0 && pt < 2000.0) scale = 1.00;
            if (fabs(eta) >= 2.0 && fabs(eta) < 2.4 && pt >= 1000.0 && pt < 2000.0) scale = 0.84;

            if (fabs(eta) >= 2.4 && fabs(eta) < 3.1 && pt >= 1000.0 && pt < 2000.0) scale = 0.704;


            if (fabs(eta) >= 0.0 && fabs(eta) < 0.4 && pt >= 2000.0) scale = 1.04;
            if (fabs(eta) >= 0.4 && fabs(eta) < 0.8 && pt >= 2000.0) scale = 1.05;

            if (fabs(eta) >= 0.8 && fabs(eta) < 1.2 && pt >= 2000.0) scale = 1.03;
            if (fabs(eta) >= 1.2 && fabs(eta) < 1.6 && pt >= 2000.0) scale = 0.917;

            if (fabs(eta) >= 1.6 && fabs(eta) < 2.0 && pt >= 2000.0) scale = 0.741;


            calibrated_pt[i] = pt*scale;
                }

        return calibrated_pt;
    }














#endif
