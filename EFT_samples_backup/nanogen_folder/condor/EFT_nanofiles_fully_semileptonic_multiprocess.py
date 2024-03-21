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

h_bquark_pt = ROOT.TH1F("h_bquark_pt", "b-quark pT Before Cuts ;pT (GeV);Events", 150, 0, 1000)
h_bquark_eta = ROOT.TH1F("h_bquark_eta", "b-quark #eta Before Cuts ;#eta;Events", 100, -5, 5)
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
    
    leptons = []
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
    
    events_after_LHE_HT_cut = 0
    events_after_lepton_selection = 0

    top_pt_cut1 = 200
    top_pt_cut2 = 400
    
    met_vector = ROOT.TLorentzVector() 
    
    
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
        if abs(pdgId) in relevant_pdgIds and is_last_copy(statusFlags): 
            if abs(pdgId) == 6: 
                
                top_4vec = ROOT.TLorentzVector()
                top_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
                tops.append(top_4vec)
                w_daughter = None
                b_daughter = None
                last_copy_top_decays.append((pt, eta, phi))
                
                # Checking if the j-th particle is a daughter of the i-th particle (top or anti-top quark)
                for j in range(entry.nGenPart):
                    if entry.GenPart_genPartIdxMother[j] == i and abs(entry.GenPart_pdgId[j]) in [24, 5]:
                        last_copy_decays.append((pt, eta, phi, pdgId, i)) # append as a tuple

                        daughter_pdgId = entry.GenPart_pdgId[j]
                        if daughter_pdgId != 6 and daughter_pdgId != -6:
                            if abs(daughter_pdgId) == 24:
                                w_4vec = ROOT.TLorentzVector()
                                w_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
                                w_bosons.append(w_4vec)
                                w_daughter = j
                            elif abs(daughter_pdgId) == 5:
                                b_daughter = j
                                b_4vec = ROOT.TLorentzVector()
                                b_4vec.SetPtEtaPhiM(pt, eta, phi, mass)
                                b_quarks.append((b_4vec, j))
                
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
                            leptons.append((lepton_pt, lepton_eta, lepton_phi, lepton_pdg))
                            leptonic_decay = True
                            if abs(lepton_pdg) == 11:
                                channel = "electron"
                            elif abs(lepton_pdg) == 13:
                                channel = "muon"
                        
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
                        histograms['h_bquark_pt'].Fill(b_vector.Pt())
                        histograms['h_bquark_eta'].Fill(b_vector.Eta())
                       
            

    is_electron_channel = any(abs(pdgId) == 11 for lepton_pt, lepton_eta, Lepton_phi, lepton_pdgId in leptons)
    is_muon_channel = any(abs(pdgId) == 13 for lepton_pt, lepton_eta, Lepton_phi, lepton_pdgId in leptons)
    channel = "electron" if is_electron_channel else "muon" if is_muon_channel else "other"

    passed_lepton_cut, passed_jet_cut, passed_met_cut, channel, top_pt_pass1, top_pt_pass2 = passes_selection_criteria(entry, leptons, tops, hadronic_top_pt, channel, top_pt_cut1, top_pt_cut2, b_quarks)
        
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
                                
    for i in range(entry.nGenPart):
        pdgId = entry.GenPart_pdgId[i]
        pt = entry.GenPart_pt[i]
        eta = entry.GenPart_eta[i]
        phi = entry.GenPart_phi[i]
        mass = entry.GenPart_mass[i]
        mother_idx = entry.GenPart_genPartIdxMother[i]
        status = entry.GenPart_status[i]
        statusFlags = entry.GenPart_statusFlags[i]
        
        met_vector_after200 = ROOT.TLorentzVector()
        met_vector_after400 = ROOT.TLorentzVector()
                                   
        for top_4vec in tops:
            if pdgId == 6:
                top_count += 1
                histograms['h_topPt'].Fill(pt)
                if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                    histograms['h_topPt_aftercut200'].Fill(pt)
                    top_count_aftercut200 += 1
                if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                    histograms['h_topPt_aftercut400'].Fill(pt)
                    top_count_aftercut400 += 1
                if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                    histograms['h_topPt_aftercut200'].Fill(pt)
                    top_count_aftercut200 += 1
                if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                    histograms['h_topPt_aftercut400'].Fill(pt)
                    top_count_aftercut400 += 1
                
            elif pdgId == -6:
                antitop_count += 1
                histograms['h_antitopPt'].Fill(pt)
                if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                    histograms['h_antitopPt_aftercut200'].Fill(pt)
                    antitop_count_aftercut200 += 1
                if channel == "electron" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                    histograms['h_antitopPt_aftercut400'].Fill(pt)
                    antitop_count_aftercut400 += 1
                if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass1:
                    histograms['h_antitopPt_aftercut200'].Fill(pt)
                    antitop_count_aftercut200 += 1
                if channel == "muon" and passed_lepton_cut and passed_jet_cut and passed_met_cut and top_pt_pass2:
                    histograms['h_antitopPt_aftercut400'].Fill(pt)
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
        histograms["h_ttbarMass_vs_HT"].Fill(LHE_HT, ttbar.M())

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
        
        channel = "electron" if is_electron_channel else "muon" if is_muon_channel else "other"
        if channel == "electron":
            jet_pt_cut = 40  
        elif channel == "muon":
            jet_pt_cut = 50  
        else:
            jet_pt_cut = 50
        leading_jet, second_leading_jet = select_leading_jets(entry, jet_pt_cut)
        
        if leading_jet:
            histograms['h_leading_jet_pt'].Fill(leading_jet[0]) #leading_jet[0] contains the pt of the leading jet
        if second_leading_jet:
            histograms['h_second_leading_jet_pt'].Fill(second_leading_jet[0])
            
        pass_criteria = passes_selection_criteria(entry, leptons, tops, hadronic_top_pt, channel, top_pt_cut1, top_pt_cut2, b_quarks)
    
 
    return leptons, tops, hadronic_top_pt, b_quarks

h_both_decays.Fill(0, both_decays_counter)


def select_leading_jets(entry, jet_pt_cut):
    leading_jet = None
    second_leading_jet = None
    highest_pt_jet = 0 
    second_high_pt=0
    jet_1=0
    jet_2=0
    for i in range(entry.nGenJet):
        jet_pt = entry.GenJet_pt[i]
        jet_eta = entry.GenJet_eta[i]
        
        if jet_pt > jet_pt_cut and abs(jet_eta) < 2.4:
            if leading_jet is None or jet_pt > leading_jet[0]:
                second_leading_jet = leading_jet
                leading_jet = (jet_pt, jet_eta, i, entry.GenJet_partonFlavour[i])
            elif second_leading_jet is None or (jet_pt > second_leading_jet[0] and jet_pt < leading_jet[0]):
                second_leading_jet = (jet_pt, jet_eta, i, entry.GenJet_partonFlavour[i])


    return leading_jet, second_leading_jet  
    
def check_b_jet_from_top(leading_jet, second_leading_jet):

    # Check if PDG ID of either leading jet is ±5 (b or anti-b-quark)
    return abs(leading_jet[3]) == 5 or abs(second_leading_jet[3]) == 5


def find_leading_b_quark(b_quarks):
    leading_b_quark = None
    for b_quark in b_quarks:
        pt, eta, phi, idx = b_quark[0].Pt(), b_quark[0].Eta(), b_quark[0].Phi(), b_quark[1]
        if pt > 30:
            if leading_b_quark is None or pt > leading_b_quark[0]:
                leading_b_quark = b_quark
    return leading_b_quark


def passes_selection_criteria(entry, leptons, tops, hadronic_top_pt, channel, top_pt_cut1, top_pt_cut2, b_quarks):

    met_cut_electron = 60
    met_cut_muon = 70
    met_cut = 0
    
    met_pt = entry.GenMET_pt
    
    top_pt_pass1 = False
    top_pt_pass2 = False
    
    
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
        return False, False, False, "other", False, False
    
        
 #Jet selection with last copy matching    

    # 1) identify first and second leading jets
    # b_quarks = find_b_quarks_from_top(entry)
    leading_jet, second_leading_jet = select_leading_jets(entry, jet_pt_cut)
    # if leading_jet is not None:
        # print("Leading Jet from passes_selection_criteria: PT = {}, ETA = {}, Index = {}, pdgId = {}".format(*leading_jet))
    # if second_leading_jet is not None:
        # print("Second Leading Jet from passes_selection_criteria: PT = {}, ETA = {}, Index = {}, pdgId = {}".format(*second_leading_jet))


    # 2) check if either leading jet is a b-quark from top
    b_jet_in_leading = False
    if leading_jet is not None and second_leading_jet is not None:
            b_jet_in_leading = check_b_jet_from_top(leading_jet, second_leading_jet)
            # print("b_jet_in_leading:", b_jet_in_leading)
    
    # Find the leading b-quark and check its pT
    leading_b_quark = find_leading_b_quark(b_quarks)
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

    
    jet_count = sum(1 for i in range(entry.nGenJet) if entry.GenJet_pt[i] > jet_pt_cut)
    passed_lepton_cut = sum(1 for lepton in leptons if lepton[0] > lepton_pt_cut and abs(lepton[1]) < lepton_eta_cut) > 0
    passed_jet_cut = jet_count > 0
    passed_met_cut = met_pt > met_cut
    

    return passed_lepton_cut, passed_jet_cut, passed_met_cut, channel, top_pt_pass1, top_pt_pass2



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
    'h_bquark_pt': h_bquark_pt,
    'h_bquark_eta': h_bquark_eta,
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
    'h_LHE_HT_1500_up_muon_AK8400' : h_LHE_HT_1500_up_muon_AK8400
    
    
    
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
    output_dir = "/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_all"
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
# createCanvas(h_bquark_pt, "b-quark pT Before Cuts", "bquarkPtDistribution.png", True)
# createCanvas(h_bquark_eta, "b-quark Eta Before Cuts", "bquarkEtaDistribution.png")
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
