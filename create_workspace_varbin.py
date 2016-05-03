import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy


import Alphabet_Header
from Alphabet_Header import *
import Plotting_Header
from Plotting_Header import *




mass=[1000,1200,1600,1800,2000,2500,3000]
VAR = "dijetmass"

#variable bin from dijet analysis 788 838 
binBoundaries = [800, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687,
        1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019 ]#, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509,


vartitle = "m_{X} (GeV)"
sigregcut = "triggerpass>0&dijetmass>800&jet1tau21<0.6&jet2tau21<0.6&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>100)&(jet1bbtag>0.4&jet2bbtag>0.4)"
lumi =2190.
background = TFile("Hbb_output.root")
UD = ['Up','Down']
SF_tau21=1.031
SF_bbtag=0.808
gSystem.Load("DrawFunctions_h.so")

mc_norm=1./(12509.4417393/10350.0)
QCD.Scale(mc_norm*SF_tau21*SF_tau21*SF_bbtag*SF_bbtag)
QCD_Antitag.Scale(mc_norm*SF_tau21*SF_tau21*SF_bbtag*SF_bbtag)
QCD_CMS_scale_13TeVUp.Scale(mc_norm*SF_tau21*SF_tau21*SF_bbtag*SF_bbtag)
QCD_CMS_scale_13TeVDown.Scale(mc_norm*SF_tau21*SF_tau21*SF_bbtag*SF_bbtag)
data_obs.Scale(mc_norm*SF_tau21*SF_tau21*SF_bbtag*SF_bbtag)


for m in mass:

	output_file = TFile("datacard/hh_mX_%s_13TeV.root"%(m),"RECREATE")
	hh=output_file.mkdir("hh")
	hh.cd()

	Signal_mX = TH1F("Signal_mX_%s"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
	print(m)

	signal_file= TFile("../Grav_%s_0.root"%(m))
	htrig = signal_file.Get("ct")
	generatedEvents =htrig.GetEntries()
	print(generatedEvents)
	tree = signal_file.Get("myTree") 
	writeplot(tree, Signal_mX, VAR, sigregcut, "weight2(nTrueInt)")
	print(Signal_mX.Integral())
	Signal_mX.Scale(lumi*0.01*SF_tau21*SF_tau21*SF_bbtag*SF_bbtag/generatedEvents)
	
	

        signal_integral = Signal_mX.Integral()
	print(signal_integral) 
        background.cd() 	
	qcd_integral = QCD.Integral()

	qcd =QCD
	qcd_antitag = QCD_Antitag
	qcd_up = QCD_CMS_scale_13TeVUp
	qcd_down = QCD_CMS_scale_13TeVDown
	data = data_obs
	output_file.cd()
        hh.cd()
	qcd_stat_up =TH1F("qcd_stat_up","",len(binBoundaries)-1, array('d',binBoundaries))
        qcd_stat_down =TH1F("qcd_stat_down","",len(binBoundaries)-1, array('d',binBoundaries))
	
	for bin in range(0,len(binBoundaries)-1):
            for Q in UD:
                qcd_syst =TH1F("%s_bin%s%s"%("QCD_CMS_stat_13TeV",bin,Q),"",len(binBoundaries)-1, array('d',binBoundaries))
		bin_stat = qcd.GetBinContent(bin+1)
		bin_at = qcd_antitag.GetBinContent(bin+1)
		if bin_at < 1 and bin_at >0:  
			bin_at=1.
		
                if Q == 'Up':
			if bin_at >0 :
			       qcd_stat_up.SetBinContent(bin+1,bin_stat+qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)	
                               qcd_syst.SetBinContent(bin+1,bin_stat+qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
			else : 
				qcd_syst.SetBinContent(bin+1,bin_stat)
				qcd_stat_up.SetBinContent(bin+1,bin_stat)
				
                if Q == 'Down':
			if bin_at >0 :
				if ( bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat >0 ):
                        		qcd_syst.SetBinContent(bin+1,bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
					qcd_stat_down.SetBinContent(bin+1,bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
				else :
					qcd_syst.SetBinContent(bin+1, 0.001)
					qcd_stat_down.SetBinContent(bin+1, 0.001)
			else : 	
				qcd_syst.SetBinContent(bin+1,bin_stat)
				qcd_stat_down.SetBinContent(bin+1,bin_stat)
		qcd_syst.Write()
		


        qcd.Write()
	qcd_up.Write()
	qcd_down.Write()
	qcd_stat_up.Write()
	qcd_stat_down.Write()
	Signal_mX.Write()
	data.Write()
	hh.Write()
	output_file.Write()
	#output_file.Close()

	

	text_file = open("datacard/hh_mX_%s_13TeV.txt"%(m), "w")


	text_file.write("max    1     number of categories\n")
        text_file.write("jmax   1     number of samples minus one\n")
        text_file.write("kmax    *     number of nuisance parameters\n")
        text_file.write("-------------------------------------------------------------------------------\n")
        text_file.write("shapes * * hh_mX_%s_13TeV.root hh/$PROCESS hh/$PROCESS_$SYSTEMATIC\n"%(m))
        text_file.write("-------------------------------------------------------------------------------\n")
        text_file.write("bin                                            hh4b\n")
        text_file.write("observation                                    -1\n")
        text_file.write("-------------------------------------------------------------------------------\n")
        text_file.write("bin                                             hh4b            hh4b\n")
        text_file.write("process                                          0      1\n")
        text_file.write("process                                         Signal_mX_%s  QCD\n"%(m))
        text_file.write("rate                                            %f  %f\n"%(signal_integral,qcd_integral))
        text_file.write("-------------------------------------------------------------------------------\n")
	text_file.write("lumi_13TeV lnN                          1.046       -\n")	
        text_file.write("CMS_eff_tau21_sf lnN                    1.25       -\n") #(0.129/1.031)*(2) 
        text_file.write("CMS_pileup lnN                    1.02       -\n")  
        text_file.write("CMS_eff_Htag_sf lnN                    1.1       -\n")   
        text_file.write("CMS_JEC lnN 		     1.02        -\n") #to be fixed	
	text_file.write("CMS_bbtag_sf lnN                 1.23        -\n") #to be fixed  
        text_file.write("CMS_JER lnN                    1.02        -\n")
        text_file.write("CMS_scale_13TeV shapeN2                           -       1.000\n")
	text_file.write("CMS_PDF_Scales lnN   1.02 -       \n")

	for bin in range(0,len(binBoundaries)-1):
		text_file.write("CMS_stat_13TeV_bin%s shapeN2                           -       1.000\n"%(bin))


	text_file.close()


	qcd_up.SetLineColor(kBlack)
        qcd_down.SetLineColor(kBlack)
	qcd_up.SetLineStyle(2)
	qcd_down.SetLineStyle(2)
  	qcd_stat_up.SetLineColor(kAzure+1)
        qcd_stat_down.SetLineColor(kAzure+1)
        qcd_stat_up.SetLineStyle(2)
        qcd_stat_down.SetLineStyle(2)	
	qcd.SetLineColor(kBlack)
	qcd.SetFillColor(kPink+3)



	data.SetStats(0)
	data.Sumw2()
	data.SetLineColor(1)
	data.SetFillColor(0)
	data.SetMarkerColor(1)
	data.SetMarkerStyle(20)
	#qcd.GetYaxis().SetTitle("events / "+str((bins[2]-bins[1])/bins[0])+" GeV")
	qcd.GetXaxis().SetTitle(vartitle)

	leg2 = TLegend(0.6,0.6,0.89,0.89)
	leg2.SetLineColor(0)
	leg2.SetFillColor(0)
	leg2.AddEntry(data, "QCD in SR", "PL")
	leg2.AddEntry(qcd, "QCD prediction", "F")
	leg2.AddEntry(qcd_up, "transfer function uncertainty", "F")
	leg2.AddEntry(qcd_stat_up, "statistical uncertainty", "F")


	FindAndSetMax([qcd,qcd_up,qcd_stat_up,data])
	C3 = TCanvas("C3", "", 800, 600)
	C3.cd()
	qcd.Draw("Hist")
	data.Draw("same E0")
	qcd_up.Draw("same")
	qcd_down.Draw("same")
	qcd_stat_up.Draw("same")
        qcd_stat_down.Draw("same")
	leg2.Draw()
	if m< 1200 :
		C3.Print("split_unc.pdf")

	output_file.Close()

