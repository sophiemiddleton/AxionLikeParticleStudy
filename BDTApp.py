from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

import os.path, sys
from shutil import copy2
import random
import pandas as pd

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import uproot
from sklearn.tree import DecisionTreeClassifier
from sklearn import datasets
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score
#from sklearn.datasets.samples_generator import make_blobs
import joblib

def bdtEvaluate(fname):
    iris = pd.read_csv(fname)

    X = iris[["event","mean","std","nhits","energy"]].values
    Y = iris[["SB"]].values
    X =iris.drop(["event"], axis=1)
    mdlFile = "sklearn_bdt01.pkl"

    bdtModel = joblib.load(mdlFile)

    vBDT = bdtModel.decision_function(X).ravel()
    vBDT.dtype = [('vBDT', np.float64)]

    with open('outputBDTApp.csv', 'w') as output_file:
        for i,j in enumerate(vBDT):

            output_file.write(str(i)+","+str(j)+'\n')


def main():
    fl = "PN.csv"
    bdtEvaluate(fl)

if __name__ == '__main__':

   main()
