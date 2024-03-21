import ROOT
ROOT.gROOT.SetBatch(True)

def create_and_fill_histograms(filename):
    file = ROOT.TFile(filename, "READ")
    tree = file.Get("Events")

    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kCyan, ROOT.kOrange]
    histograms = []
    max_y = 0

    for i in range(6):
        hist = ROOT.TH1F("h_scale_var_%d" % i, "Scale Variation %d;Scale Weight;Events" % i, 100, 0.5, 1.5)
        hist.SetLineColor(colors[i])
        hist.SetLineWidth(2)
        histograms.append(hist)

    scale_indices = [0, 1, 3, 4, 6, 7]

    for event in tree:
        lheScaleWeights = getattr(event, "LHEScaleWeight")
        for idx, scale_weight in enumerate(lheScaleWeights):
            if idx in scale_indices:
                hist_index = scale_indices.index(idx)
                histograms[hist_index].Fill(scale_weight)
                max_bin_content = histograms[hist_index].GetBinContent(histograms[hist_index].GetMaximumBin())
                if max_bin_content > max_y:
                    max_y = max_bin_content

    canvas = ROOT.TCanvas("canvas", "Overlay of Scale Variations", 800, 600)
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.SetHeader("Scale Variations", "C")
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    histograms[0].SetMaximum(max_y * 1.2)  
    histograms[0].Draw("HIST")
    for i, hist in enumerate(histograms[1:], 1):
        hist.Draw("HIST SAME")
        legend.AddEntry(hist, "Variation %d" % i, "l")

    legend.Draw()
    canvas.SaveAs("scale_variations_overlay.png")

    file.Close()

if __name__ == "__main__":
    create_and_fill_histograms("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/nano_files/1j1l_NoHT_NoNu/nanogen_123_1.root")  