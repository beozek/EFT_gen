import ROOT

def save_histograms(root_file_path, output_dir, histogram_names):
    file = ROOT.TFile(root_file_path)

    for name in histogram_names:
        histogram = file.Get(name)
        if histogram:
            canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
            histogram.Draw()

            output_path = "{}/{}.png".format(output_dir, name)
            canvas.SaveAs(output_path)
            print "Saved histogram: {}".format(output_path)


    file.Close()

if __name__ == "__main__":
    root_file_path = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_all/hadd_all/output.root"  
    output_dir = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_all/plots"  
    histogram_names = [ 'h_leading_jet_pt',
    'h_second_leading_jet_pt',
    'h_LHE_HT_0_500_ele_withoutAK8',
    'h_LHE_HT_500_750_ele_withoutAK8',
    'h_LHE_HT_750_900_ele_withoutAK8',
    'h_LHE_HT_900_1250_ele_withoutAK8',
    'h_LHE_HT_1250_1500_ele_withoutAK8',
    'h_LHE_HT_1500_up_ele_withoutAK8',
    'h_LHE_HT_0_500_ele_AK8200',
    'h_LHE_HT_500_750_ele_AK8200',
    'h_LHE_HT_750_900_ele_AK8200' ,
    'h_LHE_HT_900_12g50_ele_AK8200',
    'h_LHE_HT_1250_1500_ele_AK8200',
    'h_LHE_HT_1500_up_ele_AK8200',
    'h_LHE_HT_0_500_ele_AK8400',
    'h_LHE_HT_500_750_ele_AK8400',
    'h_LHE_HT_750_900_ele_AK8400',
    'h_LHE_HT_900_1250_ele_AK8400',
    'h_LHE_HT_1250_1500_ele_AK8400',
    'h_LHE_HT_1500_up_ele_AK8400',
    'h_LHE_HT_0_500_muon_withoutAK8',
    'h_LHE_HT_500_750_muon_withoutAK8',
    'h_LHE_HT_750_900_muon_withoutAK8',
    'h_LHE_HT_900_1250_muon_withoutAK8',
    'h_LHE_HT_1250_1500_muon_withoutAK8',
    'h_LHE_HT_1500_up_muon_withoutAK8',
    'h_LHE_HT_0_500_muon_AK8200',
    'h_LHE_HT_500_750_muon_AK8200',
    'h_LHE_HT_750_900_muon_AK8200',
    'h_LHE_HT_900_1250_muon_AK8200',
    'h_LHE_HT_1250_1500_muon_AK8200',
    'h_LHE_HT_1500_up_muon_AK8200',
    'h_LHE_HT_0_500_muon_AK8400' ,
    'h_LHE_HT_500_750_muon_AK8400',
    'h_LHE_HT_750_900_muon_AK8400',
    'h_LHE_HT_900_1250_muon_AK8400',
    'h_LHE_HT_1250_1500_muon_AK8400',
    'h_LHE_HT_1500_up_muon_AK8400'
        # 'h_leptonPt', 'h_leptoneta', 'h_leptonphi', 'h_leptonFlavor',
        # 'h_electronPt', 'h_electronPt_aftercut200', 'h_electronPt_aftercut400',
        # 'h_electroneta', 'h_electroneta_aftercut200', 'h_electroneta_aftercut400',
        # 'h_muonPt', 'h_muonPt_aftercut200', 'h_muonPt_aftercut400',
        # 'h_muoneta', 'h_muoneta_aftercut200', 'h_muoneta_aftercut400',
        # 'h_hadronic_w_mass', 'h_hadronic_w_mass_aftercut200', 'h_hadronic_w_mass_aftercut400',
        # 'h_topPt', 'h_topPt_aftercut200', 'h_topPt_aftercut400',
        # 'h_antitopPt', 'h_antitopPt_aftercut200', 'h_antitopPt_aftercut400',
        # 'h_bquark_pt', 'h_bquark_eta', 'h_bquark_pt_aftercut200', 'h_bquark_pt_aftercut400',
        # 'h_topMultiplicity', 'h_topMultiplicity_aftercut200', 'h_topMultiplicity_aftercut400',
        # 'h_antitopMultiplicity', 'h_antitopMultiplicity_aftercut200', 'h_antitopMultiplicity_aftercut400',
        # 'h_jetMultiplicity_fromW', 'h_jetMultiplicity_fromW_after200', 'h_jetMultiplicity_fromW_after400',
        # 'h_MET', 'h_MET_after200', 'h_MET_after400',
        # 'h_invariantMass', 'h_invariantMass_aftercut200', 'h_invariantMass_aftercut400',
        # 'h_jetMultiplicity', 'h_nonTopMotherJets',
        # 'h_LHE_HT_before', 'h_muon_LHE_HT_aftercut200', 'h_muon_LHE_HT_aftercut400',
        # 'h_ele_LHE_HT_aftercut200', 'h_ele_LHE_HT_aftercut400',
        # 'h_ele_LHE_HT_before', 'h_ele_LHE_HT_after_lepton_cut', 'h_ele_LHE_HT_after_jet_cut', 'h_ele_LHE_HT_after_met_cut',
        # 'h_ele_LHE_HT_after_toppt200_cut', 'h_ele_LHE_HT_after_toppt400_cut',
        # 'h_muon_LHE_HT_before', 'h_muon_LHE_HT_after_lepton_cut', 'h_muon_LHE_HT_after_jet_cut', 'h_muon_LHE_HT_after_met_cut',
        # 'h_muon_LHE_HT_after_toppt200_cut', 'h_muon_LHE_HT_after_toppt400_cut',
        # 'h_both_decays',
        # 'h_jetFromW_pt', 'h_jetFromW_eta', 'h_jetFromW_pt_aftercut200', 'h_jetFromW_pt_aftercut400',
        # 'h_ttbarMass_vs_HT', 'h_muon_ttbarMass_vs_HT_aftercut200', 'h_muon_ttbarMass_vs_HT_aftercut400',
        # 'h_ele_ttbarMass_vs_HT_aftercut200', 'h_ele_ttbarMass_vs_HT_aftercut400'
    ]

    save_histograms(root_file_path, output_dir, histogram_names)
