#include <TFile.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TStyle.h>

void createOverlayPlots() {
    TFile *file = new TFile("/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/plots_all/hadd_all/output.root");

    TH1F *h_ele_LHE_HT_before = (TH1F*)file->Get("h_ele_LHE_HT_before");
    TH1F *h_ele_LHE_HT_after_toppt200_cut = (TH1F*)file->Get("h_ele_LHE_HT_after_toppt200_cut");
    TH1F *h_ele_LHE_HT_after_toppt400_cut = (TH1F*)file->Get("h_ele_LHE_HT_after_toppt400_cut");

    if (!h_ele_LHE_HT_before || !h_ele_LHE_HT_after_toppt400_cut) {
        std::cout << "Histograms not found in file!" << std::endl;
        return;
    }

    if (h_ele_LHE_HT_before->Integral() != 0)
        h_ele_LHE_HT_before->Scale(1.0 / h_ele_LHE_HT_before->Integral());
    if (h_ele_LHE_HT_after_toppt200_cut->Integral() != 0)
        h_ele_LHE_HT_after_toppt200_cut->Scale(1.0 / h_ele_LHE_HT_after_toppt200_cut->Integral());
    
    if (h_ele_LHE_HT_after_toppt400_cut->Integral() != 0)
        h_ele_LHE_HT_after_toppt400_cut->Scale(1.0 / h_ele_LHE_HT_after_toppt400_cut->Integral());

    TCanvas *c = new TCanvas("c", "Overlay Plots", 800, 600);

    h_ele_LHE_HT_before->SetLineColor(kRed);
    h_ele_LHE_HT_after_toppt200_cut->SetLineColor(kGreen);
    h_ele_LHE_HT_after_toppt400_cut->SetLineColor(kBlue);

    h_ele_LHE_HT_before->SetTitle("LHE_HT Distribution; HT (GeV); Normalized Events");
    h_ele_LHE_HT_after_toppt200_cut->SetTitle("LHE_HT Distribution After Cuts & TopPt>200 ; HT (GeV); Normalized Events");
    h_ele_LHE_HT_after_toppt400_cut->SetTitle("LHE_HT Distribution After Cuts & TopPt>400; HT (GeV); Normalized Events");

    h_ele_LHE_HT_before->Draw("HIST");

    h_ele_LHE_HT_after_toppt200_cut->Draw("HIST SAME");
    h_ele_LHE_HT_after_toppt400_cut->Draw("HIST SAME");

    TLegend *leg = new TLegend(0.7, 0.7, 0.9, 0.9);
    leg->AddEntry(h_ele_LHE_HT_before, "Before Cut", "l");
    leg->AddEntry(h_ele_LHE_HT_after_toppt200_cut, "After Cut TopPt>200", "l");
    leg->AddEntry(h_ele_LHE_HT_after_toppt400_cut, "After Cut TopPt>400", "l");
    leg->Draw();

    c->SaveAs("overlay_plot_ele_all.png");

    delete c;
    file->Close();
    delete file;
}

int main() {
    createOverlayPlots();
    return 0;
}
