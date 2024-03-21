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

output_dir = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_all"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

h_leptonPt = ROOT.TH1F("h_leptonPt", "Lepton pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_leptoneta = ROOT.TH1F("h_leptoneta", "Lepton Eta Before Cuts; #eta;Events", 100, -5, 5)
h_leptonphi = ROOT.TH1F("h_leptonphi", "Azimuthal Angle Before Cuts; #phi;Events", 100, -ROOT.TMath.Pi(), ROOT.TMath.Pi())
bin_edges = [-16.5, -14.5, -12.5, -10.5, 10.5, 12.5, 14.5, 16.5]
h_leptonFlavor = ROOT.TH1F("h_leptonFlavor", "Lepton Flavor; PDG ID;Events", len(bin_edges)-1, array('d', bin_edges))

h_leptonFlavor.GetXaxis().SetBinLabel(1, "muon-")
h_leptonFlavor.GetXaxis().SetBinLabel(2, "electron-")
h_leptonFlavor.GetXaxis().SetBinLabel(4, "electron+")
h_leptonFlavor.GetXaxis().SetBinLabel(5, "muon+")

h_electronPt = ROOT.TH1F("h_electronPt", "Electron pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_electronPt_aftercut200 = ROOT.TH1F("h_electronPt_aftercut200", "Electron pT After Cuts & TopPt>200; pT (GeV);Events", 1000, 0, 1000)
h_electronPt_aftercut400 = ROOT.TH1F("h_electronPt_aftercut400", "Electron pT After Cuts & TopPt>400; pT (GeV);Events", 1000, 0, 1000)
h_electroneta = ROOT.TH1F("h_electroneta", "Electron #eta Before Cuts; #eta;Events", 100, -5, 5)
h_electroneta_aftercut200 = ROOT.TH1F("h_electroneta_aftercut200", "Electron #eta After Cuts & TopPt>200; #eta;Events", 100, -5, 5)
h_electroneta_aftercut400 = ROOT.TH1F("h_electroneta_aftercut400", "Electron #eta After Cuts & TopPt>400; #eta;Events", 100, -5, 5)


h_muonPt = ROOT.TH1F("h_muonPt", "Muon pT Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_muonPt_aftercut200 = ROOT.TH1F("h_muonPt_aftercut200", "Muon pT After Cuts & TopPt>200; pT (GeV);Events", 1000, 0, 1000)
h_muonPt_aftercut400 = ROOT.TH1F("h_muonPt_aftercut400", "Muon pT After Cuts & TopPt>400; pT (GeV);Events", 1000, 0, 1000)
h_muoneta = ROOT.TH1F("h_muoneta", " Muon #eta Before Cuts; #eta;Events", 100, -5, 5)
h_muoneta_aftercut200 = ROOT.TH1F("h_muoneta_aftercut200", "Muon #eta After Cuts & TopPt>200; #eta;Events", 100, -5, 5)
h_muoneta_aftercut400 = ROOT.TH1F("h_muoneta_aftercut400", "Muon #eta After Cuts & TopPt>400; #eta;Events", 100, -5, 5)

h_hadronic_w_mass = ROOT.TH1F("h_hadronic_w_mass", "Hadronic Decaying W Mass Before Cuts; M (GeV);Events", 10, 60, 100)
h_hadronic_w_mass_aftercut200  = ROOT.TH1F("h_hadronic_w_mass_aftercut200", "Hadronic Decaying W Mass After Cuts & TopPt>200; M (GeV);Events", 10, 60, 100)
h_hadronic_w_mass_aftercut400  = ROOT.TH1F("h_hadronic_w_mass_aftercut400", "Hadronic Decaying W Mass After Cuts & TopPt>400; M (GeV);Events", 10, 60, 100)


h_topPt = ROOT.TH1F("h_topPt", "Top Quark pT Before Cuts; pT (GeV);Events", 1000, 0, 3000)
h_topPt_aftercut200 = ROOT.TH1F("h_topPt_aftercut200", "Top Quark pT After Cuts & TopPt>200; pT (GeV);Events", 1000, 0, 3000)
h_topPt_aftercut400 = ROOT.TH1F("h_topPt_aftercut400", "Top Quark pT After Cuts & TopPt>400; pT (GeV);Events", 1000, 0, 3000)

h_antitopPt = ROOT.TH1F("h_antitopPt", "Anti-Top Quark p_{T} Before Cuts; p_{T} [GeV];Events", 1000, 0, 3000)
h_antitopPt_aftercut200 = ROOT.TH1F("h_antitopPt_aftercut200", "Anti-Top Quark p_{T} After Cuts & TopPt>200; p_{T} [GeV];Events", 1000, 0, 3000)
h_antitopPt_aftercut400 = ROOT.TH1F("h_antitopPt_aftercut400", "Anti-Top Quark p_{T} After Cuts & TopPt>400; p_{T} [GeV];Events", 1000, 0, 3000)

h_bquark_pt_electron = ROOT.TH1F("h_bquark_pt_electron", "b-quark pT Electron Channel ;pT (GeV);Events", 150, 0, 1000)
h_bquark_eta_electron = ROOT.TH1F("h_bquark_eta_electron", "b-quark #eta Electron Channel  ;#eta;Events", 100, -5, 5)

h_bquark_pt_muon = ROOT.TH1F("h_bquark_pt_muon", "b-quark pT Muon Channel  ;pT (GeV);Events", 150, 0, 1000)
h_bquark_eta_muon = ROOT.TH1F("h_bquark_eta_muon", "b-quark #eta Electron Channel  ;#eta;Events", 100, -5, 5)

h_bquark_pt_aftercut200 = ROOT.TH1F("h_bquark_pt_aftercut200", "b-quark pT After Cuts & TopPt>200 ;pT (GeV);Events", 150, 0, 1000)
h_bquark_pt_aftercut400 = ROOT.TH1F("h_bquark_pt_aftercut400", "b-quark pT After Cuts & TopPt>400 ;pT (GeV);Events", 150, 0, 1000)

h_topMultiplicity = ROOT.TH1F("h_topMultiplicity", "Top Multiplicity Before Cuts; N_{top};Events", 5, 0, 5)
h_topMultiplicity_aftercut200 = ROOT.TH1F("h_topMultiplicity_aftercut200", "Top Multiplicity After Cuts & TopPt>200; N_{top};Events", 5, 0, 5)
h_topMultiplicity_aftercut400 = ROOT.TH1F("h_topMultiplicity_aftercut400", "Top Multiplicity After Cuts & TopPt>400; N_{antitop};Events", 5, 0, 5)

h_antitopMultiplicity = ROOT.TH1F("h_antitopMultiplicity", "Anti-Top Multiplicity Before Cuts; N_{antitop};Events", 5, 0, 5)
h_antitopMultiplicity_aftercut200 = ROOT.TH1F("h_antitopMultiplicity_aftercut200", "Anti-Top Multiplicity After Cuts & Pt>200; N_{top};Events", 5, 0, 5)
h_antitopMultiplicity_aftercut400 = ROOT.TH1F("h_antitopMultiplicity_aftercut400", "Anti-Top Multiplicity After Cuts & Pt>400; N_{antitop};Events", 5, 0, 5)

h_jetMultiplicity_fromW = ROOT.TH1F("h_jetMultiplicity_fromW", "Jet Multiplicity from W Before Cuts; Number of Jets; Events", 10, 0, 5)
h_jetMultiplicity_fromW_after200 = ROOT.TH1F("h_jetMultiplicity_fromW_after200", "Jet Multiplicity from W After Cuts & Pt>200; Number of Jets; Events", 10, 0, 5)
h_jetMultiplicity_fromW_after400 = ROOT.TH1F("h_jetMultiplicity_fromW_after400", "Jet Multiplicity from W After Cuts & Pt>400; Number of Jets; Events", 10, 0, 5)

h_MET = ROOT.TH1F("h_MET", "MET Before Cuts;MET (GeV);Events", 100, 0, 200)
h_MET_after200 = ROOT.TH1F("h_MET_after200", "MET After Cuts & Pt>200;MET (GeV);Events", 100, 0, 200)
h_MET_after400 = ROOT.TH1F("h_MET_after400", "MET After Cuts & Pt>400;MET (GeV);Events", 100, 0, 200)

h_invariantMass = ROOT.TH1F("h_invariantMass", "Invariant Mass; M (GeV);Events", 100, 0, 7000)
h_invariantMass_aftercut200 = ROOT.TH1F("h_invariantMass_aftercut200", "Invariant Mass After Cuts & Pt>200; M (GeV);Events", 100, 0, 7000)
h_invariantMass_aftercut400 = ROOT.TH1F("h_invariantMass_aftercut400", "Invariant Mass After Cuts & Pt>400; M (GeV);Events", 100, 0, 7000)

h_jetMultiplicity = ROOT.TH1F("h_jetMultiplicity Without Cuts", "Number of Jets per Event", 10, 0, 50)

h_nonTopMotherJets = ROOT.TH1F("h_nonTopMotherJets", "Jets without Top as Mother; Count;Events", 10, 0, 50)

# h_HT = ROOT.TH1F("h_HT", "HT distribution; HT (GeV); Events", 100 ,0 ,3000)

h_LHE_HT_before = ROOT.TH1F("h_LHE_HT_before", "LHE_HT Before Cuts; HT (GeV); Events", 100, 0, 3000)

h_muon_LHE_HT_aftercut200 = ROOT.TH1F("h_muon_LHE_HT_aftercut200", "Muon Channel LHE_HT After Cuts & Pt>200; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_aftercut400 = ROOT.TH1F("h_muon_LHE_HT_aftercut400", "Muon Channel LHE_HT After Cuts & Pt>400; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_aftercut200 = ROOT.TH1F("h_ele_LHE_HT_aftercut200", "Electron Channel LHE_HT After Cuts & Pt>200; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_aftercut400 = ROOT.TH1F("h_ele_LHE_HT_aftercut400", "Electron Channel LHE_HT After Cuts & Pt>400; HT (GeV); Events", 100, 0, 3000)

h_ele_LHE_HT_before = ROOT.TH1F("h_ele_LHE_HT_before", "Electron Channel LHE_HT; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_after_lepton_cut = ROOT.TH1F("h_ele_LHE_HT_after_lepton_cut", "Electron Channel LHE_HT After Electron Pt&Eta Cut; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_after_jet_cut = ROOT.TH1F("h_ele_LHE_HT_after_jet_cut", "Electron Channel LHE_HT After Electron and Jet Cuts; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_after_met_cut = ROOT.TH1F("h_ele_LHE_HT_after_met_cut", "Electron Channel LHE_HT After Electron, Jet, and MET Cut; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_after_toppt200_cut = ROOT.TH1F("h_ele_LHE_HT_after_toppt200_cut", "Electron Channel LHE_HT After Cuts & Pt>200; HT (GeV); Events", 100, 0, 3000)
h_ele_LHE_HT_after_toppt400_cut = ROOT.TH1F("h_ele_LHE_HT_after_toppt400_cut", "Electron Channel LHE_HT After Cuts & Pt>400; HT (GeV); Events", 100, 0, 3000)

h_muon_LHE_HT_before = ROOT.TH1F("h_muon_LHE_HT_before", "Muon Channel LHE_HT; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_after_lepton_cut = ROOT.TH1F("h_muon_LHE_HT_after_lepton_cut", "Muon Channel LHE_HT After Muon Pt&Eta Cut; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_after_jet_cut = ROOT.TH1F("h_muon_LHE_HT_after_jet_cut", "Muon Channel LHE_HT After Muon and Jet Cuts; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_after_met_cut = ROOT.TH1F("h_muon_LHE_HT_after_met_cut", "Muon Channel LHE_HT After Muon, Jet, and MET Cut; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_after_toppt200_cut = ROOT.TH1F("h_muon_LHE_HT_after_toppt200_cut", "Muon Channel LHE_HT After Cuts & Pt>200; HT (GeV); Events", 100, 0, 3000)
h_muon_LHE_HT_after_toppt400_cut = ROOT.TH1F("h_muon_LHE_HT_after_toppt400_cut", "Muon Channel LHE_HT After Cuts & Pt>400; HT (GeV); Events", 100, 0, 3000)


h_both_decays = ROOT.TH1F("h_both_decays", "Events with Both Leptonic and Hadronic Decays; Number of Events; Count", 2, 0, 2)

h_jetFromW_pt = ROOT.TH1F("h_jetFromW_pt", "Jet pT from W Before Cuts; pT (GeV);Events", 1000, 0, 1000)
h_jetFromW_eta = ROOT.TH1F("h_jetFromW_eta", "Jet Eta from W Before Cuts; #eta;Events", 100, -5, 5)
h_jetFromW_pt_aftercut200 = ROOT.TH1F("h_jetFromW_pt_aftercut200", "Jet pT from W After Cuts & TopPt>200; pT (GeV);Events", 1000, 0, 1000)
h_jetFromW_pt_aftercut400 = ROOT.TH1F("h_jetFromW_pt_aftercut400", "Jet pT from W After Cuts & TopPt>400; pT (GeV);Events", 1000, 0, 1000)

h_ttbarMass_vs_HT = ROOT.TH2F("h_ttbarMass_vs_HT", "t#bar{t} Mass vs HT;HT (GeV);t#bar{t} Mass (GeV)", 100, 0, 3000, 100, 0, 7000)
h_muon_ttbarMass_vs_HT_aftercut200 = ROOT.TH2F("h_muon_ttbarMass_vs_HT_aftercut200", "t#bar{t} Mass vs HT Muon Channel After Cuts & TopPt>200;HT (GeV);t#bar{t} Mass (GeV)", 100, 0, 3000, 100, 0, 7000)
h_muon_ttbarMass_vs_HT_aftercut400 = ROOT.TH2F("h_muon_ttbarMass_vs_HT_aftercut400", "t#bar{t} Mass vs HT Muon Channel After Cuts & TopPt>400;HT (GeV);t#bar{t} Mass (GeV)", 100, 0, 3000, 100, 0, 7000)
h_ele_ttbarMass_vs_HT_aftercut200 = ROOT.TH2F("h_ele_ttbarMass_vs_HT_aftercut200", "t#bar{t} Mass vs HT Electron Channel After Cuts & TopPt>200;HT (GeV);t#bar{t} Mass (GeV)", 100, 0, 3000, 100, 0, 7000)
h_ele_ttbarMass_vs_HT_aftercut400 = ROOT.TH2F("h_ele_ttbarMass_vs_HT_aftercut400", "t#bar{t} Mass vs HT Electron Channel After Cuts & TopPt>400;HT (GeV);t#bar{t} Mass (GeV)", 100, 0, 3000, 100, 0, 7000)

h_leading_jet_pt = ROOT.TH1F("h_leading_jet_pt", "Leading Jet pT; pT (GeV);Events", 100, 0, 1000)
h_second_leading_jet_pt = ROOT.TH1F("h_second_leading_jet_pt", "Second Leading Jet pT; pT (GeV);Events", 100, 0, 1000)

h_leading_jet_pt_electron = ROOT.TH1F("h_leading_jet_pt_electron", "Leading Jet pT Electron Channel; pT (GeV);Events", 100, 0, 1000)
h_second_leading_jet_pt_electron = ROOT.TH1F("h_second_leading_jet_pt_electron", "Second Leading Jet pT Electron Channel; pT (GeV);Events", 100, 0, 1000)
h_leading_jet_pt_muon = ROOT.TH1F("h_leading_jet_pt_muon", "Leading Jet pT Muon Channel; pT (GeV);Events", 100, 0, 1000)
h_second_leading_jet_pt_muon = ROOT.TH1F("h_second_leading_jet_pt_muon", "Second Leading Jet pT Muon Channel; pT (GeV);Events", 100, 0, 1000)

h_LHE_HT_0_500_ele_withoutAK8 = ROOT.TH1F("h_LHE_HT_0_500_ele_withoutAK8", "LHE_HT for 0-500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_500_750_ele_withoutAK8 = ROOT.TH1F("h_LHE_HT_500_750_ele_withoutAK8", "LHE_HT for 500-750 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_750_900_ele_withoutAK8 = ROOT.TH1F("h_LHE_HT_750_900_ele_withoutAK8", "LHE_HT for 750-900 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_900_1250_ele_withoutAK8 = ROOT.TH1F("h_LHE_HT_900_1250_ele_withoutAK8", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1250_1500_ele_withoutAK8 = ROOT.TH1F("h_LHE_HT_1250_1500_ele_withoutAK8", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1500_up_ele_withoutAK8 = ROOT.TH1F("h_LHE_HT_1500_up_ele_withoutAK8", "LHE_HT for >1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)

h_LHE_HT_0_500_ele_AK8200 = ROOT.TH1F("h_LHE_HT_0_500_ele_AK8200", "LHE_HT for 0-500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_500_750_ele_AK8200 = ROOT.TH1F("h_LHE_HT_500_750_ele_AK8200", "LHE_HT for 500-750 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_750_900_ele_AK8200 = ROOT.TH1F("h_LHE_HT_750_900_ele_AK8200", "LHE_HT for 750-900 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_900_1250_ele_AK8200 = ROOT.TH1F("h_LHE_HT_900_1250_ele_AK8200", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1250_1500_ele_AK8200 = ROOT.TH1F("h_LHE_HT_1250_1500_ele_AK8200", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1500_up_ele_AK8200 = ROOT.TH1F("h_LHE_HT_1500_up_ele_AK8200", "LHE_HT for >1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)

h_LHE_HT_0_500_ele_AK8400 = ROOT.TH1F("h_LHE_HT_0_500_ele_AK8400", "LHE_HT for 0-500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_500_750_ele_AK8400 = ROOT.TH1F("h_LHE_HT_500_750_ele_AK8400", "LHE_HT for 500-750 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_750_900_ele_AK8400 = ROOT.TH1F("h_LHE_HT_750_900_ele_AK8400", "LHE_HT for 750-900 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_900_1250_ele_AK8400 = ROOT.TH1F("h_LHE_HT_900_1250_ele_AK8400", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1250_1500_ele_AK8400 = ROOT.TH1F("h_LHE_HT_1250_1500_ele_AK8400", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1500_up_ele_AK8400 = ROOT.TH1F("h_LHE_HT_1500_up_ele_AK8400", "LHE_HT for >1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
  
h_LHE_HT_0_500_muon_withoutAK8 = ROOT.TH1F("h_LHE_HT_0_500_muon_withoutAK8", "LHE_HT for 0-500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_500_750_muon_withoutAK8 = ROOT.TH1F("h_LHE_HT_500_750_muon_withoutAK8", "LHE_HT for 500-750 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_750_900_muon_withoutAK8 = ROOT.TH1F("h_LHE_HT_750_900_muon_withoutAK8", "LHE_HT for 750-900 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_900_1250_muon_withoutAK8 = ROOT.TH1F("h_LHE_HT_900_1250_muon_withoutAK8", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1250_1500_muon_withoutAK8 = ROOT.TH1F("h_LHE_HT_1250_1500_muon_withoutAK8", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1500_up_muon_withoutAK8 = ROOT.TH1F("h_LHE_HT_1500_up_muon_withoutAK8", "LHE_HT for >1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)

h_LHE_HT_0_500_muon_AK8200 = ROOT.TH1F("h_LHE_HT_0_500_muon_AK8200", "LHE_HT for 0-500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_500_750_muon_AK8200 = ROOT.TH1F("h_LHE_HT_500_750_muon_AK8200", "LHE_HT for 500-750 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_750_900_muon_AK8200 = ROOT.TH1F("h_LHE_HT_750_900_muon_AK8200", "LHE_HT for 750-900 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_900_1250_muon_AK8200 = ROOT.TH1F("h_LHE_HT_900_1250_muon_AK8200", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1250_1500_muon_AK8200 = ROOT.TH1F("h_LHE_HT_1250_1500_muon_AK8200", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1500_up_muon_AK8200 = ROOT.TH1F("h_LHE_HT_1500_up_muon_AK8200", "LHE_HT for >1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)

h_LHE_HT_0_500_muon_AK8400 = ROOT.TH1F("h_LHE_HT_0_500_muon_AK8400", "LHE_HT for 0-500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_500_750_muon_AK8400 = ROOT.TH1F("h_LHE_HT_500_750_muon_AK8400", "LHE_HT for 500-750 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_750_900_muon_AK8400 = ROOT.TH1F("h_LHE_HT_750_900_muon_AK8400", "LHE_HT for 750-900 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_900_1250_muon_AK8400 = ROOT.TH1F("h_LHE_HT_900_1250_muon_AK8400", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1250_1500_muon_AK8400 = ROOT.TH1F("h_LHE_HT_1250_1500_muon_AK8400", "LHE_HT for 1000-1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
h_LHE_HT_1500_up_muon_AK8400 = ROOT.TH1F("h_LHE_HT_1500_up_muon_AK8400", "LHE_HT for >1500 GeV; LHE_HT (GeV); Events", 100, 0, 3000)
  
  
  
  
def deltaR(eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = abs(phi1 - phi2)
    if dphi > ROOT.TMath.Pi():
        dphi = 2 * ROOT.TMath.Pi() - dphi
    return (deta * deta + dphi * dphi) ** 0.5
# deltaR calculates the deltaR distance in eta - phi space. 
# If this distance is less than a threshold (like 0.4, a typical jet size), we can say the jet is possibly from the top quark.         


# def calculate_HT(entry):
#     HT = 0
#     for i in range(entry.nGenJet):
#         jet_pt = entry.GenJet_pt[i]
#         HT += jet_pt
#     return HT

both_decays_counter = 0



def is_last_copy(statusFlags):
    try:
        status_flags_int = int(statusFlags)
        return (status_flags_int & (1 << 13)) != 0
    except ValueError:
        return False

def process_event(entry, histograms, relevant_pdgIds):
    
    top_count = 0
    antitop_count = 0
    
    top_count_aftercut200 = 0
    antitop_count_aftercut200 = 0
    top_count_aftercut400 = 0
    antitop_count_aftercut400 = 0
    
    # leptons = []
    tops = []
    b_quarks = []
    w_bosons = []
    hadronic_top_pt = []
    
    last_copy_decays = []
    jets_from_w = []
    
    jets_from_w_info =[]
    

    jets_from_w_count = 0
    jets_from_w_count_after200 = 0
    jets_from_w_count_after400 = 0
    
    last_copy_top_decays = []
    last_copy_partons = []
    
    leptons = []
    
    events_after_LHE_HT_cut = 0
    events_after_lepton_selection = 0

    top_pt_cut1 = 200
    top_pt_cut2 = 400
    
    met_vector = ROOT.TLorentzVector() 
    
    leptonic_decay = False
    hadronic_decay = False
    
    electron_found = False
    muon_found = False
    
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
        
        # Collect all last copy partons
        if is_last_copy(statusFlags):
            parton_4vec = ROOT.TLorentzVector()
            parton_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
            last_copy_partons.append(parton_4vec)
            
            # print("last copy parton:", parton_4vec)
            # print("last copy parton 0:", parton_4vec[0])
            # print("last copy parton 1:", parton_4vec[1])
            # print("last copy parton 2:", parton_4vec[2])
            # print("last copy parton 3:", parton_4vec[3])
        
        # Check if particle is a top or antitop quark
        if abs(pdgId) in relevant_pdgIds and is_last_copy(statusFlags):  
            if abs(pdgId) == 6: 
                
                top_4vec = ROOT.TLorentzVector()
                top_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
                tops.append(top_4vec)
                w_daughter = None
                b_daughter = None
                last_copy_top_decays.append((pt, eta, phi))
                
                # print("1) top is ok:", top_4vec[0])
                
                has_leptonic_w_decay = False
                has_hadronic_w_decay = False

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
                                # print("2) w is ok:", w_daughter)
                                
                                if any(abs(entry.GenPart_pdgId[k]) in [11, 13] for k in range(entry.nGenPart) if entry.GenPart_genPartIdxMother[k] == w_daughter):
                                    has_leptonic_w_decay = True
                                    # print("3) lepton is ok:", has_leptonic_w_decay)
                                elif any(abs(entry.GenPart_pdgId[k]) in [1, 2, 3, 4] for k in range(entry.nGenPart) if entry.GenPart_genPartIdxMother[k] == w_daughter):
                                    has_hadronic_w_decay = True
                                    
                                    # print("3) hadronic is ok:", has_hadronic_w_decay)                      
                            elif abs(daughter_pdgId) == 5:
                                b_daughter = j
                                b_4vec = ROOT.TLorentzVector()
                                b_4vec.SetPtEtaPhiM(entry.GenPart_pt[b_daughter], entry.GenPart_eta[b_daughter], entry.GenPart_phi[b_daughter], entry.GenPart_mass[b_daughter])
                                b_quarks.append((b_4vec, j))

                                # print("2) b is ok:", b_daughter)
                
                if has_leptonic_w_decay:
                    # both_decays_counter += 1
                    
                    # Check if W decays leptonically
                    for k in range(entry.nGenPart):
                        if entry.GenPart_genPartIdxMother[k] == w_daughter and abs(entry.GenPart_pdgId[k]) in [11, 13]:  
                            
                            
                            
                            lepton_pdg = entry.GenPart_pdgId[k]
                            # print('3)Lepton pdg:', lepton_pdg)
                            lepton_pt = entry.GenPart_pt[k]
                            # print('Lepton t:', lepton_pt)
                            lepton_eta = entry.GenPart_eta[k]
                            lepton_phi = entry.GenPart_phi[k]
                            histograms['h_leptonPt'].Fill(lepton_pt)
                            histograms['h_leptoneta'].Fill(lepton_eta)
                            histograms['h_leptonphi'].Fill(lepton_phi)
                            histograms['h_leptonFlavor'].Fill(entry.GenPart_pdgId[k])
                            leptons.append((lepton_pt, lepton_eta, lepton_phi, lepton_pdg))
                            leptonic_decay = True
                            if abs(lepton_pdg) == 11:
                                electron_found = True
                                # channel = "electron"
                                # print("Electron found: pt =", entry.GenPart_pt[i])
                            
                            elif abs(lepton_pdg) == 13:
                                muon_found = True
                                # channel = "muon"
                                # print("Muon found: pt =", entry.GenPart_pt[i])
                                
                                
                        else: 
                            continue
                        
                        if abs(pdgId) in [12, 14, 16]:  
                            neutrino = ROOT.TLorentzVector()
                            neutrino.SetPtEtaPhiM(pt, eta, phi, mass)
                            met_vector += neutrino

                                        
                    # Check if W decays hadronically
                    w_quarks = [k for k in range(entry.nGenPart) if entry.GenPart_genPartIdxMother[k] == w_daughter and abs(entry.GenPart_pdgId[k]) in [1, 2, 3, 4]]
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
                            
                                    
                            # Identify the jets coming from the quarks of the hadronically decaying W
                            for j in range(entry.nGenJet):
                                jet = ROOT.TLorentzVector()
                                jet.SetPtEtaPhiM(entry.GenJet_pt[j], entry.GenJet_eta[j], entry.GenJet_phi[j], 0)  # jet mass is negligible?
                                # Match jets to quarks by deltaR
                                if deltaR(jet.Eta(), jet.Phi(), quark1.Eta(), quark1.Phi()) < 0.4 or deltaR(jet.Eta(), jet.Phi(), quark2.Eta(), quark2.Phi()) < 0.4:
                                    jets_from_w.append(jet)
                                    jets_from_w_count += 1
                                    
                                    jets_from_w_info.append((j, jet.Pt(), jet.Eta(), jet.Phi()))
                                    

                        if len(jets_from_w) >= 2:
                            # Proceed with analysis for hadronic decay
                            pass
                        
                    if hadronic_decay and leptonic_decay:
                        both_decays_counter += 1

                
                    # b-quarks
                    if b_daughter is not None:
                        b_vector = ROOT.TLorentzVector()
                        b_vector.SetPtEtaPhiM(entry.GenPart_pt[b_daughter], entry.GenPart_eta[b_daughter], entry.GenPart_phi[b_daughter], entry.GenPart_mass[b_daughter])
                        # print("2) b_daughter:", b_vector.Pt())
                        # histograms['h_bquark_pt'].Fill(b_vector.Pt())
                        # histograms['h_bquark_eta'].Fill(b_vector.Eta())
                else: 
                    continue  
            else:
                continue
    
    
                    
    # print("Leptons:", leptons)
    # print("Leptons len :", len(leptons))
    is_electron_channel = any(abs(pdgId) == 11 for lepton_pt, lepton_eta, Lepton_phi, lepton_pdgId in leptons)
    is_muon_channel = any(abs(pdgId) == 13 for lepton_pt, lepton_eta, Lepton_phi, lepton_pdgId in leptons)
    
    if electron_found and not muon_found:
        channel = "electron"
    elif muon_found and not electron_found:
        channel = "muon"
    else:
        channel = "other"
    
    if channel == "other":
        return
        
    # print("Channel2:", channel)
    
    
    passed_lepton_cut, passed_jet_cut, passed_met_cut, top_pt_pass1, top_pt_pass2 = passes_selection_criteria(entry, leptons, tops, channel, hadronic_top_pt, top_pt_cut1, top_pt_cut2, b_quarks, last_copy_partons)

    print "Channel:", channel
    print "Passed Lepton Cut:", passed_lepton_cut, "Passed Jet Cut:", passed_jet_cut, "Passed MET Cut:", passed_met_cut
    # print "Top Pt Pass1:", top_pt_pass1, "Top Pt Pass2:", top_pt_pass2

    if channel == "electron":
        jet_pt_cut = 40
    elif channel == "muon":
        jet_pt_cut = 50
    else:
        jet_pt_cut = 50  
    
    matched_jets = match_jets_to_partons(entry, last_copy_partons)
    leading_jet, second_leading_jet = select_leading_jets_from_matched(matched_jets, jet_pt_cut)
    # print("Leptons2:", leptons)
    # print(passes_selection_criteria(entry, leptons, tops, channel, hadronic_top_pt, top_pt_cut1, top_pt_cut2, b_quarks, last_copy_partons))

    
    
    b_jet_matched, matched_b_quark = check_b_jet_from_top(b_quarks, leading_jet, second_leading_jet)
    # print "b_jet_matched:", b_jet_matched
    # if b_jet_matched:
        # print "Matched b-quark Pt:", matched_b_quark[0].Pt(), "Index:", matched_b_quark[1]

    if not b_jet_matched:
        leading_b_quark = find_leading_b_quark(b_quarks, leading_jet, second_leading_jet)
        # if leading_b_quark is None:
            # print "No leading b-quark found outside of leading jets"
        # else:
            # print "Leading b-quark Pt:", leading_b_quark[0].Pt(), "Index:", leading_b_quark[1]
        if leading_b_quark is None or leading_b_quark[0].Pt() < 30:
            # Veto this event as it does not meet the b-quark criteria
            return
    
    for lepton in leptons:
        lepton_pt, lepton_eta, lepton_phi, lepton_pdgId = lepton
        if abs(lepton_pdgId) == 11:
            channel = "electron"
            histograms['h_electronPt'].Fill(lepton_pt)
            histograms['h_electroneta'].Fill(lepton_eta)
                                
        elif abs(lepton_pdgId) == 13:
            channel = "muon"
            histograms['h_muonPt'].Fill(lepton_pt)
            histograms['h_muoneta'].Fill(lepton_eta)
                        
                    
        if passed_lepton_cut and passed_jet_cut and passed_met_cut: 
            if channel == "electron":
                if top_pt_pass1:
                    histograms['h_electronPt_aftercut200'].Fill(lepton_pt)
                    histograms['h_electroneta_aftercut200'].Fill(lepton_eta)
                if top_pt_pass2:
                    histograms['h_electronPt_aftercut400'].Fill(lepton_pt)
                    histograms['h_electroneta_aftercut400'].Fill(lepton_eta)  
                    
            elif channel == "muon":
                if top_pt_pass1:
                    histograms['h_muonPt_aftercut200'].Fill(lepton_pt)
                    histograms['h_muoneta_aftercut200'].Fill(lepton_eta)
                if top_pt_pass2:
                    histograms['h_muonPt_aftercut400'].Fill(lepton_pt)
                    histograms['h_muoneta_aftercut400'].Fill(lepton_eta)

    # for i in range(entry.nGenPart):
    #     pdgId = entry.GenPart_pdgId[i]
    #     pt = entry.GenPart_pt[i]
    #     eta = entry.GenPart_eta[i]
    #     phi = entry.GenPart_phi[i]
    #     mass = entry.GenPart_mass[i]
    #     mother_idx = entry.GenPart_genPartIdxMother[i]
    #     status = entry.GenPart_status[i]
    #     statusFlags = entry.GenPart_statusFlags[i]
        
    met_vector_after200 = ROOT.TLorentzVector()
    met_vector_after400 = ROOT.TLorentzVector()
                            
    for top_4vec in tops:
        if pdgId == 6:
            top_count += 1
            histograms['h_topPt'].Fill(top_4vec.Pt())
            if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_topPt_aftercut200'].Fill(top_4vec.Pt())
                top_count_aftercut200 += 1
            if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_topPt_aftercut400'].Fill(top_4vec.Pt())
                top_count_aftercut400 += 1
            if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_topPt_aftercut200'].Fill(top_4vec.Pt())
                top_count_aftercut200 += 1
            if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_topPt_aftercut400'].Fill(top_4vec.Pt())
                top_count_aftercut400 += 1
            
        elif pdgId == -6:
            antitop_count += 1
            histograms['h_antitopPt'].Fill(top_4vec.Pt())
            if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_antitopPt_aftercut200'].Fill(top_4vec.Pt())
                antitop_count_aftercut200 += 1
            if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_antitopPt_aftercut400'].Fill(top_4vec.Pt())
                antitop_count_aftercut400 += 1
            if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_antitopPt_aftercut200'].Fill(top_4vec.Pt())
                antitop_count_aftercut200 += 1
            if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_antitopPt_aftercut400'].Fill(top_4vec.Pt())
                antitop_count_aftercut400 += 1

        histograms['h_topMultiplicity'].Fill(top_count)
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
            histograms['h_topMultiplicity_aftercut200'].Fill(top_count_aftercut200)
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
            histograms['h_topMultiplicity_aftercut400'].Fill(top_count_aftercut400)
        if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
            histograms['h_topMultiplicity_aftercut200'].Fill(top_count_aftercut200)
        if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
            histograms['h_topMultiplicity_aftercut400'].Fill(top_count_aftercut400)
        
        histograms['h_antitopMultiplicity'].Fill(antitop_count)
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
            histograms['h_antitopMultiplicity_aftercut200'].Fill(antitop_count_aftercut200)
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
            histograms['h_antitopMultiplicity_aftercut400'].Fill(antitop_count_aftercut400)
        if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
            histograms['h_antitopMultiplicity_aftercut200'].Fill(antitop_count_aftercut200)
        if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
            histograms['h_antitopMultiplicity_aftercut400'].Fill(antitop_count_aftercut400)

    for w_4vec in w_bosons:
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
            histograms['h_hadronic_w_mass_aftercut200'].Fill(w_4vec.M())
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_hadronic_w_mass_aftercut400'].Fill(w_4vec.M())          
        if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_hadronic_w_mass_aftercut200'].Fill(w_4vec.M())
        if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_hadronic_w_mass_aftercut400'].Fill(w_4vec.M())

    for b_quark in b_quarks:
        b_vector, b_index = b_quark 
        # print("bquark pt:", b_vector.Pt())    
        # if passed_jet_cut: 
            # print("bquark pt:", b_vector.Pt())  
        if (channel == "electron") and passed_jet_cut:
            # print("bquark pt electron:", b_vector.Pt())
            histograms['h_bquark_pt_electron'].Fill(b_vector.Pt())
            histograms['h_bquark_eta_electron'].Fill(b_vector.Eta())
        if (channel == "muon") and passed_jet_cut:
            # print("bquark pt muon:", b_vector.Pt())
            histograms['h_bquark_pt_muon'].Fill(b_vector.Pt())
            histograms['h_bquark_eta_muon'].Fill(b_vector.Eta())
            
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
            histograms['h_bquark_pt_aftercut200'].Fill(b_vector.Pt())
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
            histograms['h_bquark_pt_aftercut400'].Fill(b_vector.Pt())
        if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
            histograms['h_bquark_pt_aftercut200'].Fill(b_vector.Pt())
        if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
            histograms['h_bquark_pt_aftercut400'].Fill(b_vector.Pt())
    

    
    for jet_info in jets_from_w_info:
        jet_idx, jet_pt, jet_eta, jet_phi = jet_info
        histograms['h_jetFromW_pt'].Fill(jet_pt)
        histograms['h_jetFromW_eta'].Fill(jet_eta)
        
        if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut:
            if top_pt_pass1:
                histograms['h_jetFromW_pt_aftercut200'].Fill(jet_pt)
            if top_pt_pass2:
                histograms['h_jetFromW_pt_aftercut400'].Fill(jet_pt)
        elif channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut:
            if top_pt_pass1:
                histograms['h_jetFromW_pt_aftercut200'].Fill(jet_pt)
            if top_pt_pass2:
                histograms['h_jetFromW_pt_aftercut400'].Fill(jet_pt)

    histograms['h_jetMultiplicity_fromW'].Fill(jets_from_w_count)
    histograms['h_jetMultiplicity_fromW_after200'].Fill(jets_from_w_count_after200)
    histograms['h_jetMultiplicity_fromW_after400'].Fill(jets_from_w_count_after400) 
    
    histograms['h_MET'].Fill(met_vector.Pt())
    
    if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
        histograms['h_MET_after200'].Fill(met_vector.Pt())
    if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
        histograms['h_MET_after400'].Fill(met_vector.Pt())
    if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
        histograms['h_MET_after200'].Fill(met_vector.Pt())
    if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
        histograms['h_MET_after400'].Fill(met_vector.Pt()) 
    
        
    
    if top_count > 0 and antitop_count > 0:
        top_idx = next((idx for idx, pdg in enumerate(entry.GenPart_pdgId) if pdg == 6), None)
        antitop_idx = next((idx for idx, pdg in enumerate(entry.GenPart_pdgId) if pdg == -6), None)
        if top_idx is not None and antitop_idx is not None:
            antitop_4vec = ROOT.TLorentzVector()
            top_4vec.SetPtEtaPhiM(entry.GenPart_pt[top_idx], entry.GenPart_eta[top_idx], entry.GenPart_phi[top_idx], entry.GenPart_mass[top_idx])
            antitop_4vec.SetPtEtaPhiM(entry.GenPart_pt[antitop_idx], entry.GenPart_eta[antitop_idx], entry.GenPart_phi[antitop_idx], entry.GenPart_mass[antitop_idx])
            ttbar = top_4vec + antitop_4vec
            m_tt = ttbar.M()
            
            if ttbar is not None:
                histograms['h_invariantMass'].Fill(ttbar.M())
            if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_invariantMass_aftercut200'].Fill(ttbar.M())
            if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_invariantMass_aftercut400'].Fill(ttbar.M())
            if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_invariantMass_aftercut200'].Fill(ttbar.M())
            if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_invariantMass_aftercut400'].Fill(ttbar.M())
                
            LHE_HT = getattr(entry, "LHE_HT", -1)
            if LHE_HT >= 0:
                if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut:
                    if 0 <= m_tt < 500:
                        histograms['h_LHE_HT_0_500_ele_withoutAK8'].Fill(LHE_HT)
                    elif 500 <= m_tt < 750:
                        histograms['h_LHE_HT_500_750_ele_withoutAK8'].Fill(LHE_HT)
                    elif 750 <= m_tt < 900:
                        histograms['h_LHE_HT_750_900_ele_withoutAK8'].Fill(LHE_HT)
                    elif 900 <= m_tt < 1250:
                        histograms['h_LHE_HT_900_1250_ele_withoutAK8'].Fill(LHE_HT)
                    elif 1250 <= m_tt < 1500:
                        histograms['h_LHE_HT_1250_1500_ele_withoutAK8'].Fill(LHE_HT)
                    elif m_tt >= 1500:
                        histograms['h_LHE_HT_1500_up_ele_withoutAK8'].Fill(LHE_HT)
                        
                    if top_pt_pass1:
                    
                        if 0 <= m_tt < 500:
                            histograms['h_LHE_HT_0_500_ele_AK8200'].Fill(LHE_HT)
                        elif 500 <= m_tt < 750:
                            histograms['h_LHE_HT_500_750_ele_AK8200'].Fill(LHE_HT)
                        elif 750 <= m_tt < 900:
                            histograms['h_LHE_HT_750_900_ele_AK8200'].Fill(LHE_HT)
                        elif 900 <= m_tt < 1250:
                            histograms['h_LHE_HT_900_1250_ele_AK8200'].Fill(LHE_HT)
                        elif 1250 <= m_tt < 1500:
                            histograms['h_LHE_HT_1250_1500_ele_AK8200'].Fill(LHE_HT)
                        elif m_tt >= 1500:
                            histograms['h_LHE_HT_1500_up_ele_AK8200'].Fill(LHE_HT)
                    
                    if top_pt_pass2:
                        
                        if 0 <= m_tt < 500:
                            histograms['h_LHE_HT_0_500_ele_AK8400'].Fill(LHE_HT)
                        elif 500 <= m_tt < 750:
                            histograms['h_LHE_HT_500_750_ele_AK8400'].Fill(LHE_HT)
                        elif 750 <= m_tt < 900:
                            histograms['h_LHE_HT_750_900_ele_AK8400'].Fill(LHE_HT)
                        elif 900 <= m_tt < 1250:
                            histograms['h_LHE_HT_900_1250_ele_AK8400'].Fill(LHE_HT)
                        elif 1250 <= m_tt < 1500:
                            histograms['h_LHE_HT_1250_1500_ele_AK8400'].Fill(LHE_HT)
                        elif m_tt >= 1500:
                            histograms['h_LHE_HT_1500_up_ele_AK8400'].Fill(LHE_HT)
                        
                if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut:
                
                    if 0 <= m_tt < 500:
                        histograms['h_LHE_HT_0_500_muon_withoutAK8'].Fill(LHE_HT)
                    elif 500 <= m_tt < 750:
                        histograms['h_LHE_HT_500_750_muon_withoutAK8'].Fill(LHE_HT)
                    elif 750 <= m_tt < 900:
                        histograms['h_LHE_HT_750_900_muon_withoutAK8'].Fill(LHE_HT)
                    elif 900 <= m_tt < 1250:
                        histograms['h_LHE_HT_900_1250_muon_withoutAK8'].Fill(LHE_HT)
                    elif 1250 <= m_tt < 1500:
                        histograms['h_LHE_HT_1250_1500_muon_withoutAK8'].Fill(LHE_HT)
                    elif m_tt >= 1500:
                        histograms['h_LHE_HT_1500_up_muon_withoutAK8'].Fill(LHE_HT)
                        
                    if top_pt_pass1:
                            
                        if 0 <= m_tt < 500:
                            histograms['h_LHE_HT_0_500_muon_AK8200'].Fill(LHE_HT)
                        elif 500 <= m_tt < 750:
                            histograms['h_LHE_HT_500_750_muon_AK8200'].Fill(LHE_HT)
                        elif 750 <= m_tt < 900:
                            histograms['h_LHE_HT_750_900_muon_AK8200'].Fill(LHE_HT)
                        elif 900 <= m_tt < 1250:
                            histograms['h_LHE_HT_900_1250_muon_AK8200'].Fill(LHE_HT)
                        elif 1250 <= m_tt < 1500:
                            histograms['h_LHE_HT_1250_1500_muon_AK8200'].Fill(LHE_HT)
                        elif m_tt >= 1500:
                            histograms['h_LHE_HT_1500_up_muon_AK8200'].Fill(LHE_HT)
                        
                    if top_pt_pass2:
                        
                        if 0 <= m_tt < 500:
                            histograms['h_LHE_HT_0_500_muon_AK8400'].Fill(LHE_HT)
                        elif 500 <= m_tt < 750:
                            histograms['h_LHE_HT_500_750_muon_AK8400'].Fill(LHE_HT)
                        elif 750 <= m_tt < 900:
                            histograms['h_LHE_HT_750_900_muon_AK8400'].Fill(LHE_HT)
                        elif 900 <= m_tt < 1250:
                            histograms['h_LHE_HT_900_1250_muon_AK8400'].Fill(LHE_HT)
                        elif 1250 <= m_tt < 1500:
                            histograms['h_LHE_HT_1250_1500_muon_AK8400'].Fill(LHE_HT)
                        elif m_tt >= 1500:
                            histograms['h_LHE_HT_1500_up_muon_AK8400'].Fill(LHE_HT)

    
    
    non_top_mother_jet_count = 0

    for i in range(entry.nGenJet):
        jet_eta = entry.GenJet_eta[i]
        jet_phi = entry.GenJet_phi[i]
        jet_pt = entry.GenJet_pt[i]
        
        for parton in last_copy_decays:
            if deltaR(jet_eta, jet_phi, parton[1], parton[2]) < 0.4: # Use indices for eta and phi
                non_top_mother_jet_count += 1
        

    histograms['h_jetMultiplicity'].Fill(entry.nGenJet)
    histograms['h_nonTopMotherJets'].Fill(non_top_mother_jet_count)
    # HT variable from data in ttree
    LHE_HT = getattr(entry, "LHE_HT", -1)
    if LHE_HT >= 0:
        histograms['h_LHE_HT_before'].Fill(LHE_HT)
        # histograms["h_ttbarMass_vs_HT"].Fill(LHE_HT, ttbar.M())

        # Apply selection criteria for LHE_HT
        if passed_lepton_cut and passed_jet_cut and passed_met_cut:
            if top_pt_pass1:
                if channel == "muon":
                    histograms['h_muon_LHE_HT_aftercut200'].Fill(LHE_HT)
                    histograms["h_muon_ttbarMass_vs_HT_aftercut200"].Fill(LHE_HT, ttbar.M())
                elif channel == "electron":
                    histograms['h_ele_LHE_HT_aftercut200'].Fill(LHE_HT)
                    histograms["h_ele_ttbarMass_vs_HT_aftercut200"].Fill(LHE_HT, ttbar.M())
            if top_pt_pass2:
                if channel == "muon":
                    histograms['h_muon_LHE_HT_aftercut400'].Fill(LHE_HT)
                    histograms["h_muon_ttbarMass_vs_HT_aftercut400"].Fill(LHE_HT, ttbar.M())
                elif channel == "electron":
                    histograms['h_ele_LHE_HT_aftercut400'].Fill(LHE_HT)
                    histograms["h_ele_ttbarMass_vs_HT_aftercut400"].Fill(LHE_HT, ttbar.M())

    
        # cuts gradually     
        if channel == "electron":
            histograms['h_ele_LHE_HT_before'].Fill(LHE_HT)
            if passed_jet_cut:
                histograms['h_ele_LHE_HT_after_jet_cut'].Fill(LHE_HT)
            if passed_lepton_cut and passed_jet_cut:
                histograms['h_ele_LHE_HT_after_lepton_cut'].Fill(LHE_HT)
            if passed_lepton_cut and passed_jet_cut and passed_met_cut:
                histograms['h_ele_LHE_HT_after_met_cut'].Fill(LHE_HT)
            if passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_ele_LHE_HT_after_toppt200_cut'].Fill(LHE_HT)
            if passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_ele_LHE_HT_after_toppt400_cut'].Fill(LHE_HT)
                
        if channel == "muon":
            histograms['h_muon_LHE_HT_before'].Fill(LHE_HT)
            if passed_jet_cut:
                histograms['h_muon_LHE_HT_after_jet_cut'].Fill(LHE_HT)
            if passed_lepton_cut and passed_jet_cut:
                histograms['h_muon_LHE_HT_after_lepton_cut'].Fill(LHE_HT)
            if passed_lepton_cut and passed_jet_cut and passed_met_cut:
                histograms['h_muon_LHE_HT_after_met_cut'].Fill(LHE_HT)
            if passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                histograms['h_muon_LHE_HT_after_toppt200_cut'].Fill(LHE_HT)
            if passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                histograms['h_muon_LHE_HT_after_toppt400_cut'].Fill(LHE_HT)

        if leading_jet is not None and second_leading_jet is not None:
            if leading_jet:
                # print("leading jet:", leading_jet[0].Pt())
                # print("leading jet pdgId:", leading_jet[1])
                histograms['h_leading_jet_pt'].Fill(leading_jet[0].Pt()) #leading_jet[0] contains the pt of the leading jet
            if second_leading_jet:
                histograms['h_second_leading_jet_pt'].Fill(second_leading_jet[0].Pt())
                # print("second leading jet:", second_leading_jet[0].Pt())
                # print("second leading jet pdgId:", second_leading_jet[1])
            
            if len(leptons)>0:  
                if channel == "electron":
                    if leading_jet:
                        histograms['h_leading_jet_pt_electron'].Fill(leading_jet[0].Pt()) #leading_jet[0] contains the pt of the leading jet
                        # print("Leading Jet electron: PT = {}, ETA = {}, Index = {}, pdgId = {}".format(*leading_jet))
                    if second_leading_jet:
                        histograms['h_second_leading_jet_pt_electron'].Fill(second_leading_jet[0].Pt())
                        # print("Second Leading Jet electron: PT = {}, ETA = {}, Index = {}, pdgId = {}".format(*second_leading_jet))

                        
                if channel == "muon":
                    if leading_jet:
                        # print("Leading Jet muon: PT = {}, ETA = {}, PHI = {}, PDG ID = {}".format(
                        #     leading_jet[0].Pt(), 
                        #     leading_jet[0].Eta(), 
                        #     leading_jet[0].Phi(), 
                        #     leading_jet[1]# ))
                        histograms['h_leading_jet_pt_muon'].Fill(leading_jet[0].Pt()) #leading_jet[0] contains the pt of the leading jet
                    if second_leading_jet:
                        histograms['h_second_leading_jet_pt_muon'].Fill(second_leading_jet[0].Pt())
                        # print("Second Leading Jet muon: PT = {}, ETA = {}, PHI = {}, PDG ID = {}".format(
                        #     second_leading_jet[0].Pt(), 
                        #     second_leading_jet[0].Eta(), 
                        #     second_leading_jet[0].Phi(), 
                        #     second_leading_jet[1]
                        # ))
        
        
        # if leading_jet is not None:
        # pass_criteria = passes_selection_criteria(entry, leptons, tops, hadronic_top_pt, channel, top_pt_cut1, top_pt_cut2, b_quarks, last_copy_partons)
    
    return leptons, tops, hadronic_top_pt, b_quarks, last_copy_partons, channel

h_both_decays.Fill(0, both_decays_counter)

# This function identifies jets that are closely matched with last copy partons. 
# It appends a tuple to matched_jets which includes the jet and its index in the GenJet collection.
def match_jets_to_partons(entry, last_copy_partons):
    matched_jets = []
    for j in range(entry.nGenJet):
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(entry.GenJet_pt[j], entry.GenJet_eta[j], entry.GenJet_phi[j], 0)  # jet mass is negligible

        # finding the closest last copy parton to this jet
        closest_parton = min(last_copy_partons, key=lambda p: deltaR(jet.Eta(), jet.Phi(), p.Eta(), p.Phi()))
        if deltaR(jet.Eta(), jet.Phi(), closest_parton.Eta(), closest_parton.Phi()) < 0.4:
            matched_jets.append((jet, j)) 

    return matched_jets


# This function filters and sorts the jets based on their Pt, 
# then identifies the leading and second-leading jets.
def select_leading_jets_from_matched(matched_jets, jet_pt_cut):
    
    filtered_jets = [(jet, pdg_id) for jet, pdg_id in matched_jets if jet.Pt() > jet_pt_cut]
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
        b_vector, b_index = b_quark
        # Check if the b-quark index matches with leading or second-leading jet
        if leading_jet and b_index == leading_jet[1]:
            return True, b_vector
        elif second_leading_jet and b_index == second_leading_jet[1]:
            return True, b_vector
    return False, None


# This function correctly identifies the leading b-quark that is not part of the leading or second-leading jets. 
# It iterates through the b_quarks, excludes those that match the leading or second-leading jets, and then finds the one with the highest Pt.
def find_leading_b_quark(b_quarks, leading_jet, second_leading_jet):
    highest_pt = 0
    leading_b_quark = None
    for b_quark in b_quarks:
        b_vector, b_index = b_quark
        # Exclude b-quarks that are already in leading or second-leading jet
        if leading_jet and b_index == leading_jet[1] or second_leading_jet and b_index == second_leading_jet[1]:
            continue
        if b_vector.Pt() > highest_pt:
            highest_pt = b_vector.Pt()
            leading_b_quark = b_quark
    return leading_b_quark


def passes_selection_criteria(entry, leptons, tops, channel, hadronic_top_pt, top_pt_cut1, top_pt_cut2, b_quarks, last_copy_partons):
    
    met_cut_electron = 60
    met_cut_muon = 70
    met_cut = 0
    
    met_pt = entry.GenMET_pt
    
    top_pt_pass1 = False
    top_pt_pass2 = False
    
    
    # Determine channel based on lepton type
    if channel == "electron":
        jet_pt_cut = 40
        lepton_pt_cut = 120
        lepton_eta_cut = 2.5
        met_cut = 60
    elif channel == "muon":
        jet_pt_cut = 50
        lepton_pt_cut = 55
        lepton_eta_cut = 2.4
        met_cut = 70
    else:
        jet_pt_cut = 50
        lepton_pt_cut = 55
        lepton_eta_cut = 2.4
        met_cut = 0
    
    #Jet selection with last copy matching    

    # 1) identify first and second leading jets
    matched_jets = match_jets_to_partons(entry, last_copy_partons)
    leading_jet, second_leading_jet = select_leading_jets_from_matched(matched_jets, jet_pt_cut)

    # if leading_jet is not None:
    #     print("Leading Jet from passes_selection_criteria: PT = {}, ETA = {}, Index = {}, pdgId = {}".format(*leading_jet))
    # if second_leading_jet is not None:
    #     print("Second Leading Jet from passes_selection_criteria: PT = {}, ETA = {}, Index = {}, pdgId = {}".format(*second_leading_jet))

    # 2) check if either leading jet is a b-quark from top
    b_jet_in_leading = False
    if leading_jet is not None and second_leading_jet is not None:
            b_jet_in_leading = check_b_jet_from_top(b_quarks, leading_jet, second_leading_jet)
            # print("b_jet_in_leading:", b_jet_in_leading)

    # Find the leading b-quark and check its pT
    leading_b_quark = find_leading_b_quark(b_quarks, leading_jet, second_leading_jet)
    # print("leading_b_quark:", leading_b_quark)
    
    leading_b_quark_high_pt = leading_b_quark is not None and leading_b_quark[0] > 30
    # print("leading_b_quark_high_pt:", leading_b_quark_high_pt)
    
    passed_jet_cut = False
    if leading_jet and second_leading_jet:
        if b_jet_in_leading or leading_b_quark_high_pt:
            passed_jet_cut = True
            # print("jet cut in if statement in passes_selection_criteria:", passed_jet_cut)

    # print("leading_jet in passes_selection_criteria:", leading_jet)
    # print("second_leading_jet in passes_selection_criteria:", second_leading_jet)
    
    
    # for top_4vec in tops:
    #     if top_4vec.Pt() > top_pt_cut1:
    #         top_pt_pass1 = True
    #     if top_4vec.Pt() > top_pt_cut2:
    #         top_pt_pass2 = True
            
    top_pt_pass1 = any(pt > top_pt_cut1 for pt in hadronic_top_pt)
    top_pt_pass2 = any(pt > top_pt_cut2 for pt in hadronic_top_pt)
    # print("Jet 0: ", entry.GenJet_pt[0])
    # print("Jet 1: ", entry.GenJet_pt[1])
    
    jet_count = 0
    if entry.nGenJet >= 2:
        jet_count = int(entry.GenJet_pt[0] > jet_pt_cut) + int(entry.GenJet_pt[1] > jet_pt_cut)
    passed_lepton_cut = sum(1 for lepton in leptons if lepton[0] > lepton_pt_cut and abs(lepton[1]) < lepton_eta_cut) > 0
    # print("lepton cut in if statement in passes_selection_criteria:", passed_lepton_cut)
    # print("Lepton PT Cut:", lepton_pt_cut, "Lepton ETA Cut:", lepton_eta_cut)
    # for lepton in leptons:
    #     print("Lepton PT:", lepton[0], "Lepton ETA:", lepton[1])
    #     if lepton[0] > lepton_pt_cut and abs(lepton[1]) < lepton_eta_cut:
    #         print("Lepton passes cuts")
    passed_jet_cut = jet_count > 0
    passed_met_cut = met_pt > met_cut

    return passed_lepton_cut, passed_jet_cut, passed_met_cut, top_pt_pass1, top_pt_pass2



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
        # Your existing code here...
        
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
    'h_electronPt_aftercut200': h_electronPt_aftercut200,
    'h_electronPt_aftercut400': h_electronPt_aftercut400,
    'h_electroneta': h_electroneta,
    'h_electroneta_aftercut200': h_electroneta_aftercut200,
    'h_electroneta_aftercut400': h_electroneta_aftercut400,
    'h_muonPt': h_muonPt,
    'h_muonPt_aftercut200': h_muonPt_aftercut200,
    'h_muonPt_aftercut400': h_muonPt_aftercut400,
    'h_muoneta': h_muoneta,
    'h_muoneta_aftercut200': h_muoneta_aftercut200,
    'h_muoneta_aftercut400': h_muoneta_aftercut400,
    'h_hadronic_w_mass': h_hadronic_w_mass,
    'h_hadronic_w_mass_aftercut200': h_hadronic_w_mass_aftercut200,
    'h_hadronic_w_mass_aftercut400': h_hadronic_w_mass_aftercut400,
    'h_topPt': h_topPt,
    'h_topPt_aftercut200': h_topPt_aftercut200,
    'h_topPt_aftercut400': h_topPt_aftercut400,
    'h_antitopPt': h_antitopPt,
    'h_antitopPt_aftercut200': h_antitopPt_aftercut200,
    'h_antitopPt_aftercut400': h_antitopPt_aftercut400,
    'h_bquark_pt_electron': h_bquark_pt_electron,
    'h_bquark_eta_electron': h_bquark_eta_electron,
    'h_bquark_pt_muon': h_bquark_pt_muon,
    'h_bquark_eta_muon': h_bquark_eta_muon,
    'h_bquark_pt_aftercut200': h_bquark_pt_aftercut200,
    'h_bquark_pt_aftercut400': h_bquark_pt_aftercut400,
    'h_topMultiplicity': h_topMultiplicity,
    'h_topMultiplicity_aftercut200': h_topMultiplicity_aftercut200,
    'h_topMultiplicity_aftercut400': h_topMultiplicity_aftercut400,
    'h_antitopMultiplicity': h_antitopMultiplicity,
    'h_antitopMultiplicity_aftercut200': h_antitopMultiplicity_aftercut200,
    'h_antitopMultiplicity_aftercut400': h_antitopMultiplicity_aftercut400,
    'h_jetMultiplicity_fromW': h_jetMultiplicity_fromW,
    'h_jetMultiplicity_fromW_after200': h_jetMultiplicity_fromW_after200,
    'h_jetMultiplicity_fromW_after400': h_jetMultiplicity_fromW_after400,
    'h_MET': h_MET,
    'h_MET_after200': h_MET_after200,
    'h_MET_after400': h_MET_after400,
    'h_invariantMass': h_invariantMass,
    'h_invariantMass_aftercut200': h_invariantMass_aftercut200,
    'h_invariantMass_aftercut400': h_invariantMass_aftercut400,
    'h_jetMultiplicity': h_jetMultiplicity,
    'h_nonTopMotherJets': h_nonTopMotherJets,
    'h_LHE_HT_before': h_LHE_HT_before,
    'h_muon_LHE_HT_aftercut200': h_muon_LHE_HT_aftercut200,
    'h_muon_LHE_HT_aftercut400': h_muon_LHE_HT_aftercut400,
    'h_ele_LHE_HT_aftercut200': h_ele_LHE_HT_aftercut200,
    'h_ele_LHE_HT_aftercut400': h_ele_LHE_HT_aftercut400,
    'h_ele_LHE_HT_before': h_ele_LHE_HT_before,
    'h_ele_LHE_HT_after_lepton_cut': h_ele_LHE_HT_after_lepton_cut,
    'h_ele_LHE_HT_after_jet_cut': h_ele_LHE_HT_after_jet_cut,
    'h_ele_LHE_HT_after_met_cut': h_ele_LHE_HT_after_met_cut,
    'h_ele_LHE_HT_after_toppt200_cut': h_ele_LHE_HT_after_toppt200_cut,
    'h_ele_LHE_HT_after_toppt400_cut': h_ele_LHE_HT_after_toppt400_cut,
    'h_muon_LHE_HT_before': h_muon_LHE_HT_before,
    'h_muon_LHE_HT_after_lepton_cut': h_muon_LHE_HT_after_lepton_cut,
    'h_muon_LHE_HT_after_jet_cut': h_muon_LHE_HT_after_jet_cut,
    'h_muon_LHE_HT_after_met_cut': h_muon_LHE_HT_after_met_cut,
    'h_muon_LHE_HT_after_toppt200_cut': h_muon_LHE_HT_after_toppt200_cut,
    'h_muon_LHE_HT_after_toppt400_cut': h_muon_LHE_HT_after_toppt400_cut,
    'h_both_decays': h_both_decays,
    'h_jetFromW_pt': h_jetFromW_pt,
    'h_jetFromW_eta': h_jetFromW_eta,
    'h_jetFromW_pt_aftercut200': h_jetFromW_pt_aftercut200,
    'h_jetFromW_pt_aftercut400': h_jetFromW_pt_aftercut400,
    'h_ttbarMass_vs_HT' : h_ttbarMass_vs_HT,
    'h_muon_ttbarMass_vs_HT_aftercut200': h_muon_ttbarMass_vs_HT_aftercut200,
    'h_muon_ttbarMass_vs_HT_aftercut400': h_muon_ttbarMass_vs_HT_aftercut400,
    'h_ele_ttbarMass_vs_HT_aftercut200': h_ele_ttbarMass_vs_HT_aftercut200,
    'h_ele_ttbarMass_vs_HT_aftercut400': h_ele_ttbarMass_vs_HT_aftercut400,
    'h_leading_jet_pt' : h_leading_jet_pt,
    'h_second_leading_jet_pt' : h_second_leading_jet_pt,
    'h_LHE_HT_0_500_ele_withoutAK8' : h_LHE_HT_0_500_ele_withoutAK8,
    'h_LHE_HT_500_750_ele_withoutAK8' : h_LHE_HT_500_750_ele_withoutAK8,
    'h_LHE_HT_750_900_ele_withoutAK8' : h_LHE_HT_750_900_ele_withoutAK8,
    'h_LHE_HT_900_1250_ele_withoutAK8' : h_LHE_HT_900_1250_ele_withoutAK8,
    'h_LHE_HT_1250_1500_ele_withoutAK8' : h_LHE_HT_1250_1500_ele_withoutAK8,
    'h_LHE_HT_1500_up_ele_withoutAK8' : h_LHE_HT_1500_up_ele_withoutAK8,
    'h_LHE_HT_0_500_ele_AK8200' : h_LHE_HT_0_500_ele_AK8200,
    'h_LHE_HT_500_750_ele_AK8200' : h_LHE_HT_500_750_ele_AK8200,
    'h_LHE_HT_750_900_ele_AK8200' : h_LHE_HT_750_900_ele_AK8200,
    'h_LHE_HT_900_1250_ele_AK8200' : h_LHE_HT_900_1250_ele_AK8200,
    'h_LHE_HT_1250_1500_ele_AK8200' : h_LHE_HT_1250_1500_ele_AK8200,
    'h_LHE_HT_1500_up_ele_AK8200' : h_LHE_HT_1500_up_ele_AK8200,
    'h_LHE_HT_0_500_ele_AK8400' : h_LHE_HT_0_500_ele_AK8400,
    'h_LHE_HT_500_750_ele_AK8400' : h_LHE_HT_500_750_ele_AK8400,
    'h_LHE_HT_750_900_ele_AK8400' : h_LHE_HT_750_900_ele_AK8400,
    'h_LHE_HT_900_1250_ele_AK8400' : h_LHE_HT_900_1250_ele_AK8400,
    'h_LHE_HT_1250_1500_ele_AK8400' : h_LHE_HT_1250_1500_ele_AK8400,
    'h_LHE_HT_1500_up_ele_AK8400' : h_LHE_HT_1500_up_ele_AK8400,
    'h_LHE_HT_0_500_muon_withoutAK8' : h_LHE_HT_0_500_muon_withoutAK8,
    'h_LHE_HT_500_750_muon_withoutAK8' : h_LHE_HT_500_750_muon_withoutAK8,
    'h_LHE_HT_750_900_muon_withoutAK8' : h_LHE_HT_750_900_muon_withoutAK8,
    'h_LHE_HT_900_1250_muon_withoutAK8' : h_LHE_HT_900_1250_muon_withoutAK8,
    'h_LHE_HT_1250_1500_muon_withoutAK8' : h_LHE_HT_1250_1500_muon_withoutAK8,
    'h_LHE_HT_1500_up_muon_withoutAK8' : h_LHE_HT_1500_up_muon_withoutAK8,
    'h_LHE_HT_0_500_muon_AK8200' : h_LHE_HT_0_500_muon_AK8200,
    'h_LHE_HT_500_750_muon_AK8200' : h_LHE_HT_500_750_muon_AK8200,
    'h_LHE_HT_750_900_muon_AK8200' : h_LHE_HT_750_900_muon_AK8200,
    'h_LHE_HT_900_1250_muon_AK8200' : h_LHE_HT_900_1250_muon_AK8200,
    'h_LHE_HT_1250_1500_muon_AK8200' : h_LHE_HT_1250_1500_muon_AK8200,
    'h_LHE_HT_1500_up_muon_AK8200' : h_LHE_HT_1500_up_muon_AK8200,
    'h_LHE_HT_0_500_muon_AK8400' : h_LHE_HT_0_500_muon_AK8400,
    'h_LHE_HT_500_750_muon_AK8400' : h_LHE_HT_500_750_muon_AK8400,
    'h_LHE_HT_750_900_muon_AK8400' : h_LHE_HT_750_900_muon_AK8400,
    'h_LHE_HT_900_1250_muon_AK8400' : h_LHE_HT_900_1250_muon_AK8400,
    'h_LHE_HT_1250_1500_muon_AK8400' : h_LHE_HT_1250_1500_muon_AK8400,
    'h_LHE_HT_1500_up_muon_AK8400' : h_LHE_HT_1500_up_muon_AK8400,
    'h_leading_jet_pt_electron' : h_leading_jet_pt_electron,
    'h_second_leading_jet_pt_electron' : h_second_leading_jet_pt_electron,
    'h_leading_jet_pt_muon' : h_leading_jet_pt_muon,
    'h_second_leading_jet_pt_muon' : h_second_leading_jet_pt_muon
    
    
    
}
    
    for entry in tree:
        process_event(entry, histograms, relevant_pdgIds)
    
    

    
    file.Close()
    
    return histograms


all_histograms = {}
output_file = ROOT.TFile("output_histograms.root", "RECREATE")

    
path = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/nano_files/1j1l_NoHT/"
root_files = [f for f in os.listdir(path) if f.endswith('.root')]
root_files = root_files[:2]

for root_file in root_files:
    full_path = os.path.join(path, root_file)
    histograms = analyze(full_path)
    
    for name, hist in histograms.items():
        if name in all_histograms:
            all_histograms[name].Add(hist)
        else:
            all_histograms[name] = hist.Clone(name)
            all_histograms[name].SetDirectory(output_file) 

output_file.cd()
for name, hist in all_histograms.items():
    hist.Write()

output_file.Close()
    
print("Total number of events:", totalEvents)
