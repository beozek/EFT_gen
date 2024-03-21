import ROOT

file = ROOT.TFile.Open("output_histograms.root")  

h_before = file.Get("h_LHE_HT_before")
h_muon_before = file.Get("h_muon_LHE_HT_before")
h_muon_after_lepton = file.Get("h_muon_LHE_HT_after_lepton_cut")
h_muon_after_jet = file.Get("h_muon_LHE_HT_after_jet_cut")
h_muon_after_met = file.Get("h_muon_LHE_HT_after_met_cut")

h_denominator = h_before.Clone("h_denominator")

h_ratio_muon_before = h_muon_before.Clone("h_ratio_muon_before")
h_ratio_muon_before.Divide(h_denominator)

h_ratio_muon_after_lepton = h_muon_after_lepton.Clone("h_ratio_muon_after_lepton")
h_ratio_muon_after_lepton.Divide(h_denominator)

h_ratio_muon_after_jet = h_muon_after_jet.Clone("h_ratio_muon_after_jet")
h_ratio_muon_after_jet.Divide(h_denominator)

h_ratio_muon_after_met = h_muon_after_met.Clone("h_ratio_muon_after_met")
h_ratio_muon_after_met.Divide(h_denominator)

c = ROOT.TCanvas("c", "Cutflow Ratios", 800, 600)
c.Divide(2, 2) 

c.cd(1)
h_ratio_muon_before.SetTitle("Ratio After Muon Flavor Smuonction")
h_ratio_muon_before.Draw()

c.cd(2)
h_ratio_muon_after_lepton.SetTitle("Ratio After Lepton Pt Cut")
h_ratio_muon_after_lepton.Draw()

c.cd(3)
h_ratio_muon_after_jet.SetTitle("Ratio After Jet Pt Cut")
h_ratio_muon_after_jet.Draw()

c.cd(4)
h_ratio_muon_after_met.SetTitle("Ratio After MET Cut")
h_ratio_muon_after_met.Draw()

c.SaveAs("ratio_plots_muo.png")

file.Close()
