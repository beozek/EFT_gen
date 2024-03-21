import ROOT

def count_events_in_range(histogram, x_min, x_max):

    bin_min = histogram.FindBin(x_min)
    bin_max = histogram.FindBin(x_max)
    return histogram.Integral(bin_min, bin_max - 1)

root_file = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_all/hadd_all/output.root", "READ")

h_some_histogram = root_file.Get("h_LHE_HT_0_500_ele_withoutAK8")
  # 'h_LHE_HT_0_500_ele_withoutAK8',
    # 'h_LHE_HT_500_750_ele_withoutAK8',
    # 'h_LHE_HT_750_900_ele_withoutAK8',
    # 'h_LHE_HT_900_1250_ele_withoutAK8',
    # 'h_LHE_HT_1250_1500_ele_withoutAK8',
    # 'h_LHE_HT_1500_up_ele_withoutAK8',
     # 'h_LHE_HT_0_500_muon_withoutAK8',
    # 'h_LHE_HT_500_750_muon_withoutAK8',
    # 'h_LHE_HT_750_900_muon_withoutAK8',
    # 'h_LHE_HT_900_1250_muon_withoutAK8',
    # 'h_LHE_HT_1250_1500_muon_withoutAK8',
    # 'h_LHE_HT_1500_up_muon_withoutAK8',

ranges = [(0, 500), (500, 800), (800, 1e6), (500, 1e6)]  # Using 1e6 as an upper bound for 'up'

for x_min, x_max in ranges:
    event_count = count_events_in_range(h_some_histogram, x_min, x_max)
    print "Number of events between %s and %s: %s" % (x_min, x_max, event_count)

root_file.Close()
