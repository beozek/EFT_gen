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



h_leptonPt = ROOT.TH1F("h_leptonPt", "Lepton pT; pT (GeV);Events", 1000, 0, 1000)
h_electronPt = ROOT.TH1F("h_electronPt", "Electron pT; pT (GeV);Events", 1000, 0, 1000)
h_muonPt = ROOT.TH1F("h_muonPt", "Muon pT; pT (GeV);Events", 1000, 0, 1000)
h_topPt = ROOT.TH1F("h_topPt", "Top Quark pT; pT (GeV);Events", 1000, 0, 3000)
h_antitopPt = ROOT.TH1F("h_antitopPt", "Anti-Top Quark p_{T}; p_{T} [GeV];Events", 1000, 0, 3000)
h_leptoneta = ROOT.TH1F("h_leptoneta", "eta; #eta;Events", 100, -5, 5)
h_electroneta = ROOT.TH1F("h_electroneta", "eta; #eta;Events", 100, -5, 5)
h_muoneta = ROOT.TH1F("h_muoneta", "eta; #eta;Events", 100, -5, 5)
h_leptonphi = ROOT.TH1F("h_leptonphi", "Azimuthal Angle; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
h_invariantMass = ROOT.TH1F("h_invariantMass", "Invariant Mass; M (GeV);Events", 100, 0, 7000)
h_hadronic_w_mass = ROOT.TH1F("h_hadronic_w_mass", "Hadronic Decaying W Mass; M (GeV);Events", 10, 60, 100)
# h_partonMultiplicity = ROOT.TH1F("h_partonMultiplicity", "Jet Multiplicity; N_{jets};Events", 20, 0, 100)
h_MET = ROOT.TH1F("hMET", "MET;MET (GeV);Events", 100, 0, 200)
h_bquark_pt = ROOT.TH1F("hbquarkPt", "b-quark pT;pT (GeV);Events", 150, 0, 1000)
h_bquark_eta = ROOT.TH1F("hbquarkEta", "b-quark #eta;#eta;Events", 100, -5, 5)
# h_angle_top_antitop = ROOT.TH1F("h_angle", "Angle between top and antitop;Angle (radians);Events", 50, 0, ROOT.TMath.Pi())

# h_decayChannel = ROOT.TH1F("h_decayChannel", "Top Decay Channels; Channel; Events", 2, 0, 2)
# h_decayChannel.GetXaxis().SetBinLabel(1, "t -> W+b")
# h_decayChannel.GetXaxis().SetBinLabel(2, "Other")


h_topMultiplicity = ROOT.TH1F("h_topMultiplicity", "Top Multiplicity; N_{top};Events", 5, 0, 5)
h_antitopMultiplicity = ROOT.TH1F("h_antitopMultiplicity", "Anti-Top Multiplicity; N_{antitop};Events", 5, 0, 5)
h_jetMultiplicity_fromW = ROOT.TH1F("h_jetMultiplicity_fromW", "Jet Multiplicity from W; Number of Jets; Events", 10, 0, 5)

# h_missingParticles = ROOT.TH1F("h_missingParticles", "Missing Particles; Particle Type; Events", 4, 0, 4)
# h_missingParticles.GetXaxis().SetBinLabel(1, "No Top")
# h_missingParticles.GetXaxis().SetBinLabel(2, "No Anti-Top")
# h_missingParticles.GetXaxis().SetBinLabel(3, "No Top & No Anti-Top")



bin_edges = [-16.5, -14.5, -12.5, -10.5, 10.5, 12.5, 14.5, 16.5]
h_leptonFlavor = ROOT.TH1F("h_leptonFlavor", "Lepton Flavor; PDG ID;Events", len(bin_edges)-1, array('d', bin_edges))

h_leptonFlavor.GetXaxis().SetBinLabel(1, "muon-")
h_leptonFlavor.GetXaxis().SetBinLabel(2, "electron-")
h_leptonFlavor.GetXaxis().SetBinLabel(4, "electron+")
h_leptonFlavor.GetXaxis().SetBinLabel(5, "muon+")


h_nonTopMotherJets = ROOT.TH1F("h_nonTopMotherJets", "Jets without Top as Mother; Count;Events", 10, 0, 50)
h_jetMultiplicity = ROOT.TH1F("h_jetMultiplicity", "Number of Jets per Event", 10, 0, 50)

# h_topMother = ROOT.TH1F("h_topMother", "Mother of Top Quarks; Mother; Events", 3, 0, 3)
# h_topMother.GetXaxis().SetBinLabel(1, "qq")
# h_topMother.GetXaxis().SetBinLabel(2, "gg")
# h_topMother.GetXaxis().SetBinLabel(3, "Other")

# h_motherPdgId = ROOT.TH1F("h_motherPdgId", "PDG ID of Top's Mother;PDG ID;Counts", 23, -6, 22)

h_HT = ROOT.TH1F("h_HT", "HT distribution; HT (GeV); Events", 100 ,0 ,3000)

h_ele_HT = ROOT.TH1F("h_ele_HT", "HT distribution Electron Channel; HT (GeV); Events", 100 ,0 ,3000)

h_muon_HT = ROOT.TH1F("h_muon_HT", "HT distribution Muon Channel; HT (GeV); Events", 100 ,0 ,3000)

# h_LHE_HT = ROOT.TH1F("h_LHE_HT", "LHE HT; HT (GeV); Events", 100, 0, 3000)

h_LHE_HT_before = ROOT.TH1F("h_LHE_HT_before", "LHE_HT Before Selection; HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_after = ROOT.TH1F("h_LHE_HT_after", "LHE_HT After Selection; HT (GeV); Events", 100, 0, 3000)

h_ele_LHE_HT_before = ROOT.TH1F("h_ele_LHE_HT_before", "LHE_HT Before Selection Electron Channel; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_after = ROOT.TH1F("h_ele_LHE_HT_after", "LHE_HT After Selection Electron Channel; HT (GeV); Events", 100, 0, 3000)

h_muon_LHE_HT_before = ROOT.TH1F("h_muon_LHE_HT_before", "LHE_HT Before Selection Muon Channel; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_after = ROOT.TH1F("h_muon_LHE_HT_after", "LHE_HT After Selection Muon Channel; HT (GeV); Events", 100, 0, 3000)


h_both_decays = ROOT.TH1F("h_both_decays", "Events with Both Leptonic and Hadronic Decays; Number of Events; Count", 2, 0, 2)


h_ele_LHE_HT_after_lepton_cut = ROOT.TH1F("h_ele_LHE_HT_after_lepton_cut", "Electron: LHE_HT After Lepton Cut; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_after_jet_cut = ROOT.TH1F("h_ele_LHE_HT_after_jet_cut", "Electron: LHE_HT After Jet Cut; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_after_met_cut = ROOT.TH1F("h_ele_LHE_HT_after_met_cut", "Electron: LHE_HT After MET Cut; HT (GeV); Events", 100, 0, 3000)

h_muon_LHE_HT_after_lepton_cut = ROOT.TH1F("h_muon_LHE_HT_after_lepton_cut", "Muon: LHE_HT After Lepton Cut; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_after_jet_cut = ROOT.TH1F("h_muon_LHE_HT_after_jet_cut", "Muon: LHE_HT After Jet Cut; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_after_met_cut = ROOT.TH1F("h_muon_LHE_HT_after_met_cut", "Muon: LHE_HT After MET Cut; HT (GeV); Events", 100, 0, 3000)


def deltaR(eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = abs(phi1 - phi2)
    if dphi > ROOT.TMath.Pi():
        dphi = 2 * ROOT.TMath.Pi() - dphi
    return (deta * deta + dphi * dphi) ** 0.5
# deltaR calculates the deltaR distance in eta - phi space. 
# If this distance is less than a threshold (like 0.4, a typical jet size), we can say the jet is possibly from the top quark.         


def calculate_HT(entry):
    HT = 0
    for i in range(entry.nGenJet):
        jet_pt = entry.GenJet_pt[i]
        HT += jet_pt
    return HT

both_decays_counter = 0


def is_last_copy(statusFlags):
    # statusFlagsList = [ord(byte) for byte in statusFlags]
    # return (statusFlags & (1 << 13)) != 0

    # try:
    #     flag = statusFlags[index]
    #     return (flag >> 13) & 1
    # except IndexError as e:
    #     print("IndexError in is_last_copy", {e}) 
    #     print("Index: ", index)
    #     return False
    # except Exception as e:
    #     print("Error in is_last_copy", e)
    #     return False
    
    try:
        status_flags_int = int(statusFlags)
        return (status_flags_int & (1 << 13)) != 0
    except ValueError:
        # Handle the case where statusFlags cannot be converted to an integer
        return False

def process_event(entry, histograms, relevant_pdgIds):
    
    top_count = 0
    antitop_count = 0
    partons = []
    leptons = []
    met_vector = ROOT.TLorentzVector()
    tops = []
    last_copy_decays = []
    jets_from_w = []
    jets_from_w_count = 0
    last_copy_top_decays = []
    
    events_after_LHE_HT_cut = 0
    events_after_lepton_selection = 0
                            
    # processing particles
    for i in range(entry.nGenPart):
        pdgId = entry.GenPart_pdgId[i]
        pt = entry.GenPart_pt[i]
        eta = entry.GenPart_eta[i]
        phi = entry.GenPart_phi[i]
        mass = entry.GenPart_mass[i]
        mother_idx = entry.GenPart_genPartIdxMother[i]
        status = entry.GenPart_status[i]
        statusFlags = entry.GenPart_statusFlags[i]
        
        # Check if particle is a top or antitop quark
        if abs(pdgId) in relevant_pdgIds: 
            if abs(pdgId) == 6 and is_last_copy(statusFlags):   # Check if it's a top/anti-top and a last copy
                
                top_4vec = ROOT.TLorentzVector()
                top_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
                tops.append(top_4vec)
                w_daughter = None
                b_daughter = None
                last_copy_top_decays.append((pt, eta, phi))
                 # mother1_pdgId = entry.GenPart_pdgId[mother_idx] if mother_idx >= 0 else None
                # if mother1_pdgId:
                #     histograms['h_motherPdgId'].Fill(mother1_pdgId)
                
                # Checking if the j-th particle is a daughter of the i-th particle (top or anti-top quark)
                for j in range(entry.nGenPart):
                    if entry.GenPart_genPartIdxMother[j] == i and abs(entry.GenPart_pdgId[j]) in [24, 5]:
                        last_copy_decays.append((pt, eta, phi)) # append as a tuple
                            # Append a tuple (or create a custom object) with relevant properties

                        daughter_pdgId = entry.GenPart_pdgId[j]
                        if daughter_pdgId != 6 and daughter_pdgId != -6:
                            if abs(daughter_pdgId) == 24:
                                w_daughter = j
                            elif abs(daughter_pdgId) == 5:
                                b_daughter = j
                
                if w_daughter is not None and b_daughter is not None:
                    leptonic_decay = False
                    hadronic_decay = False
                    
                    # Check if W decays leptonically
                    for k in range(entry.nGenPart):
                        if entry.GenPart_genPartIdxMother[k] == w_daughter and abs(entry.GenPart_pdgId[k]) in [11, 13]: 
                            lepton_pdg = entry.GenPart_pdgId[k]
                            lepton_pt = entry.GenPart_pt[k]
                            lepton_eta = entry.GenPart_eta[k]
                            lepton_phi = entry.GenPart_phi[k]
                            histograms['h_leptonPt'].Fill(lepton_pt)
                            histograms['h_leptoneta'].Fill(lepton_eta)
                            histograms['h_leptonphi'].Fill(lepton_phi)
                            histograms['h_leptonFlavor'].Fill(entry.GenPart_pdgId[k])
                            leptons.append((lepton_pt, lepton_eta, lepton_phi, entry.GenPart_pdgId[k]))
                            leptonic_decay = True
                            if abs(lepton_pdg) == 11:
                                histograms['h_electronPt'].Fill(lepton_pt)
                                histograms['h_electroneta'].Fill(lepton_eta)
                            if abs(lepton_pdg) == 13:
                                histograms['h_muonPt'].Fill(lepton_pt)
                                histograms['h_muoneta'].Fill(lepton_eta)
                                
                    
                    # Check if W decays hadronically
                    w_quarks = [k for k in range(entry.nGenPart) if entry.GenPart_genPartIdxMother[k] == w_daughter and abs(entry.GenPart_pdgId[k]) in [1, 2, 3, 4, 5]]
                    if len(w_quarks) == 2:
                        hadronic_decay = True
                        quark1 = ROOT.TLorentzVector()
                        quark2 = ROOT.TLorentzVector()
                        quark1.SetPtEtaPhiM(entry.GenPart_pt[w_quarks[0]], entry.GenPart_eta[w_quarks[0]], entry.GenPart_phi[w_quarks[0]], entry.GenPart_mass[w_quarks[0]])
                        quark2.SetPtEtaPhiM(entry.GenPart_pt[w_quarks[1]], entry.GenPart_eta[w_quarks[1]], entry.GenPart_phi[w_quarks[1]], entry.GenPart_mass[w_quarks[1]])
                        hadronic_w_mass = (quark1 + quark2).M()
                        if 65 < hadronic_w_mass < 95:
                            histograms['h_hadronic_w_mass'].Fill(hadronic_w_mass)
                            # Identify the jets coming from the quarks of the hadronically decaying W
                            

                            for j in range(entry.nGenJet):
                                jet = ROOT.TLorentzVector()
                                jet.SetPtEtaPhiM(entry.GenJet_pt[j], entry.GenJet_eta[j], entry.GenJet_phi[j], 0)  # jet mass is negligible
                                # Match jets to quarks by deltaR
                                if deltaR(jet.Eta(), jet.Phi(), quark1.Eta(), quark1.Phi()) < 0.4 or deltaR(jet.Eta(), jet.Phi(), quark2.Eta(), quark2.Phi()) < 0.4:
                                    jets_from_w.append(jet)
                                    jets_from_w_count += 1
                                    

                        if len(jets_from_w) >= 2:
                            # Proceed with analysis for hadronic decay
                            pass
                        
                    if hadronic_decay and leptonic_decay:
                        both_decays_counter += 1
                        
                    # if leptonic_decay and pdgId == 6:
                    #     top_count += 1
                    #     histograms['h_topPt'].Fill(pt)
                        
                    # elif hadronic_decay and pdgId == -6:
                    #     antitop_count += 1
                    #     histograms['h_antitopPt'].Fill(pt)
                        
                    if pdgId == 6:
                        top_count += 1
                        histograms['h_topPt'].Fill(pt)
                        
                    elif pdgId == -6:
                        antitop_count += 1
                        histograms['h_antitopPt'].Fill(pt)
                        
                
                # b-quarks
                if b_daughter is not None:
                    b_vector = ROOT.TLorentzVector()
                    b_vector.SetPtEtaPhiM(entry.GenPart_pt[b_daughter], entry.GenPart_eta[b_daughter], entry.GenPart_phi[b_daughter], entry.GenPart_mass[b_daughter])
                    histograms['h_bquark_pt'].Fill(b_vector.Pt())
                    histograms['h_bquark_eta'].Fill(b_vector.Eta())
                            
                
                if abs(pdgId) in [12, 14, 16]:
                    neutrino = ROOT.TLorentzVector()
                    neutrino.SetPtEtaPhiM(pt, eta, phi, mass)
                    met_vector += neutrino      
            
            
    
            histograms['h_topMultiplicity'].Fill(top_count)
            histograms['h_antitopMultiplicity'].Fill(antitop_count)
                            
                # if w_daughters and b_daughters:
                    # histograms['h_decayChannel'].Fill(0)  # t -> W+b
                
                
                # if mother_idx != -1:
                #     mother_pdgId = entry.GenPart_pdgId[mother_idx]
                #     if mother_pdgId == 21:  # gg
                #         histograms['h_topMother'].Fill(1)
                #     elif abs(mother_pdgId) in [1, 2, 3, 4, 5]:  # qq
                #         histograms['h_topMother'].Fill(0)
                #     else:
                #         histograms['h_topMother'].Fill(2)  # Other
    histograms['h_jetMultiplicity_fromW'].Fill(len(jets_from_w))
    histograms['h_MET'].Fill(met_vector.Pt())       
    # histograms['h_partonMultiplicity'].Fill(len(partons))

    # if top_count == 0:
    #     histograms['h_missingParticles'].Fill(0)  # No top
    # if antitop_count == 0:
    #     histograms['h_missingParticles'].Fill(1)  # No antitop
    # if top_count == 0 and antitop_count == 0:
    #     histograms['h_missingParticles'].Fill(2)  # No top and no antitop  
    
    
    if top_count > 0 and antitop_count > 0:
        top_idx = next((idx for idx, pdg in enumerate(entry.GenPart_pdgId) if pdg == 6), None)
        antitop_idx = next((idx for idx, pdg in enumerate(entry.GenPart_pdgId) if pdg == -6), None)
        if top_idx is not None and antitop_idx is not None:
            antitop_4vec = ROOT.TLorentzVector()
            top_4vec.SetPtEtaPhiM(entry.GenPart_pt[top_idx], entry.GenPart_eta[top_idx], entry.GenPart_phi[top_idx], entry.GenPart_mass[top_idx])
            antitop_4vec.SetPtEtaPhiM(entry.GenPart_pt[antitop_idx], entry.GenPart_eta[antitop_idx], entry.GenPart_phi[antitop_idx], entry.GenPart_mass[antitop_idx])
            ttbar = top_4vec + antitop_4vec
            histograms['h_invariantMass'].Fill(ttbar.M())
            # histograms['h_angle_top_antitop'].Fill(top_4vec.Angle(antitop_4vec.Vect()))

    histograms['h_topMultiplicity'].Fill(top_count)
    
    non_top_mother_jet_count = 0

    for i in range(entry.nGenJet):
        jet_eta = entry.GenJet_eta[i]
        jet_phi = entry.GenJet_phi[i]
        jet_pt = entry.GenJet_pt[i]
        
        for parton in last_copy_decays:
            if deltaR(jet_eta, jet_phi, parton[1], parton[2]) < 0.4: # Use indices for eta and phi
                non_top_mother_jet_count += 1
        
        # for parton in last_copy_decays:     
        #     is_from_top = any(deltaR(jet_eta, jet_phi, parton[1], parton[2]) < 0.4)
        #     if not is_from_top:
        #         non_top_mother_jet_count += 1

    histograms['h_jetMultiplicity'].Fill(entry.nGenJet)
    histograms['h_nonTopMotherJets'].Fill(non_top_mother_jet_count)

    # Calculated HT in this code 
    HT = calculate_HT(entry)
    histograms['h_HT'].Fill(HT)
    
    # HT variable from data in ttree
    LHE_HT = getattr(entry, "LHE_HT", -1)
    if LHE_HT >= 0:
        histograms['h_LHE_HT_before'].Fill(LHE_HT)

    is_electron_channel = any(abs(pdgId) == 11 for pt, eta, phi, pdgId in leptons)
    is_muon_channel = any(abs(pdgId) == 13 for pt, eta, phi, pdgId in leptons)
    channel = "electron" if is_electron_channel else "muon" if is_muon_channel else "other"

    # passed_lepton_cut, passed_jet_cut, passed_met_cut = passes_selection_criteria(entry, leptons, channel, last_copy_top_decays)
    passed_lepton_cut, passed_jet_cut, passed_met_cut, updated_channel = passes_selection_criteria(entry, leptons, channel, last_copy_top_decays)


    
    
    # Determine the channel based on the leptons present
    # channel = "muon" if any(abs(pdgId) == 13 for _, _, _, pdgId in leptons) else "electron"

    # Fill the histograms for the specific channel
    if channel == "muon":
        histograms['h_muon_HT'].Fill(HT)
        if LHE_HT >= 0:
            histograms['h_muon_LHE_HT_before'].Fill(LHE_HT)
    else:
        histograms['h_ele_HT'].Fill(HT)
        if LHE_HT >= 0:
            histograms['h_ele_LHE_HT_before'].Fill(LHE_HT)
            

    # Apply selection criteria
    # passes = passes_selection_criteria(entry, leptons, channel, last_copy_top_decays)

    # if passes:
    #     if channel == "muon" and LHE_HT >= 0:
    #         histograms['h_muon_LHE_HT_after'].Fill(LHE_HT)
    #     elif channel == "electron" and LHE_HT >= 0:
    #         histograms['h_ele_LHE_HT_after'].Fill(LHE_HT)
            
    if passed_lepton_cut and passed_jet_cut and passed_met_cut:
        if channel == "muon" and LHE_HT >= 0:
            histograms['h_muon_LHE_HT_after'].Fill(LHE_HT)
        elif channel == "electron" and LHE_HT >= 0:
            histograms['h_ele_LHE_HT_after'].Fill(LHE_HT)

    
    # cuts gradually     
    if channel == "electron":
        if passed_lepton_cut:
            histograms['h_ele_LHE_HT_after_lepton_cut'].Fill(LHE_HT)
        if passed_lepton_cut and passed_jet_cut:
            histograms['h_ele_LHE_HT_after_jet_cut'].Fill(LHE_HT)
        if passed_lepton_cut and passed_jet_cut and passed_met_cut:
            histograms['h_ele_LHE_HT_after_met_cut'].Fill(LHE_HT)
    elif channel == "muon":
        if passed_lepton_cut:
            histograms['h_muon_LHE_HT_after_lepton_cut'].Fill(LHE_HT)
        if passed_lepton_cut and passed_jet_cut:
            histograms['h_muon_LHE_HT_after_jet_cut'].Fill(LHE_HT)
        if passed_lepton_cut and passed_jet_cut and passed_met_cut:
            histograms['h_muon_LHE_HT_after_met_cut'].Fill(LHE_HT)
    
    
    
    return leptons

h_both_decays.Fill(0, both_decays_counter)


def passes_selection_criteria(entry, leptons, channel, last_copy_top_decays):
    
    met_cut_electron = 60
    met_cut_muon = 70
    met_cut = 0
    
    met_pt = entry.GenMET_pt
    
    # Determine channel based on lepton type
    is_electron_channel = any(abs(pdgId) == 11 for pt, eta, phi, pdgId in leptons)
    is_muon_channel = any(abs(pdgId) == 13 for pt, eta, phi, pdgId in leptons)
    
    if is_electron_channel:
        jet_pt_cut = 40
        lepton_pt_cut = 120
        lepton_eta_cut = 2.5
        met_cut = met_cut_electron
    
    elif is_muon_channel:
        jet_pt_cut = 50
        lepton_pt_cut = 55
        lepton_eta_cut = 2.4
        met_cut = met_cut_muon
    
    else:
        return False, False, False, "other"
        
    # Jet selection with last copy matching
    jet_count = 0
    for i in range(entry.nGenJet):
        jet_eta = entry.GenJet_eta[i]
        jet_phi = entry.GenJet_phi[i]
        jet_pt = entry.GenJet_pt[i]
        
            
        for parton in last_copy_top_decays:
            parton_pt, parton_eta, parton_phi = parton
            if deltaR(jet_eta, jet_phi, parton_eta, parton_phi) < 0.4:
                if jet_pt > jet_pt_cut:
                    jet_count += 1
                    break
    
    passed_lepton_cut = sum(1 for lepton in leptons if lepton[0] > lepton_pt_cut and abs(lepton[1]) < lepton_eta_cut) > 0
    passed_jet_cut = jet_count > 0
    passed_met_cut = met_pt > met_cut

    return passed_lepton_cut, passed_jet_cut, passed_met_cut, channel
     

def analyze(filename):
    print("Processing file:", filename)
    
    file = ROOT.TFile.Open(filename)
    tree = file.Get("Events")
    
    global totalEvents
    totalEvents += tree.GetEntries()
    print("Number of events in file:", tree.GetEntries())
    
    relevant_pdgIds = {12, 14, 16, 24, 1, 2, 3, 4, 5, 6, 21, 11, 13, 15}

    histograms = {
        'h_ele_HT': h_ele_HT,
        'h_muon_HT': h_muon_HT,
        'h_HT': h_HT,
        'h_leptonPt' : h_leptonPt,
        'h_electronPt' : h_electronPt,
        'h_muonPt' : h_muonPt,
        'h_topPt' : h_topPt,
        'h_antitopPt' :  h_antitopPt,
        'h_leptoneta' : h_leptoneta, 
        'h_electroneta' : h_electroneta,
        'h_muoneta' : h_muoneta,
        'h_leptonphi' : h_leptonphi, 
        'h_invariantMass' : h_invariantMass,
        'h_hadronic_w_mass' : h_hadronic_w_mass,
        'h_antitopMultiplicity' : h_antitopMultiplicity,
        # 'h_partonMultiplicity': h_partonMultiplicity, 
        'h_MET' : h_MET, 
        'h_bquark_pt': h_bquark_pt, 
        'h_bquark_eta' : h_bquark_eta, 
        # 'h_angle_top_antitop': h_angle_top_antitop, 
        # 'h_decayChannel' : h_decayChannel,
        'h_topMultiplicity' : h_topMultiplicity, 
        # 'h_missingParticles' : h_missingParticles, 
        'h_leptonFlavor' : h_leptonFlavor,
        'h_nonTopMotherJets' : h_nonTopMotherJets,
        'h_jetMultiplicity' : h_jetMultiplicity,
        # 'h_topMother' : h_topMother,
        # 'h_motherPdgId' : h_motherPdgId,
        'h_LHE_HT_before': h_LHE_HT_before,
        'h_LHE_HT_after': h_LHE_HT_after,
        'h_ele_LHE_HT_before': h_ele_LHE_HT_before,
        'h_ele_LHE_HT_after': h_ele_LHE_HT_after,
        'h_muon_LHE_HT_before': h_muon_LHE_HT_before,
        'h_muon_LHE_HT_after': h_muon_LHE_HT_after,
        'h_jetMultiplicity_fromW' : h_jetMultiplicity_fromW,
        'h_ele_LHE_HT_after_lepton_cut' : h_ele_LHE_HT_after_lepton_cut,
        'h_ele_LHE_HT_after_jet_cut' : h_ele_LHE_HT_after_jet_cut,
        'h_ele_LHE_HT_after_met_cut' : h_ele_LHE_HT_after_met_cut,
        'h_muon_LHE_HT_after_lepton_cut' : h_muon_LHE_HT_after_lepton_cut,
        'h_muon_LHE_HT_after_jet_cut' : h_muon_LHE_HT_after_jet_cut,
        'h_muon_LHE_HT_after_met_cut' : h_muon_LHE_HT_after_met_cut
    
    }
    
    for entry in tree:
        process_event(entry, histograms, relevant_pdgIds)
    #     HT = calculate_HT(entry)
    #     histograms['h_HT'].Fill(HT)
            
    #     LHE_HT = getattr(entry, "LHE_HT", -1)
    #     if LHE_HT >= 0:
    #         histograms['h_LHE_HT_before'].Fill(LHE_HT)

    #     # Process the event and get leptons
        # leptons = process_event(entry, histograms, relevant_pdgIds)

    #     # selection criteria and fill the after histogram for LHE_HT
    #     if passes_selection_criteria(entry, leptons):
    #         if LHE_HT >= 0:
    #             histograms['h_LHE_HT_after'].Fill(LHE_HT)
     
        
    
    file.Close()
    
    return histograms

all_histograms = {}
output_file = ROOT.TFile("output_histograms.root", "RECREATE")


# url = "davs://dcache-cms-webdav-wan.desy.de:2880/"
# path = "/pnfs/desy.de/cms/tier2/store/user/beozek/TT01j1lCA_HT500_v2/TT01j1lCA_HT500_v2/231004_134141/0000"
# client_instance = client.FileSystem(url)
# status, listing = client_instance.dirlist(path, DirListFlags.STAT)
# root_files = [entry.name for entry in listing if entry.name.endswith('.root')]

# for root_file in root_files:
#     full_path = url + os.path.join(path, root_file)
#     analyze(full_path)
    
path = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/nano_files/1j1l_NoHT/"
root_files = [f for f in os.listdir(path) if f.endswith('.root')]
# root_files = root_files[:2]

for root_file in root_files:
    full_path = os.path.join(path, root_file)
    histograms = analyze(full_path)
    
    for name, hist in histograms.items():
        if name in all_histograms:
            all_histograms[name].Add(hist)
        else:
            all_histograms[name] = hist.Clone(name)
            all_histograms[name].SetDirectory(output_file)  # Set the directory to the output file

output_file.cd()
for name, hist in all_histograms.items():
    hist.Write()

output_file.Close()

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
# h_decayChannel.Draw()
# canvas.cd(8)
h_MET.Draw()
canvas.cd(9)
h_leptonFlavor.Draw()
canvas.cd(10)
h_bquark_pt.Draw()
canvas.cd(11)
h_bquark_eta.Draw()
canvas.cd(12)
# h_angle_top_antitop.Draw()
# canvas.cd(13)
# h_partonMultiplicity.Draw()
# canvas.cd(14)
h_nonTopMotherJets.Draw()
canvas.cd(15)
h_topMultiplicity.Draw()
canvas.cd(16)
h_jetMultiplicity.Draw()
# canvas.cd(17)
# h_topMother.Draw()
# canvas.cd(18)
# h_missingParticles.Draw()
# canvas.cd(19)
# h_motherPdgId.Draw()


canvas.SaveAs("allPlots.png")

c_leptonPt = ROOT.TCanvas("c_leptonPt", "Lepton pT Distribution", 800, 600)
h_leptonPt.Draw()
ROOT.gPad.SetLogy(1)
c_leptonPt.SaveAs("leptonPtDistribution.png")

c_electronPt = ROOT.TCanvas("c_electronPt", "Lepton pT Distribution", 800, 600)
h_electronPt.Draw()
ROOT.gPad.SetLogy(1)
c_electronPt.SaveAs("electronPtDistribution.png")

c_muonPt = ROOT.TCanvas("c_muonPt", "Lepton pT Distribution", 800, 600)
h_muonPt.Draw()
ROOT.gPad.SetLogy(1)
c_muonPt.SaveAs("muonPtDistribution.png")

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
c_eta.SaveAs("lepton_etaDistribution.png")

c_ele_eta = ROOT.TCanvas("c_ele_eta", "Electron Eta Distribution ", 800, 600)
h_electroneta.Draw()
c_eta.SaveAs("electron_etaDistribution.png")

c_muon_eta = ROOT.TCanvas("c_eta", "Muon Eta Distribution", 800, 600)
h_muoneta.Draw()
c_muon_eta.SaveAs("muon_etaDistribution.png")

c_phi = ROOT.TCanvas("c_phi", "Lepton Azimuthal Angle Distribution", 800, 600)
h_leptonphi.Draw()
c_phi.SaveAs("lepton_phiDistribution.png")

c_invariantMass = ROOT.TCanvas("c_invariantMass", "Invariant Mass Distribution", 800, 600)
h_invariantMass.Draw()
ROOT.gPad.SetLogy(1)
c_invariantMass.SaveAs("invariantMassDistribution.png")

# c_decay = ROOT.TCanvas("c_decay", "Decay Channel Canvas", 800, 600)
# h_decayChannel.Draw()
# c_decay.SaveAs("topDecayChannel.png")

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

# c_angle = ROOT.TCanvas("cangle", "Angle between top and antitop", 800, 600)
# h_angle_top_antitop.Draw()
# c_angle.SaveAs("angleTopAntitop.png")

# c_partonMultiplicity = ROOT.TCanvas("c_partonMultiplicity", "Parton Multiplicity Distribution", 800, 600)
# h_partonMultiplicity.SetFillColor(ROOT.kBlue - 10)
# h_partonMultiplicity.SetLineColor(ROOT.kBlue)
# h_partonMultiplicity.Draw()
# ROOT.gPad.SetLogy(1)
# c_partonMultiplicity.SaveAs("partonMultiplicityDistribution.png")

c_nonTopMotherJets = ROOT.TCanvas("c_nonTopMotherJets", "Jets without Top as Mother", 800, 600)
h_nonTopMotherJets.SetFillColor(ROOT.kBlue - 10)
h_nonTopMotherJets.SetLineColor(ROOT.kBlue)
h_nonTopMotherJets.Draw()
ROOT.gPad.SetLogy(1)
c_nonTopMotherJets.SaveAs("nonTopMotherJets.png")

c_antitopMultiplicity = ROOT.TCanvas("c_antitopMultiplicity", "Anti-Top Multiplicity Distribution", 800, 600)
h_antitopMultiplicity.SetFillColor(ROOT.kBlue - 10)
h_antitopMultiplicity.SetLineColor(ROOT.kBlue)
h_antitopMultiplicity.Draw()
c_antitopMultiplicity.SaveAs("antitopMultiplicityDistribution.png")

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

c_HT = ROOT.TCanvas("c_HT", "HTDistribution", 800, 600)
h_HT.Draw()
ROOT.gPad.SetLogy(1)
c_HT.SaveAs("HT_distribution.png")

c_ele_HT = ROOT.TCanvas("c_ele_HT", "HTDistributionEle", 800, 600)
h_ele_HT.Draw()
ROOT.gPad.SetLogy(1)
c_ele_HT.SaveAs("HT_ele_distribution.png")

c_muon_HT = ROOT.TCanvas("c_muon_HT", "HTDistributionMuon", 800, 600)
h_muon_HT.Draw()
ROOT.gPad.SetLogy(1)
c_muon_HT.SaveAs("HT_muon_distribution.png")

# c_LHE_HT = ROOT.TCanvas("h_LHE_HT", "LHE HT; HT (GeV); Events", 800,600)
# h_LHE_HT.Draw()
# c_LHE_HT.SaveAs("LHE_HTincoming.png")

c_before = ROOT.TCanvas("c_before", "LHE_HT Before Selection", 800, 600)
h_LHE_HT_before.Draw()
ROOT.gPad.SetLogy(1)
c_before.SaveAs("LHE_HT_before_selection.png")

c_after = ROOT.TCanvas("c_after", "LHE_HT After Selection", 800, 600)
h_LHE_HT_after.Draw()
ROOT.gPad.SetLogy(1)
c_after.SaveAs("LHE_HT_after_selection.png")

c_ele_before = ROOT.TCanvas("c_ele_before", "LHE_HT Before Selection Electron Channel", 800, 600)
h_ele_LHE_HT_before.Draw()
ROOT.gPad.SetLogy(1)
c_ele_before.SaveAs("LHE_HT_before_selection_ele.png")

c_ele_after = ROOT.TCanvas("c_ele_after", "LHE_HT After Selection Electron Channel", 800, 600)
h_ele_LHE_HT_after.Draw()
ROOT.gPad.SetLogy(1)
c_ele_after.SaveAs("LHE_HT_after_selection_ele.png")

c_muon_before = ROOT.TCanvas("c_muon_before", "LHE_HT Before Selection Muon Channel", 800, 600)
h_muon_LHE_HT_before.Draw()
ROOT.gPad.SetLogy(1)
c_muon_before.SaveAs("LHE_HT_before_selection_muon.png")

c_muon_after = ROOT.TCanvas("c_muon_after", "LHE_HT After Selection Muon Channel", 800, 600)
h_muon_LHE_HT_after.Draw()
ROOT.gPad.SetLogy(1)
c_muon_after.SaveAs("LHE_HT_after_selection_muon.png")

c_ele_lepton_after = ROOT.TCanvas("c_ele_lepton_after", "LHE_HT After Lepton Selection Electron Channel", 800, 600)
h_ele_LHE_HT_after_lepton_cut.Draw()
ROOT.gPad.SetLogy(1)
c_ele_lepton_after.SaveAs("LHE_HT_after_lepton_selection_ele.png")

c_ele_jet_after = ROOT.TCanvas("c_ele_jet_after", "LHE_HT After Lepton & Jet Selection Electron Channel", 800, 600)
h_ele_LHE_HT_after_jet_cut.Draw()
ROOT.gPad.SetLogy(1)
c_ele_jet_after.SaveAs("LHE_HT_after_jet_selection_ele.png")

c_ele_met_after = ROOT.TCanvas("c_ele_met_after", "LHE_HT After Lepton & Jet & MET Selection Electron Channel", 800, 600) 
h_ele_LHE_HT_after_met_cut.Draw() 
ROOT.gPad.SetLogy(1)
c_ele_met_after.SaveAs("LHE_HT_after_met_selection_ele.png")


c_muon_lepton_after = ROOT.TCanvas("c_muon_lepton_after", "LHE_HT After Lepton Selection Muon Channel", 800, 600)
h_muon_LHE_HT_after_lepton_cut.Draw() 
ROOT.gPad.SetLogy(1)
c_muon_lepton_after.SaveAs("LHE_HT_after_lepton_selection_muon.png")

c_muon_jet_after = ROOT.TCanvas("c_muon_jet_after", "LHE_HT After Lepton & Jet Selection Muon Channel", 800, 600)
h_muon_LHE_HT_after_jet_cut.Draw()
ROOT.gPad.SetLogy(1)
c_muon_jet_after.SaveAs("LHE_HT_after_jet_selection_muon.png")

c_muon_met_after = ROOT.TCanvas("c_muon_met_after", "LHE_HT After Lepton & Jet & MET Selection Muon Channel", 800, 600)  
h_muon_LHE_HT_after_met_cut.Draw()
ROOT.gPad.SetLogy(1)
c_muon_met_after.SaveAs("LHE_HT_after_met_selection_muon.png")



c_hadronic_w_mass = ROOT.TCanvas("c_hadronic_w_mass", "Hadronic W Mass", 800, 600)
h_hadronic_w_mass.Draw()
ROOT.gPad.SetLogy(1)
c_hadronic_w_mass.SaveAs("hadronic_w_mass.png")

c_jetMultiplicity_fromW = ROOT.TCanvas("c_jetMultiplicity_fromW", "Jet Multiplicity from W", 800, 600)
h_jetMultiplicity_fromW.Draw()
c_jetMultiplicity_fromW.SaveAs("JetMultiplicityFromW.png")

c_both_decays = ROOT.TCanvas("c_both_decays", "Events with Both Decays", 800, 600)
h_both_decays.Draw()
c_both_decays.SaveAs("BothDecays.png")

print("Total number of events:", totalEvents)



# analyze("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/root_files/0000/GEN_LO_01j_102X_14.root")