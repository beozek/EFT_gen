import ROOT
from DataFormats.FWLite import Events

def count_events(root_file):
    events = Events(root_file)

    num_events = 0
    for i in events:
        num_events += 1
    print("Total number of events in:", num_events)
    
    return num_events

count_events("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/root_files/0000/GEN_LO_01j_102X_14.root")
