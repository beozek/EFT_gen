import ROOT

file = ROOT.TFile("output_histograms.root", "READ")

mass_histogram = file.Get("h_invariantMass")
ht_histogram = file.Get("h_ele_LHE_HT_before")
# ht_histogram = file.Get("h_muon_LHE_HT_before")
# ht_histogram = file.Get("h_ele_LHE_HT_after_met_cut")
# ht_histogram = file.Get("h_muon_LHE_HT_after_met_cut")

canvas = ROOT.TCanvas("canvas", "Invariant Mass vs HT", 800, 600)


hist2d = ROOT.TH2F("hist2d", "Invariant Mass vs HT", 100, ht_histogram.GetXaxis().GetXmin(), ht_histogram.GetXaxis().GetXmax(), 100, mass_histogram.GetXaxis().GetXmin(), 1000)

for entry in range(mass_histogram.GetNbinsX()):
    mass = mass_histogram.GetBinContent(entry)
    ht = ht_histogram.GetBinContent(entry)
    hist2d.Fill(ht, mass)

hist2d.Draw("COLZ")

hist2d.GetXaxis().SetTitle("HT")
hist2d.GetYaxis().SetTitle("Invariant Mass")

canvas.Update()

canvas.SaveAs("invariant_mass_vs_ht.png")

file.Close()
