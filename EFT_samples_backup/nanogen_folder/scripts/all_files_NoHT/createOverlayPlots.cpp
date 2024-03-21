#include <TFile.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TStyle.h>

void createOverlayPlots() {
    TFile *file = new TFile("output_histograms.root");

    TH1F *h_ele_LHE_HT_before = (TH1F*)file->Get("h_ele_LHE_HT_before");
    TH1F *h_ele_LHE_HT_after_met_cut = (TH1F*)file->Get("h_ele_LHE_HT_after_met_cut");

    if (!h_ele_LHE_HT_before || !h_ele_LHE_HT_after_met_cut) {
        std::cout << "Histograms not found in file!" << std::endl;
        return;
    }

    if (h_ele_LHE_HT_before->Integral() != 0)
        h_ele_LHE_HT_before->Scale(1.0 / h_ele_LHE_HT_before->Integral());
    if (h_ele_LHE_HT_after_met_cut->Integral() != 0)
        h_ele_LHE_HT_after_met_cut->Scale(1.0 / h_ele_LHE_HT_after_met_cut->Integral());

    TCanvas *c = new TCanvas("c", "Overlay Plots", 800, 600);

    h_ele_LHE_HT_before->SetLineColor(kRed);
    h_ele_LHE_HT_after_met_cut->SetLineColor(kBlue);

    h_ele_LHE_HT_before->SetTitle("LHE_HT Distribution Before Selections; HT (GeV); Normalized Events");
    h_ele_LHE_HT_after_met_cut->SetTitle("LHE_HT Distribution After High pT Selections; HT (GeV); Normalized Events");

    h_ele_LHE_HT_before->Draw("HIST");

    h_ele_LHE_HT_after_met_cut->Draw("HIST SAME");

    TLegend *leg = new TLegend(0.7, 0.7, 0.9, 0.9);
    leg->AddEntry(h_ele_LHE_HT_before, "Before Cut", "l");
    leg->AddEntry(h_ele_LHE_HT_after_met_cut, "After Cut", "l");
    leg->Draw();

    c->SaveAs("overlay_plot_ele.png");

    delete c;
    file->Close();
    delete file;
}

int main() {
    createOverlayPlots();
    return 0;
}
