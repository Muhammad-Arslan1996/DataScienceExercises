import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC



def main():

    labelled_data = pd.read_csv(sys.argv[1])
    unlabelled_data = pd.read_csv(sys.argv[2])
    X_unlabelled = unlabelled_data.loc[:,'tmax-01':'snwd-12'].values
    X = labelled_data.loc[:,'tmax-01':'snwd-12'].values
    y = labelled_data['city']
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)


    model = make_pipeline(
    SimpleImputer(strategy='mean'),
    StandardScaler(),
    SVC(kernel='linear', C=0.1)
    )
    model.fit(X_train, y_train)
    print(model.score(X_valid, y_valid))
    predictions = model.predict(X_unlabelled)
    pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)


if __name__ == '__main__':
    main()
