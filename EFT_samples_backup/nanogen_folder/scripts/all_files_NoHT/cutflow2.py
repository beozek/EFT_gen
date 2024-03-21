import ROOT

file = ROOT.TFile.Open("output_histograms.root")  

h_before = file.Get("h_LHE_HT_before")
h_muon_before = file.Get("h_muon_LHE_HT_before")
h_muon_after_lepton = file.Get("h_muon_LHE_HT_after_lepton_cut")
h_muon_after_jet = file.Get("h_muon_LHE_HT_after_jet_cut")
h_muon_after_met = file.Get("h_muon_LHE_HT_after_met_cut")

h_cutflow = ROOT.TH1F("h_cutflow", "Cut Flow; Cut; Number of Events", 5, 0, 5)

cut_names = ["Before Cuts", "muon", "Lepton Pt", "Jet Pt", "MET"]
for i, name in enumerate(cut_names, start=1):
    h_cutflow.GetXaxis().SetBinLabel(i, name)

h_cutflow.SetBinContent(1, h_before.GetEntries())
h_cutflow.SetBinContent(2, h_muon_before.GetEntries())
h_cutflow.SetBinContent(3, h_muon_after_lepton.GetEntries())
h_cutflow.SetBinContent(4, h_muon_after_jet.GetEntries())
h_cutflow.SetBinContent(5, h_muon_after_met.GetEntries())

c = ROOT.TCanvas("c", "Cutflow Plot", 800, 600)

c.SetLogy()

h_cutflow.SetFillColor(ROOT.kBlue)
h_cutflow.SetLineColor(ROOT.kBlack)
h_cutflow.Draw("hist")

c.SaveAs("cutflow_stairs_plot_muon.png")

file.Close()
