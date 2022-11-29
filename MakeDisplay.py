#!/usr/bin/python

# ldmx python3 MakeRootTree.py --ifile /Users/user/ldmx-sw/ALPSamples/primakoff_rootfiles/ALP_m10.root
import argparse
import importlib
import ROOT
from ROOT import TTree, TBranch, TH1F, TFile
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libHcal_Event.so")	;
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libEcal_Event.so")	;
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libRecon_Event.so")	;
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libSimCore_Event.so")	;
ROOT.gSystem.Load("/Users/user/ldmx-sw/install/lib/libFramework.so");
import os
import math
import sys
import csv
import numpy as np
from array import array
from optparse import OptionParser
#sys.path.insert(0, '../')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

filenames = ["PhotonSamples/Photon_200MeV.root","PhotonSamples/Photon_2GeV.root"]
colors = ["black","cyan"]
bars = ["k.","c."]
nametag= ["gamma200MeV","gamma2GeV"]
class GetPart:

    def __init__(self, fn1, ofn):

        #input files:
        self.fin1 = ROOT.TFile(fn1);
        self.tin1 = self.fin1.Get("LDMX_Events")

        # output files:
        self.fn_out = ofn;
        self.fout = ROOT.TFile("hist_"+self.fn_out,"RECREATE");

        #list of branches:
        self.evHeader1 = ROOT.ldmx.EventHeader()
        self.hcalRecHits = ROOT.std.vector('ldmx::HcalHit')();
        self.tin1.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        self.tin1.SetBranchAddress("HcalRecHits_backhcal",  ROOT.AddressOf( self.hcalRecHits ));

        self.x_positions = []
        self.y_positions = []
        self.z_positions = []
        self.energy = []
        # loop and save:
        self.loop();

    def loop(self):

        nent = self.tin1.GetEntriesFast();

        for i in range(nent):
            self.tin1.GetEntry(i);
            self.x_positions = []
            self.y_positions = []
            self.z_positions = []
            self.energy = []
            if (i < 20):
                for ih,hit in enumerate(self.hcalRecHits):
                    self.x_positions.append(hit.getXPos())
                    self.y_positions.append(hit.getYPos())
                    self.z_positions.append(hit.getZPos())
                    self.energy.append(hit.getEnergy())
                fig2 = plt.figure()
                ax2 = plt.axes(projection='3d')
                ax2.set_ylabel('z [mm]')
                ax2.set_xlabel("x [mm]")
                ax2.set_zlabel("y [mm]")
                ax2.scatter3D(self.x_positions, self.y_positions, self.z_positions, c=self.energy, label="Event"+str(i));
                plt.legend(loc="upper right")
                fig2.savefig("Event"+str(i)+'.pdf')
        #f.Write();
        #f.Close();

def main(options,args) :
    sc = GetPart(options.ifile1,options.ofile);

    sc.fout.Close();

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--ifile1', dest='ifile1', default = 'file1.root',help='directory with data1', metavar='idir1')
    parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')

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
