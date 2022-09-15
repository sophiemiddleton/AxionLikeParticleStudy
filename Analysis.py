import uproot
import pandas
import math
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1)

filenames = ["PN.root","ALP_m10.root","ALP_m50.root","ALP_m100.root","ALP_m150.root","ALP_m200.root"]
nametag= ["PN BKG","m = 10","m = 50","m = 100","m = 150", "m = 200"]
colors = ["black","cyan","magenta","green","blue","red"]
bars = ["k.","c.","m.","g.","b.","r."]
integrals = [1244,10000,10000,10000,10000,10000]
norm = 10000
energies = []
weights = []
"""
for i, f in enumerate(filenames):
    input_mu = uproot.open(f)
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
fig.savefig('energy.pdf')


times = []
weights = []
for i, f in enumerate(filenames):

    input_mu = uproot.open(f)
    input_parent = input_mu["LDMX_Events"]
    df = input_parent.pandas.df(flatten=False)
    time = []
    scale = norm/integrals[i]
    weight = []
    print(i, "hits : ", len(df["HcalRecHits_v12.time_"]))
    for k,e in enumerate(df["HcalRecHits_v12.time_"]):
        if len(e) !=0:
            time.append(e[0])
            weight.append(scale)
    times.append(time)
    weights.append(weight)
for m, p in enumerate(times):

    n, bins, patches = ax.hist(p,
                               bins=50,
                               label=nametag[m],
                               weights = weights[m],
                               range = (0,45),
                               histtype='step',
                               color=colors[m])
    bins = 0.5 * (bins[:-1] + bins[1:])
    plt.errorbar(bins, n, yerr=np.sqrt(n), fmt=bars[m])
ax.set_ylabel('N')
ax.set_xlabel("Time [ns]")
ax.set_yscale('log')
fig.savefig('time.pdf')


xs = []
ys = []
for i, f in enumerate(filenames):

    input_mu = uproot.open(f)
    input_parent = input_mu["LDMX_Events"]
    df = input_parent.pandas.df(flatten=False)
    x = []
    y = []
    for k,e in enumerate(df["HcalRecHits_v12.xpos_"]):
        if len(e) !=0:
            x.append(e[0])
    for k,e in enumerate(df["HcalRecHits_v12.ypos_"]):
        if len(e) !=0:
            y.append(e[0])
    xs.append(x)
    ys.append(y)

for m, p in enumerate(xs):

    plt.scatter(xs[m], ys[m],  c=colors[m])
    ax.set_ylabel('y [mm]')
    ax.set_xlabel("x [mm]")
    plt.xlim(-1000,1000)
    plt.ylim(-1000,1000)
    ax.set_yscale('log')
    plt.legend(loc="upper right")
    fig.savefig('xy'+str(m)+'.pdf')

"""

"""
if k<1 and len(e) !=0:
    for l, m in enumerate(e):
        x.append(m)
        y.append(df["HcalRecHits_v12.ypos_"][k][l])
        z.append(df["HcalRecHits_v12.zpos_"][k][l])

    fig2 = plt.figure()
    ax2 = plt.axes(projection='3d')
    ax2.set_ylabel('z [mm]')
    ax2.set_xlabel("x [mm]")
    ax2.set_zlabel("y [mm]")
    print(k)
    ax2.scatter3D(x, z, y, c=colors[i],label="Event "+str(k)+" Tag "+nametag[i]);
    plt.legend(loc="upper right")
    fig2.savefig('xyz'+str(k)+nametag[i]+'.pdf')
    print("++++++++++++")
"""

Nhits_all = []
weights = []
Z_lengths = []
mean_zs = []
std_zs = []
energies = []
# number of lists loop
for i, f in enumerate(filenames):
    print(f)
    input_mu = uproot.open(f)
    input_parent = input_mu["LDMX_Events"]
    df = input_parent.pandas.df(flatten=False)
    Nhits = []
    Z_length = []
    weight = []
    mean_z = []
    std_z = []
    energy = []
    # number of events loop
    for k,e in enumerate(df["HcalRecHits_v12.zpos_"]):
        if len(df["HcalRecHits_v12.zpos_"][k]) == 0:
            continue
        scale = norm/integrals[i]
        weight.append(scale)

        weighted_z = []
        sumE = 0
        # get total energy in event
        for p,q in enumerate(df["HcalRecHits_v12.zpos_"][k]):
            sumE += df["HcalRecHits_v12.energy_"][k][p]
        # loop over hits, weight by fraction of energy in that hit
        for p,q in enumerate(df["HcalRecHits_v12.zpos_"][k]):
            weighted_z.append(df["HcalRecHits_v12.energy_"][k][p])#q*/sumE)

        # get the mean and stddev for this event
        if len(df["HcalRecHits_v12.zpos_"][k]) != 0:
            mean_z.append(np.mean(weighted_z))
            std_z.append(np.std(weighted_z))
        # if no hits, fill as "0"
        else:
            mean_z.append(0)
            std_z.append(0)

        # for Z length
        first_z = 1e6
        last_z = 0
        for l, m in enumerate(df["HcalRecHits_v12.zpos_"][k]):
            #for n,o in enumerate(m):
            if m < first_z:
                first_z = m
            if m > last_z:
                last_z = m

        Nhits.append(len(df["HcalRecHits_v12.ypos_"][k]))
        if len(df["HcalRecHits_v12.zpos_"][k])  == 0:
            Z_length.append(0)
        else:
            Z_length.append(abs(last_z - first_z))
        energy.append(sumE)
    # one entry per list
    Z_lengths.append(Z_length)
    Nhits_all.append(Nhits)
    weights.append(weight)
    mean_zs.append(mean_z)
    std_zs.append(std_z)
    energies.append(energy)
    with open(str(f)+'.csv', 'w') as output_file:
        SB = 0
        if f == "PN.root":
            SB = -1
        else:
            SB = 1
        output_file.write("event,SB,mean,std,length,nhits,energy"+'\n')
        for r,s in enumerate(mean_zs[i]):
            output_file.write(str(r)+','+str(SB)+','+str(s)+','+str(std_zs[i][r])+','+str(Z_length[i][r])+','+str(Nhits_all[i][r])+','+str(energies[i][r])+'\n')
# make plots
fig, ax = plt.subplots(1,1)
for m, p in enumerate(Nhits_all):

    n, bins, patches = ax.hist(p,
                               bins=20,
                               weights = weights[m],
                               label=nametag[m],
                               linestyle='dashed',
                               histtype='step',
                               color=colors[m])
    #bins = 0.5 * (bins[:-1] + bins[1:])
    #plt.errorbar(bins, n, yerr=np.sqrt(n), fmt=bars[m])
ax.set_ylabel('Entres per bin')
ax.set_xlabel("NHits")
ax.set_yscale('log')
plt.legend(loc="upper right")
fig.savefig('nhits.pdf')

fig0, ax0 = plt.subplots(1,1)
for m, p in enumerate(energies):

    n, bins, patches = ax0.hist(p,
                               bins=20,
                               weights = weights[m],
                               label=nametag[m],
                               linestyle='dashed',
                               histtype='step',
                               color=colors[m])
    #bins = 0.5 * (bins[:-1] + bins[1:])
    #plt.errorbar(bins, n, yerr=np.sqrt(n), fmt=bars[m])
ax0.set_ylabel('Entres per bin')
ax0.set_xlabel("Total Energy [MeV]")
ax0.set_yscale('log')
plt.legend(loc="upper right")
fig0.savefig('energy.pdf')

fig1, ax1 = plt.subplots(1,1)
for m, p in enumerate(mean_zs):

    n, bins, patches = ax1.hist(p,
                               bins=20,
                               weights = weights[m],
                               label=nametag[m],
                               linestyle='dashed',
                               histtype='step',
                               color=colors[m])
    #bins = 0.5 * (bins[:-1] + bins[1:])
    #plt.errorbar(bins, n, yerr=np.sqrt(n), fmt=bars[m])
ax1.set_ylabel('Entres per bin')
ax1.set_xlabel("Average Z [mm]")
ax1.set_yscale('log')
plt.legend(loc="upper right")
fig1.savefig('Zav.pdf')

fig2, ax2 = plt.subplots(1,1)
for m, p in enumerate(std_zs):

    n, bins, patches = ax2.hist(p,
                               bins=20,
                               weights = weights[m],
                               label=nametag[m],
                               linestyle='dashed',
                               histtype='step',
                               color=colors[m])
    #bins = 0.5 * (bins[:-1] + bins[1:])
    #plt.errorbar(bins, n, yerr=np.sqrt(n), fmt=bars[m])
ax2.set_ylabel('Entres per bin')
ax2.set_xlabel("Std Dev Z [mm]")
ax2.set_yscale('log')
plt.legend(loc="upper right")
fig2.savefig('Zstd.pdf')

fig1, ax1 = plt.subplots(1,1)
for m, p in enumerate(Z_lengths):

    n, bins, patches = ax1.hist(p,
                               bins=20,
                               weights = weights[m],
                               label=nametag[m],
                               linestyle='dashed',
                               histtype='step',
                               color=colors[m])
    #bins = 0.5 * (bins[:-1] + bins[1:])
    #plt.errorbar(bins, n, yerr=np.sqrt(n), fmt=bars[m])
ax1.set_ylabel('Entres per bin')
ax1.set_xlabel("Z length [mm]")
ax1.set_yscale('log')
plt.legend(loc="upper right")
fig1.savefig('Z.pdf')
