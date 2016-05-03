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
output_file = TFile("MassPlotFineBins.root","RECREATE")

for m in mass:


	Graviton_cat0 = TH1F("Graviton%s_cat0"%(m), "", 3000, 0., 3000.)
	Graviton_cat1 = TH1F("Graviton%s_cat1"%(m), "", 3000, 0., 3000.)
	Graviton_cat2 = TH1F("Graviton%s_cat2"%(m), "", 3000, 0., 3000.)

	signal_file= TFile("../Grav_%s_0.root"%(m))
	htrig = signal_file.Get("ct")
	generatedEvents =htrig.GetEntries()
	print(generatedEvents)
	tree = signal_file.Get("myTree") 
	writeplot(tree, Graviton_cat0, VAR, sigregcut, "weight2( myTree.nTrueInt)")
#	Graviton_cat0.Scale(lumi*SF_tau21*SF_tau21/generatedEvents)
	writeplot(tree, Graviton_cat1, VAR, sigregcut, "weight2( myTree.nTrueInt)")
 #       Graviton_cat1.Scale(lumi*SF_tau21*SF_tau21/generatedEvents)
	writeplot(tree, Graviton_cat2, VAR, sigregcut, "weight2( myTree.nTrueInt)")
  #      Graviton_cat2.Scale(lumi*SF_tau21*SF_tau21/generatedEvents)
	

        signal_integral = Graviton_cat0.Integral()
	print(signal_integral) 
	output_file.cd()
	Graviton_cat0.Write()
	Graviton_cat1.Write()
	Graviton_cat2.Write()	

QCD_cat0 = TH1F("QCD_cat0", "", 3000, 0., 3000.)
QCD_cat1 = TH1F("QCD_cat1", "", 3000, 0., 3000.)
QCD_cat2 = TH1F("QCD_cat2", "", 3000, 0., 3000.)
background.cd()
btree = background.Get("myTree")
writeplot(btree, QCD_cat0, VAR, sigregcut, "1")#weight2( myTree.nTrueInt)")
writeplot(btree, QCD_cat1, VAR, sigregcut, "1")
writeplot(btree, QCD_cat2, VAR, sigregcut, "1")
QCD_cat0.Scale(mc_norm)
output_file.cd()
QCD_cat0.Write()
QCD_cat1.Write()
QCD_cat2.Write()
output_file.Write()
output_file.Close()


