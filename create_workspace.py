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


mass=[1000,1200,1600,2000,3000]
VAR = "dijetmass"
bins = [24,800,3000]
vartitle = "m_{X} (GeV)"
sigregcut = "(dijetmass>800&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>90)&jet1tau21<0.6&jet2tau21<0.6&(jet1bbtag>0.4&jet2bbtag>0.4))"
lumi =2190.
generatedEvents =50000.
background = TFile("Hbb_output.root")
UD = ['Up','Down']
background.cd()

print("rescaling from 3 to 2/fb ############ warning ############")

QCD.Scale(lumi/3000.)
QCD_Antitag.Scale(lumi/3000.)
QCD_CMS_scale_13TeVUp.Scale(lumi/3000.)
QCD_CMS_scale_13TeVDown.Scale(lumi/3000.)
data_obs.Scale(lumi/3000.)


for m in mass:

	output_file = TFile("datacard/hh_mX_%s_13TeV.root"%(m),"RECREATE")
	hh=output_file.mkdir("hh")
	hh.cd()

	Signal_mX = TH1F("Signal_mX_%s"%(m), "", bins[0], bins[1], bins[2])


	signal_file= TFile("../BG_%s_v6p2_0.root"%(m))
	tree = signal_file.Get("myTree") 
	writeplot(tree, Signal_mX, VAR, sigregcut, "(1.0)")
	Signal_mX.Scale(lumi/generatedEvents)
	

        signal_integral = Signal_mX.Integral()

	qcd_integral = QCD.Integral()

	qcd =QCD
	qcd_antitag = QCD_Antitag
	qcd_up = QCD_CMS_scale_13TeVUp
	qcd_down = QCD_CMS_scale_13TeVDown
	data = data_obs
	output_file.cd()
        hh.cd()
	qcd_stat_up =TH1F("qcd_stat_up","",bins[0], bins[1], bins[2])
        qcd_stat_down =TH1F("qcd_stat_down","",bins[0], bins[1], bins[2])
	
	for bin in range(0,bins[0]):
            for Q in UD:
                qcd_syst =TH1F("%s_bin%s%s"%("QCD_CMS_stat_13TeV",bin,Q),"",bins[0], bins[1], bins[2]) 
                if Q == 'Up':
			if qcd.GetBinContent(bin+1) >0 :
			       qcd_stat_up.SetBinContent(bin+1,qcd.GetBinContent(bin+1)+qcd_antitag.GetBinError(bin+1)/qcd.GetBinContent(bin+1))	
                               qcd_syst.SetBinContent(bin+1,qcd.GetBinContent(bin+1)+qcd_antitag.GetBinError(bin+1)/qcd.GetBinContent(bin+1))
			else : 
				qcd_syst.SetBinContent(bin+1,qcd.GetBinContent(bin+1))
				qcd_stat_up.SetBinContent(bin+1,qcd.GetBinContent(bin+1))
				
                if Q == 'Down':
			if qcd.GetBinContent(bin+1) >0 :
				if ( qcd.GetBinContent(bin+1)-qcd_antitag.GetBinError(bin+1)/qcd.GetBinContent(bin+1) >0 ):
                        		qcd_syst.SetBinContent(bin+1,qcd.GetBinContent(bin+1)-qcd_antitag.GetBinError(bin+1)/qcd.GetBinContent(bin+1))
					qcd_stat_down.SetBinContent(bin+1,qcd.GetBinContent(bin+1)-qcd_antitag.GetBinError(bin+1)/qcd.GetBinContent(bin+1))
				else :
					qcd_syst.SetBinContent(bin+1, 0.001)
					qcd_stat_down.SetBinContent(bin+1, 0.001)
			else : 	
				qcd_syst.SetBinContent(bin+1,qcd.GetBinContent(bin+1))
				qcd_stat_down.SetBinContent(bin+1,qcd.GetBinContent(bin+1))
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
	text_file.write("lumi_13TeV lnN                          1.046       1.046\n")	
        text_file.write("CMS_scale_13TeV shapeN2                           -       1.000\n")
	for bin in range(0,bins[0]):
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
	qcd.GetYaxis().SetTitle("events / "+str((bins[2]-bins[1])/bins[0])+" GeV")
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

