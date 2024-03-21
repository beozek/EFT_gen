import ROOT
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

def plotTtbarMass(dirPath):
    ROOT.gSystem.Exec("find {} -name '*.root' > root_files.txt".format(dirPath))
    with open("root_files.txt", "r") as f:
        root_files = [line.strip() for line in f.readlines()]

    histogram = ROOT.TH1F("hMass", "t#bar{t} Invariant Mass;Mass (GeV/c^{2});Events", 100, 0, 2000)

    for root_file in root_files:
        fillTtbarMassHistogram(root_file, histogram)

    canvas = ROOT.TCanvas("canvas", "t#bar{t} Mass Distribution", 800, 600)
    histogram.Draw()
    canvas.SetLogy()
    canvas.SaveAs("ttbarMassDistribution.png")

plotTtbarMass("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/root_files/0000")
