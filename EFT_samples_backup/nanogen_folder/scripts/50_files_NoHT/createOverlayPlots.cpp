#include <TFile.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TStyle.h>

void createOverlayPlots() {
    TFile *file = new TFile("output_histograms.root");

    TH1F *h_muon_LHE_HT_before = (TH1F*)file->Get("h_muon_LHE_HT_before");
    TH1F *h_muon_LHE_HT_after_met_cut = (TH1F*)file->Get("h_muon_LHE_HT_after_met_cut");

    if (!h_muon_LHE_HT_before || !h_muon_LHE_HT_after_met_cut) {
        std::cout << "Histograms not found in file!" << std::endl;
        return;
    }

    if (h_muon_LHE_HT_before->Integral() != 0)
        h_muon_LHE_HT_before->Scale(1.0 / h_muon_LHE_HT_before->Integral());
    if (h_muon_LHE_HT_after_met_cut->Integral() != 0)
        h_muon_LHE_HT_after_met_cut->Scale(1.0 / h_muon_LHE_HT_after_met_cut->Integral());

    TCanvas *c = new TCanvas("c", "Overlay Plots", 800, 600);

    h_muon_LHE_HT_before->SetLineColor(kRed);
    h_muon_LHE_HT_after_met_cut->SetLineColor(kBlue);

    h_muon_LHE_HT_before->SetTitle("LHE_HT Distribution Before Smuonctions; HT (GeV); Normalized Events");
    h_muon_LHE_HT_after_met_cut->SetTitle("LHE_HT Distribution After High pT Smuonctions; HT (GeV); Normalized Events");

    h_muon_LHE_HT_before->Draw("HIST");

    h_muon_LHE_HT_after_met_cut->Draw("HIST SAME");

    TLegend *leg = new TLegend(0.7, 0.7, 0.9, 0.9);
    leg->AddEntry(h_muon_LHE_HT_before, "Before Cut", "l");
    leg->AddEntry(h_muon_LHE_HT_after_met_cut, "After Cut", "l");
    leg->Draw();

    c->SaveAs("overlay_plot_muon.png");

    delete c;
    file->Close();
    delete file;
}

int main() {
    createOverlayPlots();
    return 0;
}
