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
bins = [20,1000,3000]
vartitle = "m_{X} (GeV)"
sigregcut = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&(jet1pmass<135&jet1pmass>105)&jet1tau21<0.75&jet2tau21<0.75&(jet1bbtag>-0.3&jet2bbtag>-0.3))"
lumi =2100.
generatedEvents =50000.
background = TFile("hh_13_TeV.root")
UD = ['Up','Down']

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


	background.cd()
	qcd_integral = QCD.Integral()

	qcd =QCD
	qcd_up = QCD_CMS_scale_13TeVUp
	qcd_down = QCD_CMS_scale_13TeVDown
	data = data_obs
	output_file.cd()
        hh.cd()
	for bin in range(0,bins[0]):
            for Q in UD:
                qcd_syst =TH1F("%s_bin%s%s"%("QCD_CMS_scale_13TeV",bin,Q),"",bins[0], bins[1], bins[2]) 
                if Q == 'Up':
                        qcd_syst.SetBinContent(bin+1,qcd_up.GetBinContent(bin+1))
                if Q == 'Down':
                        qcd_syst.SetBinContent(bin+1,qcd_down.GetBinContent(bin+1))
		qcd_syst.Write()
		


        qcd.Write()
	qcd_up.Write()
	qcd_down.Write()
	Signal_mX.Write()
	data.Write()
	hh.Write()
	output_file.Write()
	output_file.Close()

	

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
       # text_file.write("CMS_scale_13TeV shape                           -       1.000\n")
	for bin in range(0,bins[0]):
		text_file.write("CMS_scale_13TeV_bin%s shape                           -       1.000\n"%(bin))


	text_file.close()
