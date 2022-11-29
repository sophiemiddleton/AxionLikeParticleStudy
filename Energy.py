import uproot
import pandas
import math
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1)
path_to_files = "/Users/user/ldmx-sw/ALPSamples/photon_fusion_rootfiles"
label = "photon_fusion"

filenames = ["PN.root","ALP_m10.root","ALP_m50.root","ALP_m100.root","ALP_m150.root","ALP_m200.root"]
nametag= ["PN BKG","m = 10","m = 50","m = 100","m = 150", "m = 200"]
colors = ["black","cyan","magenta","green","blue","red"]
bars = ["k.","c.","m.","g.","b.","r."]
integrals = [1244,10000,8418,6851,5916,5258]
norm = 10000
energies = []
weights = []

for i, f in enumerate(filenames):
    input_mu = uproot.open(str(path_to_files)+"/"+str(f))
    input_parent = input_mu["LDMX_Events"]
    df = input_parent.pandas.df(flatten=False)
    energy = []
    scale = norm/integrals[i]
    weight = []
    print(i, "hits : ", len(df["HcalRecHits_v12.energy_"]))
    for k,e in enumerate(df["HcalRecHits_v12.energy_"]):
        if len(e) !=0:
            energy.append(e[0])
            weight.append(scale)
    energies.append(energy)
    weights.append(weight)
    print("in energies")
for m, p in enumerate(energies):

    n, bins, patches = ax.hist(p,
                               bins=50,
                               weights = weights[m],
                               label=nametag[m],
                               range = (0,10),
                               histtype='step',
                               color=colors[m])
    bins = 0.5 * (bins[:-1] + bins[1:])
    plt.errorbar(bins, n, yerr=np.sqrt(n), fmt=bars[m])
ax.set_ylabel('N')
ax.set_xlabel("Energy [MeV]")
ax.set_yscale('log')
plt.legend(loc="upper right")
fig.savefig(str(label)+'_energy.pdf')
