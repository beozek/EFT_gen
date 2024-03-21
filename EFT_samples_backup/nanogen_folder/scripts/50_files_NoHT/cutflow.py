import ROOT

file = ROOT.TFile.Open("output_histograms.root")

h_before = file.Get("h_LHE_HT_before")
h_ele_before = file.Get("h_ele_LHE_HT_before")
h_ele_after_lepton = file.Get("h_ele_LHE_HT_after_lepton_cut")
h_ele_after_jet = file.Get("h_ele_LHE_HT_after_jet_cut")
h_ele_after_met = file.Get("h_ele_LHE_HT_after_met_cut")

def normalize(hist):
    integral = hist.Integral()
    if integral > 0:
        hist.Scale(1.0 / integral)

normalize(h_before)
normalize(h_ele_before)
normalize(h_ele_after_lepton)
normalize(h_ele_after_jet)
normalize(h_ele_after_met)

c = ROOT.TCanvas("c", "Overlay Plot", 800, 600)

# Set distinct line colors and styles
h_before.SetLineColor(ROOT.kOrange + 7)
h_before.SetLineStyle(1)
h_before.SetLineWidth(2)

h_ele_before.SetLineColor(ROOT.kAzure - 4)
h_ele_before.SetLineStyle(1)
h_ele_before.SetLineWidth(2)

h_ele_after_lepton.SetLineColor(ROOT.kViolet + 1)
h_ele_after_lepton.SetLineStyle(1)
h_ele_after_lepton.SetLineWidth(2)

h_ele_after_jet.SetLineColor(ROOT.kTeal - 7)
h_ele_after_jet.SetLineStyle(1)
h_ele_after_jet.SetLineWidth(2)

h_ele_after_met.SetLineColor(ROOT.kPink + 1)
h_ele_after_met.SetLineStyle(1)
h_ele_after_met.SetLineWidth(2)

# Draw histograms
h_before.Draw("hist")
h_ele_before.Draw("hist same")
h_ele_after_lepton.Draw("hist same")
h_ele_after_jet.Draw("hist same")
h_ele_after_met.Draw("hist same")

# Legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(h_before, "Before Cuts", "l")
legend.AddEntry(h_ele_before, "ele Flavor", "l")
legend.AddEntry(h_ele_after_lepton, "Lepton Pt", "l")
legend.AddEntry(h_ele_after_jet, "Jet Pt", "l")
legend.AddEntry(h_ele_after_met, "MET", "l")
legend.Draw()

# Save the canvas
c.SaveAs("cutflow_ele.png")

# Close the file
file.Close()
