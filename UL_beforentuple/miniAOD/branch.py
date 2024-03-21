import ROOT

file = ROOT.TFile.Open('root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/006455CD-9CDB-B843-B50D-5721C39F30CE.root', 'READ')

tree = file.Get('Events')

# tree.Print()

for branch in tree.GetListOfBranches():
    print(branch.GetName())
