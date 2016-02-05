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
import CMS_lumi, tdrstyle

#set the tdr style
#tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.2 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

iPeriod =4

# FORMAT IS:
# dist = ("name", "location of file", "name of tree", "weight (can be more complicated than just a number, see MC example below)")
QCD = DIST("Data", "../QCD_HT_2190_twiki.root", "myTree", "(1.)")

# Now we arrange them correctly:

DistsWeWantToEstiamte = [QCD]

HbbTest = Alphabetizer("QCDalphaTest", DistsWeWantToEstiamte, [])

# apply a preselection to the trees:
presel = "(dijetmass>500&(jet1pmass<130&jet1pmass>100)&jet2tau21<0.75&jet1tau21<0.6&&jet1bbtag<-0.6)"

#presel = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&jet2tau21<0.4&jet1tau21<0.4&jet2bbtag>-0.84)"
# pick the two variables to do the estiamte it (in this case, Soft Drop Mass (from 70 to 350 in 48 bins) and tau32 (from 0 to 1))
var_array = ["jet2pmass", "jet2bbtag", 30,50,200, 200, -1.1, 1.1]
HbbTest.SetRegions(var_array, presel) # make the 2D plot
C1 = TCanvas("C1", "", 800, 600)
C1.cd()
HbbTest.TwoDPlot.Draw() # Show that plot:

# NOW DO THE ACTUAL ALPHABETIZATION: (Creating the regions)
# The command is: .GetRates(cut, bins, truthbins, center, fit)
cut = [0.4, ">"]
# so we need to give it bins:
bins = [[50,75],[75,100],[130,150],[150,200]]
#bins = [[50,70],[70,90],[130,150],[150,200]]
# truth bins (we don't want any because we are looking at real data::)
truthbins = [[100,130]]
# a central value for the fit (could be 0 if you wanted to stay in the mass variable, we are looking at tops, so we'll give it 170 GeV)
center = 115.
# and finally, a fit, taken from the file "Converters.py". We are using the linear fit, so:

F = QuadraticFit([0.1,0.1,0.1], -75, 75, "quadfit", "EMRFNEX0")
#F = LinearFit([0.2,-0.2], -75, 75, "linFit1", "EMRNS")

# All the error stuff is handled by the LinearFit class. We shouldn't have to do anything else!

# So we just run:
HbbTest.GetRates(cut, bins, truthbins, center, F)

## Let's plot the results:
C2 = TCanvas("C2", "", 800, 800)
C2.cd()
HbbTest.G.SetTitle("")
HbbTest.G.Draw("AP")
HbbTest.G.GetXaxis().SetTitle("#Delta(jet - Higgs)_{mass} (GeV)")
HbbTest.G.GetYaxis().SetTitle("N_{passed}/N_{failed}")

HbbTest.Fit.fit.Draw("same")
HbbTest.Fit.ErrUp.SetLineStyle(2)
HbbTest.Fit.ErrUp.Draw("same")
HbbTest.Fit.ErrDn.SetLineStyle(2)
HbbTest.Fit.ErrDn.Draw("same")
#HbbTest.truthG.Draw("opt")
leg = TLegend(0.6,0.6,0.89,0.89)
leg.SetLineColor(0)
leg.SetFillColor(0)
#leg.SetHeader("cut @ #tau_{2}/#tau_{1} < 0.4")
leg.AddEntry(HbbTest.G, "events used in fit", "PL")
leg.AddEntry(HbbTest.Fit.fit, "fit", "L")
leg.AddEntry(HbbTest.Fit.ErrUp, "fit errors", "L")
leg.Draw()
CMS_lumi.CMS_lumi(C2, iPeriod, 22)
C2.Print("fi_bbtag%s.pdf"%cut[0])
# Now we actually run the estiamte!

# cuts:



tag = "(dijetmass>800&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>100)&jet1tau21<0.6&jet2tau21<0.6&(jet1bbtag>0.4&jet2bbtag>0.4))"
antitag = "(dijetmass>800&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>100)&(jet1tau21<0.6&jet2tau21<0.6)&(jet1bbtag<0.4&jet2bbtag>0.4))"


# var we want to look at:
variable = "dijetmass"

#variable bin from dijet analysis 788 838 
binBoundaries = [800, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687,
        1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019 ]#, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509,


FILE = TFile("Hbb_output.root", "RECREATE")
FILE.cd()

HbbTest.MakeEstVariable(variable, binBoundaries, antitag, tag)


# now we can plot (maybe I should add some auto-plotting functions?)
#hbins = [24,800,3000]
# the real value is the sum of the histograms in self.hists_MSR
V = TH1F("data_obs", "", len(binBoundaries)-1, array('d',binBoundaries))
for i in HbbTest.hists_MSR:
	V.Add(i,1.)
# the estimate is the sum of the histograms in self.hists_EST and self.hist_MSR_SUB
N = TH1F("QCD", "", len(binBoundaries)-1, array('d',binBoundaries))
for i in HbbTest.hists_EST:
	N.Add(i,1.)
# We can do the same thing for the Up and Down shapes:
NU = TH1F("QCD_CMS_scale_13TeVUp", "", len(binBoundaries)-1, array('d',binBoundaries)) 
for i in HbbTest.hists_EST_UP:
	NU.Add(i,1.)
ND = TH1F("QCD_CMS_scale_13TeVDown", "", len(binBoundaries)-1, array('d',binBoundaries)) 
for i in HbbTest.hists_EST_DN:
	ND.Add(i,1.)
A =  TH1F("QCD_Antitag", "", len(binBoundaries)-1, array('d',binBoundaries)) 
for i in HbbTest.hists_ATAG:
        A.Add(i,1.)


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
#N.GetYaxis().SetTitle("events / "+str((hbins[2]-hbins[1])/hbins[0])+" GeV")
N.GetXaxis().SetTitle(vartitle)

leg2 = TLegend(0.6,0.6,0.89,0.89)
#leg2.SetHeader("cut @ #tau_{2}/#tau_{1} < 0.4")
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

Pull = V.Clone("Pull")
Pull.Add(N, -1.)

for i in range(Pull.GetNbinsX()+1):
	a = Pull.GetBinContent(i)
	ae = V.GetBinError(i)
	u = NU.GetBinContent(i) - N.GetBinContent(i)
	d = ND.GetBinContent(i) - N.GetBinContent(i)
	ue = math.sqrt(ae**2 + u**2)
	de = math.sqrt(ae**2 + d**2)
	if a > 0.:
		e = ue
	else:
		e = de
	if e > 1:
		f = a/e
	else:
		f = a
	Pull.SetBinContent(i, f)

Pull.GetXaxis().SetTitle("")
Pull.SetStats(0)
Pull.SetFillStyle(1001)
Pull.SetLineColor(kPink+2)
Pull.SetFillColor(kPink+2)
Pull.GetXaxis().SetNdivisions(0)
Pull.GetYaxis().SetNdivisions(4)
Pull.GetYaxis().SetTitle("(Data - Bkg)/#sigma")
Pull.GetYaxis().SetLabelSize(85/15*Pull.GetYaxis().GetLabelSize())
Pull.GetYaxis().SetTitleSize(4.2*Pull.GetYaxis().GetTitleSize())
Pull.GetYaxis().SetTitleOffset(0.175)
Pull.GetYaxis().SetRangeUser(-3.,3.)

C4 = TCanvas("C4", "", 800, 800)
#draw the lumi text on the canvas

plot = TPad("pad1", "The pad 80% of the height",0,0.15,1,1)
pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.15)
plot.Draw()
leg2.Draw()
pull.Draw()
plot.cd()
N.Draw("Hist")
V.Draw("same E0")
NU.Draw("same")
ND.Draw("same")
pull.cd()
Pull.Draw("hist")

CMS_lumi.CMS_lumi(C4, iPeriod, iPos)
C4.cd()
C4.Update()
C4.Print("pull.pdf")


