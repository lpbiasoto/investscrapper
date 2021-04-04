import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class LinearRegressionModel():

    model = None

    def __init__(self):
        self.model = LinearRegression() #Pipeline([('scaler', StandardScaler()),('lreg', LinearRegression())])

    def train_model(self, df, response_var):
        X_train, X_test, y_train, y_test = self._split_data(df, response_var)
        self._process_pipeline(X_train, y_train)
        
        print(self.model.score(X_test, y_test), self.model.coef_, self.model.intercept_)#, self.model.best_estimator_.named_steps['lreg'].coef_
        return self.model

    def _split_data(self, df, response_var):
        y = df[response_var]
        X = df.drop(columns=[response_var])
        print(X.columns)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        return X_train, X_test, y_train, y_test

    def _process_pipeline(self, X_train, y_train):
        self.model.fit(X_train, y_train)