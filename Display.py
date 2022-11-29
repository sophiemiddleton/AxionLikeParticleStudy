import uproot
import pandas
import math
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1)

filenames = ["PhotonSamples/Photon_200MeV.root","PhotonSamples/Photon_2GeV.root"]
colors = ["black","cyan"]
bars = ["k.","c."]
nametag= ["gamma200MeV","gamma2GeV"]

for i, f in enumerate(filenames):
    print("analyzing",filenames[i])
    input_mu = uproot.open(f)
    input_parent = input_mu["LDMX_Events"]
    df = input_parent.pandas.df(flatten=False)
    x = []
    y = []
    z = []
    for k,e in enumerate(df["HcalRecHits_backhcal.xpos_"]):
        if len(df["HcalRecHits_backhcal.xpos_"]) !=0 and len(df["HcalRecHits_backhcal.ypos_"]) !=0 and len(df["HcalRecHits_backhcal.zpos_"]) !=0:
            x.append(df["HcalRecHits_backhcal.xpos_"][0])
            y.append(df["HcalRecHits_backhcal.ypos_"][0])
            z.append(df["HcalRecHits_backhcal.zpos_"][0])

    for n, m in enumerate(x):
        print(xs[i])
        fig2 = plt.figure()
        ax2 = plt.axes(projection='3d')
        ax2.set_ylabel('z [mm]')
        ax2.set_xlabel("x [mm]")
        ax2.set_zlabel("y [mm]")
        ax2.scatter3D(x[i], z[i], y[i], c=colors[i],label="Event "+str(k)+" Tag "+nametag[i]);
        plt.legend(loc="upper right")
        fig2.savefig("Event "+str(n)+'.pdf')

"""
xs = []
ys = []
zs = []
for i, f in enumerate(filenames):
    print("analyzing",filenames[i])
    input_mu = uproot.open(f)
    input_parent = input_mu["LDMX_Events"]
    df = input_parent.pandas.df(flatten=False)
    x = []
    y = []
    z = []
    for k,e in enumerate(df["HcalRecHits_backhcal.xpos_"]):
        if len(e) !=0:
            x.append(e[0])
    for k,e in enumerate(df["HcalRecHits_backhcal.ypos_"]):
        if len(e) !=0:
            y.append(e[0])
    for k,e in enumerate(df["HcalRecHits_backhcal.zpos_"]):
        if len(e) !=0:
            z.append(e[0])
    xs.append(x)
    ys.append(y)
    zs.append(z)
    print("finshed",filenames[i],len(xs))
    for n, m in enumerate(xs):
        print(xs[i])
        fig2 = plt.figure()
        ax2 = plt.axes(projection='3d')
        ax2.set_ylabel('z [mm]')
        ax2.set_xlabel("x [mm]")
        ax2.set_zlabel("y [mm]")
        ax2.scatter3D(xs[i], zs[i], ys[i], c=colors[i],label="Event "+str(k)+" Tag "+nametag[i]);
        plt.legend(loc="upper right")
        fig2.savefig("Event "+str(n)+'.pdf')
"""
