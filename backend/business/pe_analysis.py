from data.scrapper import HistoricalDataScrapper
from models.linear_regression import LinearRegressionModel

def get_gold_PE_grid(ativos_dict):
    
    df = HistoricalDataScrapper().get_data(ativos_dict)
    modelo = LinearRegressionModel().train_model(df, response_var="GOLD")
    
    coefs = modelo.coef_
    intercept = modelo.intercept_

    print("Equação: Barrick Gold Price = "+str(round(coefs[0],2))+"*Gold Price "+str(round(coefs[1],2))+"*Copper Price "+str(round(intercept,2)))
    print(df.iloc[-1])

    #tratar a porra toda
    return 1

