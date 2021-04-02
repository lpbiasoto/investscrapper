import pandas as pd
from bs4 import BeautifulSoup
import requests
import pytz
from datetime import datetime
from lxml.html import fromstring
from interface import Interface
from model import LinearRegressionModel

def main():
    ativos_dict = {"Gold Futures": 8830, "GOLD": 13928, "Cobre Futuros": 8831}
    df = Interface().get_data(ativos_dict)
    modelo = LinearRegressionModel().train_model(df, "GOLD")
    # df.to_csv("teste.csv")


if __name__ == '__main__':
    main()
    