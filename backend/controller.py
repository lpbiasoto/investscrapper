from flask import Flask, request, jsonify
from business.pe_analysis import *

app = Flask(__name__)

@app.route('/')
def main():
    return "API rodando"

@app.route('/gold_PE_grid/')
def gold_PE_grid():
    ativos_dict = {"Gold Futures": 8830, "GOLD": 13928, "Cobre Futuros": 8831}
    pe_grid = get_gold_PE_grid(ativos_dict)

    message = {
        "status": 200,
        "message": "OK",
        "pe": pe_grid
    }

    response = jsonify(message)
    response.status_code = 200
    print(response)
    return response

# app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    app.run()