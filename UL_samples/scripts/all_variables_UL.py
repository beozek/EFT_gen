import ROOT
import os
import glob
import traceback
from array import array
from DataFormats.FWLite import Events, Handle
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.Config as edm



ROOT.gROOT.SetBatch(True)

totalEvents = 0

h_leptonPt = ROOT.TH1F("h_leptonPt", "Lepton pT; pT (GeV);Events", 1000, 0, 1000)
h_topPt = ROOT.TH1F("h_topPt", "Top Quark pT; pT (GeV);Events", 1000, 0, 3000)
h_antitopPt = ROOT.TH1F("h_antitopPt", "Anti-Top Quark p_{T}; p_{T} [GeV];Events", 1000, 0, 3000)
h_leptoneta = ROOT.TH1F("h_leptoneta", "eta; #eta;Events", 100, -5, 5)
h_leptonphi = ROOT.TH1F("h_leptonphi", "Azimuthal Angle; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
h_invariantMass = ROOT.TH1F("h_invariantMass", "Invariant Mass; M (GeV);Events", 100, 0, 7000)
h_partonMultiplicity = ROOT.TH1F("h_partonMultiplicity", "Jet Multiplicity; N_{jets};Events", 20, 0, 100)
h_MET = ROOT.TH1F("hMET", "MET;MET (GeV);Events", 100, 0, 200)
h_bquark_pt = ROOT.TH1F("hbquarkPt", "b-quark pT;pT (GeV);Events", 150, 0, 1000)
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

h_leptonFlavor.GetXaxis().SetBinLabel(1, "tau-")
h_leptonFlavor.GetXaxis().SetBinLabel(2, "muon-")
h_leptonFlavor.GetXaxis().SetBinLabel(3, "electron-")
h_leptonFlavor.GetXaxis().SetBinLabel(5, "electron+")
h_leptonFlavor.GetXaxis().SetBinLabel(6, "muon+")
h_leptonFlavor.GetXaxis().SetBinLabel(7, "tau+")


h_nonTopMotherJets = ROOT.TH1F("h_nonTopMotherJets", "Jets without Top as Mother; Count;Events", 10, 0, 50)
h_jetMultiplicity = ROOT.TH1F("h_jetMultiplicity", "Number of Jets per Event", 10, 0, 50)

h_topMother = ROOT.TH1F("h_topMother", "Mother of Top Quarks; Mother; Events", 3, 0, 3)
h_topMother.GetXaxis().SetBinLabel(1, "qq")
h_topMother.GetXaxis().SetBinLabel(2, "gg")
h_topMother.GetXaxis().SetBinLabel(3, "Other")

h_motherPdgId = ROOT.TH1F("h_motherPdgId", "PDG ID of Top's Mother;PDG ID;Counts", 23, -6, 22)

relevant_pdgIds = {12,14,16,24,1,2,3,4,5,6,21,11,13,15}

def analyze(filename):
    
    file = ROOT.TFile(filename)
    tree = file.Get("AnalysisTree")
    
    tree.SetBranchStatus('*', 0)
    
    branches = [
        "GenParticles", "slimmedGenJets", 
        "GenParticles.m_pdgId", "GenParticles.m_pt", "GenParticles.m_eta", 
        "GenParticles.m_phi", "GenParticles.m_energy", "GenParticles.m_mother1", 
        "GenParticles.m_mother2", "GenParticles.m_daughter1", "GenParticles.m_daughter2", 
        "GenParticles.m_spin", "slimmedGenJets.m_pdgId", "slimmedGenJets.m_pt", 
        "slimmedGenJets.m_eta", "slimmedGenJets.m_phi", "slimmedGenJets.m_energy"
    ]
    
    for branch in branches:
        tree.SetBranchStatus(branch, 1)
    
    # tree.SetBranchStatus('GenParticles*', 1)
    # tree.SetBranchStatus('slimmedGenJets*', 1)

    # GenParticles arrays
    genParticles_count = array('i', [0])
    
    m_pdgId = array('h', [0]*1000) 
    m_pt = array('f', [0.]*1000)    
    m_eta = array('f', [0.]*1000)
    m_phi = array('f', [0.]*1000)
    m_energy = array('f', [0.]*1000)
    m_mother1 = array('h', [0]*1000)
    m_mother2 = array('h', [0]*1000)
    m_daughter1 = array('h', [0]*1000)
    m_daughter2 = array('h', [0]*1000) 
    m_spin = array('h', [0]*1000)
    
    tree.SetBranchAddress("GenParticles", genParticles_count)
    tree.SetBranchAddress("GenParticles.m_pdgId", m_pdgId)
    tree.SetBranchAddress("GenParticles.m_pt", m_pt)
    tree.SetBranchAddress("GenParticles.m_eta", m_eta)
    tree.SetBranchAddress("GenParticles.m_phi", m_phi)
    tree.SetBranchAddress("GenParticles.m_energy", m_energy) 
    tree.SetBranchAddress("GenParticles.m_mother1", m_mother1)
    tree.SetBranchAddress("GenParticles.m_mother2", m_mother2)
    tree.SetBranchAddress("GenParticles.m_daughter1", m_daughter1)
    tree.SetBranchAddress("GenParticles.m_daughter2", m_daughter2)
    tree.SetBranchAddress("GenParticles.m_spin", m_spin)

       
    
    
    # slimmedGenJets arrays
    slimmedGenJets_count = array('i', [0])
    jet_pdgId = array('h', [0]*1000) 
    jet_pt = array('f', [0.]*1000)    
    jet_eta = array('f', [0.]*1000)
    jet_phi = array('f', [0.]*1000)
    jet_energy = array('f', [0.]*1000)
    
    tree.SetBranchAddress("slimmedGenJets", slimmedGenJets_count)
    tree.SetBranchAddress("slimmedGenJets.m_pdgId", jet_pdgId)
    tree.SetBranchAddress("slimmedGenJets.m_pt", jet_pt)
    tree.SetBranchAddress("slimmedGenJets.m_eta", jet_eta)
    tree.SetBranchAddress("slimmedGenJets.m_phi", jet_phi)
    tree.SetBranchAddress("slimmedGenJets.m_energy", jet_energy)
        
        
    n_events = tree.GetEntries()
    print("Number of events in the tree in the file:", n_events)
  
  
    count = 0
    
    for event in tree.GetEntries():
        print()
        
        particles = [
            {
                "pdgId": m_pdgId[j],
                "pt": pt[j], 
                "eta": eta[j], 
                "phi": phi[j], 
                "energy": energy[j], 
                "mother1": mother1[j], 
                "mother2": mother2[j], 
                "daughter1": daughter1[j], 
                "daughter2": daughter2[j], 
                "spin": spin[j]
                }
            for j in range(genParticles_count[0]) if abs(m_pdgId[j]) in relevant_pdgIds
        ]
        
        
        # GenJets
        jets = [
            {
                "pt": jet_pt[j],
                "eta": jet_eta[j],
                "phi": jet_phi[j],
                "energy": jet_energy[j],
            }
            for j in range(slimmedGenJets_count[0])
        ]
                
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
        
    
        
        for j in range(event.slimmedGenJets.size()):
            jet_count +=1
            
            mother = jet.mother()
            if mother and mother.pdgId() not in [6, -6]:
                non_top_mother_jet_count_j.append(jet)

        
        # h_jetMultiplicity.Fill(len(jets))  
        # h_nonTopMotherJets.Fill(len(non_top_mother_jet_count_j))
                
        # Iterates over each particle in the list. checks if the particle is a top of antitop. 
        # finds the mothers of the tops. makes sure that the mothers are not tops.for each particle that is top, it looks for W boson and bquark daughters
        #if both W and b quark daugthers are found, the particle is appended to the tops list. 
        #we are ensuring that we're only counting hard scatter tops and not tops from decay chain of another top. 
        
        #each top has a mother which isn't a top.
        # Each top decays into W+b.
        # iff W decays into a lepton, that lepton's pt should be greater than 30, eta is greater than 2.4. If these conditions aren't met, the loop continues to the next particle without processing the current one. 

        for i in range(event.GenParticles.size()):
            pdgId = event.GenParticles_pdgId[i]
            
            # Tops
            if abs(pdgId) == 6: 
                # Check the mothers of the top and antitop
                mother1_pdgId = particles[particle["mother1"]]["pdgId"] if 0 <= particle["mother1"] < genParticles_count[0] else None
                mother2_pdgId = particles[particle["mother2"]]["pdgId"] if 0 <= particle["mother2"] < genParticles_count[0] else None
        
                # Check if the mothers are not top
                if not any([abs(mom) == 6 for mom in [mother1_pdgId, mother2_pdgId]]):
                    if mother1_pdgId:
                        h_motherPdgId.Fill(mother1_pdgId)
                    if mother2_pdgId:
                        h_motherPdgId.Fill(mother2_pdgId)
                    
                    # Checking for W and b quark daughters
                    w_quark_daughter = None
                    b_quark_daughter = None
                    
                    daughter1 = particles[particle["daughter1"]] if 0 <= particle["daughter1"] < genParticles_count[0] else None
                    daughter2 = particles[particle["daughter2"]] if 0 <= particle["daughter2"] < genParticles_count[0] else None

                    if daughter1 and abs(daughter1["pdgId"]) == 24:
                        w_quark_daughter = daughter1
                    elif daughter1 and abs(daughter1["pdgId"]) == 5:
                        b_quark_daughter = daughter1
                        
                    if daughter2 and abs(daughter2["pdgId"]) == 24:
                        w_quark_daughter = daughter2
                    elif daughter2 and abs(daughter2["pdgId"]) == 5:
                        b_quark_daughter = daughter2
                        
                    if not w_quark_daughter or not b_quark_daughter:
                        continue
                    
                    has_high_pt_lepton = False
                    for j in range(w_quark_daughter.numberOfDaughters()):
                        lepton_candidate = w_quark_daughter.daughter(j)
                        if abs(lepton_candidate.pdgId()) in [11, 13] and lepton_candidate.pt() > 30 and abs(lepton_candidate.eta()) > 2.4:
                            has_high_pt_lepton = True
                            lepton = lepton_candidate 
                            h_leptonPt.Fill(lepton.pt())
                            h_leptoneta.Fill(lepton.eta())
                            h_leptonphi.Fill(lepton.phi())
                            h_leptonFlavor.Fill(lepton.pdgId())
                    
                    if not has_high_pt_lepton:
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


root_files_directory = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_samples/root_files/"
root_files = glob.glob(os.path.join(root_files_directory, "*.root"))

total_files = len(root_files)
processed_files = 0

print("8")
for root_file in root_files:
    print("Analyzing: ", processed_files + 1, "out of", total_files)
    analyze(root_file)
    processed_files += 1

# canvas = ROOT.TCanvas("canvas", "Analysis Plots", 4000, 4000)
# canvas.Divide(4, 5)

# canvas.cd(1)
# h_leptonPt.Draw()
# canvas.cd(2)
# h_topPt.Draw()
# canvas.cd(3)
# h_antitopPt.Draw()
# canvas.cd(4)
# h_leptoneta.Draw()
# canvas.cd(5)
# h_leptonphi.Draw()
# canvas.cd(6)
# h_invariantMass.Draw()
# canvas.cd(7)
# h_decayChannel.Draw()
# canvas.cd(8)
# h_MET.Draw()
# canvas.cd(9)
# h_leptonFlavor.Draw()
# canvas.cd(10)
# h_bquark_pt.Draw()
# canvas.cd(11)
# h_bquark_eta.Draw()
# canvas.cd(12)
# h_angle_top_antitop.Draw()
# canvas.cd(13)
# h_partonMultiplicity.Draw()
# canvas.cd(14)
# h_nonTopMotherJets.Draw()
# canvas.cd(15)
# h_topMultiplicity.Draw()
# canvas.cd(16)
# h_jetMultiplicity.Draw()
# canvas.cd(17)
# h_topMother.Draw()
# canvas.cd(18)
# h_missingParticles.Draw()
# canvas.cd(19)
# h_motherPdgId.Draw()


# canvas.SaveAs("allPlots.png")

# c_leptonPt = ROOT.TCanvas("c_leptonPt", "Lepton pT Distribution", 800, 600)
# h_leptonPt.Draw()
# ROOT.gPad.SetLogy(1)
# c_leptonPt.SaveAs("leptonPtDistribution.png")

# c_topPt = ROOT.TCanvas("c_topPt", "Top Quark pT Distribution", 800, 600)
# h_topPt.Draw()
# ROOT.gPad.SetLogy(1)
# c_topPt.SaveAs("topPtDistribution.png")

# c_antitopPt = ROOT.TCanvas("c_antitopPt", "Anti-Top Quark pT Distribution", 800, 600)
# h_antitopPt.Draw()
# ROOT.gPad.SetLogy(1)
# c_antitopPt.SaveAs("antitopPtDistribution.png")

# c_eta = ROOT.TCanvas("c_eta", "Lepton Eta Distribution", 800, 600)
# h_leptoneta.Draw()
# c_eta.SaveAs("etaDistribution.png")

# c_phi = ROOT.TCanvas("c_phi", "Lepton Azimuthal Angle Distribution", 800, 600)
# h_leptonphi.Draw()
# c_phi.SaveAs("phiDistribution.png")

# c_invariantMass = ROOT.TCanvas("c_invariantMass", "Invariant Mass Distribution", 800, 600)
# h_invariantMass.Draw()
# ROOT.gPad.SetLogy(1)
# c_invariantMass.SaveAs("invariantMassDistribution.png")

# c_decay = ROOT.TCanvas("c_decay", "Decay Channel Canvas", 800, 600)
# h_decayChannel.Draw()
# c_decay.SaveAs("topDecayChannel.png")

# c_MET = ROOT.TCanvas("cMET", "MET Distribution", 800, 600)
# h_MET.Draw()
# ROOT.gPad.SetLogy(1)
# c_MET.SaveAs("METDistribution.png")

# c_leptonFlavor = ROOT.TCanvas("c_leptonFlavor", "Lepton Flavor Distribution", 800, 600)
# h_leptonFlavor.Draw()
# c_leptonFlavor.SaveAs("leptonFlavorDistribution.png")

# c_bquark_pt = ROOT.TCanvas("cbquarkPt", "b-quark pT Distribution", 800, 600)
# h_bquark_pt.Draw()
# ROOT.gPad.SetLogy(1)
# c_bquark_pt.SaveAs("bquarkPtDistribution.png")

# c_bquark_eta = ROOT.TCanvas("cbquarkEta", "b-quark Eta Distribution", 800, 600)
# h_bquark_eta.Draw()
# c_bquark_eta.SaveAs("bquarkEtaDistribution.png")

# c_angle = ROOT.TCanvas("cangle", "Angle between top and antitop", 800, 600)
# h_angle_top_antitop.Draw()
# c_angle.SaveAs("angleTopAntitop.png")

# c_partonMultiplicity = ROOT.TCanvas("c_partonMultiplicity", "Parton Multiplicity Distribution", 800, 600)
# h_partonMultiplicity.SetFillColor(ROOT.kBlue - 10)
# h_partonMultiplicity.SetLineColor(ROOT.kBlue)
# h_partonMultiplicity.Draw()
# ROOT.gPad.SetLogy(1)
# c_partonMultiplicity.SaveAs("partonMultiplicityDistribution.png")

# c_nonTopMotherJets = ROOT.TCanvas("c_nonTopMotherJets", "Jets without Top as Mother", 800, 600)
# h_nonTopMotherJets.SetFillColor(ROOT.kBlue - 10)
# h_nonTopMotherJets.SetLineColor(ROOT.kBlue)
# h_nonTopMotherJets.Draw()
# ROOT.gPad.SetLogy(1)
# c_nonTopMotherJets.SaveAs("nonTopMotherJets.png")

# # c_antitopMultiplicity = ROOT.TCanvas("c_antitopMultiplicity", "Anti-Top Multiplicity Distribution", 800, 600)
# # h_antitopMultiplicity.SetFillColor(ROOT.kBlue - 10)
# # h_antitopMultiplicity.SetLineColor(ROOT.kBlue)
# # h_antitopMultiplicity.Draw()
# # c_antitopMultiplicity.SaveAs("antitopMultiplicityDistribution.png")

# c_topMultiplicity = ROOT.TCanvas("c_topMultiplicity", "Top Multiplicity Distribution", 800, 600)
# h_topMultiplicity.SetFillColor(ROOT.kBlue - 10)
# h_topMultiplicity.SetLineColor(ROOT.kBlue)
# h_topMultiplicity.Draw()
# ROOT.gPad.SetLogy(1)
# c_topMultiplicity.SaveAs("topMultiplicityDistribution.png")

# c_jetMultiplicity = ROOT.TCanvas("c_jetMultiplicity", "Number of Jets per Event", 800, 600)
# h_jetMultiplicity.SetFillColor(ROOT.kBlue - 10)
# h_jetMultiplicity.SetLineColor(ROOT.kBlue)
# h_jetMultiplicity.Draw()
# ROOT.gPad.SetLogy(1)
# c_jetMultiplicity.SaveAs("jetMultiplicity.png")

# c_topMother = ROOT.TCanvas("c_topMother", "Mothers of the top quark", 800, 600)
# h_topMother.Draw()
# c_topMother.SaveAs("topMother.png")

# c_missingParticles = ROOT.TCanvas("c_missingParticles", "Missing Particles", 800, 600)
# h_missingParticles.Draw()
# ROOT.gPad.SetLogy(1)
# c_missingParticles.SaveAs("missingpart.png")

# c_motherPdgId = ROOT.TCanvas("c_motherPdgId", "PDG ID of Top's Mother", 800,600)
# h_motherPdgId.Draw()
# c_motherPdgId.SaveAs("motherPDG.png")



# print("Total number of events:", totalEvents)



# analyze("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/root_files/0000/GEN_LO_01j_102X_14.root")