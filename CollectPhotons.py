import uproot
import pandas
import math
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1)

filenames = ["PN.root"]
nametag= ["PN BKG"]
colors = ["black"]
bars = ["k."]
integrals = [1244]
norm = 10000

for i, f in enumerate(filenames):
    print(f)
    input_root = uproot.open(f)
    input_parent = input_root["LDMX_Events"]
    df = input_parent.pandas.df(flatten=False)
    # loop over Target Scoring Planes
    for k, hitid in enumerate(df["TargetScoringPlaneHits_v12.id_"]):
        print(k,hitid)
