import ROOT

ROOT.gROOT.SetBatch(True)

file1 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_comparePowheg/HT800/files/combined_nanogen.root", 'READ')
file2 = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_beforentuple/nano/plots/HT800_powheg/combined.root", 'READ')

histograms = {
    "h_leptonPt":      ("h_leptonPt", "p_{T}^{lepton} [GeV]", 1000, 0, 2000),
    "h_leptoneta":     ("h_leptoneta", "#eta^{lepton}; #eta;Events", 50, -2.5, 2.5),
    "h_electronPt" :   ("h_electronPt", "p_{T}^{electron} [GeV]; pT (GeV);Events", 1000, 0, 2000),
    "h_electroneta":   ("h_electroneta", "#eta^{electron}; #eta;Events", 50, -2.5, 2.5),
    "h_muonPt" :       ("h_muonPt", "p_{T}^{muon} [GeV]; pT (GeV);Events", 1000, 0, 2000),
    "h_muoneta":       ("h_muoneta", "#eta^{muon}; #eta;Events", 50, -2.5, 2.5),
    "h_topPt" :        ("h_topPt", "p_{T}^{top} [GeV]; pT (GeV);Events", 1000, 0, 3000),
    "h_topEta":        ("h_topEta", "#eta^{top}; #eta;Events", 50, -2.5, 2.5),
    "h_antitopPt" :    ("h_antitopPt", "p_{T}^{antitop} [GeV]; pT (GeV);Events", 1000, 0, 3000),
    "h_antitopEta":    ("h_antitopEta", "#eta^{antitop}; #eta;Events", 50, -2.5, 2.5),
    "h_MET":           ("h_MET", "MET;MET (GeV);Events", 100, 0, 200),
    "h_invariantMass": ("h_invariantMass", "Invariant Mass; M (GeV);Events", 100, 0, 4000),
    "h_LHE_HT_before": ("h_LHE_HT_before", "LHE_HT; HT (GeV); Events", 100, 0, 2000),
    "h_leading_jet_pt":("h_leading_jet_pt", "p_{T}^{Leading Jet} [GeV]; pT (GeV);Events", 100, 0, 1000),
    "h_second_leading_jet_pt": ("h_second_leading_jet_pt", "p_{T}^{Second Leading Jet} [GeV]; pT (GeV);Events", 100, 0, 1000),
    "h_jet_multiplicity_last_copy": ('h_jet_multiplicity_last_copy', 'Jet Multiplicity ;Number of Jets;Events', 10, 0, 10)

}

for histogram_name, hist_def in (histograms).items():

    hist1 = file1.Get(histogram_name)
    hist2 = file2.Get(histogram_name)
    
    c = ROOT.TCanvas("c", "Overlay Histograms: " + histogram_name, 800, 600)

    if hist1 and hist2:
        if hist1.Integral() > 0:
            hist1.Scale(1.0 / hist1.Integral())
        
        if hist2.Integral() > 0:
            hist2.Scale(1.0 / hist2.Integral())
            
        max_y_value = max(hist1.GetMaximum(), hist2.GetMaximum())
        
        hist1.SetLineColor(2)
        hist2.SetLineColor(4)  
        
        hist1.SetMaximum(max_y_value * 1.2)
        
        hist1.Draw('HIST')
        hist2.Draw("HISTSAME")

        legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
        legend.AddEntry(hist1, "Madgraph EFT")
        legend.AddEntry(hist2, "Powheg")
        legend.Draw()

        c.Update()

        c.SaveAs("overlay_" + histogram_name + ".png")
    
    else:
        print("Histogram not found:", histogram_name)
        

file1.Close()
file2.Close()
