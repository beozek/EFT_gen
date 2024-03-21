import ROOT

ROOT.gROOT.SetBatch(True)

file1 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/output_weights_NoNu_latest/output_EFT_latest_v2.root", "READ")
file2 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/UL_beforentuple/nano/condor/plots/output_latest.root", "READ")
file3 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/ULvsEFT/envelope_output.root", "READ")

histograms_to_overlay = [
    ('h_leptonPt', 'h_leptonPt_weightSM', 'h_leptonPt_scale_Up', 'h_leptonPt_scale_Down'),
    ('h_leptoneta', 'h_leptoneta_weightSM', 'h_leptoneta_scale_Up', 'h_leptoneta_scale_Down'),
    ('h_electronPt', 'h_electronPt_weightSM', 'h_electronPt_scale_Up', 'h_electronPt_scale_Down'),
    ('h_electroneta', 'h_electroneta_weightSM', 'h_electroneta_scale_Up', 'h_electroneta_scale_Down'),
    ('h_muonPt', 'h_muonPt_weightSM', 'h_muonPt_scale_Up', 'h_muonPt_scale_Down'),
    ('h_muoneta', 'h_muoneta_weightSM', 'h_muoneta_scale_Up', 'h_muoneta_scale_Down'),
    ('h_topPt', 'h_topPt_weightSM', 'h_topPt_scale_Up', 'h_topPt_scale_Down'),
    ('h_topEta', 'h_topEta_weightSM', 'h_topEta_scale_Up', 'h_topEta_scale_Down'),
    ('h_antitopPt', 'h_antitopPt_weightSM', 'h_antitopPt_scale_Up', 'h_antitopPt_scale_Down'),
    ('h_antitopEta', 'h_antitopEta_weightSM', 'h_antitopEta_scale_Up', 'h_antitopEta_scale_Down'),
    ('h_invariantMass', 'h_invariantMass_weightSM', 'h_invariantMass_scale_Up', 'h_invariantMass_scale_Down'),
    ('h_leading_jet_pt', 'h_leading_jet_pt_weightSM', 'h_leading_jet_pt_scale_Up', 'h_leading_jet_pt_scale_Down'),
    ('h_second_leading_jet_pt', 'h_second_leading_jet_pt_weightSM', 'h_second_leading_jet_pt_scale_Up', 'h_second_leading_jet_pt_scale_Down'),
    ('h_jet_multiplicity_last_copy', 'h_jet_multiplicity_last_copy_weightSM', 'h_jet_multiplicity_last_copy_scale_Up', 'h_jet_multiplicity_last_copy_scale_Down'),
    ("h_jet_multiplicity_ishardprocess", "h_jet_multiplicity_ishardprocess_weightSM", "h_jet_multiplicity_ishardprocess_scale_Up", 'h_jet_multiplicity_ishardprocess_scale_Up', 'h_jet_multiplicity_ishardprocess_scale_Down'),

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
        
    hist3 = file3.Get(hist_names[2])
    if not hist3: 
        print("Histogram '{}' not found in file1.".format(hist_names[2]))
        continue
    
    hist4 = file3.Get(hist_names[3])
    if not hist4: 
        print("Histogram '{}' not found in file1.".format(hist_names[3]))
        continue
        
    if ROOT.gROOT.FindObject("c"): ROOT.gROOT.FindObject("c").Delete()
    c = ROOT.TCanvas("c", "Canvas with Ratio", 800, 800)

    pad1 = ROOT.TPad("pad1", "The pad with the histogram", 0, 0.3, 1, 1.0)
    pad2 = ROOT.TPad("pad2", "The pad with the ratio", 0, 0.05, 1, 0.3)
    pad1.SetLogy()
    pad1.Draw()
    pad2.Draw()
    
    
    pad1.cd()
    ROOT.gStyle.SetOptStat("io")
    hist1.SetLineColor(ROOT.kOrange)
    hist2.SetLineColor(ROOT.kBlue)
    hist3.SetLineColor(ROOT.kRed)
    hist4.SetLineColor(ROOT.kGreen)
    
    if hist1.Integral() > 0:
        hist1.Scale(1.0 / hist1.Integral())
    if hist2.Integral() > 0:
        hist2.Scale(1.0 / hist2.Integral())
    if hist3.Integral() > 0:
        hist3.Scale(1.0 / hist3.Integral())
    if hist4.Integral() > 0:
        hist4.Scale(1.0 / hist4.Integral())
    
    # hist1.SetLineWidth(3)
    # hist2.SetLineWidth(3)
    # hist3.SetLineWidth(3)    
    
    hist1.Draw("hist")  
    hist2.Draw("histsame")  
    hist3.Draw("histsame")  
    hist4.Draw("histsame")

    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)
    legend.AddEntry(hist1, "Powheg UL18")
    legend.AddEntry(hist2, "Madgraph EFT, Nominal (SM weight only)")
    legend.AddEntry(hist3, "Madgraph EFT, Qscale Up Variation")
    legend.AddEntry(hist4, "Madgraph EFT, Qscale Down Variation")
    legend.Draw()
    
    # Ratio plot
    pad2.cd()
    ROOT.gStyle.SetOptStat("0")
    
    ratio = hist2.Clone("ratio")
    ratio.Divide(hist1)
    ratio.SetLineColor(ROOT.kBlack)
    ratio.SetMinimum(0.0) 
    ratio.SetMaximum(1.2)
    ratio.GetYaxis().SetTitle("Madgraph SM / Powheg") 
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
    
    n_bins = ratio.GetNbinsX()
    errors_x = ROOT.Double(0)
    errors_y = ROOT.Double(0)
    graph = ROOT.TGraphAsymmErrors(n_bins)
    for i in range(1, n_bins+1):
        x = hist2.GetBinCenter(i)
        y = ratio.GetBinContent(i)
        if hist2.GetBinContent(i) >0:
            up = 1-(hist2.GetBinContent(i))/hist3.GetBinContent(i)
            down = 1-(hist2.GetBinContent(i)/ hist4.GetBinContent(i))
        graph.SetPoint(i-1, x, y)
        graph.SetPointError(i-1, 0, 0, down, up)
        print("up: ", up)
        print("down: ", down)
        # print("hist3.GetBinContent(i): ", hist3.GetBinContent(i))
        # print("hist2.GetBinContent(i): ", hist2.GetBinContent(i))

    graph.SetFillColor(ROOT.kBlue)
    graph.SetFillStyle(3005)
    graph.Draw("2 SAME") 

    c.Update()
    

    c.SaveAs("{}_errband.png".format(hist_names[0]))
  


file1.Close()
file2.Close()
