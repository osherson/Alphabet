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
QCD = DIST("Data", "../qcd_all.root", "myTree", "(1.)")

# Now we arrange them correctly:

DistsWeWantToEstiamte = [QCD]

HbbTest = Alphabetizer("QCDalphaTest", DistsWeWantToEstiamte, [])

# apply a preselection to the trees:
presel = "(dijetmass>1000&(jet1pmass<130&jet1pmass>90)&jet2tau21<0.6&jet1tau21<0.6&&jet1bbtag>0.2)"


#presel = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&jet2tau21<0.5&jet1tau21<0.5&jet2bbtag>-0.84)"
# pick the two variables to do the estiamte it (in this case, Soft Drop Mass (from 70 to 350 in 48 bins) and tau32 (from 0 to 1))
var_array = ["jet2pmass", "jet2bbtag", 30,50,200, 200, -1.1, 1.1]
HbbTest.SetRegions(var_array, presel) # make the 2D plot
C1 = TCanvas("C1", "", 800, 600)
C1.cd()
HbbTest.TwoDPlot.Draw() # Show that plot:

# NOW DO THE ACTUAL ALPHABETIZATION: (Creating the regions)
# The command is: .GetRates(cut, bins, truthbins, center, fit)
cut = [0.2, ">"]
# so we need to give it bins:
bins = [[50,70],[70,90],[130,150],[150,200]]
# truth bins (we don't want any because we are looking at real data::)
truthbins = []
# a central value for the fit (could be 0 if you wanted to stay in the mass variable, we are looking at tops, so we'll give it 170 GeV)
center = 125.
# and finally, a fit, taken from the file "Converters.py". We are using the linear fit, so:

#F = QuadraticFit([0.1,0.1,0.1], -75, 75, "quadfit", "EMRFNEX0")
F = LinearFit([0.2,-0.2], -75, 75, "linFit1", "EMRNS")

# All the error stuff is handled by the LinearFit class. We shouldn't have to do anything else!

# So we just run:
HbbTest.GetRates(cut, bins, truthbins, center, F)

## Let's plot the results:
C2 = TCanvas("C2", "", 800, 600)
C2.cd()
HbbTest.G.Draw("AP")
HbbTest.G.GetXaxis().SetTitle("#Delta(jet - Higgs)_{mass} (GeV)")
HbbTest.G.GetYaxis().SetTitle("N_{passed}/N_{failed}")
HbbTest.Fit.fit.Draw("same")
HbbTest.Fit.ErrUp.SetLineStyle(2)
HbbTest.Fit.ErrUp.Draw("same")
HbbTest.Fit.ErrDn.SetLineStyle(2)
HbbTest.Fit.ErrDn.Draw("same")

leg = TLegend(0.6,0.6,0.89,0.89)
leg.SetLineColor(0)
leg.SetFillColor(0)
#leg.SetHeader("cut @ #tau_{2}/#tau_{1} < 0.5")
leg.AddEntry(HbbTest.G, "events used in fit", "PL")
leg.AddEntry(HbbTest.Fit.fit, "linear fit", "L")
leg.AddEntry(HbbTest.Fit.ErrUp, "fit errors", "L")
leg.Draw()
C2.Print("fi_bbtag%s.pdf"%cut[0])
# Now we actually run the estiamte!

# cuts:

tag = "(dijetmass>1000&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>90)&jet1tau21<0.6&jet2tau21<0.6&(jet1bbtag>0.2&jet2bbtag>0.2))"
antitag = "(dijetmass>1000&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>90)&(jet1tau21<0.6&jet2tau21<0.6)&(jet1bbtag>0.2&jet2bbtag<0.2))"


# var we want to look at:
var_array2 = ["dijetmass", 20,1000,3000]

FILE = TFile("Hbb_output.root", "RECREATE")
FILE.cd()

HbbTest.MakeEst(var_array2, antitag, tag)


# now we can plot (maybe I should add some auto-plotting functions?)
hbins = [20,1000,3000]
# the real value is the sum of the histograms in self.hists_MSR
V = TH1F("data_obs", "", hbins[0],hbins[1], hbins[2])
for i in HbbTest.hists_MSR:
	V.Add(i,1.)
# the estimate is the sum of the histograms in self.hists_EST and self.hist_MSR_SUB
N = TH1F("QCD", "", hbins[0], hbins[1], hbins[2])
for i in HbbTest.hists_EST:
	N.Add(i,1.)
# We can do the same thing for the Up and Down shapes:
NU = TH1F("QCD_CMS_scale_13TeVUp", "", hbins[0],hbins[1], hbins[2])
for i in HbbTest.hists_EST_UP:
	NU.Add(i,1.)
ND = TH1F("QCD_CMS_scale_13TeVDown", "", hbins[0],hbins[1], hbins[2])
for i in HbbTest.hists_EST_DN:
	ND.Add(i,1.)

vartitle = "m_{X} (GeV)"

NU.SetLineColor(kBlack)
ND.SetLineColor(kBlack)
NU.SetLineStyle(2)
ND.SetLineStyle(2)
N.SetLineColor(kBlack)
N.SetFillColor(kPink+3)



V.SetStats(0)
V.Sumw2()
V.SetLineColor(1)
V.SetFillColor(0)
V.SetMarkerColor(1)
V.SetMarkerStyle(20)
N.GetYaxis().SetTitle("events / "+str((hbins[2]-hbins[1])/hbins[0])+" GeV")
N.GetXaxis().SetTitle(vartitle)

leg2 = TLegend(0.6,0.6,0.89,0.89)
#leg2.SetHeader("cut @ #tau_{2}/#tau_{1} < 0.5")
leg2.SetLineColor(0)
leg2.SetFillColor(0)
leg2.AddEntry(V, "QCD in SR", "PL")
leg2.AddEntry(N, "QCD prediction", "F")
leg2.AddEntry(NU, "uncertainty", "F")


FindAndSetMax([V,N, NU, ND])
C3 = TCanvas("C3", "", 800, 600)
C3.cd()
N.Draw("Hist")
V.Draw("same E0")
NU.Draw("same")
ND.Draw("same")
leg2.Draw()
FILE.Write()
FILE.Save()
C3.Print("bkg_bbtag%s.pdf"%cut[0])





