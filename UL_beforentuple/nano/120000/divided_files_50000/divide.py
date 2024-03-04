import ROOT

def split_tree(original_file_path, tree_name, entries_per_file):
    original_file = ROOT.TFile.Open(original_file_path, "READ")
    tree = original_file.Get(tree_name)
    
    total_entries = tree.GetEntries()
    num_splits = total_entries // entries_per_file + (1 if total_entries % entries_per_file > 0 else 0)
    
    for i in range(num_splits):
        start_entry = i * entries_per_file
        end_entry = start_entry + entries_per_file if i < num_splits - 1 else total_entries
        
        new_file = ROOT.TFile.Open("split_correct_{}.root".format(i + 1), "RECREATE")
        new_tree = tree.CloneTree(0) 
        
        for j in range(start_entry, end_entry):
            tree.GetEntry(j)
            new_tree.Fill()
        
        new_tree.AutoSave()
        new_file.Close()
    
    original_file.Close()

split_tree("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_beforentuple/nano/120000/0520A050-AF68-EF43-AA5B-5AA77C74ED73.root", "Events", 50000) 




