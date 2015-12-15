#!/bin/bash
for i in 1000 1200 1600 2000 3000
do
	echo "mass point $i"
	mkdir Limits/sig$i
	combine datacard/hh_mX_$i\_13TeV.txt -M Asymptotic -v2 -t -1 -m $i -n CMSHH4b --rMax 1000 --rMin 0.01 &> CMS_HH4b_$i\_13TeV_asymptoticCLs.out
	mv higgsCombineCMSHH4b.Asymptotic.mH$i\.root Limits/CMS_$i\_HH4b_13TeV_asymptoticCLs.root
	combine -M MaxLikelihoodFit --robustFit=1 --rMin=-5 --rMax=5 -t -1 --plots --out Limits/sig$i datacard/hh_mX_$i\_13TeV.txt &> CMS_HH4b_$i\_13TeV_MaxLikelihood.out
done
