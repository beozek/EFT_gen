import ROOT
import os
import glob
from array import array

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

def analyze(filename):
    # Open the file and get the TTree
    file = ROOT.TFile.Open(filename)
    tree = file.Get("AnalysisTree") 
    
    global totalEvents
    totalEvents += tree.GetEntries()
    print("Number of events in file:", tree.GetEntries())
    
    relevant_pdgIds = {12, 14, 16, 24, 1, 2, 3, 4, 5, 6, 21, 11, 13, 15}
    
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        
        particles = tree.GenParticles
        jets = tree.slimmedGenJets

        particles = [p for p in particles if abs(p.pdgId) in relevant_pdgIds]
        
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
        
        for jet in jets:
            h_jetMultiplicity.Fill(jet.pt.size())  
            # NOTE: Adjust here as the jet mother logic was removed.
            # Adjust the histogram filling accordingly.
        
        for particle in particles:
            pdgId = particle.pdgId
            
            # Tops
            if abs(pdgId) == 6:
                # Using direct mother information
                mother1_pdgId = abs(particle.mother1)
                mother2_pdgId = abs(particle.mother2) if particle.mother2 else None

                if mother1_pdgId != 6 and (not mother2_pdgId or mother2_pdgId != 6):
                    h_motherPdgId.Fill(mother1_pdgId)
                    if mother2_pdgId:
                        h_motherPdgId.Fill(mother2_pdgId)
                
                w_daughter = particle.daughter1 if abs(particle.daughter1) == 24 else particle.daughter2
                b_daughter = particle.daughter1 if abs(particle.daughter1) == 5 else particle.daughter2
                
                if not w_daughter or not b_daughter:
                    continue
                    
                tops.append(particle)
                h_decayChannel.Fill(0)  # t -> W+b
                
                if pdgId == 6:
                    top_count += 1
                    h_topPt.Fill(particle.pt)
                    top = ROOT.TLorentzVector()
                    top.SetPxPyPzE(particle.px, particle.py, particle.pz, particle.pt)  # Note: pt is used here, adjust if needed.
                elif pdgId == -6:
                    antitop_count += 1
                    h_antitopPt.Fill(particle.pt)
                    antitop = ROOT.TLorentzVector()
                    antitop.SetPxPyPzE(particle.px, particle.py, particle.pz, particle.pt)
                
                # Adjust this logic based on how you have the daughters in the new format.
                # Assuming one of the daughters from W is lepton.
                lepton_candidate = w_daughter.daughter1 if abs(w_daughter.daughter1) in [11, 13] else w_daughter.daughter2
                
                if abs(lepton_candidate.pdgId) in [11, 13] and lepton_candidate.pt > 30 and abs(lepton_candidate.eta) < 2.4:
                    h_leptonPt.Fill(lepton_candidate.pt)
                    h_leptoneta.Fill(lepton_candidate.eta)
                    h_leptonphi.Fill(lepton_candidate.phi)
                    h_leptonFlavor.Fill(lepton_candidate.pdgId)
                    
                if mother1_pdgId == 21 and (not mother2_pdgId or mother2_pdgId == 21):
                    h_topMother.Fill(1)  # gg
                elif mother1_pdgId in {1, 2, 3, 4, 5} and (not mother2_pdgId or mother2_pdgId in {1, 2, 3, 4, 5}):
                    h_topMother.Fill(0)  # qq
                else:
                    h_topMother.Fill(2)  # Other
        
            # Partons
            if abs(pdgId) in [1, 2, 3, 4, 5, 6, 21]:
                partons.append(particle)
            
            if abs(pdgId) == 5:
                bquarks.append(particle)
                b_vector = ROOT.TLorentzVector()
                b_vector.SetPxPyPzE(particle.px, particle.py, particle.pz, particle.pt)
                h_bquark_pt.Fill(b_vector.Pt())
                h_bquark_eta.Fill(b_vector.Eta())

            if abs(pdgId) in [12, 14, 16]:
                neutrino = ROOT.TLorentzVector()
                neutrino.SetPxPyPzE(particle.px, particle.py, particle.pz, particle.pt)
                h_MET.Fill(neutrino.Pt())
        
        h_partonMultiplicity.Fill(len(partons))
        h_topMultiplicity.Fill(len(tops))

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
            
    file.Close()
            
# root_files_directory = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_samples/root_files/Ntuple_10.root"
# root_files = glob.glob(os.path.join(root_files_directory, "*.root"))

# total_files = len(root_files)
# processed_files = 0


# for root_file in root_files:
#     print('Analyzing: ',processed_files + 1, 'out of',total_files)
#     analyze(root_file)
#     processed_files += 1

canvas = ROOT.TCanvas("canvas", "Analysis Plots", 4000, 4000)
canvas.Divide(4, 5)

canvas.cd(1)
h_leptonPt.Draw()
canvas.cd(2)
h_topPt.Draw()
canvas.cd(3)
h_antitopPt.Draw()
canvas.cd(4)
h_leptoneta.Draw()
canvas.cd(5)
h_leptonphi.Draw()
canvas.cd(6)
h_invariantMass.Draw()
canvas.cd(7)
h_decayChannel.Draw()
canvas.cd(8)
h_MET.Draw()
canvas.cd(9)
h_leptonFlavor.Draw()
canvas.cd(10)
h_bquark_pt.Draw()
canvas.cd(11)
h_bquark_eta.Draw()
canvas.cd(12)
h_angle_top_antitop.Draw()
canvas.cd(13)
h_partonMultiplicity.Draw()
canvas.cd(14)
h_nonTopMotherJets.Draw()
canvas.cd(15)
h_topMultiplicity.Draw()
canvas.cd(16)
h_jetMultiplicity.Draw()
canvas.cd(17)
h_topMother.Draw()
canvas.cd(18)
h_missingParticles.Draw()
canvas.cd(19)
h_motherPdgId.Draw()


canvas.SaveAs("allPlots.png")

c_leptonPt = ROOT.TCanvas("c_leptonPt", "Lepton pT Distribution", 800, 600)
h_leptonPt.Draw()
ROOT.gPad.SetLogy(1)
c_leptonPt.SaveAs("leptonPtDistribution.png")

c_topPt = ROOT.TCanvas("c_topPt", "Top Quark pT Distribution", 800, 600)
h_topPt.Draw()
ROOT.gPad.SetLogy(1)
c_topPt.SaveAs("topPtDistribution.png")

c_antitopPt = ROOT.TCanvas("c_antitopPt", "Anti-Top Quark pT Distribution", 800, 600)
h_antitopPt.Draw()
ROOT.gPad.SetLogy(1)
c_antitopPt.SaveAs("antitopPtDistribution.png")

c_eta = ROOT.TCanvas("c_eta", "Lepton Eta Distribution", 800, 600)
h_leptoneta.Draw()
c_eta.SaveAs("etaDistribution.png")

c_phi = ROOT.TCanvas("c_phi", "Lepton Azimuthal Angle Distribution", 800, 600)
h_leptonphi.Draw()
c_phi.SaveAs("phiDistribution.png")

c_invariantMass = ROOT.TCanvas("c_invariantMass", "Invariant Mass Distribution", 800, 600)
h_invariantMass.Draw()
ROOT.gPad.SetLogy(1)
c_invariantMass.SaveAs("invariantMassDistribution.png")

c_decay = ROOT.TCanvas("c_decay", "Decay Channel Canvas", 800, 600)
h_decayChannel.Draw()
c_decay.SaveAs("topDecayChannel.png")

c_MET = ROOT.TCanvas("cMET", "MET Distribution", 800, 600)
h_MET.Draw()
ROOT.gPad.SetLogy(1)
c_MET.SaveAs("METDistribution.png")

c_leptonFlavor = ROOT.TCanvas("c_leptonFlavor", "Lepton Flavor Distribution", 800, 600)
h_leptonFlavor.Draw()
c_leptonFlavor.SaveAs("leptonFlavorDistribution.png")

c_bquark_pt = ROOT.TCanvas("cbquarkPt", "b-quark pT Distribution", 800, 600)
h_bquark_pt.Draw()
ROOT.gPad.SetLogy(1)
c_bquark_pt.SaveAs("bquarkPtDistribution.png")

c_bquark_eta = ROOT.TCanvas("cbquarkEta", "b-quark Eta Distribution", 800, 600)
h_bquark_eta.Draw()
c_bquark_eta.SaveAs("bquarkEtaDistribution.png")

c_angle = ROOT.TCanvas("cangle", "Angle between top and antitop", 800, 600)
h_angle_top_antitop.Draw()
c_angle.SaveAs("angleTopAntitop.png")

c_partonMultiplicity = ROOT.TCanvas("c_partonMultiplicity", "Parton Multiplicity Distribution", 800, 600)
h_partonMultiplicity.SetFillColor(ROOT.kBlue - 10)
h_partonMultiplicity.SetLineColor(ROOT.kBlue)
h_partonMultiplicity.Draw()
ROOT.gPad.SetLogy(1)
c_partonMultiplicity.SaveAs("partonMultiplicityDistribution.png")

c_nonTopMotherJets = ROOT.TCanvas("c_nonTopMotherJets", "Jets without Top as Mother", 800, 600)
h_nonTopMotherJets.SetFillColor(ROOT.kBlue - 10)
h_nonTopMotherJets.SetLineColor(ROOT.kBlue)
h_nonTopMotherJets.Draw()
ROOT.gPad.SetLogy(1)
c_nonTopMotherJets.SaveAs("nonTopMotherJets.png")

# c_antitopMultiplicity = ROOT.TCanvas("c_antitopMultiplicity", "Anti-Top Multiplicity Distribution", 800, 600)
# h_antitopMultiplicity.SetFillColor(ROOT.kBlue - 10)
# h_antitopMultiplicity.SetLineColor(ROOT.kBlue)
# h_antitopMultiplicity.Draw()
# c_antitopMultiplicity.SaveAs("antitopMultiplicityDistribution.png")

c_topMultiplicity = ROOT.TCanvas("c_topMultiplicity", "Top Multiplicity Distribution", 800, 600)
h_topMultiplicity.SetFillColor(ROOT.kBlue - 10)
h_topMultiplicity.SetLineColor(ROOT.kBlue)
h_topMultiplicity.Draw()
ROOT.gPad.SetLogy(1)
c_topMultiplicity.SaveAs("topMultiplicityDistribution.png")

c_jetMultiplicity = ROOT.TCanvas("c_jetMultiplicity", "Number of Jets per Event", 800, 600)
h_jetMultiplicity.SetFillColor(ROOT.kBlue - 10)
h_jetMultiplicity.SetLineColor(ROOT.kBlue)
h_jetMultiplicity.Draw()
ROOT.gPad.SetLogy(1)
c_jetMultiplicity.SaveAs("jetMultiplicity.png")

c_topMother = ROOT.TCanvas("c_topMother", "Mothers of the top quark", 800, 600)
h_topMother.Draw()
c_topMother.SaveAs("topMother.png")

c_missingParticles = ROOT.TCanvas("c_missingParticles", "Missing Particles", 800, 600)
h_missingParticles.Draw()
ROOT.gPad.SetLogy(1)
c_missingParticles.SaveAs("missingpart.png")

c_motherPdgId = ROOT.TCanvas("c_motherPdgId", "PDG ID of Top's Mother", 800,600)
h_motherPdgId.Draw()
c_motherPdgId.SaveAs("motherPDG.png")



print("Total number of events:", totalEvents)

analyze("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_samples/root_files/Ntuple_10.root")

