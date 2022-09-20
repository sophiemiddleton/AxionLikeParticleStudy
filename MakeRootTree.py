#!/usr/bin/python
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
#import matplotlib.pyplot as plt
#sys.path.insert(0, '../')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


class GetPart:

    def __init__(self, fn1, ofn, tag):

        self.label = 'photon_fusion'
        self.mass = 200
        #input files:
        self.fin1 = ROOT.TFile(fn1);
        self.tin1 = self.fin1.Get("LDMX_Events")
        self.tag = int(tag);

        # output files:
        #self.fn_out = ofn;
        #self.fout = ROOT.TFile("hist_"+self.fn_out,"RECREATE");

        #list of branches:
        self.evHeader1 = ROOT.ldmx.EventHeader()
        self.hcalRecHits = ROOT.std.vector('ldmx::HcalHit')();
        self.tin1.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        self.tin1.SetBranchAddress("HcalRecHits_v12",  ROOT.AddressOf( self.hcalRecHits ));

        # loop and save:
        self.loop();


    def loop(self):
        f = TFile( 'ALPStudy_'+self.label+"_m"+str(self.mass)+'.root', 'RECREATE' )
        Features = TTree( 'Features', 'Information about events' )

        NHits = array('i',[0])
        Features.Branch("NHits",  NHits,  'NHits/I')
        ZLength = array('d',[0])
        Features.Branch("ZLength",  ZLength,  'ZLength/D')
        ZAverage = array('d',[0])
        Features.Branch("ZAverage",  ZAverage,  'ZAverage/D')
        ZWidth = array('d',[0])
        Features.Branch("ZWidth",  ZWidth,  'ZWidth/D')
        XYWidth = array('d',[0])
        Features.Branch("XYWidth",  XYWidth,  'XYWidth/D')


        nent = self.tin1.GetEntriesFast();

        for i in range(nent):
            self.tin1.GetEntry(i);
            NHits[0] = 0
            ZLength[0] = 0.
            ZAverage[0] = 0.
            ZWidth[0] = 0.
            XYWidth[0] = 0.
            sumE = 0

            x_positions = []
            y_positions = []
            z_positions = []
            weighted_z = []
            energies = []

            for ih,hit in enumerate(self.hcalRecHits):
                NHits[0] += 1;
                energies.append(hit.getEnergy())
                x_positions.append(hit.getXPos())
                y_positions.append(hit.getYPos())
                z_positions.append(hit.getZPos())
                sumE += hit.getEnergy()

            # for Z length
            first_z = 1e6
            last_z = 0
            for l, m in enumerate(z_positions):
                #for n,o in enumerate(m):
                if m < first_z:
                    first_z = m
                if m > last_z:
                    last_z = m

            # loop over hits, weight by fraction of energy in that hit
            for p,q in enumerate(energies):
                w = z_positions[p]*q/sumE
                weighted_z.append(w)
            # loop over hits,get transverse shower Information
            for p,q in enumerate(x_positions):
                XYWidth[0] = math.sqrt(x_positions[p]*x_positions[p] + y_positions[p]*y_positions[p])

            # get the mean and stddev for this event
            if len(z_positions) != 0:
                ZAverage[0] = (np.mean(weighted_z))
                ZWidth[0] = (np.std(weighted_z))
                ZLength[0] = (abs(last_z - first_z))
            # if no hits, fill as "0"
            #else:
            #    ZAverage[0] = 0
            #    ZWidth[0] = 0
            #    ZLength[0] = 0

            if len(z_positions) != 0:
                Features.Fill()
        f.Write();
        f.Close();

def main(options,args) :
    sc = GetPart(options.ifile1,options.ofile,options.tag);
    #sc.fout.Close();

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
