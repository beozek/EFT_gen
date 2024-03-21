import ROOT

def change_histogram_titles(root_file_path, new_titles):
    file = ROOT.TFile(root_file_path, "UPDATE")
    
    for hist_name, new_title in new_titles.items():
        histogram = file.Get(hist_name)
        
        if histogram:
            histogram.SetTitle(new_title)
            histogram.Write()
        else:
            print "Histogram {} not found in the file.".format(hist_name)

    # Close the file
    file.Close()

# Example usage
root_file_path = "../plots_all/hadd_all/output.root" 
new_titles = {

    'h_LHE_HT_0_500_ele_withoutAK8': "LHE_HT Distribution For 0 < Mtt < 500",
    'h_LHE_HT_500_750_ele_withoutAK8' : "LHE_HT Distribution For 500 < Mtt < 750",
    'h_LHE_HT_750_900_ele_withoutAK8'  : "LHE_HT Distribution For 750 < Mtt < 900",
    'h_LHE_HT_900_1250_ele_withoutAK8'  : "LHE_HT Distribution For 900 < Mtt < 1250",
    'h_LHE_HT_1250_1500_ele_withoutAK8'  : "LHE_HT Distribution For 1250 < Mtt < 1500",
    'h_LHE_HT_1500_up_ele_withoutAK8'  : "LHE_HT Distribution For 1500 < Mtt",
    'h_LHE_HT_0_500_ele_AK8200'  : "LHE_HT Distribution For 0 < Mtt < 500",
    'h_LHE_HT_500_750_ele_AK8200'  : "LHE_HT Distribution For 500 < Mtt < 750",
    'h_LHE_HT_750_900_ele_AK8200' : "LHE_HT Distribution For 750 < Mtt < 900",
    'h_LHE_HT_900_1250_ele_AK8200'  : "LHE_HT Distribution For 900 < Mtt < 1250",
    'h_LHE_HT_1250_1500_ele_AK8200' : "LHE_HT Distribution For 1250 < Mtt < 1500",
    'h_LHE_HT_1500_up_ele_AK8200' : "LHE_HT Distribution For 1500 < Mtt ",
    'h_LHE_HT_0_500_ele_AK8400' : "LHE_HT Distribution For 0 < Mtt < 500",
    'h_LHE_HT_500_750_ele_AK8400' : "LHE_HT Distribution For 500 < Mtt < 750",
    'h_LHE_HT_750_900_ele_AK8400' : "LHE_HT Distribution For 750 < Mtt < 900",
    'h_LHE_HT_900_1250_ele_AK8400' : "LHE_HT Distribution For 900 < Mtt < 1250",
    'h_LHE_HT_1250_1500_ele_AK8400' : "LHE_HT Distribution For 1250 < Mtt < 1500",
    'h_LHE_HT_1500_up_ele_AK8400' : "LHE_HT Distribution For 1500 < Mtt ",
    'h_LHE_HT_0_500_muon_withoutAK8' : "LHE_HT Distribution For 0 < Mtt < 500",
    'h_LHE_HT_500_750_muon_withoutAK8' : "LHE_HT Distribution For 500 < Mtt < 750",
    'h_LHE_HT_750_900_muon_withoutAK8' : "LHE_HT Distribution For 750 < Mtt < 900",
    'h_LHE_HT_900_1250_muon_withoutAK8' : "LHE_HT Distribution For 900 < Mtt < 1250",
    'h_LHE_HT_1250_1500_muon_withoutAK8' : "LHE_HT Distribution For 1250 < Mtt < 1500",
    'h_LHE_HT_1500_up_muon_withoutAK8' : "LHE_HT Distribution For 1500 < Mtt",
    'h_LHE_HT_0_500_muon_AK8200' : "LHE_HT Distribution For 0 < Mtt < 500",
    'h_LHE_HT_500_750_muon_AK8200' : "LHE_HT Distribution For 500 < Mtt < 750",
    'h_LHE_HT_750_900_muon_AK8200' : "LHE_HT Distribution For 750 < Mtt < 900",
    'h_LHE_HT_900_1250_muon_AK8200' : "LHE_HT Distribution For 900 < Mtt < 1250",
    'h_LHE_HT_1250_1500_muon_AK8200' : "LHE_HT Distribution For 1250 < Mtt < 1500",
    'h_LHE_HT_1500_up_muon_AK8200' : "LHE_HT Distribution For 1500 < Mtt ",
    'h_LHE_HT_0_500_muon_AK8400'  : "LHE_HT Distribution For 0 < Mtt < 500",
    'h_LHE_HT_500_750_muon_AK8400' : "LHE_HT Distribution For 500 < Mtt < 750",
    'h_LHE_HT_750_900_muon_AK8400' : "LHE_HT Distribution For 750 < Mtt < 900",
    'h_LHE_HT_900_1250_muon_AK8400' : "LHE_HT Distribution For 900 < Mtt < 1250",
    'h_LHE_HT_1250_1500_muon_AK8400' : "LHE_HT Distribution For 1250 < Mtt < 1500",
    'h_LHE_HT_1500_up_muon_AK8400' : "LHE_HT Distribution For 1500 < Mtt "
}

change_histogram_titles(root_file_path, new_titles)
