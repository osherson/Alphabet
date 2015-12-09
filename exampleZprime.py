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

### DEFINE THE DISTRIBUTIONS YOU WANT TO USE:

# DISTRIBUTIONS YOU WANT TO ESTIMATE:

# FORMAT IS:
# dist = ("name", "location of file", "name of tree", "weight (can be more complicated than just a number, see MC example below)")
dataMu = DIST("Mu", "/home/bjr/trees_fixed_2D/SingleMuon_Run2015D_PromptReco-v4_decosa.root", "tree", "(1.0)")
dataEl = DIST("El", "/home/bjr/trees_fixed_2D/SingleElectron_Run2015D_PromptReco-v4_decosa.root", "tree", "(1.0)")
# DISTRIBUTIONS YOU NEED TO SUBTRACT (KNOWN MC CONTRIBUTIONS):
lumi = str(1.5407) # can't forget to scale to lumi!
ttbar = DIST("ttbar", "/home/bjr/trees_fixed_2D/TT_TuneZ2star_13TeV-powheg-pythia6-tauola.root", "tree", "("+lumi+"*weight*2.71828^(-0.0001*(MCantitoppt+MCtoppt)))")
singletop1 = DIST("st1", "/home/bjr/trees_fixed_2D/ST_tW_top_5f_DS_inclusiveDecays.root", "tree", "("+lumi+"*weight)")
singletop2 = DIST("st2", "/home/bjr/trees_fixed_2D/ST_tW_antitop_5f_DS_inclusiveDecays.root", "tree", "("+lumi+"*weight)") 
singletop3 = DIST("st3", "/home/bjr/trees_fixed_2D/ST_t-channel_5f_leptonDecays.root", "tree", "("+lumi+"*weight)") 
singletop4 = DIST("st4", "/home/bjr/trees_fixed_2D/ST_s-channel_4f_leptonDecays.root", "tree", "("+lumi+"*weight)")

# Now we arrange them correctly:

DistsWeWantToEstiamte = [dataMu,dataEl]
DistsThatWeWantToIgnore = [ttbar,singletop1,singletop2,singletop3,singletop4]

Type1ChannelAlphabetizer = Alphabetizer("type1Alphabet", DistsWeWantToEstiamte, DistsThatWeWantToIgnore)

# apply a preselection to the trees:
presel = "(lepIsLoose>0.&(lepTopMass>100)&(lep2Ddr>0.5||lep2Drel>0.25)&wPt>100&tagJetPt>400)"
# pick the two variables to do the estiamte it (in this case, Soft Drop Mass (from 70 to 350 in 48 bins) and tau32 (from 0 to 1))
var_array = ["tagJetSDMass", "tagJetTau3/tagJetTau2", 48,70,350, 20, 0, 1]
Type1ChannelAlphabetizer.SetRegions(var_array, presel) # make the 2D plot
C1 = TCanvas("C1", "", 800, 600)
C1.cd()
Type1ChannelAlphabetizer.TwoDPlot.Draw() # Show that plot:

# NOW DO THE ACTUAL ALPHABETIZATION: (Creating the regions)
# The command is: .GetRates(cut, bins, truthbins, center, fit)
cut = [0.5, "<"]
# so we need to give it bins:
bins = [[70,90],[90,110],[210,350]]
# truth bins (we don't want any because we are looking at real data::)
truthbins = []
# a central value for the fit (could be 0 if you wanted to stay in the mass variable, we are looking at tops, so we'll give it 170 GeV)
center = 170.
# and finally, a fit, taken from the file "Converters.py". We are using the linear fit, so:
F = LinearFit([0.5,0.5], -100, 180, "linFit1", "EMRNS")
# All the error stuff is handled by the LinearFit class. We shouldn't have to do anything else!

# So we just run:
Type1ChannelAlphabetizer.GetRates(cut, bins, truthbins, center, F)

## Let's plot the results:
C2 = TCanvas("C2", "", 800, 600)
C2.cd()
Type1ChannelAlphabetizer.G.Draw("AP")
Type1ChannelAlphabetizer.Fit.fit.Draw("same")
Type1ChannelAlphabetizer.Fit.ErrUp.Draw("same")
Type1ChannelAlphabetizer.Fit.ErrDn.Draw("same")

# Now we actually run the estiamte!

# cuts:
antitag = "(((isMu>0.&lepIsLoose>0.&(lepTopMass>140&lepTopMass<250)&(lep2Ddr>0.5||lep2Drel>0.25)))&tagJetSDMass>110&tagJetSDMass<210&tagJetTau3/tagJetTau2>0.5&wPt>100&tagJetPt>400)"

tag = "(((isMu>0.&lepIsLoose>0.&(lepTopMass>140&lepTopMass<250)&(lep2Ddr>0.5||lep2Drel>0.25)))&tagJetSDMass>110&tagJetSDMass<210&tagJetTau3/tagJetTau2<0.5&wPt>100&tagJetPt>400)" 

# var we want to look at:
var_array2 = ["eventMass", 30, 0, 3000]

FILE = TFile("output.root", "RECREATE")
FILE.cd()

Type1ChannelAlphabetizer.MakeEst(var_array2, antitag, tag)


# now we can plot (maybe I should add some auto-plotting functions?)

# the real value is the sum of the histograms in self.hists_MSR
V = TH1F("V", "", 30, 0, 3000)
for i in Type1ChannelAlphabetizer.hists_MSR:
	V.Add(i,1.)
# the estimate is the sum of the histograms in self.hists_EST and self.hist_MSR_SUB
N = TH1F("N", "", 30, 0, 3000)
for i in Type1ChannelAlphabetizer.hists_EST:
	N.Add(i,1.)
for i in Type1ChannelAlphabetizer.hists_MSR_SUB:
	N.Add(i,1.)
# but we need to subtract the ones from the subtractable quantities in self.hisy_EST_SUB (these are already measured once)
for i in Type1ChannelAlphabetizer.hists_EST_SUB:
	N.Add(i,-1.)

# We can do the same thing for the Up and Down shapes:
NU = TH1F("NU", "", 30, 0, 3000)
for i in Type1ChannelAlphabetizer.hists_EST_UP:
	NU.Add(i,1.)
for i in Type1ChannelAlphabetizer.hists_EST_SUB_UP:
	NU.Add(i,-1.)
for i in Type1ChannelAlphabetizer.hists_MSR_SUB:
	NU.Add(i,1.)
ND = TH1F("ND", "", 30, 0, 3000)
for i in Type1ChannelAlphabetizer.hists_EST_DN:
	ND.Add(i,1.)
for i in Type1ChannelAlphabetizer.hists_EST_SUB_DN:
	ND.Add(i,-1.)
for i in Type1ChannelAlphabetizer.hists_MSR_SUB:
	ND.Add(i,1.)

N.SetFillColor(kYellow)
ND.SetLineStyle(2)
NU.SetLineStyle(2)

FindAndSetMax([V,N, NU, ND])
C3 = TCanvas("C3", "", 800, 600)
C3.cd()
N.Draw("Hist")
V.Draw("same E0")
NU.Draw("same")
ND.Draw("same")

FILE.Write()
FILE.Save()
