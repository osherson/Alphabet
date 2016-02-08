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


vartitle = "m_{X} (GeV)"
sigregcut = "(dijetmass>800&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>100)&jet1tau21<0.6&jet2tau21<0.6&(jet1bbtag>0.4&jet2bbtag>0.4)&triggerpass>0)"
lumi =2190.
background = TFile("../QCD_HT_2190_twiki.root")
SF_tau21=1.031
gSystem.Load("DrawFunctions_C.so")

mc_norm=1./(12509.4417393/10350.0)


for m in mass:

	output_file = TFile("hh_mX_%s_13TeV.root"%(m),"RECREATE")

	Signal_mX = TH1F("Signal_mX_%s"%(m), "", 3000, 0., 3000.)

	signal_file= TFile("../Grav_%s_0.root"%(m))
	htrig = signal_file.Get("ct")
	generatedEvents =htrig.GetEntries()
	print(generatedEvents)
	tree = signal_file.Get("myTree") 
	writeplot(tree, Signal_mX, VAR, sigregcut, "weight2( myTree.nTrueInt)")
	Signal_mX.Scale(lumi*SF_tau21*SF_tau21/generatedEvents)
	

        signal_integral = Signal_mX.Integral()
	print(signal_integral) 
	output_file.cd()
	Signal_mX.Write()
	output_file.Write()
	output_file.Close()

output_file2 = TFile("hh_mX_background_13TeV.root","RECREATE")
Background_mX = TH1F("Background_mX", "", 3000, 0., 3000.)
background.cd()
btree = background.Get("myTree")
writeplot(btree, Background_mX, VAR, sigregcut, "1")#weight2( myTree.nTrueInt)")
Background_mX.Scale(mc_norm)
output_file2.cd()
Background_mX.Write()
output_file2.Write()
output_file2.Close()


