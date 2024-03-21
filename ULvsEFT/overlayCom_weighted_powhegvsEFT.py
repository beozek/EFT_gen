import ROOT

ROOT.gROOT.SetBatch(True)

file1 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/output_weights_NoNu_latest/output_EFT_latest.root", "READ")
file2 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/UL_beforentuple/nano/condor/plots/output_latest.root", "READ")
file3 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/ULvsEFT/envelope_output.root", "READ")

output_file = ROOT.TFile.Open("output_madgraphVSpowheg.root", "RECREATE")

histograms_to_overlay = [
    ('h_leptonPt', 'h_leptonPt_weightSM', 'h_leptonPt_scale_Up', 'h_leptonPt_scale_Down'),
    ('h_leptoneta', 'h_leptoneta_weightSM', 'h_leptonEta_scale_Up', 'h_leptonEta_scale_Down'),
    ('h_electronPt', 'h_electronPt_weightSM', 'h_electronPt_scale_Up', 'h_electronPt_scale_Down'),
    ('h_electroneta', 'h_electroneta_weightSM', 'h_electronEta_scale_Up', 'h_electronEta_scale_Down'),
    ('h_muonPt', 'h_muonPt_weightSM', 'h_muonPt_scale_Up', 'h_muonPt_scale_Down'),
    ('h_muoneta', 'h_muoneta_weightSM', 'h_muonEta_scale_Up', 'h_muonEta_scale_Down'),
    ('h_topPt', 'h_topPt_weightSM', 'h_topPt_scale_Up', 'h_topPt_scale_Down'),
    ('h_topEta', 'h_topEta_weightSM', 'h_topEta_scale_Up', 'h_topEta_scale_Down'),
    ('h_antitopPt', 'h_antitopPt_weightSM', 'h_antitopPt_scale_Up', 'h_antitopPt_scale_Down'),
    ('h_antitopEta', 'h_antitopEta_weightSM', 'h_antitopEta_scale_Up', 'h_antitopEta_scale_Down'),
    ('h_invariantMass', 'h_invariantMass_weightSM', 'h_invariantMass_scale_Up', 'h_invariantMass_scale_Down'),
    ('h_leading_jet_pt', 'h_leading_jet_pt_weightSM', 'h_leading_jet_pt_scale_Up', 'h_leading_jet_pt_scale_Down'),
    ('h_second_leading_jet_pt', 'h_second_leading_jet_pt_weightSM', 'h_second_leading_jet_pt_scale_Up', 'h_second_leading_jet_pt_scale_Down'),
    ('h_jet_multiplicity_last_copy', 'h_jet_multiplicity_last_copy_weightSM', 'h_jet_multiplicity_last_copy_scale_Up', 'h_jet_multiplicity_last_copy_scale_Down'),
    ("h_jet_multiplicity_ishardprocess", "h_jet_multiplicity_ishardprocess_weightSM", "h_jet_multiplicity_ishardprocess_scale_Up", 'h_jet_multiplicity_ishardprocess_scale_Down'),

    # ('h_mtt_vs_LHEHT', 'h_mtt_vs_LHEHT_weightSM', 'h_mtt_vs_LHEHT_ctGRe'),
    # ('h_bquark_pt', 'h_bquark_pt_weightSM', 'h_bquark_pt_ctGRe'),
    # ('h_bquark_eta', 'h_bquark_eta_weightSM', 'h_bquark_eta_ctGRe'),
    # ('h_LHE_HT', 'h_LHE_HT_weightSM', 'h_LHE_HT_ctGRe'),
    # ('h_LHE_HT_0_500', 'h_LHE_HT_0_500_weightSM', 'h_LHE_HT_0_500_ctGRe'),
    # ('h_LHE_HT_500_750', 'h_LHE_HT_500_750_weightSM', 'h_LHE_HT_500_750_ctGRe'),
    # ('h_LHE_HT_750_1000', 'h_LHE_HT_750_1000_weightSM', 'h_LHE_HT_750_1000_ctGRe'),
    # ('h_LHE_HT_1000_1500', 'h_LHE_HT_1000_1500_weightSM', 'h_LHE_HT_1000_1500_ctGRe'),
    # ('h_LHE_HT_1500Inf', 'h_LHE_HT_1500Inf_weightSM', 'h_LHE_HT_1500Inf_ctGRe'),
]
pastelRed = ROOT.TColor.GetColor("#FFA07A")  # Pastel red (Light Salmon)
pastelGreen = ROOT.TColor.GetColor("#98FB98")  # Pastel green (Pale Green)
pastelBlue = ROOT.TColor.GetColor("#ADD8E6")  # Pastel blue (Light Blue)
pastelPurple = ROOT.TColor.GetColor("#DDA0DD")  # Pastel purple (Plum)
pastelYellow = ROOT.TColor.GetColor("#FFFACD")  # Pastel yellow (Lemon Chiffon)
pastelCyan = ROOT.TColor.GetColor("#E0FFFF")  # Pastel cyan (Light Cyan)

for hist_names in histograms_to_overlay:

    hist1 = file1.Get(hist_names[1]) #EFT SM
    hist2 = file2.Get(hist_names[0]) #Powheg 
    hist3 = file3.Get(hist_names[2]) #madgraph up variation
    hist4 = file3.Get(hist_names[3]) #madgraph down

    c = ROOT.TCanvas("c", "Canvas with Ratio", 800, 800)
    
    pad1 = ROOT.TPad("pad1", "The pad with the histogram", 0, 0.3, 1, 1.0)
    pad2 = ROOT.TPad("pad2", "The pad with the ratio", 0, 0.05, 1, 0.3)
    pad1.SetLogy()
    pad1.SetBottomMargin(0) 
    pad2.SetTopMargin(0)  
    pad2.SetBottomMargin(0.33)

    pad1.Draw()
    pad2.Draw()
    
    ROOT.gStyle.SetOptStat("iorme")
  
    if hist1.Integral() > 0:
        hist1.Scale(1.0 / hist1.Integral())
    if hist2.Integral() > 0:
        hist2.Scale(1.0 / hist2.Integral())
    if hist3.Integral() > 0:
        hist3.Scale(1.0 / hist3.Integral())
    if hist4.Integral() > 0:
        hist4.Scale(1.0 / hist4.Integral())
        

    hist1.SetLineColor(ROOT.kRed)
    hist2.SetLineColor(ROOT.kGreen-2)
    
    # hist1.SetLineWidth(3)
    # hist2.SetLineWidth(3)    
    
    
    pad1.cd()
    hist1.Draw("hist")
    hist2.Draw("histsame")
    
    systematic_uncertainty_main = hist1.Clone("systematic_uncertainty_main")
    for i in range(1, hist1.GetNbinsX() + 1):
        bin_content_nominal = hist1.GetBinContent(i)
        bin_error_up = abs(hist3.GetBinContent(i) - bin_content_nominal)
        bin_error_down = abs(hist4.GetBinContent(i) - bin_content_nominal)
        bin_error_max = max(bin_error_up, bin_error_down)

        systematic_uncertainty_main.SetBinError(i, bin_error_max)
    
    systematic_uncertainty_main.SetFillStyle(3245)  
    systematic_uncertainty_main.SetFillColor(ROOT.kGray+2)
    systematic_uncertainty_main.SetLineColor(ROOT.kGray+2)
    # systematic_uncertainty_main.SetMarkerStyle(1)
    systematic_uncertainty_main.Draw("E2 SAME")
    

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(hist1, "Madgraph EFT, SM")
    legend.AddEntry(hist2, "Powheg UL18")
    legend.AddEntry(systematic_uncertainty_main, "Q2 Uncertainty", "f")

    legend.Draw()
    
    pad2.cd()
    ROOT.gStyle.SetOptStat("0")

    
    ratio = hist1.Clone("ratio")
    ratio.Divide(hist2)
    ratio.SetLineColor(ROOT.kBlack)
    ratio.SetMinimum(0.0) 
    ratio.SetMaximum(2.0)
    ratio.GetYaxis().SetTitle("Madgraph SM/Powheg") 
    ratio.GetYaxis().SetTitleSize(0.1) 
    ratio.GetYaxis().SetTitleOffset(0.5)
    ratio.GetYaxis().SetLabelSize(0.05) 
    ratio.GetYaxis().CenterTitle(True)
    ratio.SetTitle("")
    
    ratio.GetXaxis().SetTitleSize(0.12)  
    ratio.GetXaxis().SetTitleOffset(1.0) 
    ratio.GetXaxis().SetLabelSize(0.1) 

    ratio.Draw("ep")
    
    line = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1, ratio.GetXaxis().GetXmax(), 1)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineStyle(2)
    line.Draw("same")
    
    
    
    systematic_uncertainty = hist1.Clone("systematic_uncertainty")
    systematic_uncertainty.Reset("ICES")

    for i in range(1, hist1.GetNbinsX() + 1):
        bin_content_nominal = hist1.GetBinContent(i)
        bin_error_up = abs(hist3.GetBinContent(i) - bin_content_nominal)
        bin_error_down = abs(hist4.GetBinContent(i) - bin_content_nominal)
        bin_error_max = max(bin_error_up, bin_error_down)
        systematic_uncertainty.SetBinContent(i, 1)  
        if bin_content_nominal != 0:
            systematic_uncertainty.SetBinError(i, bin_error_max / bin_content_nominal)

    systematic_uncertainty.GetYaxis().SetTitle("SM / ctGRe")
    systematic_uncertainty.GetYaxis().SetTitleSize(0.1) 
    systematic_uncertainty.GetYaxis().SetTitleOffset(0.5)
    systematic_uncertainty.GetYaxis().SetLabelSize(0.05) 

    systematic_uncertainty.SetFillColor(ROOT.kGray+2)
    systematic_uncertainty.SetFillStyle(3245)
    systematic_uncertainty.SetLineColor(ROOT.kGray+2)
    systematic_uncertainty.GetYaxis().SetLabelSize(0.08) 
    systematic_uncertainty.SetTitle("")
    systematic_uncertainty.GetXaxis().SetTitleSize(0.12)  
    systematic_uncertainty.GetXaxis().SetTitleOffset(1.0) 
    systematic_uncertainty.GetXaxis().SetLabelSize(0.1) 
    systematic_uncertainty.Draw("E2 SAME")
    
    c.Update()


    c.SaveAs("{}_powheg.pdf".format(hist_names[0]))
    
    
    
# for hist_names in histograms_to_overlay:
    
    # hist1 = file1.Get(hist_names[1])
    # hist1_clone = hist1.Clone(hist_names[1])
    # hist1_clone.Write() 
    
    # hist2 = file1.Get(hist_names[2])
    # hist2_clone = hist2.Clone(hist_names[2])  
    # hist2_clone.Write() 
    

file1.Close()
file2.Close()
file3.Close()
# output_file.Close()
