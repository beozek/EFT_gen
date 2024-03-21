import ROOT
import os
import glob
from array import array
import subprocess
import xml.etree.ElementTree as ET
from DataFormats.FWLite import Events, Handle
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.Config as edm
from XRootD import client
from XRootD.client.flags import DirListFlags, StatInfoFlags, OpenFlags, QueryCode



ROOT.gROOT.SetBatch(True)

totalEvents = 0

h_leptonPt = ROOT.TH1F("h_leptonPt", "Lepton pT; pT (GeV);Events", 100, 0, 1000)
h_topPt = ROOT.TH1F("h_topPt", "Top Quark pT; pT (GeV);Events", 100, 0, 3000)
h_antitopPt = ROOT.TH1F("h_antitopPt", "Anti-Top Quark p_{T}; p_{T} [GeV];Events", 1000, 0, 3000)
h_muonPt = ROOT.TH1F("h_muonPt", "Muon pT; pT (GeV);Events", 100, 0, 1000)
h_muoneta = ROOT.TH1F("h_muoneta", "eta; #eta;Events", 100, -5, 5)
h_electronPt = ROOT.TH1F("h_electronPt", "Electron pT; pT (GeV);Events", 100, 0, 1000)
h_electroneta = ROOT.TH1F("h_electroneta", "eta; #eta;Events", 100, -5, 5)
h_leptoneta = ROOT.TH1F("h_leptoneta", "eta; #eta;Events", 100, -5, 5)
h_leptonphi = ROOT.TH1F("h_leptonphi", "Azimuthal Angle; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
h_invariantMass = ROOT.TH1F("h_invariantMass", "Invariant Mass; M (GeV);Events", 100, 0, 7000)
h_partonMultiplicity = ROOT.TH1F("h_partonMultiplicity", "Jet Multiplicity; N_{jets};Events", 20, 0, 100)
h_MET = ROOT.TH1F("hMET", "MET;MET (GeV);Events", 100, 0, 200)
h_bquark_pt = ROOT.TH1F("hbquarkPt", "b-quark pT;pT (GeV);Events", 100, 0, 1000)
h_bquark_eta = ROOT.TH1F("hbquarkEta", "b-quark #eta;#eta;Events", 100, -5, 5)
h_angle_top_antitop = ROOT.TH1F("h_angle", "Angle between top and antitop;Angle (radians);Events", 50, 0, ROOT.TMath.Pi())

h_decayChannel = ROOT.TH1F("h_decayChannel", "Top Decay Channels; Channel; Events", 2, 0, 2)
h_decayChannel.GetXaxis().SetBinLabel(1, "t -> W+b")
h_decayChannel.GetXaxis().SetBinLabel(2, "Other")


h_topMultiplicity = ROOT.TH1F("h_topMultiplicity", "Top Multiplicity; N_{top};Events", 5, 0, 5)
# h_antitopMultiplicity = ROOT.TH1F("h_antitopMultiplicity", "Anti-Top Multiplicity; N_{antitop};Events", 5, 0, 5)

h_missingParticles = ROOT.TH1F("h_missingParticles", "Missing Particles; Particle Type; Events", 4, 0, 4)
h_missingParticles.GetXaxis().SetBinLabel(1, "No Top")
h_missingParticles.GetXaxis().SetBinLabel(2, "No Anti-Top")
h_missingParticles.GetXaxis().SetBinLabel(3, "No Top & No Anti-Top")



bin_edges = [-16.5, -14.5, -12.5, -10.5, 10.5, 12.5, 14.5, 16.5]
h_leptonFlavor = ROOT.TH1F("h_leptonFlavor", "Lepton Flavor; PDG ID;Events", len(bin_edges)-1, array('d', bin_edges))

h_leptonFlavor.GetXaxis().SetBinLabel(1, "muon-")
h_leptonFlavor.GetXaxis().SetBinLabel(2, "electron-")
h_leptonFlavor.GetXaxis().SetBinLabel(4, "electron+")
h_leptonFlavor.GetXaxis().SetBinLabel(5, "muon+")


h_nonTopMotherJets = ROOT.TH1F("h_nonTopMotherJets", "Jets without Top as Mother; Count;Events", 10, 0, 50)
h_jetMultiplicity = ROOT.TH1F("h_jetMultiplicity", "Number of Jets per Event", 10, 0, 50)

h_topMother = ROOT.TH1F("h_topMother", "Mother of Top Quarks; Mother; Events", 3, 0, 3)
h_topMother.GetXaxis().SetBinLabel(1, "qq")
h_topMother.GetXaxis().SetBinLabel(2, "gg")
h_topMother.GetXaxis().SetBinLabel(3, "Other")

h_motherPdgId = ROOT.TH1F("h_motherPdgId", "PDG ID of Top's Mother;PDG ID;Counts", 23, -6, 22)

h_HT = ROOT.TH1F("h_HT", "HT; HT (GeV);Events", 100, 0, 5000)

def is_light_quark_or_gluon(pdgId):
    return abs(pdgId) < 6 or abs(pdgId) == 21

def is_from_top_or_W(particle):
    mother = particle.mother(0)
    while mother:
        if abs(mother.pdgId()) in [6, 24]:
            return True
        mother = mother.mother(0)
    return False

def analyze(filename):
    events = Events(filename)
    global totalEvents 
    totalEvents += events.size()
    print("Number of events in file:", events.size())
    
    handle = Handle('vector<reco::GenParticle>')
    genJetsHandle = Handle('vector<reco::GenJet>')
    
    lheHandle = Handle('LHEEventProduct')
    
    relevant_pdgIds = {12,14,16,24,1,2,3,4,5,6,21,11,13,15}
   
    for i, event in enumerate(events):
        # GenParticles
        event.getByLabel("prunedGenParticles", handle)
        particles = handle.product()

        particles = [p for p in particles if abs(p.pdgId()) in relevant_pdgIds]

        # GenJets
        events.getByLabel("slimmedGenJets", genJetsHandle)
        jets = genJetsHandle.product()
        
        # Access LHE particles
        event.getByLabel("externalLHEProducer", lheHandle)
        lheEvent = lheHandle.product()
        
        HT = 0
        
        # Loop over LHE particles
        for i in range(lheEvent.hepeup().NUP):
            pdgId = lheEvent.hepeup().IDUP[i]
            status = lheEvent.hepeup().ISTUP[i] # status
            px = lheEvent.hepeup().PUP[i][0]  # px
            py = lheEvent.hepeup().PUP[i][1]  # py
            
            if status == 1: 
                pT = (px**2 + py**2)**0.5
                HT += pT
        h_HT.Fill(HT)
        # print("HT: ", HT)
   
        
        # print("Number of particles in event:", len(particles))
        
        tops = []
        bquarks = []
        leptons = []
        neutrinos = []
        partons = []
        non_top_mother_jet_count_j = []
        
        top = None
        antitop = None
        
        top_count = 0
        antitop_count = 0
        not_top = 0
        jet_count = 0
        non_top_mother_jet_count = 0
        

        
        for jet in jets:
            jet_count +=1
            
            mother = jet.mother()
            if mother and mother.pdgId() not in [6, -6]:
                non_top_mother_jet_count_j.append(jet)

        
        h_jetMultiplicity.Fill(len(jets))  
        h_nonTopMotherJets.Fill(len(non_top_mother_jet_count_j))
                
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
                
                # Check the mothers of the top and antitop
                mother1 = particle.mother(0)
                mother2 = particle.numberOfMothers() > 1 and particle.mother(1) or None
                if mother1:
                    h_motherPdgId.Fill(mother1.pdgId())
                if mother2:
                    h_motherPdgId.Fill(mother2.pdgId())
                    
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
                    
                tops.append(particle)
                h_decayChannel.Fill(0)  # t -> W+b
                
                if particle.pdgId() == 6:
                    top_count += 1
                    h_topPt.Fill(particle.pt())
                    top = ROOT.TLorentzVector()
                    top.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                elif particle.pdgId() == -6:
                    antitop_count += 1
                    h_antitopPt.Fill(particle.pt())
                    antitop = ROOT.TLorentzVector()
                    antitop.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                
                has_high_pt_lepton = False
                for j in range(w_quark_daughter.numberOfDaughters()):
                    lepton_candidate = w_quark_daughter.daughter(j)
                    # if abs(lepton_candidate.pdgId()) in [11, 13] and lepton_candidate.pt() > 30 and abs(lepton_candidate.eta()) < 2.4:
                    if abs(lepton_candidate.pdgId()) in [11, 13]:
                        has_high_pt_lepton = True
                        lepton = lepton_candidate 
                        h_leptonPt.Fill(lepton.pt())
                        h_leptoneta.Fill(lepton.eta())
                        h_leptonphi.Fill(lepton.phi())
                        h_leptonFlavor.Fill(lepton.pdgId())
                        if abs(lepton_candidate.pdgId()) in [13]:
                            h_muonPt.Fill(lepton.pt())
                            h_muoneta.Fill(lepton.eta())
                            
                        if abs(lepton_candidate.pdgId()) in [11]:
                            h_electronPt.Fill(lepton.pt())
                            h_electroneta.Fill(lepton.eta())
                      
                if not has_high_pt_lepton:
                    continue
                
                if mother1 and mother2 and set([abs(mother1.pdgId()), abs(mother2.pdgId())]) == {21}:
                    h_topMother.Fill(1)  # gg
                elif mother1 and mother2 and set([abs(mother1.pdgId()), abs(mother2.pdgId())]).issubset({1,2,3,4,5}):
                    h_topMother.Fill(0)  # qq
                else:
                    h_topMother.Fill(2)  # Other
        
        
            # Partons
            if abs(pdgId) in [1, 2, 3, 4, 5, 6, 21]:
                partons.append(particle) 
            
            
            if abs(pdgId) == 5:
                bquarks.append(particle)
                
                b_vector = ROOT.TLorentzVector()
                b_vector.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                
                if pdgId == 5:
                    h_bquark_pt.Fill(b_vector.Pt())
                    h_bquark_eta.Fill(b_vector.Eta())

        
            if abs(pdgId) in [12, 14, 16]:
                neutrino = ROOT.TLorentzVector()
                neutrino.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                h_MET.Fill(neutrino.Pt())
                
        h_partonMultiplicity.Fill(len(partons))
        h_topMultiplicity.Fill(len(tops))
        # h_antitopMultiplicity.Fill(antitop_count)
        
        if top_count == 0:
            h_missingParticles.Fill(0)  # Filling "no top" bin

        if antitop_count == 0:
            h_missingParticles.Fill(1)  # Filling "no antitop" bin

        if top_count == 0 and antitop_count == 0:
            h_missingParticles.Fill(2)  # Filling "no top and antitop" bin
     
        if top and antitop:
            ttbar = top + antitop
            h_invariantMass.Fill(ttbar.M())
            h_angle_top_antitop.Fill(top.Angle(antitop.Vect()))


url = "root://cmsxrootd.fnal.gov/"
path = "/store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/006455CD-9CDB-B843-B50D-5721C39F30CE.root"

# client_instance = client.FileSystem(url)
# status, listing = client_instance.dirlist(path, DirListFlags.STAT)
# root_files = [entry.name for entry in listing if entry.name.endswith('.root')]
# root_files = root_files[:2]

# for root_file in root_files:
full_path = url + os.path.join(path)
analyze(full_path)

def normalize_histogram(hist):
    for bin in range(1, hist.GetNbinsX() + 1):
        content = hist.GetBinContent(bin)
        error = hist.GetBinError(bin)
        hist.SetBinContent(bin, content / (totalEvents))
        hist.SetBinError(bin, error / (totalEvents))

# Normalize histograms before drawing them
histograms = [h_leptonPt, h_topPt, h_leptoneta, h_leptonphi, h_invariantMass, h_MET,
              h_bquark_pt, h_bquark_eta, h_muonPt,h_muoneta, h_electronPt, h_electroneta, h_antitopPt, h_HT ]

for hist in histograms:
    normalize_histogram(hist)

c_leptonPt = ROOT.TCanvas("c_leptonPt", "Lepton pT Distribution", 800, 600)
h_leptonPt.Draw("HIST")
ROOT.gPad.SetLogy(1)
c_leptonPt.SaveAs("leptonPtDistribution.png")

c_muonPt = ROOT.TCanvas("c_muonPt", "Muon pT Distribution", 800, 600)
h_muonPt.Draw("HIST")
ROOT.gPad.SetLogy(1)
c_muonPt.SaveAs("muonPtDistribution.png")

c_muoneta = ROOT.TCanvas("c_muonEta", "Muon eta Distribution", 800, 600)
h_muoneta.Draw("HIST")
c_muoneta.SaveAs("muonEtaDistribution.png")

c_electronPt = ROOT.TCanvas("c_electronPt", "Electron pT Distribution", 800, 600)
h_electronPt.Draw("HIST")
ROOT.gPad.SetLogy(1)
c_electronPt.SaveAs("electronPtDistribution.png")

c_electroneta = ROOT.TCanvas("c_electronEta", "Electron eta Distribution", 800, 600)
h_electroneta.Draw("HIST")
c_electroneta.SaveAs("electronEtaDistribution.png")


c_topPt = ROOT.TCanvas("c_topPt", "Top Quark pT Distribution", 800, 600)
h_topPt.Draw("HIST")
ROOT.gPad.SetLogy(1)
c_topPt.SaveAs("topPtDistribution.png")

c_antitopPt = ROOT.TCanvas("c_antitopPt", "Anti-Top Quark pT Distribution", 800, 600)
h_antitopPt.Draw("HIST")
ROOT.gPad.SetLogy(1)
c_antitopPt.SaveAs("antitopPtDistribution.png")

c_eta = ROOT.TCanvas("c_eta", "Lepton Eta Distribution", 800, 600)
h_leptoneta.Draw("HIST")
c_eta.SaveAs("etaDistribution.png")

# c_phi = ROOT.TCanvas("c_phi", "Lepton Azimuthal Angle Distribution", 800, 600)
# h_leptonphi.Draw("HIST")
# c_phi.SaveAs("phiDistribution.png")

c_invariantMass = ROOT.TCanvas("c_invariantMass", "Invariant Mass Distribution", 800, 600)
h_invariantMass.Draw("HIST")
ROOT.gPad.SetLogy(1)
c_invariantMass.SaveAs("invariantMassDistribution.png")

# c_decay = ROOT.TCanvas("c_decay", "Decay Channel Canvas", 800, 600)
# h_decayChannel.Draw("HIST")
# c_decay.SaveAs("topDecayChannel.png")

c_MET = ROOT.TCanvas("cMET", "MET Distribution", 800, 600)
h_MET.Draw("HIST")
ROOT.gPad.SetLogy(1)
c_MET.SaveAs("METDistribution.png")

# c_leptonFlavor = ROOT.TCanvas("c_leptonFlavor", "Lepton Flavor Distribution", 800, 600)
# h_leptonFlavor.Draw("HIST")
# c_leptonFlavor.SaveAs("leptonFlavorDistribution.png")

c_bquark_pt = ROOT.TCanvas("cbquarkPt", "b-quark pT Distribution", 800, 600)
h_bquark_pt.Draw("HIST")
ROOT.gPad.SetLogy(1)
c_bquark_pt.SaveAs("bquarkPtDistribution.png")

c_bquark_eta = ROOT.TCanvas("cbquarkEta", "b-quark Eta Distribution", 800, 600)
h_bquark_eta.Draw("HIST")
c_bquark_eta.SaveAs("bquarkEtaDistribution.png")

c_HT = ROOT.TCanvas("HT", "HT Distribution No Cut", 800, 600)
h_HT.Draw("HIST")
c_HT.SaveAs("HT_LHEpart.png")


print("Total number of events:", totalEvents)



# analyze("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/root_files/0000/GEN_LO_01j_102X_14.root")