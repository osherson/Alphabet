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

def Type1Alphabetizer(name, D, TT, MC, p, a ,t, VAR):
	a = "("+a+"&"+p+")"
	t = "("+t+"&"+p+")"
	DistsWeWantToEstiamte = D
	DistsThatWeWantToIgnore = TT + MC
	ALFBTZR = Alphabetizer(name[0]+name[1], DistsWeWantToEstiamte, DistsThatWeWantToIgnore)
	var_array = ["tagJetSDMass", "tagJetTau3/tagJetTau2", 48,70,350, 20, 0, 1]
	ALFBTZR.SetRegions(var_array, p)
	C = TCanvas("C1_2d"+name[0]+name[1], "", 1600, 1200)
	C.cd()
	ALFBTZR.TwoDPlot.Draw()
	C.SaveAs("C_2d_"+name[0]+name[1]+".root")
	cut = [0.5, "<"]
	bins = [[70,90],[90,110],[210,350]]
	truthbins = []
	center = 170.
	t1Fit = LinearFit([0.5,0.5], -100, 180, "LF", "EMRNSQ")
	ALFBTZR.GetRates(cut, bins, truthbins, center, t1Fit)
	C2 = TCanvas("C2_fit_"+name[0]+name[1], "", 1600, 1200)
	C2.cd()
	ALFBTZR.G.Draw("AP")
	ALFBTZR.Fit.fit.Draw("same")
	ALFBTZR.Fit.ErrUp.Draw("same")
	ALFBTZR.Fit.ErrDn.Draw("same")
	C2.SaveAs("C2_fit"+name[0]+name[1]+".root")
	ALFBTZR.MakeEst(VAR, a, t)
	FILE = TFile("output_"+name[0]+name[1]+".root", "RECREATE")
	FILE.cd()
	D = TH1F(name[0]+"__DATA"+name[1], "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_MSR:
		D.Add(i,1.)
	E = TH1F(name[0]+"__EST"+name[1], "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST:
		E.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB:
		E.Add(i,-1.)
	Eu = TH1F(name[0]+"__EST__fit"+name[0]+"__up", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST_UP:
		Eu.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB_UP:
		E.Add(i,-1.)
	Ed = TH1F(name[0]+"__EST__fit"+name[0]+"__down", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST_DN:
		Ed.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB_DN:
			E.Add(i,-1.)
	T = TH1F(name[0]+"__TT"+name[1], "", VAR[1], VAR[2], VAR[3])
	M = TH1F(name[0]+"__MC"+name[1], "", VAR[1], VAR[2], VAR[3])
	for i in range(0,len(DistsThatWeWantToIgnore)):
		if i < len(TT):
			T.Add(ALFBTZR.hists_MSR_SUB[i],1.)
		else:
			M.Add(ALFBTZR.hists_MSR_SUB[i],1.)
	FILE.Write()
	FILE.Save()
	FILE.Close()
	Pull = TH1F(name[0]+"PULL", "", VAR[1], VAR[2], VAR[3])
	PullE = TH1F(name[0]+"PULLE", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_MSR:
		Pull.Add(i,1.)
	for i in ALFBTZR.hists_EST:
		PullE.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB:
		PullE.Add(i,-1.)
	for i in range(0,len(DistsThatWeWantToIgnore)):
		PullE.Add(ALFBTZR.hists_MSR_SUB[i],1.)
	EU = TH1F(name[0]+"UP", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST_UP:
		EU.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB_UP:
		EU.Add(i,-1.)
	ED = TH1F(name[0]+"DOWN", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST_DN:
		ED.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB_DN:
		ED.Add(i,-1.)
	Pull.SetFillColor(kPink)
	for i in range(Pull.GetNbinsX()+1):
		V = Pull.GetBinContent(i) - PullE.GetBinContent(i)
		Ve = Pull.GetBinError(i)
		u = EU.GetBinContent(i) - PullE.GetBinContent(i)
		d = ED.GetBinContent(i) - PullE.GetBinContent(i)
		ue = math.sqrt(Ve**2 + u**2)
		de = math.sqrt(Ve**2 + d**2)
		if V > 0.:
			e = ue
		else:
			e = de
		if e > 1:
			f = V/e
		else:
			f = V
		Pull.SetBinContent(i, f)	
	C3 = TCanvas("C3_Pull_"+name[0]+name[1], "", 1600, 1200)
	C3.cd()
	Pull.Draw("hist")
	C3.SaveAs("C3_Pull_"+name[0]+name[1]+".root")

def Type2Alphabetizer(name, D, TT, MC, p, a ,t, VAR):
	a = "("+a+"&"+p+")"
	t = "("+t+"&"+p+")"
	DistsWeWantToEstiamte = D
	DistsThatWeWantToIgnore = TT + MC
	ALFBTZR = Alphabetizer(name[0]+name[1], DistsWeWantToEstiamte, DistsThatWeWantToIgnore)
	var_array = ["tagJetSDMass", "tagJetTau2/tagJetTau1", 90,40,130, 20, 0, 1]
	ALFBTZR.SetRegions(var_array, p)
	C = TCanvas("C1_2d"+name[0]+name[1], "", 1600, 1200)
	C.cd()
	ALFBTZR.TwoDPlot.Draw()
	C.SaveAs("C_2d_"+name[0]+name[1]+".root")
	cut = [0.6, "<"]
	bins =[[40,50],[50,60],[60,70],[100,110],[110,120],[120,130]]
	truthbins = []
	center = 85.
	t2Fit = QuadraticFit([0.1,0.1,0.1], -45, 45, "QF", "EMRFNEX0Q")
	ALFBTZR.GetRates(cut, bins, truthbins, center, t2Fit)
	C2 = TCanvas("C2_fit_"+name[0]+name[1], "", 1600, 1200)
	C2.cd()
	ALFBTZR.G.Draw("AP")
	ALFBTZR.Fit.fit.Draw("same")
	ALFBTZR.Fit.ErrUp.Draw("same")
	ALFBTZR.Fit.ErrDn.Draw("same")
	C2.SaveAs("C2_fit"+name[0]+name[1]+".root")
	ALFBTZR.MakeEst(VAR, a, t)
	FILE = TFile("output_"+name[0]+name[1]+".root", "RECREATE")
	FILE.cd()
	D = TH1F(name[0]+"__DATA"+name[1], "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_MSR:
		D.Add(i,1.)
	E = TH1F(name[0]+"__EST"+name[1], "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST:
		E.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB:
		E.Add(i,-1.)
	Eu = TH1F(name[0]+"__EST__fit"+name[0]+"__up", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST_UP:
		Eu.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB_UP:
		E.Add(i,-1.)
	Ed = TH1F(name[0]+"__EST__fit"+name[0]+"__down", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST_DN:
		Ed.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB_DN:
			E.Add(i,-1.)
	T = TH1F(name[0]+"__TT"+name[1], "", VAR[1], VAR[2], VAR[3])
	M = TH1F(name[0]+"__MC"+name[1], "", VAR[1], VAR[2], VAR[3])
	for i in range(0,len(DistsThatWeWantToIgnore)):
		if i < len(TT):
			T.Add(ALFBTZR.hists_MSR_SUB[i],1.)
		else:
			M.Add(ALFBTZR.hists_MSR_SUB[i],1.)
	FILE.Write()
	FILE.Save()
	FILE.Close()
	Pull = TH1F(name[0]+"PULL", "", VAR[1], VAR[2], VAR[3])
	PullE = TH1F(name[0]+"PULLE", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_MSR:
		Pull.Add(i,1.)
	for i in ALFBTZR.hists_EST:
		PullE.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB:
		PullE.Add(i,-1.)
	for i in range(0,len(DistsThatWeWantToIgnore)):
		PullE.Add(ALFBTZR.hists_MSR_SUB[i],1.)
	EU = TH1F(name[0]+"UP", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST_UP:
		EU.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB_UP:
		EU.Add(i,-1.)
	ED = TH1F(name[0]+"DOWN", "", VAR[1], VAR[2], VAR[3])
	for i in ALFBTZR.hists_EST_DN:
		ED.Add(i,1.)
	for i in ALFBTZR.hists_EST_SUB_DN:
		ED.Add(i,-1.)
	Pull.SetFillColor(kPink)
	for i in range(Pull.GetNbinsX()+1):
		V = Pull.GetBinContent(i) - PullE.GetBinContent(i)
		Ve = Pull.GetBinError(i)
		u = EU.GetBinContent(i) - PullE.GetBinContent(i)
		d = ED.GetBinContent(i) - PullE.GetBinContent(i)
		ue = math.sqrt(Ve**2 + u**2)
		de = math.sqrt(Ve**2 + d**2)
		if V > 0.:
			e = ue
		else:
			e = de
		if e > 1:
			f = V/e
		else:
			f = V
		Pull.SetBinContent(i, f)	
	C3 = TCanvas("C3_Pull_"+name[0]+name[1], "", 1600, 1200)
	C3.cd()
	Pull.Draw("hist")
	C3.SaveAs("C3_Pull_"+name[0]+name[1]+".root")


dataMu = DIST("Mu", "/home/bjr/trees_fixed_2D/SingleMuon_Run2015D_PromptReco-v4_decosa.root", "tree", "(1.0)")
dataEl = DIST("El", "/home/bjr/trees_fixed_2D/SingleElectron_Run2015D_PromptReco-v4_decosa.root", "tree", "(1.0)")
lumi = str(1.5) # can't forget to scale to lumi!
ttbar = DIST("ttbar", "/home/bjr/trees_fixed_2D/TT_TuneZ2star_13TeV-powheg-pythia6-tauola.root", "tree", "("+lumi+"*0.8*weight*2.71828^(-0.0001*(MCantitoppt+MCtoppt)))")
singletop1 = DIST("st1", "/home/bjr/trees_fixed_2D/ST_tW_top_5f_DS_inclusiveDecays.root", "tree", "("+lumi+"*0.8*weight)")
singletop2 = DIST("st2", "/home/bjr/trees_fixed_2D/ST_tW_antitop_5f_DS_inclusiveDecays.root", "tree", "("+lumi+"*0.8*weight)") 
singletop3 = DIST("st3", "/home/bjr/trees_fixed_2D/ST_t-channel_5f_leptonDecays.root", "tree", "("+lumi+"*0.8*weight)") 
singletop4 = DIST("st4", "/home/bjr/trees_fixed_2D/ST_s-channel_4f_leptonDecays.root", "tree", "("+lumi+"*0.8*weight)")

Type1Alphabetizer(	["MU1",""],
			[dataMu,dataEl],
			[ttbar],
			[singletop1,singletop2,singletop3,singletop4],
			"(lepIsLoose>0.&lepMiniIso<1.&(lepTopMass>140&lepTopMass<250)&eventMass<2100&lepPt>50.&leadJetPt>100.&wPt>100.)",
			"(isMu>0.&tagJetSDMass>110&tagJetSDMass<210&tagJetTau3/tagJetTau2>0.5)",
			"(isMu>0.&tagJetSDMass>110&tagJetSDMass<210&tagJetTau3/tagJetTau2<0.5)",
			["eventMass", 17, 400., 2100.]
		)

Type1Alphabetizer(	["EL1",""],
			[dataMu,dataEl],
			[ttbar],
			[singletop1,singletop2,singletop3,singletop4],
			"(lepIsLoose>0.&lepMiniIso<1.&(lepTopMass>140&lepTopMass<250)&eventMass<2100&lepPt>50.&leadJetPt>100.&wPt>100.)",
			"(isEl>0.&tagJetSDMass>110&tagJetSDMass<210&tagJetTau3/tagJetTau2>0.5)",
			"(isEl>0.&tagJetSDMass>110&tagJetSDMass<210&tagJetTau3/tagJetTau2<0.5)",
			["eventMass", 17, 400., 2100.]
		)

Type2Alphabetizer(	["MU2",""],
			[dataMu,dataEl],
			[ttbar],
			[singletop1,singletop2,singletop3,singletop4],
			"((lepIsLoose>0.&lepMiniIso<1.&((lepTopMass>140&lepTopMass<250&hadTopMass2<250&hadTopMass2>140)||(lepTopMass2>140&lepTopMass2<250&hadTopMass<20&hadTopMass>140))&eventMass<2100&(wPt+tagJetPt+leadJetPt+offJetPt>700))&lepPt>50.&leadJetPt>100.&wPt>100.)",
			"(isMu>0.&tagJetSDMass>70&tagJetSDMass<100&tagJetTau2/tagJetTau1>0.6)",
			"(isMu>0.&tagJetSDMass>70&tagJetSDMass<100&tagJetTau2/tagJetTau1<0.6)",
			["eventMass2", 17, 400., 2100.]
		)

Type2Alphabetizer(	["EL2",""],
			[dataMu,dataEl],
			[ttbar],
			[singletop1,singletop2,singletop3,singletop4],
			"((lepIsLoose>0.&lepMiniIso<1.&((lepTopMass>140&lepTopMass<250&hadTopMass2<250&hadTopMass2>140)||(lepTopMass2>140&lepTopMass2<250&hadTopMass<20&hadTopMass>140))&eventMass<2100&(wPt+tagJetPt+leadJetPt+offJetPt>700))&lepPt>50.&leadJetPt>100.&wPt>100.)",
			"(isEl>0.&tagJetSDMass>70&tagJetSDMass<100&tagJetTau2/tagJetTau1>0.6)",
			"(isEl>0.&tagJetSDMass>70&tagJetSDMass<100&tagJetTau2/tagJetTau1<0.6)",
			["eventMass2", 17, 400., 2100.]
		)














