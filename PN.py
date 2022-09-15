#!/bin/python3

import os
import sys
import json

from LDMX.Framework import ldmxcfg

# set a 'pass name'; avoid sim or reco(n) as they are apparently overused
p=ldmxcfg.Process("v12")

# Ecal hardwired/geometry stuff
import LDMX.Ecal.EcalGeometry
import LDMX.Ecal.ecal_hardcoded_conditions

from LDMX.Ecal import digi
from LDMX.Ecal import vetos
from LDMX.Hcal import hcal



from LDMX.TrigScint.trigScint import TrigScintDigiProducer

from LDMX.Detectors.makePath import *

from LDMX.SimCore import simcfg

from LDMX.Hcal import digi as hcaldigi
from LDMX.DetDescr.HcalGeometry import HcalGeometry
from LDMX.DetDescr.EcalHexReadout import EcalHexReadoutGeometry
from LDMX.Ecal import EcalGeometry
from LDMX.Hcal import HcalGeometry
from LDMX.Hcal import hcal_hardcoded_conditions
from LDMX.Ecal import ecal_hardcoded_conditions


#
# Instantiate the simulator.
#
from LDMX.Biasing import ecal # or target, idk what kind of PN you want
from LDMX.SimCore import generators

sim = ecal.photo_nuclear('ldmx-det-v12',generators.single_4gev_e_upstream_tagger())

#
# Set the path to the detector to use.
#
sim.setDetector( 'ldmx-det-v12', True  )
sim.scoringPlanes = makeScoringPlanesPath('ldmx-det-v12')

#
# Set run parameters
#

sim.description = "ECal photo-nuclear, xsec bias 450"
sim.randomSeeds = [ 1,2 ]
sim.beamSpotSmear = [20., 80., 0]

#
# Fire an electron upstream of the tagger tracker
#
#sim.generators = [ generators.single_4gev_e_upstream_tagger() ]


#
# Enable and configure the biasing
#
#sim.biasingOn(True)
#sim.biasingConfigure('photonNuclear', 'ecal', 2500., 450)

#
# Configure the sequence in which user actions should be called.
#
"""
sim.actions = [ filters.TaggerVetoFilter(),
                                    filters.TargetBremFilter(),
                                    filters.EcalProcessFilter(),
                                    filters.TrackProcessFilter.photo_nuclear() ]

findableTrack = ldmxcfg.Producer("findable", "ldmx::FindableTrackProcessor", "EventProc")

trackerVeto = ldmxcfg.Producer("trackerVeto", "ldmx::TrackerVetoProcessor", "EventProc")
"""

ecalDigi   =digi.EcalDigiProducer()
ecalrec=digi.EcalRecProducer()
#ecalVeto   =vetos.EcalVetoProcessor()
hcalDigis  =hcaldigi.HcalDigiProducer()
hcalrec = hcaldigi.HcalRecProducer()
hcalVeto   =hcal.HcalVetoProcessor()

"""
tsDigisTag  =TrigScintDigiProducer.tagger()
tsDigisUp  =TrigScintDigiProducer.up()
tsDigisDown  =TrigScintDigiProducer.down()
"""

p.sequence=[ sim, ecalDigi, ecalrec, hcalDigis, hcalrec, hcalVeto]#, tsDigisTag, tsDigisUp, tsDigisDown] #, trackerHitKiller, simpleTrigger, findableTrack, trackerVeto ]
p.outputFiles=["simoutput.root"]

p.maxEvents = 200000
p.logFrequency = 10
