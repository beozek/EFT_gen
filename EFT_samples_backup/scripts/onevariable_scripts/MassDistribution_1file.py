import ROOT
from DataFormats.FWLite import Events, Handle
# events and handle from DataFormats.FWLite are used to process the event data from the root files

def fillTtbarMassHistogram(filename):
    # events creates an object,looping over all the events in the root file
    # handle is an FWLite utility to handle different types of objects stored in the root file
    
    events = Events(filename)
    handle = Handle('vector<reco::GenParticle>')

    # histogram of the invariant mass of ttbar pairs with 100 bins, ranging from 0 to 2000 GeV
    histogram = ROOT.TH1F("hMass", "t#bar{t} Invariant Mass;Mass (GeV/c^{2});Events", 100, 0, 2000)
    
    # looping over each event in the root file
    for event in events:
        # with getByLabel function, I am retrieving data labeled as "genParticles" from the event 
        # then getting the actual data product through handle.product()
        event.getByLabel("genParticles", handle)
        particles = handle.product()

        # For each event, assign top and anti-top quarks to none and will assign them later if they are found in the event
        top, antitop = None, None
        
        # this loop checks each particle in the event for its pdgId
        # if the particle is top or antitop, it initializes a four-momentum (TLorentzVector) using its px, py, pz, and energy
        for particle in particles:
            if particle.pdgId() == 6:
                top = ROOT.TLorentzVector()
                top.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
            elif particle.pdgId() == -6:
                antitop = ROOT.TLorentzVector()
                antitop.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                
        # if both top and antitop quarks are found in the event, their four-momenta are added to get the four-momentum of the ttbar 
        # the invariant mass of the ttbar is calculated and the histogram is filled
        if top and antitop:
            ttbar = top + antitop
            histogram.Fill(ttbar.M())

    canvas = ROOT.TCanvas("canvas", "t#bar{t} Mass Distribution", 800, 600)
    histogram.Draw()
    # canvas.SetLogy()
    canvas.SaveAs("ttbarMassDistribution_notlog.png")

fillTtbarMassHistogram("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/root_files/0000/GEN_LO_01j_102X_14.root")

