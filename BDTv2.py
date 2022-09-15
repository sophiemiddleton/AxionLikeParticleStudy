# ImprovingBDT

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn as sk
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import metrics
import csv
import xgboost as xgb

from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import datasets
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split as tts
from sklearn.model_selection import GridSearchCV
from subprocess import check_call

import joblib
from scipy.stats import ks_2samp as kstest

def sklClassificationTrain(X_train, y_train, n_estimators=80, learning_rate=0.325): # TODO optimize these
    dt = DecisionTreeClassifier(criterion='entropy',
                                max_depth=3,
                                min_samples_leaf=1,
                                min_samples_split=2,
                                random_state=11,
                                splitter='best')
    bdt = AdaBoostClassifier(dt, algorithm='SAMME', n_estimators=n_estimators, learning_rate=learning_rate)
    bdt.fit(X_train, y_train)
    bfile = 'sklearn_bdt01.pkl'
    joblib.dump(bdt, bfile)
    print("finished training")
    return bdt

def compare_train_test(clf, X_train, y_train, X_test, y_test, bins=40, sname=50):
    print("comparing")
    trnNum = "00"
    decisions = []
    for X,y in ((X_train, y_train), (X_test, y_test)):
        d1 = clf.decision_function(X[y>0.0]).ravel()
        d2 = clf.decision_function(X[y<0.0]).ravel()
        decisions += [d1, d2]
    sigStat, sigPval = kstest(decisions[0], decisions[2])
    bkgStat, bkgPval = kstest(decisions[1], decisions[3])
    print("Kolmogorov-Smirnov test: signal (backgroud) p-value = %.3f (%.3f)"%(sigPval, bkgPval))

    low = min(np.min(d) for d in decisions)
    high = max(np.max(d) for d in decisions)
    low_high = (low,high)

    fig, ax = plt.subplots(figsize=(8, 6))
    #======================================================

    ax.hist(decisions[2],
             facecolor='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', density=True, edgecolor='navy',
             label='Signal (test)')
    ax.hist(decisions[3],
             facecolor='r', alpha=0.5, range=low_high, bins=bins, color='r',
             histtype='step', linewidth=2, density=True, hatch='///',
             label='Background (test)')

    hist, bins = np.histogram(decisions[0],
                              bins=bins, range=low_high, density=True)
    scale = len(decisions[0]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    ax.errorbar(center, hist, yerr=err, capsize=2, fmt='o', c='b',
                 label='Signal (train)')

    hist, bins = np.histogram(decisions[1],
                              bins=bins, range=low_high, density=True)
    scale = len(decisions[1]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    ax.errorbar(center, hist, yerr=err, capsize=2, fmt='o', c='r',
                 label='Background (train)')

    plt.xlim(-1, 1)
    #plt.ylim(0, 5)
    textstr = '\n'.join((r'Kolmogorov-Smirnov test:', r'signal (background) p-value = %.3f (%.3f)'%(sigPval, bkgPval)))
    props = dict(boxstyle='round', facecolor='white')

    plt.xlabel("BDT response", fontsize=18, horizontalalignment='right', x=1.0)
    plt.ylabel("(1/N) dN/dx", fontsize=18, horizontalalignment='right', y=1.0)
    plt.tick_params(axis='both', length=6, width=1, direction='in', which='both')
    plt.legend(loc='best')
    ax.text(0.475, 0.75, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top',
             horizontalalignment='center', bbox=props)
    #plt.tight_layout()
    plt.savefig("sklearn_overtrain_" + str(sname) + "tree_BDT210511_" + trnNum + ".pdf", format='pdf', dpi=400)
    #plt.savefig("sklearn_overtrain_" + str(sname) + "tree_BDT0805_" + trnNum + ".png", format='png', dpi=400)
    #plt.show()
    ax.clear()

    #===============================================
    # plot the efficiency and punzi figure of merit
    sigTot = len(decisions[0])
    bkgTot = len(decisions[1])
    ebins = []
    sigEff = []
    bkgEff = []
    purity = []
    significance = []
    for ibin in range(1000):
        lbin = -1 + (2./1000) * ibin
        rbin = -1 + (2./1000) * (ibin + 1)
        ebins.append((lbin + rbin)/2.0)
        sigPass = 0
        bkgPass = 0
        for scores in decisions[0]:
           if scores > lbin:
               sigPass += 1

        for scoreb in decisions[1]:
           if scoreb > lbin:
               bkgPass += 1
        #print("the %3d bin [%5.2f, %5.2f] has efficiency: %0.2f  %0.2f" %(n, lbin, rbin, sigPass/sigTot, bkgPass/bkgTot))
        sigEff.append(sigPass / sigTot)
        bkgEff.append(bkgPass / bkgTot)
        if sigPass + bkgPass == 0:
            purity.append(0)
            #significance.append(0)
        else:
            purity.append(sigPass / (sigPass + bkgPass))
            #significance.append(sigPass / np.sqrt(sigPass + bkgPass))
        #significance.append(sigPass /(1.5 + np.sqrt(bkgPass)))
        # the FOM should be signal efficiency / (1.5 + sqrt(background events))
        significance.append((sigPass/sigTot) / (1.5 + np.sqrt(bkgPass)))
        #significance.append(sigPass /(2.5 + np.sqrt(bkgPass)))

    #print(significance)
    sef = ax.plot(ebins, sigEff, color='b', linewidth=2, label='Signal efficiency')
    bef = ax.plot(ebins, bkgEff, color='r', linewidth=2, label='Background efficiency')
    pur = ax.plot(ebins, purity, color='b', linestyle='dashed', linewidth=2, label='Signal purity')
    plt.grid(True)
    #leg1 = ax.legend([sef, bef], ['Signal efficiency', 'Background efficiency'], loc='upper left')
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 1.25)

    ax.set_xlabel("Cut value applied on BDT output", fontsize=18, horizontalalignment='right', x=1.0)
    ax.set_ylabel("Efficiency (Purity)", fontsize=18, horizontalalignment='right', y=1.0)
    ax.tick_params(axis='both', length=6, width=1, direction='in', which='both')


    ax1 = ax.twinx()
    msign = max(significance)
    ax1.set_ylim(0, msign*1.25)
    color = 'tab:green'
    ax1.set_ylabel("Significance", fontsize=18, horizontalalignment='right', y=1.0, color=color)
    #sign = ax1.plot(ebins, significance, color=color, linewidth=2, label=r'$S/\sqrt{S+B}$')
    sign = ax1.plot(ebins, significance, color=color, linewidth=2, label=r'$\dfrac{\epsilon_{S}}{3/2 + \sqrt{B}}$')
    #sign = ax1.plot(ebins, significance, color=color, linewidth=2, label=r'$S/(5/2 + \sqrt{B})$')
    ax1.tick_params(axis='y', labelcolor=color, length=6, width=1, direction='in')

    #leg2 = plt.legend([pur, sign], ['Purity', r'$S/\sqrt{S+B}$'], loc='upper right')
    lns = sef + bef + pur + sign
    lab = [l.get_label() for l in lns]

    plt.legend(lns, lab, loc='upper right', fontsize=14, ncol=2, mode="expand", borderaxespad=0.1)

    vcut = []
    for idx, val in enumerate(significance):
        if val == msign:
            #print(-1 + (2./1000)*idx, val)
            vcut.append(-1 + (2./1000)*idx)

    #textstr = '\n'.join((r'best cut: $S/(3/2+\sqrt{B})$ = %.2f'%vcut[0]))
    #props = dict(boxstyle='round', facecolor='white')
    #ax.text(-0.35, 0.35, r'best cut: $S/\sqrt{S+B}$ = %.2f'%vcut[0], fontsize=14)
    ax.text(0.25, 0.15, 'best cut:\n$\dfrac{\epsilon_{S}}{3/2+\sqrt{B}}$ = %.2f'%vcut[0], fontsize=14, horizontalalignment='center')
    #ax.text(-0.35, 0.35, r'best cut: $S/(5/2+\sqrt{B})$ = %.2f'%vcut[0], fontsize=14)

    #fig.tight_layout()
    #plt.show()
    #plt.savefig("sklearn_mvaeffs_BDT.pdf", format='pdf', dpi=400)
    plt.savefig("sklearn_mvaeffs_BDT_3sigma210511_" + trnNum + ".pdf", format='pdf', dpi=400)

if __name__ == '__main__':

    #iris = datasets.load_iris()
    iris = pd.read_csv("combined.csv")

    X = iris[["mean","std","nhits","energy"]].values
    Y = iris[["SB"]].values
    X =iris.drop(["event"], axis=1)

    X_dev, X_eval, y_dev, y_eval = tts(X, Y, test_size=0.5, random_state=42)
    X_train, X_test, y_train, y_test = tts(X_dev, y_dev, test_size=0.5, random_state=492)

    rlearn = 0.1
    nEst = 100
    print("==================%3d===================="%nEst)
    bdt = sklClassificationTrain(X_train, y_train, n_estimators=nEst, learning_rate=rlearn)
    model_name = "sklearn_classification_nTree" + str(nEst) + ".pkl"
    joblib.dump(bdt, model_name)

    # assessing the classifier performace
    y_predicted = bdt.predict(X_test)
    print("============= test %s trees ===================="%nEst)
    #print("============= test %s learning rate ===================="%rlearn)
    print(classification_report(y_test, y_predicted, target_names=["background", "signal"]))
    print("Area under ROC curve: %.4f"%(roc_auc_score(y_test, bdt.decision_function(X_test))))

    y_predicted = bdt.predict(X_train)
    print("============= train %s trees ==================="%nEst)
    print(classification_report(y_train, y_predicted, target_names=["background", "signal"]))
    print("Area under ROC curve: %.4f"%(roc_auc_score(y_train, bdt.decision_function(X_train))))

    compare_train_test(bdt, X_train, y_train, X_test, y_test, sname=nEst)
