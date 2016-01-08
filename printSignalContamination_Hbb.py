# TEST AREA
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

# Our functions:
import Alphabet_Header
from Alphabet_Header import *
import Plotting_Header
from Plotting_Header import *
import Converters
from Converters import *
import Distribution_Header
from Distribution_Header import *
import Alphabet
from Alphabet import *



mass=[1000,1200,1600,3000]
VAR = "dijetmass"
bins = [20,1000,3000]
vartitle = "m_{X} (GeV)"
hbins = [[50,70],[70,90],[130,150],[150,200]]

sigregcut = "(dijetmass>1000&&jet2tau21<0.6&jet1tau21<0.6&&jet1bbtag>-0.2)"
lumi =2190.
generatedEvents =50000.

bkg_file= TFile("../qcd_all.root")
treeb = bkg_file.Get("myTree")


SignalPass_mX = TH1F("SignalPass_mX", "", bins[0], bins[1], bins[2])
SignalFail_mX = TH1F("SignalFail_mX", "", bins[0], bins[1], bins[2])
BkgPass_mX = TH1F("BkgPass_mX", "", bins[0], bins[1], bins[2])
BkgFail_mX = TH1F("BkgFail_mX", "", bins[0], bins[1], bins[2])

for m in mass:
   
   signal_file= TFile("../BG_%s_v6p2_0.root"%(m))
   print("================ MASS is %s (GeV) ==============="%m)	
   tree = signal_file.Get("myTree")


   for l in hbins:

#	SignalPass_mX = TH1F("SignalPass_mX", "", bins[0], bins[1], bins[2])
 #       SignalFail_mX = TH1F("SignalFail_mX", "", bins[0], bins[1], bins[2])
 #       BkgPass_mX = TH1F("BkgPass_mX", "", bins[0], bins[1], bins[2])
 #       BkgFail_mX = TH1F("BkgFail_mX", "", bins[0], bins[1], bins[2])


	cut_pass = sigregcut + "&&jet2bbtag>-0.2" + "&& jet1pmass>%s && jet1pmass<%s && jet2pmass>%s && jet2pmass<%s"%(l[0],l[1],l[0],l[1])
	cut_fail = sigregcut + "&&jet2bbtag<-0.2" + "&& jet1pmass>%s &&jet1pmass<%s && jet2pmass>%s && jet2pmass<%s"%(l[0],l[1],l[0],l[1])
	 
         
        writeplot(tree, SignalPass_mX, VAR, cut_pass, "(1.0)")
        writeplot(tree, SignalFail_mX, VAR, cut_fail, "(1.0)")
        writeplot(treeb, BkgPass_mX, VAR, cut_pass, "(1.0)")
        writeplot(treeb, BkgFail_mX, VAR, cut_fail, "(1.0)")

        SignalPass_mX.Scale(lumi/generatedEvents)
	SignalFail_mX.Scale(lumi/generatedEvents)	

	print "pass and mass bin : %s-%s"%(l[0],l[1])
	print "signal contamination is:%s "%(SignalPass_mX.Integral()/BkgPass_mX.Integral())
	print "signal is %s, background is %s"%(SignalPass_mX.Integral(),BkgPass_mX.Integral())
 	print "fail and mass bin : %s-%s"%(l[0],l[1])
        print "signal contamination is:%s "%(SignalFail_mX.Integral()/BkgFail_mX.Integral())
	print "signal is %s, background is %s"%(SignalFail_mX.Integral(),BkgFail_mX.Integral())
	






