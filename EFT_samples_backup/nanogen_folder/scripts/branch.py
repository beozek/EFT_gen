import ROOT

# Open the ROOT file
file = ROOT.TFile.Open("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/nano_files/1j1l_NoHT/nanogen_123_1.root")

# Assuming the TTree is named "Events" (this is common but might be different in your file)
tree = file.Get("Events")

# Print the branch names
for branch in tree.GetListOfBranches():
    print(branch.GetName())

file.Close()
