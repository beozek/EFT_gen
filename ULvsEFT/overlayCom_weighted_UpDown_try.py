import ROOT

ROOT.gROOT.SetBatch(True)

file1 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/output_weights_NoNu_latest/output_EFT_latest.root", "READ")
file2 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/UL_beforentuple/nano/condor/plots/output_latest.root", "READ")

histograms_to_overlay = [
    ('h_leptonPt', 'h_leptonPt_weightSM', 'h_leptonPt_scale_', 'h_leptonPt_scale_3'),
    ('h_leptoneta', 'h_leptoneta_weightSM', 'h_leptoneta_scale_', 'h_leptoneta_scale_3'),
    ('h_electronPt', 'h_electronPt_weightSM', 'h_electronPt_scale_', 'h_electronPt_scale_3'),
    ('h_electroneta', 'h_electroneta_weightSM', 'h_electroneta_scale_', 'h_electroneta_scale_3'),
    ('h_muonPt', 'h_muonPt_weightSM', 'h_muonPt_scale_', 'h_muonPt_scale_3'),
    ('h_muoneta', 'h_muoneta_weightSM', 'h_muoneta_scale_', 'h_muoneta_scale_3'),
    ('h_topPt', 'h_topPt_weightSM', 'h_topPt_scale_', 'h_topPt_scale_3'),
    ('h_topEta', 'h_topEta_weightSM', 'h_topEta_scale_', 'h_topEta_scale_3'),
    ('h_antitopPt', 'h_antitopPt_weightSM', 'h_antitopPt_scale_', 'h_antitopPt_scale_3'),
    ('h_antitopEta', 'h_antitopEta_weightSM', 'h_antitopEta_scale_', 'h_antitopEta_scale_3'),
    ('h_invariantMass', 'h_invariantMass_weightSM', 'h_invariantMass_scale_', 'h_invariantMass_scale_3'),
    ('h_leading_jet_pt', 'h_leading_jet_pt_weightSM', 'h_leading_jet_pt_scale_', 'h_leading_jet_pt_scale_3'),
    ('h_second_leading_jet_pt', 'h_second_leading_jet_pt_weightSM', 'h_second_leading_jet_pt_scale_', 'h_second_leading_jet_pt_scale_3'),
    ('h_jet_multiplicity_last_copy', 'h_jet_multiplicity_last_copy_weightSM', 'h_jet_multiplicity_last_copy_scale_', 'h_jet_multiplicity_last_copy_scale_3'),
    ("h_jet_multiplicity_ishardprocess", "h_jet_multiplicity_ishardprocess_weightSM", "h_jet_multiplicity_ishardprocess_scale_", 'h_jet_multiplicity_ishardprocess_scale_', 'h_jet_multiplicity_ishardprocess_scale_3'),

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
    if not hist2:  
        print("Histogram '{}' not found in file1.".format(hist_names[1]))
        continue
        
    hist3 = file1.Get(hist_names[2]+"0")
    print("hist name: ", hist_names[2]+"0")
    if not hist3: 
        print("Histogram '{}' not found in file1.".format(hist_names[2]))
        continue
    
    hist4 = file1.Get(hist_names[2]+"1")
    if not hist4: 
        print("Histogram '{}' not found in file1.".format(hist_names[2]))
        continue
    hist5 = file1.Get(hist_names[2]+"3")
    if not hist5:
        print("Histogram '{}' not found in file1.".format(hist_names[2]))
        continue
    
    hist6 = file1.Get(hist_names[2]+"4")
    if not hist6: 
        print("Histogram '{}' not found in file1.".format(hist_names[2]))
        continue
    hist7 = file1.Get(hist_names[2]+"6")
    if not hist7: 
        print("Histogram '{}' not found in file1.".format(hist_names[2]))
        continue
    
    hist8 = file1.Get(hist_names[2]+"7")
    if not hist8: 
        print("Histogram '{}' not found in file1.".format(hist_names[2]))
        continue
    
    
    hist1.SetLineColor(ROOT.kRed)
    hist2.SetLineColor(ROOT.kBlue)
    hist3.SetLineColor(ROOT.kGreen)
    hist4.SetLineColor(ROOT.kMagenta)
    hist5.SetLineColor(ROOT.kCyan)
    hist6.SetLineColor(ROOT.kOrange)
    hist7.SetLineColor(ROOT.kYellow)
    hist8.SetLineColor(ROOT.kBlack)
    
    
    # hist1.SetLineWidth(3)
    # hist2.SetLineWidth(3)
    # hist3.SetLineWidth(3)

    c = ROOT.TCanvas("c", "canvas", 800, 600)
    c.SetLogy(1) 
    ROOT.gStyle.SetOptStat("io")
    
    hist1.Draw("hist")  
    hist2.Draw("histsame")  
    hist3.Draw("histsame")  
    hist4.Draw("histsame")
    hist5.Draw("histsame")  
    hist6.Draw("histsame")  
    hist7.Draw("histsame")
    hist8.Draw("histsame")  


    legend = ROOT.TLegend(1, 1, 1, 1)
    legend.AddEntry(hist1, "Powheg UL18")
    legend.AddEntry(hist2, "Madgraph EFT, Nominal (SM weight only)")
    legend.AddEntry(hist3, "Madgraph EFT, Scale Index 0 ")
    legend.AddEntry(hist4, "Madgraph EFT, Scale Index 1 ")
    legend.AddEntry(hist5, "Madgraph EFT, Scale Index 3 ")
    legend.AddEntry(hist6, "Madgraph EFT, Scale Index 4 ")
    legend.AddEntry(hist7, "Madgraph EFT, Scale Index 6 ")
    legend.AddEntry(hist8, "Madgraph EFT, Scale Index 7 ")
    legend.Draw()

    c.SaveAs("{}.png".format(hist_names[0]))
  


file1.Close()
file2.Close()
