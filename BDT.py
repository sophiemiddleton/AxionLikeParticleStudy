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

# Load data, select features and ignore target in the X list:
iris = pd.read_csv("combined.csv")

X = iris[["mean","std","nhits","energy"]].values
Y = iris[["SB"]].values
X =iris.drop(["event"], axis=1)
data_dmatrix = xgb.DMatrix(data=X,label=Y)
#split data, fit and predict:
X_train , X_test, y_train, y_test = train_test_split(X,Y,test_size = 0.5, random_state = 100)
xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.3, learning_rate = 1.0,
                max_depth = 5, alpha = 10, n_estimators = 300)
xg_reg.fit(X_train,y_train)

y_pred = xg_reg.predict(X_test)

#Write out the prediction
pd.DataFrame(y_pred).to_csv("outputs_filename.csv", index=False)

# print results and make simple plot:
#print('reg score: ',regr.score(X_test,y_test))
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
print('r2', np.sqrt(metrics.r2_score(y_test, y_pred)))

fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)

lims = [
    np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
    np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
]

ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
ax.set_aspect('equal')
ax.set_xlim(lims)
ax.set_ylim(lims)
plt.xlabel("Actual")
plt.ylabel("Predicted")
fig.show()
fig.savefig("predicted.pdf")
xgb.plot_importance(xg_reg,grid=False)
