import ROOT
import os
import glob
from array import array
from DataFormats.FWLite import Events, Handle
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.Config as edm
from XRootD import client
from XRootD.client.flags import DirListFlags, StatInfoFlags, OpenFlags, QueryCode
from multiprocessing import Pool

ROOT.gROOT.SetBatch(True)

totalEvents = 0

# Define only the b-quark pT histogram with a focus on the 0-20 GeV range
h_bquark_pt = ROOT.TH1F("hbquarkPt", "b-quark pT;pT (GeV);Events", 100, 0, 20)

def analyze(filename):
    print("Processing file:", filename)
    events = Events(filename)
    global totalEvents 
    totalEvents += events.size()
    print("Number of events in file:", events.size())
    
    handle = Handle('vector<reco::GenParticle>')
    
    relevant_pdgIds = {5,6,24,11,13}
   
    for event in events:
        # GenParticles
        event.getByLabel("genParticles", handle)
        particles = handle.product()

        particles = [p for p in particles if abs(p.pdgId()) in relevant_pdgIds]

        for particle in particles:
            pdgId = particle.pdgId()

            # Tops
            if abs(pdgId) == 6: 

                has_top_daughter = False
                for i in range(particle.numberOfDaughters()):
                    daughter = particle.daughter(i)
                    if abs(daughter.pdgId()) == 6:
                        has_top_daughter = True
                        break
                if has_top_daughter:
                    continue
                    
                # Checking for W and b quark daughters
                w_quark_daughter = None
                b_quark_daughter = None
                for i in range(particle.numberOfDaughters()):
                    daughter = particle.daughter(i)
                    if abs(daughter.pdgId()) == 24:
                        w_quark_daughter = daughter
                    elif abs(daughter.pdgId()) == 5:
                        b_quark_daughter = daughter
                        
                if not w_quark_daughter or not b_quark_daughter:
                    continue
                
                has_high_pt_lepton = False
                for j in range(w_quark_daughter.numberOfDaughters()):
                    lepton_candidate = w_quark_daughter.daughter(j)
                    # if abs(lepton_candidate.pdgId()) in [11, 13] and lepton_candidate.pt() > 30 and abs(lepton_candidate.eta()) < 2.4:
                    if abs(lepton_candidate.pdgId()) in [11, 13]:
                        has_high_pt_lepton = True
                        
                
                if not has_high_pt_lepton:
                    continue
                
            if abs(pdgId) == 5:
                
                b_vector = ROOT.TLorentzVector()
                b_vector.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                
                if pdgId == 5:
                    h_bquark_pt.Fill(b_vector.Pt())

url = "root://eos.grid.vbc.ac.at/"
path = "/store/user/schoef/TT01j1lCA_HT500_v2/TT01j1lCA_HT500_v2/230918_163019/0000"
client_instance = client.FileSystem(url)
status, listing = client_instance.dirlist(path, DirListFlags.STAT)
root_files = [entry.name for entry in listing if entry.name.endswith('.root')]
root_files = root_files[:5]

for root_file in root_files:
    full_path = url + os.path.join(path, root_file)
    analyze(full_path)

# Plot the combined histogram
c_bquark_pt = ROOT.TCanvas("cbquarkPt", "b-quark pT Distribution", 800, 600)
h_bquark_pt.Draw()
ROOT.gPad.SetLogy(1)
c_bquark_pt.SaveAs("bquarkPtDistribution.png")


