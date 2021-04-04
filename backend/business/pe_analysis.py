from data.scrapper import HistoricalDataScrapper
from models.linear_regression_model import LinearRegressionModel
from models.pe_grid_element import PEGridElement
from models.pe_grid import PEGrid
from datetime import datetime, timedelta
import numpy as np

def get_gold_PE_grid(start_date, end_date, ativos_dict):
    
    df = HistoricalDataScrapper().get_data(datetime.now().date()-timedelta(365), datetime.now().date(), ativos_dict)
    modelo = LinearRegressionModel().train_model(df, response_var="GOLD")
    
    coefs = modelo.coef_
    intercept = modelo.intercept_
    last_prices = df.iloc[-1]
    
    #poderia ser trazido a partir de algum DB ou um novo método no scrapper
    EPS_2020 = 1.31

    pegrid = PEGrid()

    #GOLD = A*Gold Futures + B*Copper Futures + C
    print("Equação: Barrick Gold Price = "+str(round(coefs[0],2))+"*Gold Price "+str(round(coefs[1],2))+"*Copper Price "+str(round(intercept,2)))
    print(df.iloc[-1])

    for x in range(0,11):
        for y in range(0,11):
            element = PEGridElement(get_perc_P_var(x),get_perc_P_var(y),round((get_perc_P_var(y)*last_prices["Gold Futures"]*coefs[0] + get_perc_P_var(x)*last_prices["Cobre Futuros"]*coefs[1] + last_prices["GOLD"])/EPS_2020,2))
            pegrid.add_element(element)
    return pegrid.to_JSON()

def get_perc_P_var(x):
    return round(0.02*x-0.1,2)