import ROOT

# Open the ROOT file
file = ROOT.TFile.Open("root://eos.grid.vbc.ac.at//store/user/schoef/TT01j1lCA_HT500_v2/TT01j1lCA_HT500_v2/230918_163019/0000/GEN_LO_0j_102X_1.root")
# Assuming the TTree is named "Events" (this is common but might be different in your file)
tree = file.Get("Events")

# Print the branch names
for branch in tree.GetListOfBranches():
    print(branch.GetName())

file.Close()
