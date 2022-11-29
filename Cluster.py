import os

from LDMX.Framework import ldmxcfg
from LDMX.SimCore import generators
from LDMX.SimCore import simulator

p=ldmxcfg.Process("v12")

from LDMX.Hcal import hcal
from LDMX.Hcal import digi
from LDMX.Ecal import digi as ecaldigi
from LDMX.Ecal import ecalClusters
from LDMX.DetDescr.HcalGeometry import HcalGeometry
#from LDMX.DetDescr.EcalHexReadout import EcalHexReadoutGeometry
from LDMX.Ecal import EcalGeometry
from LDMX.Hcal import HcalGeometry
from LDMX.Hcal import hcal_hardcoded_conditions
from LDMX.Ecal import ecal_hardcoded_conditions
#from LDMX.Tools.HgcrocEmulator import HgcrocEmulator
# Instantiate the simulator
sim = simulator.simulator("signal")

# Set the detector to use and enable the scoring planes
sim.setDetector( 'ldmx-det-v12', True)

# Set the run number
#p.runNumber = {{ run }}

# Set a description of what type of run this is.
sim.description = "Signal generated using the v12 detector."

# Set the random seeds
sim.randomSeeds = [ 1,2 ]

# Smear the beamspot
sim.beamSpotSmear = [ 20., 80., 0 ]

# Enable the LHE generator
sim.generators.append(generators.lhe( "Signal Generator", ("/Users/user/ldmx-sw/ALPSamples/primakoff_samples/primakoff_events/m_100/unweighted_events.lhe" )))
hcalDigis = digi.HcalDigiProducer()#ecalDigis = ecaldigi.EcalDigiProducer()
hcalrec = digi.HcalRecProducer()
hcalcluster = hcal.HcalClusterProducer()
#ecalrec = ecaldigi.EcalRecProducer()

geom = HcalGeometry.HcalGeometryProvider.getInstance()
p.sequence=[ sim, hcalDigis, hcalrec, hcalcluster]

p.outputFiles = [ "ALP_m100.root"]

p.maxEvents = 500
p.logFrequency = 10
p.lheFilePath = ("/Users/user/ldmx-sw/ALPSamples/primakoff_samples/primakoff_events/m_100/unweighted_events.lhe" )
p.pause()
