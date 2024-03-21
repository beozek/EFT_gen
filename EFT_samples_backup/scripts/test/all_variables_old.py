import ROOT
import os
import glob
from array import array
from DataFormats.FWLite import Events, Handle

ROOT.gROOT.SetBatch(True)

totalEvents = 0

h_leptonPt = ROOT.TH1F("h_leptonPt", "Lepton pT; pT (GeV);Events", 1000, 0, 100)
h_topPt = ROOT.TH1F("h_topPt", "Top Quark pT; pT (GeV);Events", 1000, 0, 3000)
h_rapidity = ROOT.TH1F("h_rapidity", "Rapidity; y;Events", 100, -5, 5)
h_pseudorapidity = ROOT.TH1F("h_pseudorapidity", "Pseudorapidity; #eta;Events", 100, -5, 5)
h_phi = ROOT.TH1F("h_phi", "Azimuthal Angle; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
h_invariantMass = ROOT.TH1F("h_invariantMass", "Invariant Mass; M (GeV);Events", 100, 0, 7000)
h_jetMultiplicity = ROOT.TH1F("h_jetMultiplicity", "Jet Multiplicity; N_{jets};Events", 20, 0, 2000)
h_MET = ROOT.TH1F("hMET", "MET;MET (GeV);Events", 100, 0, 200)
h_bjet_pt = ROOT.TH1F("hbjetPt", "b-jet pT;pT (GeV);Events", 150, 0, 300)
h_bjet_eta = ROOT.TH1F("hbjetEta", "b-jet #eta;#eta;Events", 100, -5, 5)
h_angle_top_antitop = ROOT.TH1F("h_angle", "Angle between top and antitop;Angle (radians);Events", 50, 0, ROOT.TMath.Pi())


bin_edges = [-16.5, -14.5, -12.5, -10.5, 10.5, 12.5, 14.5, 16.5]
h_leptonFlavor = ROOT.TH1F("h_leptonFlavor", "Lepton Flavor; PDG ID;Events", len(bin_edges)-1, array('d', bin_edges))

h_leptonFlavor.GetXaxis().SetBinLabel(1, "tau-")
h_leptonFlavor.GetXaxis().SetBinLabel(2, "muon-")
h_leptonFlavor.GetXaxis().SetBinLabel(3, "electron-")
h_leptonFlavor.GetXaxis().SetBinLabel(5, "electron+")
h_leptonFlavor.GetXaxis().SetBinLabel(6, "muon+")
h_leptonFlavor.GetXaxis().SetBinLabel(7, "tau+")



def analyze(filename):
    events = Events(filename)
    global totalEvents 
    totalEvents += events.size()
    print("Number of events in file:", events.size())
    handle = Handle('vector<reco::GenParticle>')

    
    for event in events:
        event.getByLabel("genParticles", handle)
        particles = handle.product()
        # print("Number of particles in event:", len(particles))
        
        tops = []
        bquarks = []
        leptons = []
        neutrinos = []
        jets= []
        top = None
        antitop = None

        for particle in particles:
            pdgId = particle.pdgId()
            
            if abs(pdgId) in [1, 2, 3, 4, 5, 6, 21]:  # quarks (21) and gluons (1-6)
                jets.append(particle)
            
            # lepton_count = 0
            if abs(pdgId) in [11, 13, 15]:  # e, mu, tau (15)
                
                # lepton_count += 1
                lepton = particle
                h_leptonPt.Fill(lepton.pt())
                h_rapidity.Fill(lepton.rapidity())
                h_pseudorapidity.Fill(lepton.eta())
                h_phi.Fill(lepton.phi())
                h_leptonFlavor.Fill(pdgId)
                
            
            # print("Number of leptons processed:", lepton_count)
            
            if abs(pdgId) == 6:
                tops.append(particle)
                h_topPt.Fill(particle.pt())
                
                if particle.pdgId() == 6:
                    top = ROOT.TLorentzVector()
                    top.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                elif particle.pdgId() == -6:
                    antitop = ROOT.TLorentzVector()
                    antitop.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
        

            if abs(pdgId) == 5:
                bquarks.append(particle)
                
                b_vector = ROOT.TLorentzVector()
                b_vector.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                
                if pdgId == 5:
                    h_bjet_pt.Fill(b_vector.Pt())
                    h_bjet_eta.Fill(b_vector.Eta())

        
            if abs(pdgId) in [12, 14, 16]:
                neutrino = ROOT.TLorentzVector()
                neutrino.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                h_MET.Fill(neutrino.Pt())
        
        h_jetMultiplicity.Fill(len(jets))
            
        if top and antitop:
            ttbar = top + antitop
            h_invariantMass.Fill(ttbar.M())
            h_angle_top_antitop.Fill(top.Angle(antitop.Vect()))

    
root_files_directory = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/root_files/0000/"
root_files = glob.glob(os.path.join(root_files_directory, "*.root"))

for root_file in root_files:
    print("Analyzing: ", root_file)
    analyze(root_file)

canvas = ROOT.TCanvas("canvas", "Analysis Plots", 2400, 2400)
canvas.Divide(3, 4)
canvas.Divide(12, 12) 

canvas.cd(1)
h_leptonPt.Draw()
canvas.cd(2)
h_topPt.Draw()
canvas.cd(3)
h_rapidity.Draw()
canvas.cd(4)
h_pseudorapidity.Draw()
canvas.cd(5)
h_phi.Draw()
canvas.cd(6)
h_invariantMass.Draw()
canvas.cd(7)
h_jetMultiplicity.Draw()
canvas.cd(8)
h_MET.Draw()
canvas.cd(9)
h_leptonFlavor.Draw()
canvas.cd(10)
h_bjet_pt.Draw()
canvas.cd(11)
h_bjet_eta.Draw()
canvas.cd(12)
h_angle_top_antitop.Draw()


canvas.SaveAs("allPlots.png")


c_leptonPt = ROOT.TCanvas("c_leptonPt", "Lepton pT Distribution", 800, 600)
h_leptonPt.Draw()
c_leptonPt.SaveAs("leptonPtDistribution.png")

c_topPt = ROOT.TCanvas("c_topPt", "Top Quark pT Distribution", 800, 600)
h_topPt.Draw()
c_topPt.SaveAs("topPtDistribution.png")

c_rapidity = ROOT.TCanvas("c_rapidity", "Rapidity Distribution", 800, 600)
h_rapidity.Draw()
c_rapidity.SaveAs("rapidityDistribution.png")

c_pseudorapidity = ROOT.TCanvas("c_pseudorapidity", "Pseudorapidity Distribution", 800, 600)
h_pseudorapidity.Draw()
c_pseudorapidity.SaveAs("pseudorapidityDistribution.png")

c_phi = ROOT.TCanvas("c_phi", "Azimuthal Angle Distribution", 800, 600)
h_phi.Draw()
c_phi.SaveAs("phiDistribution.png")

c_invariantMass = ROOT.TCanvas("c_invariantMass", "Invariant Mass Distribution", 800, 600)
h_invariantMass.Draw()
c_invariantMass.SaveAs("invariantMassDistribution.png")

c_jetMultiplicity = ROOT.TCanvas("c_jetMultiplicity", "Jet Multiplicity Distribution", 800, 600)
h_jetMultiplicity.SetFillColor(ROOT.kBlue - 10)
h_jetMultiplicity.SetLineColor(ROOT.kBlue)
h_jetMultiplicity.Draw()
c_jetMultiplicity.SaveAs("jetMultiplicityDistribution.png")


c_leptonFlavor = ROOT.TCanvas("c_leptonFlavor", "Lepton Flavor Distribution", 800, 600)
h_leptonFlavor.Draw()
c_leptonFlavor.SaveAs("leptonFlavorDistribution.png")


c_MET = ROOT.TCanvas("cMET", "MET Distribution", 800, 600)
h_MET.Draw()
c_MET.SaveAs("METDistribution.png")

c_bjet_pt = ROOT.TCanvas("cbjetPt", "b-jet pT Distribution", 800, 600)
h_bjet_pt.Draw()
c_bjet_pt.SaveAs("bjetPtDistribution.png")

c_bjet_eta = ROOT.TCanvas("cbjetEta", "b-jet Eta Distribution", 800, 600)
h_bjet_eta.Draw()
c_bjet_eta.SaveAs("bjetEtaDistribution.png")

c_angle = ROOT.TCanvas("cangle", "Angle between top and antitop", 800, 600)
h_angle_top_antitop.Draw()
c_angle.SaveAs("angleTopAntitop.png")

print("Total number of events:", totalEvents)



# analyze("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/root_files/0000/GEN_LO_01j_102X_14.root")