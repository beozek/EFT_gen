import ROOT

from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *

events = Events("/pnfs/desy.de/cms/tier2/store/user/tiroy/TT01j1l_HT800/TT01j1l_HT800/230824_060122/0000/GEN_LO_01j_102X_355.root")

#handle = Handle('std::vector<reco::GenParticle>')
handle = Handle('vector<reco::GenParticle>')
events.to(0)

#events.getByLabel("genParticles", handle)
#events.getByLabel("recoGenParticles", handle)
events.getByLabel("genParticles", handle)
#events.getByLabel(("recoGenParticles",handle))
lhe_product = handle.product()
num=0
for particle in list(lhe_product):
    print(particle.pdgId())
#for pdgid in list(genInfo.pdgId()):
#	print pdgid

#for weight in list(lhe_product.weights()):
    #print weight.id, weight.wgt
 #   if 'ctG' in weight.id:
#	num+=1
#	print weight.id, weight.wgt
 
