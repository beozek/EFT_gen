# -*- coding: utf-8 -*-
import ROOT
import os
import glob
from array import array
import subprocess
import argparse
import sys
from DataFormats.FWLite import Events, Handle
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.Config as edm
from XRootD import client
from XRootD.client.flags import DirListFlags, StatInfoFlags, OpenFlags, QueryCode
import multiprocessing



ROOT.gROOT.SetBatch(True)

totalEvents = 0

output_dir = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/UL_beforentuple/nano/condor/plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

h_leptonPt = ROOT.TH1F("h_leptonPt", "Lepton pT ; pT (GeV);Events", 25, 0, 500)
h_leptoneta = ROOT.TH1F("h_leptoneta", "Lepton Eta ; #eta;Events", 100, -5, 5)
h_leptonphi = ROOT.TH1F("h_leptonphi", "Azimuthal Angle ; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
bin_edges = [-16.5, -14.5, -12.5, -10.5, 10.5, 12.5, 14.5, 16.5]
h_leptonFlavor = ROOT.TH1F("h_leptonFlavor", "Lepton Flavor; PDG ID;Events", len(bin_edges)-1, array('d', bin_edges))
h_leptonFlavor.GetXaxis().SetBinLabel(1, "muon-")
h_leptonFlavor.GetXaxis().SetBinLabel(2, "electron-")
h_leptonFlavor.GetXaxis().SetBinLabel(4, "electron+")
h_leptonFlavor.GetXaxis().SetBinLabel(5, "muon+")

h_electronPt = ROOT.TH1F("h_electronPt", "Electron pT ; pT (GeV);Events", 25, 0, 500)
h_electroneta = ROOT.TH1F("h_electroneta", "Electron #eta ; #eta;Events", 100, -5, 5)

h_muonPt = ROOT.TH1F("h_muonPt", "Muon pT ; pT (GeV);Events", 25, 0, 500)
h_muoneta = ROOT.TH1F("h_muoneta", " Muon #eta ; #eta;Events", 100, -5, 5)

h_hadronic_w_mass = ROOT.TH1F("h_hadronic_w_mass", "Hadronic Decaying W Mass ; M (GeV);Events", 10, 60, 100)

h_topPt = ROOT.TH1F("h_topPt", "Top Quark pT ; pT (GeV);Events", 100, 0, 2000)
h_topEta = ROOT.TH1F("h_topEta", "Top Quark #eta ;#eta;Events", 100, -5, 5)

h_antitopPt = ROOT.TH1F("h_antitopPt", "Anti-Top Quark p_{T} ; p_{T} [GeV];Events", 100, 0, 2000)
h_antitopEta = ROOT.TH1F("h_antitopEta", "Anti-Top Quark #eta ;#eta;Events", 100, -5, 5)

h_bquark_pt = ROOT.TH1F("h_bquark_pt", "b-quark pT ;pT (GeV);Events", 50, 0, 1000)
h_bquark_eta = ROOT.TH1F("h_bquark_eta", "b-quark #eta  ;#eta;Events", 100, -5, 5)

h_topMultiplicity = ROOT.TH1F("h_topMultiplicity", "Top Multiplicity ; N_{top};Events", 5, 0, 5)
h_antitopMultiplicity = ROOT.TH1F("h_antitopMultiplicity", "Anti-Top Multiplicity ; N_{antitop};Events", 5, 0, 5)

h_jetMultiplicity_fromW = ROOT.TH1F("h_jetMultiplicity_fromW", "Jet Multiplicity from W ; Number of Jets; Events", 10, 0, 5)

# h_MET = ROOT.TH1F("h_MET", "MET ;MET (GeV);Events", 100, 0, 200)

h_invariantMass = ROOT.TH1F("h_invariantMass", "Invariant Mass; M (GeV);Events", 250, 0, 5000)

h_jetMultiplicity = ROOT.TH1F("h_jetMultiplicity Without Cuts", "Number of Jets per Event", 10, 0, 50)

h_nonTopMotherJets = ROOT.TH1F("h_nonTopMotherJets", "Jets without Top as Mother; Count;Events", 10, 0, 50)

h_LHE_HT = ROOT.TH1F("h_LHE_HT", "LHE_HT ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_0_500 = ROOT.TH1F("h_LHE_HT_0_500", "LHE_HT Mtt = [0,500] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_500_750 = ROOT.TH1F("h_LHE_HT_500_750", "LHE_HT Mtt = [500,750] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_750_1000 = ROOT.TH1F("h_LHE_HT_750_1000", "LHE_HT Mtt = [750,1000] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_1000_1500 = ROOT.TH1F("h_LHE_HT_1000_1500", "LHE_HT Mtt = [1000,1500] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_1500Inf = ROOT.TH1F("h_LHE_HT_1500Inf", "LHE_HT Mtt = [1500,Inf) ; HT (GeV); Events", 150, 0, 3000)

h_both_decays = ROOT.TH1F("h_both_decays", "Events with Both Leptonic and Hadronic Decays; Number of Events; Count", 2, 0, 2)

h_jetFromW_pt = ROOT.TH1F("h_jetFromW_pt", "Jet pT from W ; pT (GeV);Events", 1000, 0, 1000)
h_jetFromW_eta = ROOT.TH1F("h_jetFromW_eta", "Jet Eta from W ; #eta;Events", 100, -5, 5)

h_leading_jet_pt = ROOT.TH1F("h_leading_jet_pt", "Leading Jet pT; pT (GeV);Events", 100, 0, 1000)
h_second_leading_jet_pt = ROOT.TH1F("h_second_leading_jet_pt", "Second Leading Jet pT; pT (GeV);Events", 100, 0, 1000)

h_jet_multiplicity_last_copy = ROOT.TH1F('h_jet_multiplicity_last_copy', 'Jet Multiplicity Last Copy;Number of Jets;Events', 10, 0, 10)
  
h_mtt_vs_LHEHT = ROOT.TH2F("h_mtt_vs_LHEHT", "Invariant Mass of ttbar vs. LHE HT;LHE HT (GeV);m_{tt} (GeV)", 50, 0, 1000, 50, 300, 5000)


h_jet_multiplicity_hardprocess = ROOT.TH1F('h_jet_multiplicity_hardprocess', 'Jet Multiplicity HardProcess before FSR;Number of Jets;Events', 10, 0, 10)

h_jet_multiplicity_ishardprocess = ROOT.TH1F('h_jet_multiplicity_ishardprocess', 'Jet Multiplicity isHardProcess ;Number of Jets;Events', 10, 0, 10)

h_pdgId_last_copy = ROOT.TH1F('h_pdgId_last_copy', 'PDG ID Last Copy',  51, -25.5, 25.5)
h_pdgId_first_copy = ROOT.TH1F('h_pdgId_first_copy', 'PDG ID First Copy', 51, -25.5, 25.5)
h_pdgId_ishardprocess = ROOT.TH1F('h_pdgId_ishardprocess', 'PDG ID isHardProcess', 51, -25.5, 25.5)
h_pdgId_fromhardprocess = ROOT.TH1F('h_pdgId_fromhardprocess', 'PDG ID fromHardProcess', 51, -25.5, 25.5)


def deltaR(eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = abs(phi1 - phi2)
    if dphi > ROOT.TMath.Pi():
        dphi = 2 * ROOT.TMath.Pi() - dphi
    return (deta * deta + dphi * dphi) ** 0.5
# deltaR calculates the deltaR distance in eta - phi space. 
# If this distance is less than a threshold (like 0.4, a typical jet size), we can say the jet is possibly from the top quark.         

both_decays_counter = 0

def passes_selection_HT(entry):
    LHE_HT = getattr(entry, "LHE_HT", -1)
                
    if LHE_HT < 800:
        return False
    
    return True

def is_last_copy(statusFlags):
    try:
        status_flags_int = int(statusFlags)
        return (status_flags_int & (1 << 13)) != 0 # (1 << 13), it indicates 14th element in the list which is isLastCopy(). FLAGS = ['isPrompt', 'isDecayedLeptonHadron', 'isTauDecayProduct', 'isPromptTauDecayProduct', 'isDirectTauDecayProduct', 'isDirectPromptTauDecayProduct', 'isDirectHadronDecayProduct', 'isHardProcess', 'fromHardProcess', 'isHardProcessTauDecayProduct', 'isDirectHardProcessTauDecayProduct', 'fromHardProcessBeforeFSR', 'isFirstCopy', 'isLastCopy', 'isLastCopyBeforeFSR']
    except ValueError:
        return False
    
def is_first_copy(statusFlags):
    try:
        status_flags_int = int(statusFlags)
        return (status_flags_int & (1 << 12)) != 0
    except ValueError:
        return False

def ishardprocess(statusFlags):
    try:
        status_flags_int = int(statusFlags)
        return (status_flags_int & (1 << 7)) != 0
    except ValueError:
        return False
    
def fromHardProcess(statusFlags):
    try:
        status_flags_int = int(statusFlags)
        return (status_flags_int & (1 << 11)) != 0
    except ValueError:
        return False

def process_event(entry, histograms, relevant_pdgIds):
    # if not passes_selection_HT(entry):
    #     return
    
    top_count = 0
    antitop_count = 0
    
    # leptons = []
    tops = []
    b_quarks = []
    w_bosons = []
    hadronic_top_pt = []
    
    last_copy_decays = []
    jets_from_w = []
    
    jets_from_w_info =[]
    
    jets_from_w_count = 0
    
    last_copy_top_decays = []
    last_copy_partons = []
    first_copy_partons = []
    hardprocess_beforeFSR = []
    ishard_process = []
    fromHardProcess_jets = []
    
    
    leptons = []
    
    w_quarks1 = []
    w_quarks2 = []
    w_quarks_indices = []
    
    met_vector = ROOT.TLorentzVector() 
    values_and_weights = []
    jets =[]
    
    leptonic_decay = False
    hadronic_decay = False
    
    electron_found = False
    muon_found = False   
    
    top_4vec = None
    antitop_4vec = None
    
    top_related_parton_indices = set()
    
    
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

        if is_last_copy(statusFlags):
            parton_4vec = ROOT.TLorentzVector()
            parton_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
            last_copy_partons.append((parton_4vec, i)) 
            
        if is_first_copy(statusFlags):
            parton_4vec = ROOT.TLorentzVector()
            parton_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
            first_copy_partons.append((parton_4vec, i)) 
        
        
        if ishardprocess(statusFlags):
            parton_4vec = ROOT.TLorentzVector()
            parton_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
            # if abs(pdgId) in (1,2,3,4,5,21):
            ishard_process.append((parton_4vec, entry.GenPart_pdgId[i])) 
        
        if fromHardProcess(statusFlags): 
            parton_4vec = ROOT.TLorentzVector()
            parton_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
            # if abs(pdgId) in (1,2,3,4,5,21): 
            fromHardProcess_jets.append((parton_4vec, i))
            
        
        # Check if particle is a top or antitop quark
        if abs(pdgId) in relevant_pdgIds and is_last_copy(statusFlags):  
            if abs(pdgId) == 6:
                top_related_parton_indices.add(i)
                
                w_daughter = None
                b_daughter = None
                last_copy_top_decays.append((pdgId))
                
                has_leptonic_w_decay = False
                has_hadronic_w_decay = False
                
                vec = ROOT.TLorentzVector()
                vec.SetPtEtaPhiM(entry.GenPart_pt[i], entry.GenPart_eta[i], entry.GenPart_phi[i], entry.GenPart_mass[i])
                if pdgId == 6:
                    top_4vec = vec
                else:
                    antitop_4vec = vec
                    
                tops.append((top_4vec, pdgId))
                
                
                # Checking if the j-th particle is a daughter of the i-th particle (top or anti-top quark)
                for j in range(entry.nGenPart):
                    if entry.GenPart_genPartIdxMother[j] == i and abs(entry.GenPart_pdgId[j]) in [24, 5]:
                        last_copy_decays.append((pt, eta, phi, pdgId, i)) # append as a tuple
                        top_related_parton_indices.add(j)
                        daughter_pdgId = entry.GenPart_pdgId[j]
                        
                        if daughter_pdgId != 6 and daughter_pdgId != -6:
                            if abs(daughter_pdgId) == 24:
                                
                                w_daughter = j
                                w_4vec = ROOT.TLorentzVector()
                                w_4vec.SetPtEtaPhiM(entry.GenPart_pt[w_daughter], entry.GenPart_eta[w_daughter], entry.GenPart_phi[w_daughter], entry.GenPart_mass[w_daughter])
                                w_bosons.append(w_4vec)
                                
                                if any(abs(entry.GenPart_pdgId[k]) in [11, 13] for k in range(entry.nGenPart) if entry.GenPart_genPartIdxMother[k] == w_daughter):
                                    has_leptonic_w_decay = True
                                elif any(abs(entry.GenPart_pdgId[k]) in [1, 2, 3, 4] for k in range(entry.nGenPart) if entry.GenPart_genPartIdxMother[k] == w_daughter):
                                    has_hadronic_w_decay = True
                                    
                            elif abs(daughter_pdgId) == 5:
                                b_daughter = j
                                b_4vec = ROOT.TLorentzVector()
                                b_4vec.SetPtEtaPhiM(entry.GenPart_pt[b_daughter], entry.GenPart_eta[b_daughter], entry.GenPart_phi[b_daughter], entry.GenPart_mass[b_daughter])
                                b_quarks.append((b_4vec, entry.GenPart_pdgId[j]))

                
                if has_leptonic_w_decay:
                    
                    # Check if W decays leptonically
                    for k in range(entry.nGenPart):
                        if entry.GenPart_genPartIdxMother[k] == w_daughter:
                            top_related_parton_indices.add(k)
                            if abs(entry.GenPart_pdgId[k]) in [11, 13]:  
                            
                                lepton_pdg = entry.GenPart_pdgId[k]
                                lepton_pt = entry.GenPart_pt[k]
                                lepton_eta = entry.GenPart_eta[k]
                                lepton_phi = entry.GenPart_phi[k]
                                
                                leptons.append((lepton_pt, lepton_eta, lepton_phi, lepton_pdg))
                                leptonic_decay = True
                                
                                if abs(lepton_pdg) == 11:
                                    electron_found = True
                                
                                elif abs(lepton_pdg) == 13:
                                    muon_found = True
           
                                
                        else: 
                            continue
                        
                        if abs(pdgId) in [12, 14, 16]:  
                            neutrino = ROOT.TLorentzVector()
                            neutrino.SetPtEtaPhiM(pt, eta, phi, mass)
                            met_vector += neutrino

       
                if has_hadronic_w_decay:
                      
                                      
                    # Check if W decays hadronically
                    for j in range(entry.nGenPart):
                        if entry.GenPart_genPartIdxMother[j] == w_daughter and abs(entry.GenPart_pdgId[j]) in [1, 2, 3, 4]:
                            w_quarks_indices.append(j)
                            top_related_parton_indices.add(j)
                    
                    
                    if len(w_quarks_indices) == 2:
                        hadronic_decay = True
                        hadronic_top_pt.append(pt)
                        
                        quark1_vec = ROOT.TLorentzVector()
                        quark2_vec = ROOT.TLorentzVector()
                        quark1_index, quark2_index = w_quarks_indices
                        
                        quark1_vec.SetPtEtaPhiM(entry.GenPart_pt[quark1_index], entry.GenPart_eta[quark1_index], entry.GenPart_phi[quark1_index], entry.GenPart_mass[quark1_index])
                        quark2_vec.SetPtEtaPhiM(entry.GenPart_pt[quark2_index], entry.GenPart_eta[quark2_index], entry.GenPart_phi[quark2_index], entry.GenPart_mass[quark2_index])
                        
                        w_quarks1.append((quark1_vec, entry.GenPart_pdgId[quark1_index]))
                        w_quarks2.append((quark2_vec, entry.GenPart_pdgId[quark2_index]))
                        
                        hadronic_w_mass = (quark1_vec + quark2_vec).M()
                        if 65 < hadronic_w_mass < 95: # I include this line to ensure that the events are indeed hadronic W decays
                            histograms['h_hadronic_w_mass'].Fill(hadronic_w_mass)
   
                            
            
                # b-quarks
                if b_daughter is not None:
                    b_vector = ROOT.TLorentzVector()
                    b_vector.SetPtEtaPhiM(entry.GenPart_pt[b_daughter], entry.GenPart_eta[b_daughter], entry.GenPart_phi[b_daughter], entry.GenPart_mass[b_daughter])
                    
            else: 
                continue  
        else:
            continue
    
    for _, pdgId in last_copy_partons:
        histograms['h_pdgId_last_copy'].Fill(pdgId) 
    
    for _, pdgId in first_copy_partons:
        histograms['h_pdgId_first_copy'].Fill(pdgId) 
        
    for _,pdgId in ishard_process:
        histograms['h_pdgId_ishardprocess'].Fill(pdgId)
    
    for _,pdgId in fromHardProcess_jets:
        histograms['h_pdgId_fromhardprocess'].Fill(pdgId)
    
    
    
    if len(w_quarks_indices) == 2 and len(b_quarks) == 2:
        # jet collection = jets
        jets = []
        for j in range(entry.nGenJet):
            jet_vec = ROOT.TLorentzVector()
            jet_vec.SetPtEtaPhiM(entry.GenJet_pt[j], entry.GenJet_eta[j], entry.GenJet_phi[j], 0)  # Assuming massless jets
            jets.append((jet_vec, j))
        
            
        partons = b_quarks + w_quarks1 + w_quarks2
        
        matched_jets_indices = set()
        matched_partons_indices = set()
        matches = []

        
        # matching wquarks+bquarks from top with jets (LAST COPY)
        for jet_index, jet in enumerate(jets):
            closest_deltaR = float('inf')
            closest_parton_index = None
            closest_parton_pdgId = None
            
            unmatched_partons = [(idx, parton) for idx, parton in enumerate(partons) if idx not in matched_partons_indices]
            
            if not unmatched_partons:
                continue
            
            closest_deltaR, closest_parton_index, closest_parton_pdgId = min(
                ((deltaR(jet[0].Eta(), jet[0].Phi(), parton[1][0].Eta(), parton[1][0].Phi()), parton[0], parton[1][1]) for parton in unmatched_partons),
                key=lambda x: x[0])
     

            
            if closest_deltaR < 0.4:
                matched_jets_indices.add(jet_index)
                matched_partons_indices.add(closest_parton_index)
                matches.append((jet, (partons[closest_parton_index][0], closest_parton_pdgId)))

            
        b_quark_jets = [jet for jet, parton in matches if abs(parton[1]) == 5]

        jets_from_w = [jet for jet, parton in matches if abs(parton[1]) in [1, 2, 3, 4]]
        
        combined_jets = list(set(b_quark_jets + jets_from_w))
    
        # matching partons in isHARDPROCESS with jets excluding ttbar jets
        additional_ishardprocess_jets = []
        matched_jets_indices_ishardprocess = set()
        matched_partons_indices_ishardprocess = set()
        for jet_index, jet in enumerate(jets):
            if jet_index not in matched_jets_indices: 
                closest_deltaR = float('inf')
                closest_parton_index = None
                closest_parton_pdgId = None
                
                unmatched_ishardprocess_partons = [(idx, parton) for idx, parton in enumerate(ishard_process) if idx not in matched_partons_indices_ishardprocess and idx not in top_related_parton_indices]

                if not unmatched_ishardprocess_partons:
                    continue
                
                closest_deltaR, closest_parton_index, closest_parton_pdgId = min(
                    ((deltaR(jet[0].Eta(), jet[0].Phi(), parton[0].Eta(), parton[0].Phi()), idx, parton[1]) for idx, parton in unmatched_ishardprocess_partons),
                    key=lambda x: x[0])
                
                if closest_deltaR < 0.4:
                    matched_jets_indices_ishardprocess.add(jet_index)
                    matched_partons_indices_ishardprocess.add(closest_parton_index)
                    additional_ishardprocess_jets.append((jet, ishard_process[closest_parton_index]))


        # if (len(b_quark_jets)<2 or len(jets_from_w)<2):
        #     print ("Total jets:", len(jets))
        #     print ("Total partons:", len(partons))
            
        #     print("bquarks matched: ", len(b_quark_jets))
        #     print("jets_from_w matched: ", len(jets_from_w))
            
        #     for dR, jet_index, parton_index in dR_list:
        #         if dR < 5:
        #             print("Delta R: {}, Jet index: {}, Parton index: {}". format(dR,jet_index, parton_index))
        
        
        
        # checking if there is any overlap 
        jets_from_b_set = set(b_quark_jets)
        jets_from_w_set = set(jets_from_w)

        overlapping_jets = jets_from_b_set.intersection(jets_from_w_set)
        if len(overlapping_jets)>0:
            print("overlapping: ", len(overlapping_jets))

        
        # matching partons in fromHARDPROCESS with jets excluding ttbar jets
        additional_fromhardprocess_jets = []
        matched_jets_indices_fromhardprocess = set()
        matched_partons_indices_fromhardprocess = set()
        for jet_index, jet in enumerate(jets):
            if jet_index not in matched_jets_indices: 
                closest_deltaR = float('inf')
                closest_parton_index = None
                closest_parton_pdgId = None
                
                unmatched_fromhardprocess_partons = [(idx, parton) for idx, parton in enumerate(fromHardProcess_jets) if idx not in matched_partons_indices_fromhardprocess and idx not in top_related_parton_indices]

                if not unmatched_fromhardprocess_partons:
                    continue
                
                closest_deltaR, closest_parton_index, closest_parton_pdgId = min(
                    ((deltaR(jet[0].Eta(), jet[0].Phi(), parton[0].Eta(), parton[0].Phi()), idx, parton[1]) for idx, parton in unmatched_fromhardprocess_partons),
                    key=lambda x: x[0])
                
                if closest_deltaR < 0.4:
                    matched_jets_indices_fromhardprocess.add(jet_index)
                    matched_partons_indices_fromhardprocess.add(closest_parton_index)
                    additional_fromhardprocess_jets.append((jet, fromHardProcess_jets[closest_parton_index]))



        
        # last copy matching list
        combined_jets = list(set(b_quark_jets + jets_from_w))
        
        # isHardProcess jet matching list
        total_jets_count = len(combined_jets) + len([jet for jet, parton in additional_ishardprocess_jets if abs(parton[1]) in [1, 2, 3, 4, 5, 21]])
        
        # fromHardProcess jet matching list
        matched_quark_jets_hardprocess = len(combined_jets) + len([jet for jet, parton in additional_fromhardprocess_jets if abs(parton[1]) in [1, 2, 3, 4, 5, 21]])

        
        
        histograms['h_jet_multiplicity_last_copy'].Fill(len(combined_jets))
        histograms['h_jet_multiplicity_ishardprocess'].Fill(total_jets_count)  
            
        histograms['h_jet_multiplicity_hardprocess'].Fill(matched_quark_jets_hardprocess)  
        

        histograms['h_jetMultiplicity'].Fill(entry.nGenJet)
 
        jet_pt_cut = 10
        leading_jet, second_leading_jet = select_leading_jets_from_matched(matches, jet_pt_cut) 
    
        for lepton in leptons:
            lepton_pt, lepton_eta, lepton_phi, lepton_pdgId = lepton
            
            histograms['h_leptonPt'].Fill(lepton_pt)
            histograms['h_leptoneta'].Fill(lepton_eta)
            histograms['h_leptonphi'].Fill(lepton_phi)
            histograms['h_leptonFlavor'].Fill(entry.GenPart_pdgId[k])

            
            if abs(lepton_pdgId) == 11:
                histograms['h_electronPt'].Fill(lepton_pt)
                histograms['h_electroneta'].Fill(lepton_eta)
                
                                    
            elif abs(lepton_pdgId) == 13:
                histograms['h_muonPt'].Fill(lepton_pt)
                histograms['h_muoneta'].Fill(lepton_eta)
                
        
        for top_4vec, pdgId in tops:
            if pdgId == 6:
                top_count += 1
                histograms['h_topPt'].Fill(top_4vec.Pt())
                histograms['h_topEta'].Fill(top_4vec.Eta())
 
                
            elif pdgId == -6:
                antitop_count += 1
                histograms['h_antitopPt'].Fill(antitop_4vec.Pt())
                histograms['h_antitopEta'].Fill(antitop_4vec.Eta())
 
            histograms['h_topMultiplicity'].Fill(top_count)
            
            histograms['h_antitopMultiplicity'].Fill(antitop_count)
            
        for b_quark in b_quarks:
            b_vector, b_index = b_quark 
            
            histograms['h_bquark_pt'].Fill(b_vector.Pt())
            histograms['h_bquark_eta'].Fill(b_vector.Eta())

        for jet_info in jets_from_w_info:
            jet_idx, jet_pt, jet_eta, jet_phi = jet_info
            histograms['h_jetFromW_pt'].Fill(jet_pt)
            histograms['h_jetFromW_eta'].Fill(jet_eta)
            
        
        histograms['h_jetMultiplicity_fromW'].Fill(jets_from_w_count)
       
        # histograms['h_MET'].Fill(met_vector.Pt())
                
            
        if top_4vec and antitop_4vec:
            ttbar = top_4vec + antitop_4vec
            m_tt = ttbar.M()
            p_tt = ttbar.Pt()
            eta_tt = ttbar.Eta()

            histograms['h_invariantMass'].Fill(ttbar.M())
       
            LHE_HT = getattr(entry, "LHE_HT", -1)
            if LHE_HT >= 0:                    
                    
                LHE_HT = getattr(entry, "LHE_HT", -1)
                if LHE_HT >= 0:
    
                    if 0 <= m_tt < 500:
                        histograms['h_LHE_HT_0_500'].Fill(LHE_HT)
                    elif 500 <= m_tt < 750:
                        histograms['h_LHE_HT_500_750'].Fill(LHE_HT)

                    elif 750 <= m_tt < 1000:
                        histograms['h_LHE_HT_750_1000'].Fill(LHE_HT)
                        
                    elif 1000 <= m_tt < 1500:
                        histograms['h_LHE_HT_1000_1500'].Fill(LHE_HT)
                        
                    elif m_tt >= 1500:
                        histograms['h_LHE_HT_1500Inf'].Fill(LHE_HT)
                   
            
        
        
        # HT variable from data in ttree
        LHE_HT = getattr(entry, "LHE_HT", -1)
        if LHE_HT >= 0:
            histograms['h_mtt_vs_LHEHT'].Fill(LHE_HT, m_tt)
            histograms['h_LHE_HT'].Fill(LHE_HT)
                    
        
        if leading_jet is not None and second_leading_jet is not None:
            if leading_jet:
                histograms['h_leading_jet_pt'].Fill(leading_jet[0].Pt()) #leading_jet[0] contains the pt of the leading jet
            if second_leading_jet:
                histograms['h_second_leading_jet_pt'].Fill(second_leading_jet[0].Pt())

       
    return leptons, tops, hadronic_top_pt, b_quarks, last_copy_partons



# This function identifies jets that are closely matched with last copy partons. 
# It appends a tuple to matched_jets which includes the jet and its index in the GenJet collection.

def one_to_one_matching(entry, b_quarks, w_quarks1, w_quarks2):
    
    jets = []
    for j in range(entry.nGenJet):
        jet_vec = ROOT.TLorentzVector()
        jet_vec.SetPtEtaPhiM(entry.GenJet_pt[j], entry.GenJet_eta[j], entry.GenJet_phi[j], 0)  # Assuming massless jets
        jets.append(jet_vec)
        
    partons = b_quarks + w_quarks1 + w_quarks2
    
    matched_jets_indices = set()
    matched_partons_indices = set()
    matches = []

    for jet_index, jet in enumerate(jets):
        closest_deltaR = float('inf')
        closest_parton_index = None
        for parton_index, (parton_vec, _) in enumerate(partons):
            dR = deltaR(jet.Eta(), jet.Phi(), parton_vec.Eta(), parton_vec.Phi())
            if dR < closest_deltaR and parton_index not in matched_partons_indices:
                closest_deltaR = dR
                closest_parton_index = parton_index
        
        if closest_deltaR < 0.4 and closest_parton_index is not None:
            matched_jets_indices.add(jet_index)
            matched_partons_indices.add(closest_parton_index)
            matches.append((jets[jet_index], partons[closest_parton_index]))

    return matches


# This function filters and sorts the jets based on their Pt, 
# then identifies the leading and second-leading jets.
def select_leading_jets_from_matched(matches, jet_pt_cut):
    
    filtered_jets = [(jet, pdg_id) for (jet, _), pdg_id in matches if jet.Pt() > jet_pt_cut]
    # Sort the matched jets by their pT in descending order
    sorted_jets = sorted(filtered_jets, key=lambda jet_tuple: jet_tuple[0].Pt(), reverse=True)

    # Select the leading and second leading jets
    leading_jet = sorted_jets[0] if len(sorted_jets) > 0 else None
    second_leading_jet = sorted_jets[1] if len(sorted_jets) > 1 else None

    return leading_jet, second_leading_jet


# This function checks if any of the b-quarks (from the b_quarks list, so it is from top) is the same as the leading or second-leading jet (identified by their indices). 
# If it finds a match, it returns True along with the b-quark's vector (b_vector)
# Otherwise, it returns False and None


# def check_b_jet_from_top(b_quarks, leading_jet, second_leading_jet):
#     for b_quark in b_quarks:
#         b_vector, _ = b_quark
#         if leading_jet and deltaR(leading_jet[0].Eta(), leading_jet[0].Phi(), b_vector.Eta(), b_vector.Phi()) < 0.4:
#             return True, b_vector
#         elif second_leading_jet and deltaR(second_leading_jet[0].Eta(), second_leading_jet[0].Phi(), b_vector.Eta(), b_vector.Phi()) < 0.4:
#             return True, b_vector
#     return False, None

# This function correctly identifies the leading b-quark that is not part of the leading or second-leading jets. 
# It iterates through the b_quarks, excludes those that match the leading or second-leading jets, and then finds the one with the highest Pt.
def find_leading_b_quark(b_quarks, leading_jet, second_leading_jet, last_copy_partons):
    highest_pt = 0
    leading_b_quark = None
    for b_quark in b_quarks:
        b_vector, _ = b_quark
        if leading_jet and deltaR(leading_jet[0].Eta(), leading_jet[0].Phi(), b_vector.Eta(), b_vector.Phi()) < 0.4:
            continue
        if second_leading_jet and deltaR(second_leading_jet[0].Eta(), second_leading_jet[0].Phi(), b_vector.Eta(), b_vector.Phi()) < 0.4:
            continue
        if b_vector.Pt() > highest_pt:
            highest_pt = b_vector.Pt()
            leading_b_quark = b_quark
    # veto if no suitable b-quark is found
    return leading_b_quark if highest_pt > 30 else None



def analyze(filename):
    print("Processing file:", filename)
    
    # file = ROOT.TFile.Open(filename)
    # tree = file.Get("Events")
    
    if not os.path.isfile(filename):
        print "Error: The path provided is not a file:", filename
        return None

    try:
        file = ROOT.TFile.Open(filename)
        if not file or file.IsZombie():
            print "Error: Unable to open file:", filename
            return None

        tree = file.Get("Events")
        
    except Exception as e:
        print "An error occurred while processing the file {}: {}".format(filename, str(e))
        return None
    
    global totalEvents
    totalEvents += tree.GetEntries()
    print("Number of events in file:", tree.GetEntries())
    
    relevant_pdgIds = {12, 14, 16, 24, 1, 2, 3, 4, 5, 6, 21, 11, 13, 15}
    
    histograms = {
    'h_leptonPt': h_leptonPt,
    'h_leptoneta': h_leptoneta,
    'h_leptonphi': h_leptonphi,
    'h_leptonFlavor': h_leptonFlavor,
    'h_electronPt': h_electronPt,
    'h_electroneta': h_electroneta,
    'h_muonPt': h_muonPt,
    'h_muoneta': h_muoneta,
    'h_hadronic_w_mass': h_hadronic_w_mass,
    'h_topPt': h_topPt,
    'h_topEta': h_topEta,
    'h_antitopPt': h_antitopPt,
    'h_antitopEta': h_antitopEta,
    'h_topMultiplicity': h_topMultiplicity,
    'h_antitopMultiplicity': h_antitopMultiplicity,
    'h_jetMultiplicity_fromW': h_jetMultiplicity_fromW,
    # 'h_MET': h_MET,
    'h_invariantMass': h_invariantMass,
    'h_jetMultiplicity': h_jetMultiplicity,
    'h_nonTopMotherJets': h_nonTopMotherJets,
    'h_LHE_HT' : h_LHE_HT,
    'h_LHE_HT_0_500' : h_LHE_HT_0_500,
    'h_LHE_HT_500_750' : h_LHE_HT_500_750,
    'h_LHE_HT_750_1000' : h_LHE_HT_750_1000,
    'h_LHE_HT_1000_1500' : h_LHE_HT_1000_1500,
    'h_LHE_HT_1500Inf' : h_LHE_HT_1500Inf,
    'h_both_decays': h_both_decays,
    'h_jetFromW_pt': h_jetFromW_pt,
    'h_jetFromW_eta': h_jetFromW_eta,
    'h_leading_jet_pt' : h_leading_jet_pt,
    'h_second_leading_jet_pt' : h_second_leading_jet_pt,
    "h_jet_multiplicity_last_copy" : h_jet_multiplicity_last_copy,
    "h_mtt_vs_LHEHT" : h_mtt_vs_LHEHT,
    "h_bquark_pt" : h_bquark_pt,
    "h_bquark_eta": h_bquark_eta,
    "h_pdgId_last_copy": h_pdgId_last_copy,
    "h_pdgId_first_copy": h_pdgId_first_copy,
    "h_pdgId_ishardprocess" : h_pdgId_ishardprocess,
    "h_pdgId_fromhardprocess" : h_pdgId_fromhardprocess,
    "h_jet_multiplicity_hardprocess" : h_jet_multiplicity_hardprocess,
    "h_jet_multiplicity_ishardprocess" : h_jet_multiplicity_ishardprocess,

    
}
    
    for entry in tree:
        process_event(entry, histograms, relevant_pdgIds)
    
    

    
    file.Close()
    
    return histograms


def createCanvas(histogram, title, filename, logy=False, fillColor=None, lineColor=None):
    canvas = ROOT.TCanvas(title, title, 800, 600)
    if fillColor is not None:
        histogram.SetFillColor(fillColor)
    if lineColor is not None:
        histogram.SetLineColor(lineColor)
    histogram.Draw()
    if logy:
        ROOT.gPad.SetLogy(1)
    canvas_filepath = os.path.join(output_dir, filename)
    canvas.SaveAs(canvas_filepath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python EFT_nanofiles_fully_semileptonic.py <input file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_dir = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/UL_beforentuple/nano/condor/plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    histograms = analyze(input_filename)
    
    output_filename = os.path.basename(input_filename).replace('.root', '_histograms.root')
    output_file_path = os.path.join(output_dir, output_filename)
    output_file = ROOT.TFile(output_file_path, "RECREATE")
    for name, hist in histograms.items():
        hist.SetDirectory(output_file)
        hist.Write()
    output_file.Close()
    
    # for name, hist in histograms.items():
    #     canvas_title = "{} Canvas".format(name)
    #     canvas_filename = "{}.png".format(name)
    #     createCanvas(hist, canvas_title, canvas_filename, output_dir=output_dir)

    print("Processed: {}".format(input_filename))

# createCanvas(h_leptonPt, "Lepton pT Distribution", "leptonPtDistribution.png", True)
# createCanvas(h_leptoneta, "Lepton Eta Distribution", "leptonEtaDistribution.png")
# createCanvas(h_leptonphi, "Lepton Phi Distribution", "leptonPhiDistribution.png")
# createCanvas(h_leptonFlavor, "Lepton Flavor Distribution", "leptonFlavorDistribution.png")
# createCanvas(h_electronPt, "Electron pT Distribution", "electronPtDistribution.png", True)
# createCanvas(h_electronPt_aftercut200, "Electron pT After Cut 200 Distribution", "electronPtAfterCut200Distribution.png", True)
# createCanvas(h_electronPt_aftercut400, "Electron pT After Cut 400 Distribution", "electronPtAfterCut400Distribution.png", True)
# createCanvas(h_electroneta, "Electron Eta Distribution", "electronEtaDistribution.png")
# createCanvas(h_electroneta_aftercut200, "Electron Eta After Cut 200 Distribution", "electronEtaAfterCut200Distribution.png")
# createCanvas(h_electroneta_aftercut400, "Electron Eta After Cut 400 Distribution", "electronEtaAfterCut400Distribution.png")
# createCanvas(h_muonPt, "Muon pT Distribution", "muonPtDistribution.png", True)
# createCanvas(h_muonPt_aftercut200, "Muon pT After Cut 200 Distribution", "muonPtAfterCut200Distribution.png", True)
# createCanvas(h_muonPt_aftercut400, "Muon pT After Cut 400 Distribution", "muonPtAfterCut400Distribution.png", True)
# createCanvas(h_muoneta, "Muon Eta Distribution", "muonEtaDistribution.png")
# createCanvas(h_muoneta_aftercut200, "Muon Eta After Cut 200 Distribution", "muonEtaAfterCut200Distribution.png")
# createCanvas(h_muoneta_aftercut400, "Muon Eta After Cut 400 Distribution", "muonEtaAfterCut400Distribution.png")
# createCanvas(h_hadronic_w_mass, "Hadronic Decaying W Mass ", "hadronicWMassDistribution.png")
# createCanvas(h_hadronic_w_mass_aftercut200, "Hadronic Decaying W Mass After Cuts & TopPt>200", "hadronicWMassAfterCut200Distribution.png")
# createCanvas(h_hadronic_w_mass_aftercut400, "Hadronic Decaying W Mass After Cuts & TopPt>400", "hadronicWMassAfterCut400Distribution.png")
# createCanvas(h_topPt, "Top Quark pT ", "topPtDistribution.png", True)
# createCanvas(h_topPt_aftercut200, "Top Quark pT After Cuts & TopPt>200", "topPtAfterCut200Distribution.png", True)
# createCanvas(h_topPt_aftercut400, "Top Quark pT After Cuts & TopPt>400", "topPtAfterCut400Distribution.png", True)
# createCanvas(h_antitopPt, "Anti-Top Quark pT ", "antitopPtDistribution.png", True)
# createCanvas(h_antitopPt_aftercut200, "Anti-Top Quark pT After Cuts & TopPt>200", "antitopPtAfterCut200Distribution.png", True)
# createCanvas(h_antitopPt_aftercut400, "Anti-Top Quark pT After Cuts & TopPt>400", "antitopPtAfterCut400Distribution.png", True)
# createCanvas(h_bquark_pt_electron, "b-quark pT Electron Channel", "bquarkPtDistribution.png", True)
# createCanvas(h_bquark_eta_electron, "b-quark Eta Electron Channel", "bquarkEtaDistribution.png")
# createCanvas(h_bquark_pt_muon, "b-quark pT Muon Channel", "bquarkPtDistribution.png", True)
# createCanvas(h_bquark_eta_muon, "b-quark Eta Muon Channel ", "bquarkEtaDistribution.png")

# createCanvas(h_bquark_pt_aftercut200, "b-quark pT After Cuts & TopPt>200", "bquarkPtAfterCut200Distribution.png", True)
# createCanvas(h_bquark_pt_aftercut400, "b-quark pT After Cuts & TopPt>400", "bquarkPtAfterCut400Distribution.png", True)
# createCanvas(h_topMultiplicity, "Top Multiplicity ", "topMultiplicityDistribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_topMultiplicity_aftercut200, "Top Multiplicity After Cuts & TopPt>200", "topMultiplicityAfterCut200Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_topMultiplicity_aftercut400, "Top Multiplicity After Cuts & TopPt>400", "topMultiplicityAfterCut400Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_antitopMultiplicity, "Anti-Top Multiplicity ", "antitopMultiplicityDistribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_antitopMultiplicity_aftercut200, "Anti-Top Multiplicity After Cuts & Pt>200", "antitopMultiplicityAfterCut200Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_antitopMultiplicity_aftercut400, "Anti-Top Multiplicity After Cuts & Pt>400", "antitopMultiplicityAfterCut400Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_jetMultiplicity_fromW, "Jet Multiplicity from W ", "jetMultiplicityFromWDistribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_jetMultiplicity_fromW_after200, "Jet Multiplicity from W After Cuts & Pt>200", "jetMultiplicityFromWAfterCut200Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_jetMultiplicity_fromW_after400, "Jet Multiplicity from W After Cuts & Pt>400", "jetMultiplicityFromWAfterCut400Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_MET, "MET ", "METDistribution.png")
# createCanvas(h_MET_after200, "MET After Cuts & Pt>200", "METAfterCut200Distribution.png")
# createCanvas(h_MET_after400, "MET After Cuts & Pt>400", "METAfterCut400Distribution.png")
# createCanvas(h_invariantMass, "Invariant Mass", "invariantMassDistribution.png", True)
# createCanvas(h_invariantMass_aftercut200, "Invariant Mass After Cuts & Pt>200", "invariantMassAfterCut200Distribution.png", True)
# createCanvas(h_invariantMass_aftercut400, "Invariant Mass After Cuts & Pt>400", "invariantMassAfterCut400Distribution.png", True)
# createCanvas(h_jetMultiplicity, "Jet Multiplicity Without Cuts", "jetMultiplicityDistribution.png", True, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_nonTopMotherJets, "Jets without Top as Mother", "nonTopMotherJetsDistribution.png")
# createCanvas(h_LHE_HT_before, "LHE_HT ", "LHE_HTBeforeCutsDistribution.png", True)
# createCanvas(h_muon_LHE_HT_aftercut200, "Muon Channel LHE_HT After Cuts & Pt>200", "muonLHE_HTAfterCut200Distribution.png", True)
# createCanvas(h_muon_LHE_HT_aftercut400, "Muon Channel LHE_HT After Cuts & Pt>400", "muonLHE_HTAfterCut400Distribution.png", True)
# createCanvas(h_ele_LHE_HT_aftercut200, "Electron Channel LHE_HT After Cuts & Pt>200", "eleLHE_HTAfterCut200Distribution.png", True)
# createCanvas(h_ele_LHE_HT_aftercut400, "Electron Channel LHE_HT After Cuts & Pt>400", "eleLHE_HTAfterCut400Distribution.png", True)
# createCanvas(h_ele_LHE_HT_before, "Electron Channel LHE_HT", "eleLHE_HTBeforeCutsDistribution.png", True)
# createCanvas(h_ele_LHE_HT_after_lepton_cut, "Electron Channel LHE_HT After Electron Pt&Eta Cut", "eleLHE_HTAfterLeptonCutDistribution.png", True)
# createCanvas(h_ele_LHE_HT_after_jet_cut, "Electron Channel LHE_HT After Electron and Jet Cuts", "eleLHE_HTAfterJetCutDistribution.png", True)
# createCanvas(h_ele_LHE_HT_after_met_cut, "Electron Channel LHE_HT After Electron, Jet, and MET Cut", "eleLHE_HTAfterMETCutDistribution.png", True)
# createCanvas(h_ele_LHE_HT_after_toppt200_cut, "Electron Channel LHE_HT After Cuts & Pt>200", "eleLHE_HTAfterTopPt200CutDistribution.png", True)
# createCanvas(h_ele_LHE_HT_after_toppt400_cut, "Electron Channel LHE_HT After Cuts & Pt>400", "eleLHE_HTAfterTopPt400CutDistribution.png", True)
# createCanvas(h_muon_LHE_HT_before, "Muon Channel LHE_HT", "muonLHE_HTBeforeCutsDistribution.png", True)
# createCanvas(h_muon_LHE_HT_after_lepton_cut, "Muon Channel LHE_HT After Muon Pt&Eta Cut", "muonLHE_HTAfterLeptonCutDistribution.png", True)
# createCanvas(h_muon_LHE_HT_after_jet_cut, "Muon Channel LHE_HT After Muon and Jet Cuts", "muonLHE_HTAfterJetCutDistribution.png", True)
# createCanvas(h_muon_LHE_HT_after_met_cut, "Muon Channel LHE_HT After Muon, Jet, and MET Cut", "muonLHE_HTAfterMETCutDistribution.png", True)
# createCanvas(h_muon_LHE_HT_after_toppt200_cut, "Muon Channel LHE_HT After Cuts & Pt>200", "muonLHE_HTAfterTopPt200CutDistribution.png", True)
# createCanvas(h_muon_LHE_HT_after_toppt400_cut, "Muon Channel LHE_HT After Cuts & Pt>400", "muonLHE_HTAfterTopPt400CutDistribution.png", True)
# createCanvas(h_both_decays, "Events with Both Leptonic and Hadronic Decays", "bothdecays.png", False )     
# createCanvas(h_jetFromW_pt, "Jet pT from W ; pT (GeV)", "jetfromW_pt.png")
# createCanvas(h_jetFromW_eta,"Jet Eta from W ", "jetfromW_eta.png")
# createCanvas(h_jetFromW_pt_aftercut200, "Jet pT from W After Cuts & TopPt>200; pT (GeV)", "jetfromW_pt_after200.png")
# createCanvas(h_jetFromW_pt_aftercut400, "Jet pT from W After Cuts & TopPt>400; pT (GeV)", "jetfromW_pt_after400.png") 
       
print("Total number of events:", totalEvents)
