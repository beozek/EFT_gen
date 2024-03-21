import ROOT

file = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_all/hadd_all/output.root") 

h_before = file.Get("h_LHE_HT_before")
h_ele_before = file.Get("h_ele_LHE_HT_before")
h_ele_after_lepton = file.Get("h_ele_LHE_HT_after_lepton_cut")
h_ele_after_jet = file.Get("h_ele_LHE_HT_after_jet_cut")
h_ele_after_met = file.Get("h_ele_LHE_HT_after_met_cut")
h_ele_after_pt200 = file.Get("h_ele_LHE_HT_after_toppt200_cut")
h_ele_after_pt400 = file.Get("h_ele_LHE_HT_after_toppt400_cut")

h_denominator = h_before.Clone("h_denominator")

h_ratio_ele_before = h_ele_before.Clone("h_ratio_ele_before")
h_ratio_ele_before.Divide(h_denominator)

h_ratio_ele_after_lepton = h_ele_after_lepton.Clone("h_ratio_ele_after_lepton")
h_ratio_ele_after_lepton.Divide(h_denominator)

h_ratio_ele_after_jet = h_ele_after_jet.Clone("h_ratio_ele_after_jet")
h_ratio_ele_after_jet.Divide(h_denominator)

h_ratio_ele_after_met = h_ele_after_met.Clone("h_ratio_ele_after_met")
h_ratio_ele_after_met.Divide(h_denominator)

c = ROOT.TCanvas("c", "Cutflow Ratios", 800, 600)
c.Divide(2, 2) 

c.cd(1)
h_ratio_ele_before.SetTitle("Ratio After ele Flavor Selection")
h_ratio_ele_before.Draw()

c.cd(2)
h_ratio_ele_after_lepton.SetTitle("Ratio After Lepton Pt Cut")
h_ratio_ele_after_lepton.Draw()

c.cd(3)
h_ratio_ele_after_jet.SetTitle("Ratio After Jet Pt Cut")
h_ratio_ele_after_jet.Draw()

c.cd(4)
h_ratio_ele_after_met.SetTitle("Ratio After MET Cut")
h_ratio_ele_after_met.Draw()

c.SaveAs("ratio_plots_ele.png")

file.Close()
