import ROOT
import os
import glob
from array import array
import subprocess
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

selected_weights_indices = [11, 26, 40]

def create_histograms(prefix=""):
    hists = {}
    hists["h_leptonPt"] = ROOT.TH1F(prefix + "h_leptonPt", "Lepton pT; pT (GeV);Events", 100, 0, 1000)
    hists["h_topPt"] = ROOT.TH1F(prefix + "h_topPt", "Top Quark pT; pT (GeV);Events", 100, 0, 3000)
    hists["h_leptoneta"] = ROOT.TH1F(prefix + "h_leptoneta", "eta; #eta;Events", 100, -5, 5)
    hists["h_MET"] = ROOT.TH1F(prefix + "hMET", "MET;MET (GeV);Events", 100, 0, 200)
    hists["h_invariantMass"] = ROOT.TH1F(prefix + "h_invariantMass", "Invariant Mass; M (GeV);Events", 100, 0, 7000)
    hists["h_leptonphi"] = ROOT.TH1F(prefix + "h_leptonphi", "Azimuthal Angle; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
    hists["h_bquark_pt"] = ROOT.TH1F(prefix + "hbquarkPt", "b-quark pT;pT (GeV);Events", 100, 0, 1000)
    hists["h_bquark_eta"] = ROOT.TH1F(prefix + "hbquarkEta", "b-quark #eta;#eta;Events", 100, -5, 5)
    return hists

# Create a dictionary of histograms for each weight
histograms_for_weights = {}
for i in selected_weights_indices:
    histograms_for_weights[i] = create_histograms("w{}_".format(i))



def analyze(filename):
    events = Events(filename)
    global totalEvents 
    totalEvents += events.size()
    print("Number of events in file:", events.size())
    
    handle = Handle('vector<reco::GenParticle>')
    genJetsHandle = Handle('vector<reco::GenJet>')
    
    weightsHandle = Handle('LHEEventProduct')
    
    relevant_pdgIds = {12,14,16,24,1,2,3,4,5,6,21,11,13,15}
    
    event_number = 0
    for event in events:
        
        event_number += 1
        # GenParticles
        event.getByLabel("genParticles", handle)
        particles = handle.product()

        particles = [p for p in particles if abs(p.pdgId()) in relevant_pdgIds]

        # GenJets
        event.getByLabel("ak4GenJets", genJetsHandle)
        jets = genJetsHandle.product()
        
        # Extracting weights for the event
        
        event.getByLabel("externalLHEProducer", weightsHandle)
        lhe_info = weightsHandle.product()
        weights = lhe_info.weights()
        
        dummy_weight = weights[0].wgt
        
        # if weights:
        #     weight = weights[40].wgt #this takes first weight
        
        # print('Event: ', event_number)
        # print('Weight Id: ', weights[40].id)
        # print('Weight wgt: ', weights[40].wgt)
            
        # for w in weights:
        #     print(w.id, w.wgt)
        
        # h_leptonPt.Fill(lepton.pt(), weight * 10) 
        
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
                    h_topPt.Fill(particle.pt(), dummy_weight)
                    for i in selected_weights_indices:
                        weight = weights[i].wgt
                        histograms_for_weights[i]['h_topPt'].Fill(particle.pt(), weight)
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
                        h_leptonPt.Fill(lepton.pt(), dummy_weight)
                        h_leptoneta.Fill(lepton.eta(), dummy_weight)
                        h_leptonphi.Fill(lepton.phi(), dummy_weight)
                        h_leptonFlavor.Fill(lepton.pdgId())
                        
                        for i in selected_weights_indices:
                            weight = weights[i].wgt
                            histograms_for_weights[i]['h_leptonPt'].Fill(lepton.pt(), weight)
                            histograms_for_weights[i]['h_leptoneta'].Fill(lepton.eta(), weight)
                            histograms_for_weights[i]['h_leptonphi'].Fill(lepton.phi(), weight)
                
                        
                
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
                    h_bquark_pt.Fill(b_vector.Pt(), dummy_weight)
                    h_bquark_eta.Fill(b_vector.Eta(), dummy_weight)
                    for i in selected_weights_indices:
                        weight = weights[i].wgt
                        histograms_for_weights[i]['h_bquark_pt'].Fill(b_vector.Pt(), weight)
                        histograms_for_weights[i]['h_bquark_eta'].Fill(b_vector.Eta(), weight)


        
            if abs(pdgId) in [12, 14, 16]:
                neutrino = ROOT.TLorentzVector()
                neutrino.SetPxPyPzE(particle.px(), particle.py(), particle.pz(), particle.energy())
                h_MET.Fill(neutrino.Pt(), dummy_weight)
                for i in selected_weights_indices:
                    weight = weights[i].wgt
                    histograms_for_weights[i]['h_MET'].Fill(neutrino.Pt(), weight)

                
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
            h_invariantMass.Fill(ttbar.M(), dummy_weight)
            h_angle_top_antitop.Fill(top.Angle(antitop.Vect()))
            for i in selected_weights_indices:
                weight = weights[i].wgt
                histograms_for_weights[i]['h_invariantMass'].Fill(ttbar.M(), weight)

url = "root://eos.grid.vbc.ac.at/"
path = "/store/user/schoef/TT01j1lCA_HT500_v2/TT01j1lCA_HT500_v2/230918_163019/0000"
client_instance = client.FileSystem(url)
status, listing = client_instance.dirlist(path, DirListFlags.STAT)
root_files = [entry.name for entry in listing if entry.name.endswith('.root')]
root_files = root_files[:2]

for root_file in root_files:
    full_path = url + os.path.join(path, root_file)
    analyze(full_path)

# url = "root://eos.grid.vbc.ac.at/"
# path = "/store/user/schoef/TT01j1lCA_HT500_v2/TT01j1lCA_HT500_v2/230918_163019/0000"
# client_instance = client.FileSystem(url)
# status, listing = client_instance.dirlist(path, DirListFlags.STAT)
# root_files = [entry.name for entry in listing if entry.name.endswith('.root')]

# for root_file in root_files:
#     full_path = url + os.path.join(path, root_file)
#     analyze(full_path)


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

nominal_histograms = {
    'h_leptonPt': h_leptonPt,
    'h_topPt': h_topPt,
    'h_leptoneta': h_leptoneta,
    'h_MET': h_MET,
    'h_invariantMass': h_invariantMass,
    'h_leptonphi': h_leptonphi,
    'h_bquark_pt': h_bquark_pt,
    'h_bquark_eta': h_bquark_eta
}

weight_names = {
    0: "Nominal",
    11: "cQj18",
    26: "cQd8",
    40: "cQj18 & cQd8"
}

def draw_histograms():
    # Define colors for different weights
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kCyan, ROOT.kYellow, ROOT.kViolet, ROOT.kTeal]
    
    for hist_key in histograms_for_weights[selected_weights_indices[0]].keys():
        c = ROOT.TCanvas("c_{}".format(hist_key), hist_key, 800, 600)
        leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
        
        # Find the maximum y-value among all histograms (nominal + weighted)
        max_y = nominal_histograms[hist_key].GetMaximum()
        for weight_index in selected_weights_indices:
            max_y = max(max_y, histograms_for_weights[weight_index][hist_key].GetMaximum())

        # Set the maximum y-value for the nominal histogram
        nominal_histograms[hist_key].SetMaximum(max_y * 1.1)  # 1.1 is just a factor to leave some space on top
        nominal_histograms[hist_key].SetLineColor(ROOT.kBlack)
        nominal_histograms[hist_key].SetStats(0)
        
        # Set the canvas to display in logarithmic scale on the y-axis
        ROOT.gPad.SetLogy(1)
        
        nominal_histograms[hist_key].Draw("HIST")
        leg.AddEntry(nominal_histograms[hist_key], weight_names[0], "l")

        
        # Draw histograms for each weight on top of the nominal one
        for idx, weight_index in enumerate(selected_weights_indices):
            histograms_for_weights[weight_index][hist_key].SetLineColor(colors[idx])
            histograms_for_weights[weight_index][hist_key].SetStats(0)
            histograms_for_weights[weight_index][hist_key].Draw("HIST SAME")
            leg.AddEntry(histograms_for_weights[weight_index][hist_key],  weight_names[weight_index], "l")
        
        leg.Draw()
        c.SaveAs("{}.png".format(hist_key))



draw_histograms()



print("Total number of events:", totalEvents)



# analyze("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/root_files/0000/GEN_LO_01j_102X_14.root")