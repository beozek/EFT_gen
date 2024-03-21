import ROOT

file = ROOT.TFile("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/output_weights_NoNu_latest/output_EFT_ctGreweighted.root", "READ")

histograms = [
    'h_leptonPt_scale', 'h_leptonEta_scale',
    'h_electronPt_scale', 'h_electronEta_scale',
    'h_muonPt_scale', 'h_muonEta_scale',
    'h_topPt_scale', 'h_topEta_scale',
    'h_antitopPt_scale', 'h_antitopEta_scale',
    'h_invariantMass_scale',
    'h_leading_jet_pt_scale', 'h_second_leading_jet_pt_scale',
    'h_jet_multiplicity_ishardprocess_scale', 'h_jet_multiplicity_last_copy_scale'
]
    
variations = [0,1,3,4,6,7]  #number of scale weights

output_file = ROOT.TFile("envelope_output_ctGRe.root", "RECREATE")

for histname in histograms:
    min_hist = None
    max_hist = None
    
    for ivar in variations:
        hist_name = "{}_{}".format(histname, ivar)
        hist = file.Get(hist_name)

        if not hist:
            print("Histogram not found:", hist_name)
            continue
        
        if min_hist is None:
            min_hist = hist.Clone("{}_Down".format(histname))
            max_hist = hist.Clone("{}_Up".format(histname))
            min_hist.Reset()
            max_hist.Reset()
        
            for ibin in range(1, hist.GetNbinsX() + 1):
                min_hist.SetBinContent(ibin, hist.GetBinContent(ibin))
                max_hist.SetBinContent(ibin, hist.GetBinContent(ibin))
                
        else:
            for ibin in range(1, hist.GetNbinsX() + 1):
                bin_content = hist.GetBinContent(ibin)
                if bin_content < min_hist.GetBinContent(ibin):
                    min_hist.SetBinContent(ibin, bin_content)
                if bin_content > max_hist.GetBinContent(ibin):
                    max_hist.SetBinContent(ibin, bin_content)

    
    min_hist.Write()
    max_hist.Write()

output_file.Close()
file.Close()