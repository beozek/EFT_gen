import ROOT

file = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_all/hadd_all/output.root") 

h_before = file.Get("h_LHE_HT_before")
# h_muon_before = file.Get("h_muon_LHE_HT_before")
h_muon_after_lepton = file.Get("h_muon_LHE_HT_after_lepton_cut")
h_muon_after_jet = file.Get("h_muon_LHE_HT_after_jet_cut")
h_muon_after_met = file.Get("h_muon_LHE_HT_after_met_cut")
h_muon_after_pt200 = file.Get("h_muon_LHE_HT_after_toppt200_cut")
h_muon_after_pt400 = file.Get("h_muon_LHE_HT_after_toppt400_cut")


# def normalize(hist):
#     integral = hist.Integral()
#     if integral > 0:
#         hist.Scale(1.0 / integral)

# normalize(h_before)
# normalize(h_muon_before)
# normalize(h_muon_after_lepton)
# normalize(h_muon_after_jet)
# normalize(h_muon_after_met)
# normalize(h_muon_after_pt200)
# normalize(h_muon_after_pt400)

c = ROOT.TCanvas("c", "Cutflow Plot", 800, 600)
c.SetLogy()

# alpha = 0.35

h_before.SetLineColor(ROOT.kBlack)
h_before.SetLineStyle(1)
h_before.SetLineWidth(2)
# h_before.SetFillColorAlpha(ROOT.kBlack, alpha)
h_before.Draw("hist")

# h_muon_before.SetLineColor(ROOT.kBlue)
# h_muon_before.SetLineStyle(2)
# h_muon_before.SetLineWidth(2)
# # h_muon_before.SetFillColorAlpha(ROOT.kBlue, alpha)
# h_muon_before.Draw("hist same")

h_muon_after_lepton.SetLineColor(ROOT.kRed)
h_muon_after_lepton.SetLineStyle(3)
h_muon_after_lepton.SetLineWidth(2)
# h_muon_after_lepton.SetFillColorAlpha(ROOT.kRed, alpha)
h_muon_after_lepton.Draw("hist same")

h_muon_after_jet.SetLineColor(ROOT.kGreen)
h_muon_after_jet.SetLineStyle(4)
h_muon_after_jet.SetLineWidth(2)
# h_muon_after_jet.SetFillColorAlpha(ROOT.kGreen, alpha)
h_muon_after_jet.Draw("hist same")

h_muon_after_met.SetLineColor(ROOT.kMagenta)
h_muon_after_met.SetLineStyle(5)
h_muon_after_met.SetLineWidth(2)
# h_muon_after_met.SetFillColorAlpha(ROOT.kMagenta, alpha)
h_muon_after_met.Draw("hist same")

h_muon_after_pt200.SetLineColor(ROOT.kOrange)
h_muon_after_pt200.SetLineStyle(6)
h_muon_after_pt200.SetLineWidth(2)
# h_muon_after_pt200.SetFillColorAlpha(ROOT.kOrange, alpha)
h_muon_after_pt200.Draw("hist same")

h_muon_after_pt400.SetLineColor(ROOT.kYellow)
h_muon_after_pt400.SetLineStyle(7)
h_muon_after_pt400.SetLineWidth(2)
# h_muon_after_pt400.SetFillColorAlpha(ROOT.kYellow, alpha)
h_muon_after_pt400.Draw("hist same")


legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(h_before, "Before Cuts", "l")
# legend.AddEntry(h_muon_before, "Muon", "l")
legend.AddEntry(h_muon_after_lepton, "Lepton Pt", "l")
legend.AddEntry(h_muon_after_jet, "Jet Pt", "l")
legend.AddEntry(h_muon_after_met, "MET", "l")
legend.AddEntry(h_muon_after_pt200, "Top_Pt>200", "l")
legend.AddEntry(h_muon_after_pt400, "Top_Pt>400", "l")
legend.Draw()

c.SaveAs("cutflow_plot_muon.png")

file.Close()
