import ROOT
ROOT.gROOT.SetBatch(True)

h_nominal = ROOT.TH1F("h_nominal", "Nominal", 10, 0, 10)
h_weighted = ROOT.TH1F("h_weighted", "Weighted", 10, 0, 10)

for x in range(1, 11): 
    h_nominal.Fill(x)
    h_weighted.Fill(x, 3) 

for i in range(1, h_nominal.GetNbinsX() + 1):
    print("Bin {}, Nominal: {}, Weighted: {}". format(i,h_nominal.GetBinContent(i), h_weighted.GetBinContent(i)))

c = ROOT.TCanvas("c", "Comparison", 800, 600)
h_nominal.SetLineColor(ROOT.kBlue)
h_weighted.SetLineColor(ROOT.kRed)

h_weighted.Draw("hist")
h_nominal.Draw("histsame")
c.SaveAs("comparison.png")
