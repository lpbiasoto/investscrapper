
# from model import LinearRegressionModel
from flask import Flask, request, jsonify
from business.pe_analysis import *
# def main():


# app = Flask(__name__)


# @app.route('/gold_PE_grid/')
# def gold_PE_grid():
ativos_dict = {"Gold Futures": 8830, "GOLD": 13928, "Cobre Futuros": 8831}
response = get_gold_PE_grid(ativos_dict)

    # df.to_csv("teste.csv")


# app.run(debug=True, host='0.0.0.0')

# if __name__ == '__main__':
#     main()
    