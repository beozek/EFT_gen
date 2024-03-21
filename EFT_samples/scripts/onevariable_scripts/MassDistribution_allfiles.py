import ROOT
import os
from DataFormats.FWLite import Events, Handle

def fillTtbarMassHistogram(filename, histogram):
    events = Events(filename)
    handle = Handle('vector<reco::GenParticle>')
    
    for event in events:
        event.getByLabel("genParticles", handle)
        particles = handle.product()

        top, antitop = None, None
        
        for particle in particles:
            if particle.pdgId() == 6:
                top = ROOT.TLorentzVector()
                top.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
            elif particle.pdgId() == -6:
                antitop = ROOT.TLorentzVector()
                antitop.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                
        if top and antitop:
            ttbar = top + antitop
            histogram.Fill(ttbar.M())

def processDirectory(directory_path):
    histogram = ROOT.TH1F("hMass", "t#bar{t} Invariant Mass;Mass (GeV/c^{2});Events", 100, 0, 2000)

    for root_file in os.listdir(directory_path):
        if root_file.endswith('.root'):
            full_path = os.path.join(directory_path, root_file)
            fillTtbarMassHistogram(full_path, histogram)

    # Drawing and saving the histogram
    canvas = ROOT.TCanvas("canvas", "t#bar{t} Mass Distribution", 800, 600)
    histogram.Draw()
    # canvas.SetLogy()
    canvas.SaveAs("ttbarMassDistribution_combined.png")

processDirectory("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/root_files/0000/try")
