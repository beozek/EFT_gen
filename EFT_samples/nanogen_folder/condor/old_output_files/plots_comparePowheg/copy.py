import ROOT
ROOT.gROOT.SetBatch(True)
f = ROOT.TFile("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_comparePowheg/output_EFT_hardprocess.root", "UPDATE")
hist = f.Get("h_pdgId_fromhardprocess")

c = ROOT.TCanvas("c", "canvas", 800, 600)

axis = hist.GetXaxis()
for bin in range(1, axis.GetNbins() + 1):
    label = str(int(axis.GetBinLowEdge(bin) + axis.GetBinWidth(bin) / 2))
    axis.SetBinLabel(bin, label)
    # if bin % 2 == 0:
    #     label = str(int(axis.GetBinLowEdge(bin) + axis.GetBinWidth(bin) / 2))
    #     axis.SetBinLabel(bin, label)
    # else:
    #     axis.SetBinLabel(bin, "") 

hist.Draw()
c.SaveAs("{}.pdf".format("fromhardcopy"))

f.Write()
f.Close()
