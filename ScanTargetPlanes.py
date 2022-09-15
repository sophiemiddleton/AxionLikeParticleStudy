#!/usr/bin/python
import argparse
import importlib
import ROOT
from ROOT import TTree, TBranch, TH1F
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libHcal_Event.so")	;
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libEcal_Event.so")	;
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libRecon_Event.so")	;
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libSimCore_Event.so")	;
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libFramework.so");
import os
import math
import sys
import csv
from array import array
from optparse import OptionParser
#import matplotlib.pyplot as plt
#sys.path.insert(0, '../')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


class GetPhotons:

    def __init__(self, fn1, ofn, tag):

        #input files:
        self.fin1 = ROOT.TFile(fn1);
        self.tin1 = self.fin1.Get("LDMX_Events")
        self.tag = int(tag);

        # output files:
        self.fn_out = ofn;
        self.fout = ROOT.TFile("hist_"+self.fn_out,"RECREATE");

        #list of branches:
        self.evHeader1 = ROOT.ldmx.EventHeader()
        self.simParticles1 = ROOT.std.map(int, 'ldmx::SimParticle')();
        self.hcalHits1 = ROOT.std.vector('ldmx::HcalHit')();
        self.hcalSimHits1 = ROOT.std.vector('ldmx::SimCalorimeterHit')();
        self.ecalHits1 = ROOT.std.vector('ldmx::EcalHit')();
        self.ecalSimHits1 = ROOT.std.vector('ldmx::SimCalorimeterHit')();
        self.hcalScoringPlaneHits1 = ROOT.std.vector('ldmx::SimTrackerHit')();
        self.ecalScoringPlaneHits1 = ROOT.std.vector('ldmx::SimTrackerHit')();
        self.targetScoringPlaneHits1 = ROOT.std.vector('ldmx::SimTrackerHit')();
        self.tin1.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        self.tin1.SetBranchAddress("HcalSimHits_test",  ROOT.AddressOf( self.hcalSimHits1 ));
        #self.tin1.SetBranchAddress("HcalRecHits_test",  ROOT.AddressOf( self.hcalHits1 ));
        self.tin1.SetBranchAddress("SimParticles_test",  ROOT.AddressOf( self.simParticles1 ));
        self.tin1.SetBranchAddress("EcalSimHits_test",  ROOT.AddressOf( self.ecalSimHits1 ));
        #self.tin1.SetBranchAddress("EcalRecHits_test",  ROOT.AddressOf( self.ecalHits1 ));
        self.tin1.SetBranchAddress("HcalScoringPlaneHits_test",  ROOT.AddressOf(self.hcalScoringPlaneHits1));
        self.tin1.SetBranchAddress("EcalScoringPlaneHits_test",  ROOT.AddressOf(self.ecalScoringPlaneHits1));
        self.tin1.SetBranchAddress("TargetScoringPlaneHits_test",  ROOT.AddressOf(self.targetScoringPlaneHits1));

        self.energy = []
        self.mom_x = []
        self.mom_y = []
        self.mom_z = []
        self.phi = []
        self.polar = []
        # loop and save:
        self.loop();
        self.writeOutHistos();

    def writeOutHistos(self):
        self.fout.cd();

    def loop(self):
        nent = self.tin1.GetEntriesFast();
        print("Entries ",nent);
        f = open('data.csv', 'w')

        print("Energy [MeV],Mom x [MeV/c], Mom y [MeV/c], Mom z [MeV/c]")
        f.write("Event No.,Energy [MeV],Mom x [MeV/c], Mom y [MeV/c], Mom z [MeV/c]\n")
        for i in range(nent):
            self.tin1.GetEntry(i);

            for ih,hit in enumerate(self.targetScoringPlaneHits1):

                hitID = hit.getID() & 0xFFF ;
                if hitID ==4 and hit.getPdgID() == 22:# and hit.getTrackID()==1:
                    print(hit.getEnergy(),",",hit.getMomentum()[0],",",hit.getMomentum()[1],",",hit.getMomentum()[2])
                    self.energy.append(hit.getEnergy())
                    self.mom_x.append(hit.getMomentum()[0])
                    self.mom_y.append(hit.getMomentum()[1])
                    self.mom_z.append(hit.getMomentum()[2])
                    self.phi.append(math.atan2(hit.getMomentum()[1],hit.getMomentum()[0]))
                    self.polar.append(math.acos(hit.getMomentum()[2]/math.sqrt(hit.getMomentum()[0]*hit.getMomentum()[0] + hit.getMomentum()[1]*hit.getMomentum()[1] + hit.getMomentum()[2]*hit.getMomentum()[2])))
                    f.write(str(i)+","+str(hit.getEnergy())+","+str(hit.getMomentum()[0])+","+str(hit.getMomentum()[1])+","+str(hit.getMomentum()[2])+"\n")
            #print("hitID = ",hitID, hit.getPdgID())

def main(options,args) :
    sc = GetPhotons(options.ifile1,options.ofile,options.tag);
    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.energy,
            bins=100, range=(0,4000), alpha=0.5, histtype='step', label="Target")
    plt.yscale('log')
    fig.savefig("energy.pdf")
    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.mom_x,
            bins=100, range=(0,4000), alpha=0.5, histtype='step', label="Target")
    plt.yscale('log')
    fig.savefig("momx.pdf")
    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.mom_y,
            bins=100, range=(0,4000), alpha=0.5, histtype='step', label="Target")
    plt.yscale('log')
    fig.savefig("momy.pdf")
    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.mom_z,
            bins=100, range=(0,4000), alpha=0.5, histtype='step', label="Target")
    plt.yscale('log')
    fig.savefig("momz.pdf")
    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.phi,
            bins=100, range=(0,4), alpha=0.5, histtype='step', label="Target")
    plt.yscale('log')
    fig.savefig("phi.pdf")
    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.polar,
            bins=100, range=(0,4), alpha=0.5, histtype='step', label="Target")
    plt.yscale('log')
    fig.savefig("polar.pdf")
    sc.fout.Close();

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--ifile1', dest='ifile1', default = 'file1.root',help='directory with data1', metavar='idir1')
    parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()


    ROOT.gStyle.SetPadTopMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.16)
    ROOT.gStyle.SetPadRightMargin(0.10)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("1.1f")
    ROOT.gStyle.SetOptFit(0000)
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    # Get the Event library
    ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libHcal_Event.so")	;
    ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libFramework.so");
    ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libEcal_Event.so")	;
    ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libRecon_Event.so")	;
    ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libSimCore_Event.so")	;

    main(options,args);
