import ROOT
import os

ROOT.gROOT.SetBatch(True)

totalEvents = 0

# Define only the b-quark pT histogram with a focus on the 0-20 GeV range
h_bquark_pt = ROOT.TH1F("hbquarkPt", "b-quark pT;pT (GeV);Events", 100, 0, 20)

def analyze(filename):
    print("Processing file:", filename)
    
    file = ROOT.TFile.Open(filename)
    tree = file.Get("Events")
    
    global totalEvents
    totalEvents += tree.GetEntries()
    print("Number of events in file:", tree.GetEntries())
    
    relevant_pdgIds = {5, 6, 24, 11, 13}
    
    for entry in tree:
        nGenPart = entry.nGenPart
        
        for i in range(nGenPart):
            pdgId = entry.GenPart_pdgId[i]
            pt = entry.GenPart_pt[i]
            eta = entry.GenPart_eta[i]
            phi = entry.GenPart_phi[i]
            mass = entry.GenPart_mass[i]

            if abs(pdgId) in relevant_pdgIds:
                # Tops
                if abs(pdgId) == 6:
                    
                    # Check for top daughters
                    has_top_daughter = any(abs(entry.GenPart_pdgId[j]) == 6 for j in range(nGenPart))
                    if has_top_daughter:
                        continue

                    # Checking for W and b quark daughters
                    w_quark_daughter = [j for j in range(nGenPart) if abs(entry.GenPart_pdgId[j]) == 24]
                    b_quark_daughter = [j for j in range(nGenPart) if abs(entry.GenPart_pdgId[j]) == 5]

                    if not w_quark_daughter or not b_quark_daughter:
                        continue
                    
                    has_high_pt_lepton = any(abs(entry.GenPart_pdgId[j]) in [11, 13] for j in range(nGenPart))
                    if not has_high_pt_lepton:
                        continue

                # b-quarks
                if abs(pdgId) == 5:
                    b_vector = ROOT.TLorentzVector()
                    b_vector.SetPtEtaPhiM(pt, eta, phi, mass)
                    h_bquark_pt.Fill(b_vector.Pt())
                        
    file.Close()

path = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/nano_files/"
root_files = [f for f in os.listdir(path) if f.endswith('.root')]
root_files = root_files[:5]

for root_file in root_files:
    full_path = os.path.join(path, root_file)
    analyze(full_path)
    
    
# Plot the combined histogram
c_bquark_pt = ROOT.TCanvas("cbquarkPt", "b-quark pT Distribution", 800, 600)
h_bquark_pt.Draw()
ROOT.gPad.SetLogy(1)
c_bquark_pt.SaveAs("bquarkPtDistribution_nano.png")


