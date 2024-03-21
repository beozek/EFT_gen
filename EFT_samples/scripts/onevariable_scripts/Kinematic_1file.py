import ROOT
from DataFormats.FWLite import Events, Handle

def plot_kinematics(filename):
    events = Events(filename)

    handle = Handle('vector<reco::GenParticle>')
    label = "genParticles"
    events.getByLabel(label, handle)

    h_pt = ROOT.TH1F("h_pt", "Top Quark p_T; p_T (GeV); Events", 100, 0, 1000)
    h_eta = ROOT.TH1F("h_eta", "Top Quark Eta; Eta; Events", 50, -5, 5)
    h_phi = ROOT.TH1F("h_phi", "Top Quark Phi; Phi; Events", 64, -3.2, 3.2)
    
    # Loop over events
    for event in events:
        event.getByLabel(label, handle)
        particles = handle.product()

        for particle in particles:
            if abs(particle.pdgId()) == 6:
                h_pt.Fill(particle.pt())
                h_eta.Fill(particle.eta())
                h_phi.Fill(particle.phi())

    # Draw histograms
    canvas_pt = ROOT.TCanvas("canvas_pt", "Top Quark p_T", 800, 600)
    h_pt.Draw()
    canvas_pt.SaveAs("top_pt.png")

    canvas_eta = ROOT.TCanvas("canvas_eta", "Top Quark Eta", 800, 600)
    h_eta.Draw()
    canvas_eta.SaveAs("top_eta.png")

    canvas_phi = ROOT.TCanvas("canvas_phi", "Top Quark Phi", 800, 600)
    h_phi.Draw()
    canvas_phi.SaveAs("top_phi.png")

# Usage
plot_kinematics("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/root_files/0000/GEN_LO_01j_102X_14.root")
