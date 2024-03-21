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

output_dir = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_comparePowheg"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

h_leptonPt = ROOT.TH1F("h_leptonPt", "Lepton pT Before Cuts; pT (GeV);Events", 50, 0, 1000)
h_leptoneta = ROOT.TH1F("h_leptoneta", "Lepton Eta Before Cuts; #eta;Events", 100, -5, 5)
h_leptonphi = ROOT.TH1F("h_leptonphi", "Azimuthal Angle Before Cuts; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
bin_edges = [-16.5, -14.5, -12.5, -10.5, 10.5, 12.5, 14.5, 16.5]
h_leptonFlavor = ROOT.TH1F("h_leptonFlavor", "Lepton Flavor; PDG ID;Events", len(bin_edges)-1, array('d', bin_edges))
h_leptonFlavor.GetXaxis().SetBinLabel(1, "muon-")
h_leptonFlavor.GetXaxis().SetBinLabel(2, "electron-")
h_leptonFlavor.GetXaxis().SetBinLabel(4, "electron+")
h_leptonFlavor.GetXaxis().SetBinLabel(5, "muon+")

h_electronPt = ROOT.TH1F("h_electronPt", "Electron pT Before Cuts; pT (GeV);Events", 50, 0, 1000)
h_electroneta = ROOT.TH1F("h_electroneta", "Electron #eta Before Cuts; #eta;Events", 100, -5, 5)

h_muonPt = ROOT.TH1F("h_muonPt", "Muon pT Before Cuts; pT (GeV);Events", 50, 0, 1000)
h_muoneta = ROOT.TH1F("h_muoneta", " Muon #eta Before Cuts; #eta;Events", 100, -5, 5)

h_hadronic_w_mass = ROOT.TH1F("h_hadronic_w_mass", "Hadronic Decaying W Mass Before Cuts; M (GeV);Events", 10, 60, 100)

h_topPt = ROOT.TH1F("h_topPt", "Top Quark pT Before Cuts; pT (GeV);Events", 150, 0, 3000)
h_topEta = ROOT.TH1F("h_topEta", "Top Quark #eta ;#eta;Events", 100, -5, 5)

h_antitopPt = ROOT.TH1F("h_antitopPt", "Anti-Top Quark p_{T} Before Cuts; p_{T} [GeV];Events", 150, 0, 3000)
h_antitopEta = ROOT.TH1F("h_antitopEta", "Anti-Top Quark #eta ;#eta;Events", 100, -5, 5)

h_bquark_pt = ROOT.TH1F("h_bquark_pt", "b-quark pT ;pT (GeV);Events", 150, 0, 1000)
h_bquark_eta = ROOT.TH1F("h_bquark_eta", "b-quark #eta  ;#eta;Events", 100, -5, 5)

h_topMultiplicity = ROOT.TH1F("h_topMultiplicity", "Top Multiplicity Before Cuts; N_{top};Events", 5, 0, 5)
h_antitopMultiplicity = ROOT.TH1F("h_antitopMultiplicity", "Anti-Top Multiplicity Before Cuts; N_{antitop};Events", 5, 0, 5)

h_jetMultiplicity_fromW = ROOT.TH1F("h_jetMultiplicity_fromW", "Jet Multiplicity from W Before Cuts; Number of Jets; Events", 10, 0, 5)

# h_MET = ROOT.TH1F("h_MET", "MET Before Cuts;MET (GeV);Events", 100, 0, 200)

h_invariantMass = ROOT.TH1F("h_invariantMass", "Invariant Mass; M (GeV);Events", 250, 0, 5000)

h_jetMultiplicity = ROOT.TH1F("h_jetMultiplicity Without Cuts", "Number of Jets per Event", 10, 0, 50)

h_nonTopMotherJets = ROOT.TH1F("h_nonTopMotherJets", "Jets without Top as Mother; Count;Events", 10, 0, 50)

h_LHE_HT = ROOT.TH1F("h_LHE_HT", "LHE_HT ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_0_500 = ROOT.TH1F("h_LHE_HT_0_500", "LHE_HT Mtt = [0,500] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_500_750 = ROOT.TH1F("h_LHE_HT_500_750", "LHE_HT Mtt = [500,750] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_750_1000 = ROOT.TH1F("h_LHE_HT_750_1000", "LHE_HT Mtt = [750,1000] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_1000_1500 = ROOT.TH1F("h_LHE_HT_1000_1500", "LHE_HT Mtt = [1000,1500] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_1500Inf = ROOT.TH1F("h_LHE_HT_1500Inf", "LHE_HT Mtt = [1000,1500] ; HT (GeV); Events", 150, 0, 3000)

h_both_decays = ROOT.TH1F("h_both_decays", "Events with Both Leptonic and Hadronic Decays; Number of Events; Count", 2, 0, 2)

h_jetFromW_pt = ROOT.TH1F("h_jetFromW_pt", "Jet pT from W Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_jetFromW_eta = ROOT.TH1F("h_jetFromW_eta", "Jet Eta from W Before Cuts; #eta;Events", 100, -5, 5)

h_leading_jet_pt = ROOT.TH1F("h_leading_jet_pt", "Leading Jet pT; pT (GeV);Events", 100, 0, 1000)
h_second_leading_jet_pt = ROOT.TH1F("h_second_leading_jet_pt", "Second Leading Jet pT; pT (GeV);Events", 100, 0, 1000)

h_jet_multiplicity_last_copy = ROOT.TH1F('h_jet_multiplicity_last_copy', 'Jet Multiplicity Last Copy;Number of Jets;Events', 10, 0, 10)
  
h_mtt_vs_LHEHT = ROOT.TH2F("h_mtt_vs_LHEHT", "Invariant Mass of ttbar vs. LHE HT;LHE HT (GeV);m_{tt} (GeV)", 50, 0, 1000, 50, 300, 5000)




# weight SM: "LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p"

h_leptonPt_weightSM = ROOT.TH1F("h_leptonPt_weightSM", "Lepton pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_leptoneta_weightSM = ROOT.TH1F("h_leptoneta_weightSM", "Lepton Eta Before Cuts; #eta;Events", 100, -5, 5)
h_leptonphi_weightSM = ROOT.TH1F("h_leptonphi_weightSM", "Azimuthal Angle Before Cuts; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
bin_edges = [-16.5, -14.5, -12.5, -10.5, 10.5, 12.5, 14.5, 16.5]
h_leptonFlavor_weightSM = ROOT.TH1F("h_leptonFlavor_weightSM", "Lepton Flavor; PDG ID;Events", len(bin_edges)-1, array('d', bin_edges))
h_leptonFlavor_weightSM.GetXaxis().SetBinLabel(1, "muon-")
h_leptonFlavor_weightSM.GetXaxis().SetBinLabel(2, "electron-")
h_leptonFlavor_weightSM.GetXaxis().SetBinLabel(4, "electron+")
h_leptonFlavor_weightSM.GetXaxis().SetBinLabel(5, "muon+")

h_electronPt_weightSM = ROOT.TH1F("h_electronPt_weightSM", "Electron pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_electroneta_weightSM = ROOT.TH1F("h_electroneta_weightSM", "Electron #eta Before Cuts; #eta;Events", 100, -5, 5)

h_muonPt_weightSM = ROOT.TH1F("h_muonPt_weightSM", "Muon pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_muoneta_weightSM = ROOT.TH1F("h_muoneta_weightSM", " Muon #eta Before Cuts; #eta;Events", 100, -5, 5)

h_hadronic_w_mass_weightSM = ROOT.TH1F("h_hadronic_w_mass_weightSM", "Hadronic Decaying W Mass Before Cuts; M (GeV);Events", 10, 60, 100)

h_topPt_weightSM = ROOT.TH1F("h_topPt_weightSM", "Top Quark pT Before Cuts; pT (GeV);Events", 1000, 0, 3000)
h_topEta_weightSM = ROOT.TH1F("h_topEta_weightSM", "Top Quark #eta ;#eta;Events", 100, -5, 5)

h_antitopPt_weightSM = ROOT.TH1F("h_antitopPt_weightSM", "Anti-Top Quark p_{T} Before Cuts; p_{T} [GeV];Events", 1000, 0, 3000)
h_antitopEta_weightSM = ROOT.TH1F("h_antitopEta_weightSM", "Anti-Top Quark #eta ;#eta;Events", 100, -5, 5)

h_bquark_pt_weightSM = ROOT.TH1F("h_bquark_pt_weightSM", "b-quark pT ;pT (GeV);Events", 150, 0, 1000)
h_bquark_eta_weightSM = ROOT.TH1F("h_bquark_eta_weightSM", "b-quark #eta  ;#eta;Events", 100, -5, 5)

h_topMultiplicity_weightSM = ROOT.TH1F("h_topMultiplicit_weightSM", "Top Multiplicity Before Cuts; N_{top};Events", 5, 0, 5)
h_antitopMultiplicity_weightSM = ROOT.TH1F("h_antitopMultiplicity_weightSM", "Anti-Top Multiplicity Before Cuts; N_{antitop};Events", 5, 0, 5)

h_jetMultiplicity_fromW_weightSM = ROOT.TH1F("h_jetMultiplicity_fromW_weightSM", "Jet Multiplicity from W Before Cuts; Number of Jets; Events", 10, 0, 5)

# h_MET_weightSM = ROOT.TH1F("h_MET_weightSM", "MET Before Cuts;MET (GeV);Events", 100, 0, 200)

h_invariantMass_weightSM = ROOT.TH1F("h_invariantMass_weightSM", "Invariant Mass; M (GeV);Events", 250, 0, 5000)

h_jetMultiplicity_weightSM = ROOT.TH1F("h_jetMultiplicity_weightSM", "Number of Jets per Event", 10, 0, 50)

h_nonTopMotherJets_weightSM = ROOT.TH1F("h_nonTopMotherJets_weightSM", "Jets without Top as Mother; Count;Events", 10, 0, 50)

h_LHE_HT_weightSM = ROOT.TH1F("h_LHE_HT_weightSM", "LHE_HT ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_0_500_weightSM = ROOT.TH1F("h_LHE_HT_0_500_weightSM", "LHE_HT Mtt = [0,500] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_500_750_weightSM = ROOT.TH1F("h_LHE_HT_500_750_weightSM", "LHE_HT Mtt = [500,750] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_750_1000_weightSM = ROOT.TH1F("h_LHE_HT_750_1000_weightSM", "LHE_HT Mtt = [750,1000] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_1000_1500_weightSM = ROOT.TH1F("h_LHE_HT_1000_1500_weightSM", "LHE_HT Mtt = [1000,1500] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_1500Inf_weightSM = ROOT.TH1F("h_LHE_HT_1500Inf_weightSM", "LHE_HT Mtt = [1000,1500] ; HT (GeV); Events", 150, 0, 3000)

h_both_decays_weightSM  = ROOT.TH1F("h_both_decays_weightSM", "Events with Both Leptonic and Hadronic Decays; Number of Events; Count", 2, 0, 2)

h_jetFromW_pt_weightSM  = ROOT.TH1F("h_jetFromW_pt_weightSM", "Jet pT from W Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_jetFromW_eta_weightSM  = ROOT.TH1F("h_jetFromW_eta_weightSM", "Jet Eta from W Before Cuts; #eta;Events", 100, -5, 5)

h_leading_jet_pt_weightSM  = ROOT.TH1F("h_leading_jet_pt_weightSM", "Leading Jet pT; pT (GeV);Events", 100, 0, 1000)
h_second_leading_jet_pt_weightSM  = ROOT.TH1F("h_second_leading_jet_pt_weightSM", "Second Leading Jet pT; pT (GeV);Events", 100, 0, 1000)

h_jet_multiplicity_last_copy_weightSM  = ROOT.TH1F('h_jet_multiplicity_last_copy_weightSM', 'Jet Multiplicity Last Copy;Number of Jets;Events', 10, 0, 10)
  
h_mtt_vs_LHEHT_weightSM  = ROOT.TH2F("h_mtt_vs_LHEHT_weightSM", "Invariant Mass of ttbar vs. LHE HT;LHE HT (GeV);m_{tt} (GeV)", 50, 0, 1000, 50, 300, 5000)


# weight ctGRe: LHEWeight_ctGRe_1p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p"

h_leptonPt_ctGRe = ROOT.TH1F("h_leptonPt_ctGRe", "Lepton pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_leptoneta_ctGRe = ROOT.TH1F("h_leptoneta_ctGRe", "Lepton Eta Before Cuts; #eta;Events", 100, -5, 5)
h_leptonphi_ctGRe = ROOT.TH1F("h_leptonphi_ctGRe", "Azimuthal Angle Before Cuts; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
bin_edges = [-16.5, -14.5, -12.5, -10.5, 10.5, 12.5, 14.5, 16.5]
h_leptonFlavor_ctGRe = ROOT.TH1F("h_leptonFlavor_ctGRe", "Lepton Flavor; PDG ID;Events", len(bin_edges)-1, array('d', bin_edges))
h_leptonFlavor_ctGRe.GetXaxis().SetBinLabel(1, "muon-")
h_leptonFlavor_ctGRe.GetXaxis().SetBinLabel(2, "electron-")
h_leptonFlavor_ctGRe.GetXaxis().SetBinLabel(4, "electron+")
h_leptonFlavor_ctGRe.GetXaxis().SetBinLabel(5, "muon+")

h_electronPt_ctGRe = ROOT.TH1F("h_electronPt_ctGRe", "Electron pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_electroneta_ctGRe = ROOT.TH1F("h_electroneta_ctGRe", "Electron #eta Before Cuts; #eta;Events", 100, -5, 5)

h_muonPt_ctGRe = ROOT.TH1F("h_muonPt_ctGRe", "Muon pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_muoneta_ctGRe = ROOT.TH1F("h_muoneta_ctGRe", " Muon #eta Before Cuts; #eta;Events", 100, -5, 5)

h_hadronic_w_mass_ctGRe = ROOT.TH1F("h_hadronic_w_mass_ctGRe", "Hadronic Decaying W Mass Before Cuts; M (GeV);Events", 10, 60, 100)

h_topPt_ctGRe = ROOT.TH1F("h_topPt_ctGRe", "Top Quark pT Before Cuts; pT (GeV);Events", 1000, 0, 3000)
h_topEta_ctGRe = ROOT.TH1F("h_topEta_ctGRe", "Top Quark #eta ;#eta;Events", 100, -5, 5)

h_antitopPt_ctGRe = ROOT.TH1F("h_antitopPt_ctGRe", "Anti-Top Quark p_{T} Before Cuts; p_{T} [GeV];Events", 1000, 0, 3000)
h_antitopEta_ctGRe = ROOT.TH1F("h_antitopEta_ctGRe", "Anti-Top Quark #eta ;#eta;Events", 100, -5, 5)

h_bquark_pt_ctGRe = ROOT.TH1F("h_bquark_pt_ctGRe", "b-quark pT ;pT (GeV);Events", 150, 0, 1000)
h_bquark_eta_ctGRe = ROOT.TH1F("h_bquark_eta_ctGRe", "b-quark #eta  ;#eta;Events", 100, -5, 5)

h_topMultiplicity_ctGRe = ROOT.TH1F("h_topMultiplicit_ctGRe", "Top Multiplicity Before Cuts; N_{top};Events", 5, 0, 5)
h_antitopMultiplicity_ctGRe = ROOT.TH1F("h_antitopMultiplicity_ctGRe", "Anti-Top Multiplicity Before Cuts; N_{antitop};Events", 5, 0, 5)

h_jetMultiplicity_fromW_ctGRe = ROOT.TH1F("h_jetMultiplicity_fromW_ctGRe", "Jet Multiplicity from W Before Cuts; Number of Jets; Events", 10, 0, 5)

# h_MET_ctGRe = ROOT.TH1F("h_MET_ctGRe", "MET Before Cuts;MET (GeV);Events", 100, 0, 200)

h_invariantMass_ctGRe = ROOT.TH1F("h_invariantMass_ctGRe", "Invariant Mass; M (GeV);Events", 250, 0, 5000)

h_jetMultiplicity_ctGRe = ROOT.TH1F("h_jetMultiplicity_ctGRe", "Number of Jets per Event", 10, 0, 50)

h_nonTopMotherJets_ctGRe = ROOT.TH1F("h_nonTopMotherJets_ctGRe", "Jets without Top as Mother; Count;Events", 10, 0, 50)

h_LHE_HT_ctGRe = ROOT.TH1F("h_LHE_HT_ctGRe", "LHE_HT ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_0_500_ctGRe = ROOT.TH1F("h_LHE_HT_0_500_ctGRe", "LHE_HT Mtt = [0,500] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_500_750_ctGRe = ROOT.TH1F("h_LHE_HT_500_750_ctGRe", "LHE_HT Mtt = [500,750] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_750_1000_ctGRe = ROOT.TH1F("h_LHE_HT_750_1000_ctGRe", "LHE_HT Mtt = [750,1000] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_1000_1500_ctGRe = ROOT.TH1F("h_LHE_HT_1000_1500_ctGRe", "LHE_HT Mtt = [1000,1500] ; HT (GeV); Events", 150, 0, 3000)
h_LHE_HT_1500Inf_ctGRe = ROOT.TH1F("h_LHE_HT_1500Inf_ctGRe", "LHE_HT Mtt = [1000,1500] ; HT (GeV); Events", 150, 0, 3000)

h_both_decays_ctGRe  = ROOT.TH1F("h_both_decays_ctGRe", "Events with Both Leptonic and Hadronic Decays; Number of Events; Count", 2, 0, 2)

h_jetFromW_pt_ctGRe  = ROOT.TH1F("h_jetFromW_pt_ctGRe", "Jet pT from W Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_jetFromW_eta_ctGRe  = ROOT.TH1F("h_jetFromW_eta_ctGRe", "Jet Eta from W Before Cuts; #eta;Events", 100, -5, 5)

h_leading_jet_pt_ctGRe  = ROOT.TH1F("h_leading_jet_pt_ctGRe", "Leading Jet pT; pT (GeV);Events", 100, 0, 1000)
h_second_leading_jet_pt_ctGRe  = ROOT.TH1F("h_second_leading_jet_pt_ctGRe", "Second Leading Jet pT; pT (GeV);Events", 100, 0, 1000)

h_jet_multiplicity_last_copy_ctGRe  = ROOT.TH1F('h_jet_multiplicity_last_copy_ctGRe', 'Jet Multiplicity Last Copy;Number of Jets;Events', 10, 0, 10)
  
h_mtt_vs_LHEHT_ctGRe  = ROOT.TH2F("h_mtt_vs_LHEHT_ctGRe", "Invariant Mass of ttbar vs. LHE HT;LHE HT (GeV);m_{tt} (GeV)", 50, 0, 1000, 50, 300, 5000)




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
        return (status_flags_int & (1 << 13)) != 0
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
    
   
    weight_0 = entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0)
    weight_1 = entry.GetLeaf("LHEWeight_ctGRe_1p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0)
    print("SM weight: ",entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("ctGRe: ", entry.GetLeaf("LHEWeight_ctGRe_1p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("cQj18: ",entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_1p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))    
    print("cQj38e: ", entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_1p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("cQj11: ",entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_1p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("cjj31: ", entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_1p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("ctu8: ", entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_1p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("ctd8: ",entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_1p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("ctj8: ",entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_1p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("cQu8: ", entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_1p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("cQd8: ", entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_1p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("ctu1: ",entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_1p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("ctd1: ", entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_1p_ctj1_0p_cQu1_0p_cQd1_0p").GetValue(0))
    print("ctj1: ",entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_1p_cQu1_0p_cQd1_0p").GetValue(0))
    print("cQu1: ", entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_1p_cQd1_0p").GetValue(0))
    print("cQd1: ",entry.GetLeaf("LHEWeight_ctGRe_0p_cQj18_0p_cQj38_0p_cQj11_0p_cjj31_0p_ctu8_0p_ctd8_0p_ctj8_0p_cQu8_0p_cQd8_0p_ctu1_0p_ctd1_0p_ctj1_0p_cQu1_0p_cQd1_1p").GetValue(0))
    
    
    
    
    
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
            
        
        # Check if particle is a top or antitop quark
        if abs(pdgId) in relevant_pdgIds and is_last_copy(statusFlags):  
            if abs(pdgId) == 6:
                
                # top_4vec = ROOT.TLorentzVector()
                # top_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
                
                w_daughter = None
                b_daughter = None
                last_copy_top_decays.append((pt, eta, phi))
                
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
                                b_quarks.append((b_4vec, j))

                
                if has_leptonic_w_decay:
                    
                    # Check if W decays leptonically
                    for k in range(entry.nGenPart):
                        if entry.GenPart_genPartIdxMother[k] == w_daughter and abs(entry.GenPart_pdgId[k]) in [11, 13]:  
                            
                            lepton_pdg = entry.GenPart_pdgId[k]
                            lepton_pt = entry.GenPart_pt[k]
                            lepton_eta = entry.GenPart_eta[k]
                            lepton_phi = entry.GenPart_phi[k]
                            
                            # histograms['h_leptonPt'].Fill(lepton_pt)
                            # histograms['h_leptoneta'].Fill(lepton_eta)
                            # histograms['h_leptonphi'].Fill(lepton_phi)
                            # histograms['h_leptonFlavor'].Fill(entry.GenPart_pdgId[k])
                            
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

                
                w_quarks = []                     
                # Check if W decays hadronically
                for j in range(entry.nGenPart):
                    if entry.GenPart_genPartIdxMother[j] == w_daughter and abs(entry.GenPart_pdgId[j]) in [1, 2, 3, 4]:
                        w_quarks.append(j)

                if len(w_quarks) == 2:
                    hadronic_decay = True
                    hadronic_top_pt.append(pt)
                    
                    quark1 = ROOT.TLorentzVector()
                    quark2 = ROOT.TLorentzVector()
                    quark1.SetPtEtaPhiM(entry.GenPart_pt[w_quarks[0]], entry.GenPart_eta[w_quarks[0]], entry.GenPart_phi[w_quarks[0]], entry.GenPart_mass[w_quarks[0]])
                    quark2.SetPtEtaPhiM(entry.GenPart_pt[w_quarks[1]], entry.GenPart_eta[w_quarks[1]], entry.GenPart_phi[w_quarks[1]], entry.GenPart_mass[w_quarks[1]])
                    hadronic_w_mass = (quark1 + quark2).M()
                    if 65 < hadronic_w_mass < 95: # I include this line to ensure that the events are indeed hadronic W decays
                        histograms['h_hadronic_w_mass'].Fill(hadronic_w_mass)
                        histograms['h_hadronic_w_mass_weightSM'].Fill(hadronic_w_mass, weight_0)
                        histograms['h_hadronic_w_mass_ctGRe'].Fill(hadronic_w_mass, weight_1)
                        
                        
                        # Identify the jets coming from the quarks of the hadronically decaying W
                        for m in range(entry.nGenJet):
                            jet = ROOT.TLorentzVector()
                            jet.SetPtEtaPhiM(entry.GenJet_pt[m], entry.GenJet_eta[m], entry.GenJet_phi[m], 0)
                            # Match jets to quarks by deltaR
                            if deltaR(jet.Eta(), jet.Phi(), quark1.Eta(), quark1.Phi()) < 0.4 or deltaR(jet.Eta(), jet.Phi(), quark2.Eta(), quark2.Phi()) < 0.4:
                                jets_from_w.append(jet)
                                jets_from_w_count += 1
                                jets_from_w_info.append((m, jet.Pt(), jet.Eta(), jet.Phi()))

            
                # b-quarks
                if b_daughter is not None:
                    b_vector = ROOT.TLorentzVector()
                    b_vector.SetPtEtaPhiM(entry.GenPart_pt[b_daughter], entry.GenPart_eta[b_daughter], entry.GenPart_phi[b_daughter], entry.GenPart_mass[b_daughter])
                    
            else: 
                continue  
        else:
            continue
    
    matched_jets = match_jets_to_partons(entry, last_copy_partons)
    leading_jet, second_leading_jet = select_leading_jets_from_matched(matched_jets)

    # b_jet_matched check determines if any of the leading or second-leading jets match with a b-quark from top decay
    b_jet_matched, matched_b_quark = check_b_jet_from_top(b_quarks, leading_jet, second_leading_jet)
    if not b_jet_matched:
        leading_b_quark = find_leading_b_quark(b_quarks, leading_jet, second_leading_jet, last_copy_partons)
        if leading_b_quark is None or leading_b_quark[0].Pt() < 30:
            # Veto this event as it does not meet the b-quark criteria
            return
        
    # if top_4vec and antitop_4vec:
    #     ttbar = top_4vec + antitop_4vec
    #     m_tt = ttbar.M()

    #     histograms['h_invariantMass'].Fill(ttbar.M())
        
    #     LHE_HT = getattr(entry, "LHE_HT", -1)
    #     if LHE_HT >= 0:
    #         histograms['h_mtt_vs_LHEHT'].Fill(LHE_HT, m_tt)
    
    # print("Leptons:", leptons)
    # print("Leptons len :", len(leptons))
    

    
    if len(w_quarks) == 2:
        for lepton in leptons:
            lepton_pt, lepton_eta, lepton_phi, lepton_pdgId = lepton
            
            histograms['h_leptonPt'].Fill(lepton_pt)
            histograms['h_leptoneta'].Fill(lepton_eta)
            histograms['h_leptonphi'].Fill(lepton_phi)
            histograms['h_leptonFlavor'].Fill(entry.GenPart_pdgId[k])
            
            # histograms['h_leptonPt_weightSM'].Fill(lepton_pt, weight_0)
            # histograms['h_leptoneta_weightSM'].Fill(lepton_eta, weight_0)
            # histograms['h_leptonphi_weightSM'].Fill(lepton_phi, weight_0)
            # histograms['h_leptonFlavor_weightSM'].Fill(entry.GenPart_pdgId[k], weight_0)
            
            # histograms['h_leptonPt_ctGRe'].Fill(lepton_pt, weight_1)
            # histograms['h_leptoneta_ctGRe'].Fill(lepton_eta, weight_1)
            # histograms['h_leptonphi_ctGRe'].Fill(lepton_phi, weight_1)
            # histograms['h_leptonFlavor_ctGRe'].Fill(entry.GenPart_pdgId[k], weight_1)
            
            if abs(lepton_pdgId) == 11:
                histograms['h_electronPt'].Fill(lepton_pt)
                histograms['h_electroneta'].Fill(lepton_eta)
                
                # histograms['h_electronPt_weightSM'].Fill(lepton_pt, weight_0)
                # histograms['h_electroneta_weightSM'].Fill(lepton_eta, weight_0)
                
                # histograms['h_electronPt_ctGRe'].Fill(lepton_pt, weight_1)
                # histograms['h_electroneta_ctGRe'].Fill(lepton_eta, weight_1)
                                    
            elif abs(lepton_pdgId) == 13:
                histograms['h_muonPt'].Fill(lepton_pt)
                histograms['h_muoneta'].Fill(lepton_eta)
                
                # histograms['h_muonPt_weightSM'].Fill(lepton_pt, weight_0)
                # histograms['h_muoneta_weightSM'].Fill(lepton_eta, weight_0)
                
                # histograms['h_muonPt_ctGRe'].Fill(lepton_pt,weight_1)
                # histograms['h_muoneta_ctGRe'].Fill(lepton_eta, weight_1)
        
        for top_4vec, pdgId in tops:
            if pdgId == 6:
                top_count += 1
                histograms['h_topPt'].Fill(top_4vec.Pt())
                histograms['h_topEta'].Fill(top_4vec.Eta())
                
                # histograms['h_topPt_weightSM'].Fill(top_4vec.Pt(), weight_0)
                # histograms['h_topEta_weightSM'].Fill(top_4vec.Eta(), weight_0)
                
                # histograms['h_topPt_ctGRe'].Fill(top_4vec.Pt(),weight_1)
                # histograms['h_topEta_ctGRe'].Fill(top_4vec.Eta(), weight_1)
                
            elif pdgId == -6:
                antitop_count += 1
                histograms['h_antitopPt'].Fill(antitop_4vec.Pt())
                histograms['h_antitopEta'].Fill(antitop_4vec.Eta())
                
                # histograms['h_antitopPt_weightSM'].Fill(antitop_4vec.Pt(), weight_0)
                # histograms['h_antitopEta_weightSM'].Fill(antitop_4vec.Eta(), weight_0)
                
                # histograms['h_antitopPt_ctGRe'].Fill(antitop_4vec.Pt(), weight_1)
                # histograms['h_antitopEta_ctGRe'].Fill(antitop_4vec.Eta(), weight_1)

            histograms['h_topMultiplicity'].Fill(top_count)
            # histograms['h_topMultiplicity_weightSM'].Fill(top_count, weight_0)
            # histograms['h_topMultiplicity_ctGRe'].Fill(top_count, weight_1)
            
            histograms['h_antitopMultiplicity'].Fill(antitop_count)
            # histograms['h_antitopMultiplicity_weightSM'].Fill(antitop_count, weight_0)
            # histograms['h_antitopMultiplicity_ctGRe'].Fill(antitop_count, weight_1)

        for b_quark in b_quarks:
            b_vector, b_index = b_quark 
            
            histograms['h_bquark_pt'].Fill(b_vector.Pt())
            histograms['h_bquark_eta'].Fill(b_vector.Eta())

            # histograms['h_bquark_pt_weightSM'].Fill(b_vector.Pt(), weight_0)
            # histograms['h_bquark_eta_weightSM'].Fill(b_vector.Eta(), weight_0)
            
            # histograms['h_bquark_pt_ctGRe'].Fill(b_vector.Pt(), weight_1)
            # histograms['h_bquark_eta_ctGRe'].Fill(b_vector.Eta(), weight_1)
            
        for jet_info in jets_from_w_info:
            jet_idx, jet_pt, jet_eta, jet_phi = jet_info
            histograms['h_jetFromW_pt'].Fill(jet_pt)
            histograms['h_jetFromW_eta'].Fill(jet_eta)
            
            # histograms['h_jetFromW_pt_weightSM'].Fill(jet_pt, weight_0)
            # histograms['h_jetFromW_eta_weightSM'].Fill(jet_eta, weight_0)
            
            # histograms['h_jetFromW_pt_ctGRe'].Fill(jet_pt, weight_1)
            # histograms['h_jetFromW_eta_ctGRe'].Fill(jet_eta, weight_1)
            

        histograms['h_jetMultiplicity_fromW'].Fill(jets_from_w_count)
        # histograms['h_jetMultiplicity_fromW_weightSM'].Fill(jets_from_w_count, weight_0)
        # histograms['h_jetMultiplicity_fromW_ctGRe'].Fill(jets_from_w_count, weight_1)
        
        # histograms['h_MET'].Fill(met_vector.Pt())
                
            
        if top_4vec and antitop_4vec:
            ttbar = top_4vec + antitop_4vec
            m_tt = ttbar.M()
            p_tt = ttbar.Pt()
            eta_tt = ttbar.Eta()

            histograms['h_invariantMass'].Fill(ttbar.M())
            # histograms['h_invariantMass_weightSM'].Fill(ttbar.M(), weight_0)
            # histograms['h_invariantMass_ctGRe'].Fill(ttbar.M(), weight_1)
            
            LHE_HT = getattr(entry, "LHE_HT", -1)
            if LHE_HT >= 0:                    
                    
                LHE_HT = getattr(entry, "LHE_HT", -1)
                if LHE_HT >= 0:
    
                    if 0 <= m_tt < 500:
                        histograms['h_LHE_HT_0_500'].Fill(LHE_HT)
                        # histograms['h_LHE_HT_0_500_weightSM'].Fill(LHE_HT, weight_0)
                        # histograms['h_LHE_HT_0_500_ctGRe'].Fill(LHE_HT, weight_1)
                    elif 500 <= m_tt < 750:
                        histograms['h_LHE_HT_500_750'].Fill(LHE_HT)
                        # histograms['h_LHE_HT_500_750_weightSM'].Fill(LHE_HT, weight_0)
                        # histograms['h_LHE_HT_500_750_ctGRe'].Fill(LHE_HT, weight_1)
                    elif 750 <= m_tt < 1000:
                        histograms['h_LHE_HT_750_1000'].Fill(LHE_HT)
                        # histograms['h_LHE_HT_750_1000_weightSM'].Fill(LHE_HT, weight_0)
                        # histograms['h_LHE_HT_750_1000_ctGRe'].Fill(LHE_HT, weight_1)
                    elif 1000 <= m_tt < 1500:
                        histograms['h_LHE_HT_1000_1500'].Fill(LHE_HT)
                        # histograms['h_LHE_HT_1000_1500_weightSM'].Fill(LHE_HT, weight_0)
                        # histograms['h_LHE_HT_1000_1500_ctGRe'].Fill(LHE_HT, weight_1)
                    elif m_tt >= 1500:
                        histograms['h_LHE_HT_1500Inf'].Fill(LHE_HT)
                        # histograms['h_LHE_HT_1500Inf_weightSM'].Fill(LHE_HT, weight_0)
                        # histograms['h_LHE_HT_1500Inf_ctGRe'].Fill(LHE_HT, weight_1)
            
        
        b_quark_jets = []
        w_decay_quark_jets = []

        # Match jets to b-quarks
        for i in range(entry.nGenJet):
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM(entry.GenJet_pt[i], entry.GenJet_eta[i], entry.GenJet_phi[i], 0) # Assuming jet mass is negligible
            for b_quark in b_quarks:
                b_quark_vector, _ = b_quark 
                if deltaR(jet.Eta(), jet.Phi(), b_quark_vector.Eta(), b_quark_vector.Phi()) < 0.4:
                    b_quark_jets.append(jet)
                    break
        
            
        # Match jets to W-boson decay products
        for i in range(entry.nGenJet):
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM(entry.GenJet_pt[i], entry.GenJet_eta[i], entry.GenJet_phi[i], 0) # Again, assuming jet mass is negligible
            for w_decay_product in jets_from_w:
                if jet not in b_quark_jets and deltaR(jet.Eta(), jet.Phi(), w_decay_product.Eta(), w_decay_product.Phi()) < 0.4:
                    w_decay_quark_jets.append(jet)
                    break
                
        combined_jets = list(set(b_quark_jets + w_decay_quark_jets))
        
        histograms['h_jet_multiplicity_last_copy'].Fill(len(combined_jets))
        # histograms['h_jet_multiplicity_last_copy_weightSM'].Fill(len(combined_jets), weight_0)
        # histograms['h_jet_multiplicity_last_copy_ctGRe'].Fill(len(combined_jets), weight_1)
    
        histograms['h_jetMultiplicity'].Fill(entry.nGenJet)
        # histograms['h_jetMultiplicity_weightSM'].Fill(entry.nGenJet, weight_0)
        # histograms['h_jetMultiplicity_ctGRe'].Fill(entry.nGenJet, weight_1)
        
        # HT variable from data in ttree
        LHE_HT = getattr(entry, "LHE_HT", -1)
        if LHE_HT >= 0:
            histograms['h_mtt_vs_LHEHT'].Fill(LHE_HT, m_tt)
            histograms['h_LHE_HT'].Fill(LHE_HT)
            
            # histograms['h_mtt_vs_LHEHT_weightSM'].Fill(LHE_HT, m_tt, weight_0)
            # histograms['h_LHE_HT_weightSM'].Fill(LHE_HT, weight_0)
            
            # histograms['h_mtt_vs_LHEHT_ctGRe'].Fill(LHE_HT, m_tt, weight_1)
            # histograms['h_LHE_HT_ctGRe'].Fill(LHE_HT, weight_1)
        
        
        if leading_jet is not None and second_leading_jet is not None:
            if leading_jet:
                histograms['h_leading_jet_pt'].Fill(leading_jet[0].Pt()) #leading_jet[0] contains the pt of the leading jet
                # histograms['h_leading_jet_pt_weightSM'].Fill(leading_jet[0].Pt(), weight_0)
                # histograms['h_leading_jet_pt_ctGRe'].Fill(leading_jet[0].Pt(), weight_1)
            if second_leading_jet:
                histograms['h_second_leading_jet_pt'].Fill(second_leading_jet[0].Pt())
                # histograms['h_second_leading_jet_pt_weightSM'].Fill(second_leading_jet[0].Pt(), weight_0)
                # histograms['h_second_leading_jet_pt_ctGRe'].Fill(second_leading_jet[0].Pt(), weight_1)
                

       
    return leptons, tops, hadronic_top_pt, b_quarks, last_copy_partons



# This function identifies jets that are closely matched with last copy partons. 
# It appends a tuple to matched_jets which includes the jet and its index in the GenJet collection.

def match_jets_to_partons(entry, last_copy_partons):
    matched_jets = []
    for j in range(entry.nGenJet):
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(entry.GenJet_pt[j], entry.GenJet_eta[j], entry.GenJet_phi[j], 0)  # jet mass is negligible

        # finding the closest last copy parton to this jet
        closest_parton = min(last_copy_partons, key=lambda p: deltaR(jet.Eta(), jet.Phi(), p[0].Eta(), p[0].Phi()))  # p[0] is the TLorentzVector
        if deltaR(jet.Eta(), jet.Phi(), closest_parton[0].Eta(), closest_parton[0].Phi()) < 0.4:
            matched_jets.append((jet, j)) 

    return matched_jets


# This function filters and sorts the jets based on their Pt, 
# then identifies the leading and second-leading jets.
def select_leading_jets_from_matched(matched_jets):
    
    filtered_jets = [(jet, pdg_id) for jet, pdg_id in matched_jets]
    # Sort the matched jets by their pT in descending order
    sorted_jets = sorted(filtered_jets, key=lambda jet_tuple: jet_tuple[0].Pt(), reverse=True)

    # Select the leading and second leading jets
    leading_jet = sorted_jets[0] if len(sorted_jets) > 0 else None
    second_leading_jet = sorted_jets[1] if len(sorted_jets) > 1 else None

    return leading_jet, second_leading_jet


# This function checks if any of the b-quarks (from the b_quarks list, so it is from top) is the same as the leading or second-leading jet (identified by their indices). 
# If it finds a match, it returns True along with the b-quark's vector (b_vector)
# Otherwise, it returns False and None


def check_b_jet_from_top(b_quarks, leading_jet, second_leading_jet):
    for b_quark in b_quarks:
        b_vector, _ = b_quark
        if leading_jet and deltaR(leading_jet[0].Eta(), leading_jet[0].Phi(), b_vector.Eta(), b_vector.Phi()) < 0.4:
            return True, b_vector
        elif second_leading_jet and deltaR(second_leading_jet[0].Eta(), second_leading_jet[0].Phi(), b_vector.Eta(), b_vector.Phi()) < 0.4:
            return True, b_vector
    return False, None

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
    
    # 'h_leptonPt_weightSM': h_leptonPt_weightSM,
    # 'h_leptoneta_weightSM': h_leptoneta_weightSM,
    # 'h_leptonphi_weightSM': h_leptonphi_weightSM,
    # 'h_leptonFlavor_weightSM': h_leptonFlavor_weightSM,
    # 'h_electronPt_weightSM': h_electronPt_weightSM,
    # 'h_electroneta_weightSM': h_electroneta_weightSM,
    # 'h_muonPt_weightSM': h_muonPt_weightSM,
    # 'h_muoneta_weightSM': h_muoneta_weightSM,
    'h_hadronic_w_mass_weightSM': h_hadronic_w_mass_weightSM,
    # 'h_topPt_weightSM': h_topPt_weightSM,
    # 'h_topEta_weightSM': h_topEta_weightSM,
    # 'h_antitopPt_weightSM': h_antitopPt_weightSM,
    # 'h_antitopEta_weightSM': h_antitopEta_weightSM,
    # 'h_topMultiplicity_weightSM': h_topMultiplicity_weightSM,
    # 'h_antitopMultiplicity_weightSM': h_antitopMultiplicity_weightSM,
    # 'h_jetMultiplicity_fromW_weightSM': h_jetMultiplicity_fromW_weightSM,
    # # 'h_MET_weightSM_weightSM': h_MET_weightSM,
    # 'h_invariantMass_weightSM': h_invariantMass_weightSM,
    # 'h_jetMultiplicity_weightSM': h_jetMultiplicity_weightSM,
    # 'h_nonTopMotherJets_weightSM': h_nonTopMotherJets_weightSM,
    # 'h_LHE_HT_weightSM' : h_LHE_HT_weightSM,
    # 'h_LHE_HT_0_500_weightSM' : h_LHE_HT_0_500_weightSM,
    # 'h_LHE_HT_500_750_weightSM' : h_LHE_HT_500_750_weightSM,
    # 'h_LHE_HT_750_1000_weightSM' : h_LHE_HT_750_1000_weightSM,
    # 'h_LHE_HT_1000_1500_weightSM' : h_LHE_HT_1000_1500_weightSM,
    # 'h_LHE_HT_1500Inf_weightSM' : h_LHE_HT_1500Inf_weightSM,
    # 'h_both_decays_weightSM': h_both_decays_weightSM,
    # 'h_jetFromW_pt_weightSM': h_jetFromW_pt_weightSM,
    # 'h_jetFromW_eta_weightSM': h_jetFromW_eta_weightSM,
    # 'h_leading_jet_pt_weightSM' : h_leading_jet_pt_weightSM,
    # 'h_second_leading_jet_pt_weightSM' : h_second_leading_jet_pt_weightSM,
    # "h_jet_multiplicity_last_copy_weightSM" : h_jet_multiplicity_last_copy_weightSM,
    # "h_mtt_vs_LHEHT_weightSM" : h_mtt_vs_LHEHT_weightSM,
    # "h_bquark_pt_weightSM" : h_bquark_pt_weightSM,
    # "h_bquark_eta_weightSM": h_bquark_eta_weightSM,
    
    # 'h_leptonPt_ctGRe': h_leptonPt_ctGRe,
    # 'h_leptoneta_ctGRe': h_leptoneta_ctGRe,
    # 'h_leptonphi_ctGRe': h_leptonphi_ctGRe,
    # 'h_leptonFlavor_ctGRe': h_leptonFlavor_ctGRe,
    # 'h_electronPt_ctGRe': h_electronPt_ctGRe,
    # 'h_electroneta_ctGRe': h_electroneta_ctGRe,
    # 'h_muonPt_ctGRe': h_muonPt_ctGRe,
    # 'h_muoneta_ctGRe': h_muoneta_ctGRe,
    'h_hadronic_w_mass_ctGRe': h_hadronic_w_mass_ctGRe,
    # 'h_topPt_ctGRe': h_topPt_ctGRe,
    # 'h_topEta_ctGRe': h_topEta_ctGRe,
    # 'h_antitopPt_ctGRe': h_antitopPt_ctGRe,
    # 'h_antitopEta_ctGRe': h_antitopEta_ctGRe,
    # 'h_topMultiplicity_ctGRe': h_topMultiplicity_ctGRe,
    # 'h_antitopMultiplicity_ctGRe': h_antitopMultiplicity_ctGRe,
    # 'h_jetMultiplicity_fromW_ctGRe': h_jetMultiplicity_fromW_ctGRe,
    # # 'h_MET_ctGRe_ctGRe': h_MET_ctGRe,
    # 'h_invariantMass_ctGRe': h_invariantMass_ctGRe,
    # 'h_jetMultiplicity_ctGRe': h_jetMultiplicity_ctGRe,
    # 'h_nonTopMotherJets_ctGRe': h_nonTopMotherJets_ctGRe,
    # 'h_LHE_HT_ctGRe' : h_LHE_HT_ctGRe,
    # 'h_LHE_HT_0_500_ctGRe' : h_LHE_HT_0_500_ctGRe,
    # 'h_LHE_HT_500_750_ctGRe' : h_LHE_HT_500_750_ctGRe,
    # 'h_LHE_HT_750_1000_ctGRe' : h_LHE_HT_750_1000_ctGRe,
    # 'h_LHE_HT_1000_1500_ctGRe' : h_LHE_HT_1000_1500_ctGRe,
    # 'h_LHE_HT_1500Inf_ctGRe' : h_LHE_HT_1500Inf_ctGRe,
    # 'h_both_decays_ctGRe': h_both_decays_ctGRe,
    # 'h_jetFromW_pt_ctGRe': h_jetFromW_pt_ctGRe,
    # 'h_jetFromW_eta_ctGRe': h_jetFromW_eta_ctGRe,
    # 'h_leading_jet_pt_ctGRe' : h_leading_jet_pt_ctGRe,
    # 'h_second_leading_jet_pt_ctGRe' : h_second_leading_jet_pt_ctGRe,
    # "h_jet_multiplicity_last_copy_ctGRe" : h_jet_multiplicity_last_copy_ctGRe,
    # "h_mtt_vs_LHEHT_ctGRe" : h_mtt_vs_LHEHT_ctGRe,
    # "h_bquark_pt_ctGRe" : h_bquark_pt_ctGRe,
    # "h_bquark_eta_ctGRe": h_bquark_eta_ctGRe,
    
    
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
    output_dir = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_comparePowheg"
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
# createCanvas(h_hadronic_w_mass, "Hadronic Decaying W Mass Before Cuts", "hadronicWMassDistribution.png")
# createCanvas(h_hadronic_w_mass_aftercut200, "Hadronic Decaying W Mass After Cuts & TopPt>200", "hadronicWMassAfterCut200Distribution.png")
# createCanvas(h_hadronic_w_mass_aftercut400, "Hadronic Decaying W Mass After Cuts & TopPt>400", "hadronicWMassAfterCut400Distribution.png")
# createCanvas(h_topPt, "Top Quark pT Before Cuts", "topPtDistribution.png", True)
# createCanvas(h_topPt_aftercut200, "Top Quark pT After Cuts & TopPt>200", "topPtAfterCut200Distribution.png", True)
# createCanvas(h_topPt_aftercut400, "Top Quark pT After Cuts & TopPt>400", "topPtAfterCut400Distribution.png", True)
# createCanvas(h_antitopPt, "Anti-Top Quark pT Before Cuts", "antitopPtDistribution.png", True)
# createCanvas(h_antitopPt_aftercut200, "Anti-Top Quark pT After Cuts & TopPt>200", "antitopPtAfterCut200Distribution.png", True)
# createCanvas(h_antitopPt_aftercut400, "Anti-Top Quark pT After Cuts & TopPt>400", "antitopPtAfterCut400Distribution.png", True)
# createCanvas(h_bquark_pt_electron, "b-quark pT Electron Channel", "bquarkPtDistribution.png", True)
# createCanvas(h_bquark_eta_electron, "b-quark Eta Electron Channel", "bquarkEtaDistribution.png")
# createCanvas(h_bquark_pt_muon, "b-quark pT Muon Channel", "bquarkPtDistribution.png", True)
# createCanvas(h_bquark_eta_muon, "b-quark Eta Muon Channel ", "bquarkEtaDistribution.png")

# createCanvas(h_bquark_pt_aftercut200, "b-quark pT After Cuts & TopPt>200", "bquarkPtAfterCut200Distribution.png", True)
# createCanvas(h_bquark_pt_aftercut400, "b-quark pT After Cuts & TopPt>400", "bquarkPtAfterCut400Distribution.png", True)
# createCanvas(h_topMultiplicity, "Top Multiplicity Before Cuts", "topMultiplicityDistribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_topMultiplicity_aftercut200, "Top Multiplicity After Cuts & TopPt>200", "topMultiplicityAfterCut200Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_topMultiplicity_aftercut400, "Top Multiplicity After Cuts & TopPt>400", "topMultiplicityAfterCut400Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_antitopMultiplicity, "Anti-Top Multiplicity Before Cuts", "antitopMultiplicityDistribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_antitopMultiplicity_aftercut200, "Anti-Top Multiplicity After Cuts & Pt>200", "antitopMultiplicityAfterCut200Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_antitopMultiplicity_aftercut400, "Anti-Top Multiplicity After Cuts & Pt>400", "antitopMultiplicityAfterCut400Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_jetMultiplicity_fromW, "Jet Multiplicity from W Before Cuts", "jetMultiplicityFromWDistribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_jetMultiplicity_fromW_after200, "Jet Multiplicity from W After Cuts & Pt>200", "jetMultiplicityFromWAfterCut200Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_jetMultiplicity_fromW_after400, "Jet Multiplicity from W After Cuts & Pt>400", "jetMultiplicityFromWAfterCut400Distribution.png", False, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_MET, "MET Before Cuts", "METDistribution.png")
# createCanvas(h_MET_after200, "MET After Cuts & Pt>200", "METAfterCut200Distribution.png")
# createCanvas(h_MET_after400, "MET After Cuts & Pt>400", "METAfterCut400Distribution.png")
# createCanvas(h_invariantMass, "Invariant Mass", "invariantMassDistribution.png", True)
# createCanvas(h_invariantMass_aftercut200, "Invariant Mass After Cuts & Pt>200", "invariantMassAfterCut200Distribution.png", True)
# createCanvas(h_invariantMass_aftercut400, "Invariant Mass After Cuts & Pt>400", "invariantMassAfterCut400Distribution.png", True)
# createCanvas(h_jetMultiplicity, "Jet Multiplicity Without Cuts", "jetMultiplicityDistribution.png", True, fillColor=ROOT.kBlue - 10,lineColor=ROOT.kBlue)
# createCanvas(h_nonTopMotherJets, "Jets without Top as Mother", "nonTopMotherJetsDistribution.png")
# createCanvas(h_LHE_HT_before, "LHE_HT Before Cuts", "LHE_HTBeforeCutsDistribution.png", True)
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
# createCanvas(h_jetFromW_pt, "Jet pT from W Before Cuts; pT (GeV)", "jetfromW_pt.png")
# createCanvas(h_jetFromW_eta,"Jet Eta from W Before Cuts", "jetfromW_eta.png")
# createCanvas(h_jetFromW_pt_aftercut200, "Jet pT from W After Cuts & TopPt>200; pT (GeV)", "jetfromW_pt_after200.png")
# createCanvas(h_jetFromW_pt_aftercut400, "Jet pT from W After Cuts & TopPt>400; pT (GeV)", "jetfromW_pt_after400.png") 
       
print("Total number of events:", totalEvents)
