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
QCD = DIST("QCD", "/home/osherson/Work/Alphabet/QCD_HT_v6p3.root", "myTree", "(1.)")

# Now we arrange them correctly:

DistsWeWantToEstiamte = [QCD]

HbbTest = Alphabetizer("QCDalphaTest", DistsWeWantToEstiamte, [])

# apply a preselection to the trees:
presel = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&jet2tau21<0.5&jet1tau21<0.5&jet2bbtag>-0.84)"
# pick the two variables to do the estiamte it (in this case, Soft Drop Mass (from 70 to 350 in 48 bins) and tau32 (from 0 to 1))
var_array = ["jet1pmass", "jet1bbtag", 30,50,200, 200, -1.1, 1.1]
HbbTest.SetRegions(var_array, presel) # make the 2D plot
C1 = TCanvas("C1", "", 800, 600)
C1.cd()
HbbTest.TwoDPlot.Draw() # Show that plot:

# NOW DO THE ACTUAL ALPHABETIZATION: (Creating the regions)
# The command is: .GetRates(cut, bins, truthbins, center, fit)
cut = [-0.84, ">"]
# so we need to give it bins:
bins = [[50,80],[80,105],[135,160],[160,200]]
# truth bins (we don't want any because we are looking at real data::)
truthbins = []
# a central value for the fit (could be 0 if you wanted to stay in the mass variable, we are looking at tops, so we'll give it 170 GeV)
center = 125.
# and finally, a fit, taken from the file "Converters.py". We are using the linear fit, so:

F = QuadraticFit([0.1,0.1,0.1], -75, 75, "quadfit", "EMRFNEX0")
#F = LinearFit([0.5,-0.5], -75, 75, "linFit1", "EMRNS")

# All the error stuff is handled by the LinearFit class. We shouldn't have to do anything else!

# So we just run:
HbbTest.GetRates(cut, bins, truthbins, center, F)

## Let's plot the results:
C2 = TCanvas("C2", "", 800, 600)
C2.cd()
HbbTest.G.Draw("AP")
HbbTest.Fit.fit.Draw("same")
HbbTest.Fit.ErrUp.Draw("same")
HbbTest.Fit.ErrDn.Draw("same")

# Now we actually run the estiamte!

# cuts:
tag = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&(jet1pmass<135&jet1pmass>105)&jet1tau21<0.5&jet2tau21<0.5&(jet1bbtag>-0.84&jet2bbtag>-0.84))"

antitag = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&(jet1pmass<135&jet1pmass>105)&jet1tau21<0.5&jet2tau21<0.5&(jet1bbtag<-0.84&jet2bbtag>-0.84))"

# var we want to look at:
var_array2 = ["dijetmass", 20,1000,3000]

FILE = TFile("Hbb_output.root", "RECREATE")
FILE.cd()

HbbTest.MakeEst(var_array2, antitag, tag)


# now we can plot (maybe I should add some auto-plotting functions?)

# the real value is the sum of the histograms in self.hists_MSR
V = TH1F("V", "", 20,1000,3000)
for i in HbbTest.hists_MSR:
	V.Add(i,1.)
# the estimate is the sum of the histograms in self.hists_EST and self.hist_MSR_SUB
N = TH1F("N", "", 20,1000,3000)
for i in HbbTest.hists_EST:
	N.Add(i,1.)
# We can do the same thing for the Up and Down shapes:
NU = TH1F("NU", "", 20,1000,3000)
for i in HbbTest.hists_EST_UP:
	NU.Add(i,1.)
ND = TH1F("ND", "", 20,1000,3000)
for i in HbbTest.hists_EST_DN:
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
