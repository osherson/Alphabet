# Try with Hbb regions to predict DiJet mass spect.
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

def writeplot(myTree, plot, var, Cut, Weight): # Fills a plot from a file (needs to have a TTree called "tree"... might change this later)
	temp = plot.Clone("temp") # Allows to add multiple distributions to the plot
#	chain = ROOT.TChain("myTree")
#	chain.Add(File)
	myTree.Draw(var+">>"+"temp", Weight+"*"+Cut, "goff") # Actual plotting (and making of the cut + Weighing if necsr)
	plot.Add(temp)

def write2dplot(File, plot, var, var2, Cut, Weight): # Same as above, but 2D plotter
	temp = plot.Clone("temp")
	chain = ROOT.TChain("myTree")
	chain.Add(File)
#        myTree.SetWeight(3000.0)
	chain.Draw(var2+":"+var+">>"+"temp", Weight+"*"+Cut, "goff")
	plot.Add(temp)

def FindAndSetMax(someset):
	maximum = 0.0
	for i in someset:
		i.SetStats(0)
		t = i.GetMaximum()
		if t > maximum:
			maximum = t
	for j in someset:
		j.GetYaxis().SetRangeUser(0,maximum*1.25)


def Alphabetize(plot, bins, cut): # Takes a 2D plot and measures the Pass/Fail ratios in given bins
	x = []
	y = []
	exl = []
	eyl = []
	exh = []
	eyh = []  # ALL OF THESE ARE THE COMPONENTS OF A TGraphAsymmErrors object.
	hx = []
	hy = []
	ehx = []
	ehy = []

	for b in bins: # loop through the bins (bins are along the mass axis and should contain a gap for the sigreg)
		passed = 0
		failed = 0
		for i in range(plot.GetNbinsX()):  # Get pass/failed
			for j in range(plot.GetNbinsY()):
				if plot.GetXaxis().GetBinCenter(i) < b[1] and plot.GetXaxis().GetBinCenter(i) > b[0]:
					if plot.GetYaxis().GetBinCenter(j) < cut:
						failed = failed + plot.GetBinContent(i,j)
					else:
						passed = passed + plot.GetBinContent(i,j)
		if passed < 0:
			passed = 0
		if failed < 0:
			failed = 0
		if passed == 0 or failed == 0:
			continue
		x.append((float((b[0]+b[1])/2)-125.))  # do the math in these steps (calculate error)
		exl.append(float((b[1]-b[0])/2))
		exh.append(float((b[1]-b[0])/2))
		y.append(passed/(failed))      # NOTE: negative bins are not corrected, if you're getting negative values your bins are too fine.
		ep = math.sqrt(passed)
		ef = math.sqrt(failed)
		err = (passed/(failed))*math.sqrt((ep/passed)+(ef/(passed))**2)
		eyh.append(err)
		if (passed/failed) - err > 0.:
			eyl.append(err)
		else:
			eyl.append(passed/failed)
	G = TGraphAsymmErrors(len(x), scipy.array(x), scipy.array(y), scipy.array(exl), scipy.array(exh), scipy.array(eyl), scipy.array(eyh))
	G.SetMarkerStyle(21)
	G.GetYaxis().SetTitleSize(0.05)
#	G.GetYaxis().SetTitleOffset(1.0)
	G.GetXaxis().SetTitleOffset(0.87)
	G.GetXaxis().SetTitleSize(0.04)
	G.SetTitle("")
	return G  # Returns a TGAE which you can fit or plot.

def AlphabetFitter(G): # Linear fit to output of above function
	funclin = TF1("bfitting_function_linear", "[0]+ [1]*x",-75,75) # linear
	funclin.SetParameter(0, 0.5) 
	funclin.SetParameter(1, -0.5)
	G.Fit(funclin)#, "EMQRN")
	funclin.SetLineColor(kViolet)

	fitter = TVirtualFitter.GetFitter()
	cov = fitter.GetCovarianceMatrixElement(0,1)

	funclinup = TF1("bfitting_function_linear_up", "[0]+ [1]*x + sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",-75,75) #errors
	funclinup.SetParameter(0, funclin.GetParameter(0))
	funclinup.SetParameter(1, funclin.GetParameter(1))
	funclinup.SetParameter(2, funclin.GetParErrors()[0])
	funclinup.SetParameter(3, funclin.GetParErrors()[1])
	funclinup.SetParameter(4, cov)

	funclindn = TF1("bfitting_function_linear_dn", "[0]+ [1]*x - sqrt((x*x*[3]*[3])+(x*2*[4])+([2]*[2]))",-75,75)
	funclindn.SetParameter(0, funclin.GetParameter(0))
	funclindn.SetParameter(1, funclin.GetParameter(1))
	funclindn.SetParameter(2, funclin.GetParErrors()[0])
	funclindn.SetParameter(3, funclin.GetParErrors()[1])
	funclindn.SetParameter(4, cov)

	funclinup.SetLineColor(kViolet)
	funclindn.SetLineColor(kViolet)
	funclinup.SetLineStyle(2)
	funclindn.SetLineStyle(2)
	return [funclin, funclinup, funclindn]


def MakeConvFactors(WFit): # Turns a Fit from above into something useable by a root Draw>> program.
	ConvFact = "({0:2.9f} + ((jet1pmass-125.)*{1:2.9f}))".format(WFit[0].GetParameter(0),WFit[0].GetParameter(1))
	ConvFactUp = "({0:2.9f} + ((jet1pmass-125.)*{1:2.9f}) + ((jet1pmass-125.)*(jet1pmass-125.)*{3:2.9f}*{3:2.9f}+((jet1pmass-125.)*2*{4:2.9f})+({2:2.9f}*{2:2.9f}))^0.5)".format(WFit[0].GetParameter(0),WFit[0].GetParameter(1),WFit[1].GetParameter(2),WFit[1].GetParameter(3),WFit[1].GetParameter(4))
	ConvFactDn = "({0:2.9f} + ((jet1pmass-125.)*{1:2.9f}) - ((jet1pmass-125.)*(jet1pmass-125.)*{3:2.9f}*{3:2.9f}+((jet1pmass-125.)*2*{4:2.9f})+({2:2.9f}*{2:2.9f}))^0.5)".format(WFit[0].GetParameter(0),WFit[0].GetParameter(1),WFit[1].GetParameter(2),WFit[1].GetParameter(3),WFit[1].GetParameter(4))
	return [ConvFact, ConvFactUp, ConvFactDn]


preselectioncut = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&jet2tau21<0.75&jet1tau21<0.75&&jet2bbtag>-0.3)"
sigregcut = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&(jet1pmass<135&jet1pmass>105)&jet1tau21<0.75&jet2tau21<0.75&(jet1bbtag>-0.3&jet2bbtag>-0.3))"
antitagcut = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&(jet1pmass<135&jet1pmass>105)&(jet1tau21<0.75&jet2tau21<0.75)&(jet1bbtag<-0.3&jet2bbtag>-0.3))"

#
Data2DHist = TH2F("Data2DHist", "", 30,50,200, 40, -1, 1)
#
write2dplot("../qcd_all.root", Data2DHist, "jet1pmass", "jet1bbtag", preselectioncut, "(1.0)")


#--- Plot the 2D scan so that we can see what we've got


Databins = [[50,80],[80,105],[135,160],[160,200]]
Higgsbins = [[105,135]]
Data_PF_plot = Alphabetize(Data2DHist, Databins, -0.3)
Data_PF_plot2 = Alphabetize(Data2DHist, Higgsbins, -0.3)
DataFit = AlphabetFitter(Data_PF_plot)
Data_PF_plot2.SetLineColor(kRed)
Data_PF_plot2.SetMarkerColor(kRed)

# LEGEND AND PLOTTING:
Data_PF_plot.GetXaxis().SetTitle("#Delta(jet - Higgs)_{mass} (GeV)")
Data_PF_plot.GetYaxis().SetTitle("N_{passed}/N_{failed}")

leg = TLegend(0.11,0.6,0.4,0.89)
leg.SetLineColor(0)
leg.SetFillColor(0)
#leg.SetHeader("cut @ #tau_{2}/#tau_{1} < 0.5")
leg.AddEntry(Data_PF_plot, "events used in fit", "PL")
leg.AddEntry(Data_PF_plot2, "value at higgs mass", "PL")
leg.AddEntry(DataFit[0], "linear fit", "L")
leg.AddEntry(DataFit[1], "fit errors", "L")

# PLOT!
Datac2 = TCanvas("Datac2", "", 800, 600)
Datac2.cd()
Data_PF_plot.Draw("AP")
Data_PF_plot2.Draw("P")
DataFit[0].Draw("same")
DataFit[1].Draw("same")
DataFit[2].Draw("same")
leg.Draw()
Datac2.Print("fit.pdf")

VAR = "dijetmass"
bins = [20,1000,3000]
vartitle = "m_{X} (GeV)"
output_file = TFile("hh_13_TeV.root","RECREATE")

Dataantitag = TH1F("QCD", "", bins[0], bins[1], bins[2])
DataantitagUP = TH1F("QCD_CMS_scale_13TeVUp", "", bins[0], bins[1], bins[2])
DataantitagDN = TH1F("QCD_CMS_scale_13TeVDown", "", bins[0], bins[1], bins[2])
DataantitagUP.SetLineColor(kBlack)
DataantitagDN.SetLineColor(kBlack)
DataantitagUP.SetLineStyle(2)
DataantitagDN.SetLineStyle(2)
Datasigreg = TH1F("data_obs", "", bins[0], bins[1], bins[2])
Datasigreg.SetLineColor(kBlack)
DataConv = MakeConvFactors(DataFit)




# Fill step:
chain = ROOT.TChain("myTree")
chain.Add("../qcd_all.root")
# myTree.SetWeight(3000.0)

writeplot(myTree, Datasigreg, VAR, sigregcut, "(1.0)")
writeplot(myTree, Dataantitag, VAR, antitagcut, "("+DataConv[0]+")")
writeplot(myTree, DataantitagUP, VAR, antitagcut, "("+DataConv[1]+")")
writeplot(myTree, DataantitagDN, VAR, antitagcut, "("+DataConv[2]+")")


Datasigreg.SetStats(0)
Datasigreg.Sumw2()
Datasigreg.SetLineColor(1)
Datasigreg.SetFillColor(0)
Datasigreg.SetMarkerColor(1)
Datasigreg.SetMarkerStyle(20)
Datasigreg.GetYaxis().SetTitle("events / "+str((bins[2]-bins[1])/bins[0])+" GeV")
Datasigreg.GetXaxis().SetTitle(vartitle)

Dataantitag.SetFillColor(kPink+3)

leg2 = TLegend(0.6,0.6,0.89,0.89)
#leg2.SetHeader("cut @ #tau_{2}/#tau_{1} < 0.5")
leg2.SetLineColor(0)
leg2.SetFillColor(0)
leg2.AddEntry(Datasigreg, "QCD in SR", "PL")
leg2.AddEntry(Dataantitag, "QCD prediction", "F")
leg2.AddEntry(DataantitagUP, "uncertainty", "F")

FindAndSetMax([Dataantitag,DataantitagUP,DataantitagDN,Datasigreg])
Datac3 = TCanvas("Datac3", "", 800, 600)
Datac3.cd()


Datasigreg.Draw("E0")
Dataantitag.Draw("same Hist")
Datasigreg.Draw("same E0")
DataantitagUP.Draw("same Hist")
DataantitagDN.Draw("same Hist")
leg2.Draw()
Datac3.Print("bkg.pdf")


output_file.cd()
Dataantitag.Write()
DataantitagUP.Write()
DataantitagDN.Write()
output_file.Write()
output_file.Close()

