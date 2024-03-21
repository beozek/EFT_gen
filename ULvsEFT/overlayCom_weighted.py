import ROOT

ROOT.gROOT.SetBatch(True)

file1 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_comparePowheg/noHT_weights/output_EFT.root", "READ")
file2 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/UL_beforentuple/nano/condor/plots/output_powheg.root", "READ")

output_file = ROOT.TFile.Open("output_powheg_madgraph.root", "RECREATE")


histograms_to_overlay = [
    # ('h_leptonPt', 'h_leptonPt_weightSM', 'h_leptonPt_ctGRe'),
    # ('h_leptoneta', 'h_leptoneta_weightSM', 'h_leptoneta_ctGRe'),
    # ('h_electronPt', 'h_electronPt_weightSM', 'h_electronPt_ctGRe'),
    # ('h_electroneta', 'h_electroneta_weightSM', 'h_electroneta_ctGRe'),
    # ('h_muonPt', 'h_muonPt_weightSM', 'h_muonPt_ctGRe'),
    # ('h_muoneta', 'h_muoneta_weightSM', 'h_muoneta_ctGRe'),
    # ('h_topPt', 'h_topPt_weightSM', 'h_topPt_ctGRe'),
    # ('h_topEta', 'h_topEta_weightSM', 'h_topEta_ctGRe'),
    # ('h_antitopPt', 'h_antitopPt_weightSM', 'h_antitopPt_ctGRe'),
    # ('h_antitopEta', 'h_antitopEta_weightSM', 'h_antitopEta_ctGRe'),
    # ('h_invariantMass', 'h_invariantMass_weightSM', 'h_invariantMass_ctGRe'),
    # ('h_LHE_HT', 'h_LHE_HT_weightSM', 'h_LHE_HT_ctGRe'),
    # ('h_LHE_HT_0_500', 'h_LHE_HT_0_500_weightSM', 'h_LHE_HT_0_500_ctGRe'),
    # ('h_LHE_HT_500_750', 'h_LHE_HT_500_750_weightSM', 'h_LHE_HT_500_750_ctGRe'),
    # ('h_LHE_HT_750_1000', 'h_LHE_HT_750_1000_weightSM', 'h_LHE_HT_750_1000_ctGRe'),
    # ('h_LHE_HT_1000_1500', 'h_LHE_HT_1000_1500_weightSM', 'h_LHE_HT_1000_1500_ctGRe'),
    # ('h_LHE_HT_1500Inf', 'h_LHE_HT_1500Inf_weightSM', 'h_LHE_HT_1500Inf_ctGRe'),
    # ('h_leading_jet_pt', 'h_leading_jet_pt_weightSM', 'h_leading_jet_pt_ctGRe'),
    # ('h_second_leading_jet_pt', 'h_second_leading_jet_pt_weightSM', 'h_second_leading_jet_pt_ctGRe'),
    ('h_jet_multiplicity_last_copy', 'h_jet_multiplicity_last_copy_weightSM', 'h_jet_multiplicity_last_copy_ctGRe'),
    # ('h_mtt_vs_LHEHT', 'h_mtt_vs_LHEHT_weightSM', 'h_mtt_vs_LHEHT_ctGRe'),
    # ('h_bquark_pt', 'h_bquark_pt_weightSM', 'h_bquark_pt_ctGRe'),
    # ('h_bquark_eta', 'h_bquark_eta_weightSM', 'h_bquark_eta_ctGRe'),
]

pastelRed = ROOT.TColor.GetColor("#FFA07A")  # Pastel red (Light Salmon)
pastelGreen = ROOT.TColor.GetColor("#98FB98")  # Pastel green (Pale Green)
pastelBlue = ROOT.TColor.GetColor("#ADD8E6")  # Pastel blue (Light Blue)
pastelPurple = ROOT.TColor.GetColor("#DDA0DD")  # Pastel purple (Plum)
pastelYellow = ROOT.TColor.GetColor("#FFFACD")  # Pastel yellow (Lemon Chiffon)
pastelCyan = ROOT.TColor.GetColor("#E0FFFF")  # Pastel cyan (Light Cyan)

for hist_names in histograms_to_overlay:
    
    hist1 = file2.Get(hist_names[0])
    if not hist1:  
        print("Histogram '{}' not found in file2.".format(hist_names[0]))
        continue

    hist2 = file1.Get(hist_names[1])
    if not hist2:  # Check if hist2 is successfully retrieved
        print("Histogram '{}' not found in file1.".format(hist_names[1]))
        continue
        
    hist3 = file1.Get(hist_names[2])
    if not hist3:  # Check if hist3 is successfully retrieved
        print("Histogram '{}' not found in file1.".format(hist_names[2]))
        continue
    
    # hist1 = hist1.Rebin(10, hist1.GetName() + "_rebinned")
    # hist2 = hist2.Rebin(10, hist2.GetName() + "_rebinned")
    # hist3 = hist3.Rebin(10, hist3.GetName() + "_rebinned")
    
    if hist1.Integral() > 0:
        hist1.Scale(1.0 / hist1.Integral())
    if hist2.Integral() > 0:
        hist2.Scale(1.0 / hist2.Integral())
    if hist3.Integral() > 0:
        hist3.Scale(1.0 / hist3.Integral())

    hist1.SetLineColor(ROOT.kOrange)
    hist2.SetLineColor(ROOT.kBlue)
    hist3.SetLineColor(ROOT.kRed)
    
    # hist1.SetLineWidth(3)
    # hist2.SetLineWidth(3)
    # hist3.SetLineWidth(3)

    c = ROOT.TCanvas("c", "canvas", 800, 600)
    # c.SetLogy(1) 
    ROOT.gStyle.SetOptStat("io")
    
    # hist1.Draw("hist")  
    hist2.Draw("hist")  
    hist3.Draw("histsame")  

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(hist1, "Powheg UL18")
    legend.AddEntry(hist2, "Madgraph EFT, SM")
    legend.AddEntry(hist3, "Madgraph EFT, ctGRe")
    legend.Draw()

    c.SaveAs("{}_.png".format(hist_names[0]))
  
    
    
for hist_names in histograms_to_overlay:
    
#     # output_file.Open()
#     hist1 = file2.Get(hist_names[0])
#     hist1_clone = hist1.Clone(hist_names[0] + "_powheg")
#     hist1_clone.Write() 
    
    hist2 = file1.Get(hist_names[1])
    hist2_clone = hist2.Clone(hist_names[1])  
    hist2_clone.Write() 
    
    hist3 = file1.Get(hist_names[2])
    hist3_clone = hist3.Clone(hist_names[2]) 
    hist3_clone.Write()

file1.Close()
file2.Close()
output_file.Close()
