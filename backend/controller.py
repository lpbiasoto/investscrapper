from flask import Flask, request, jsonify
from flask_caching import Cache
from business.pe_analysis import *

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/')
def main():
    return "API rodando"

@app.route('/gold_PE_grid/')
def gold_PE_grid():
    ativos_dict = {"Gold Futures": 8830, "GOLD": 13928, "Cobre Futuros": 8831}
    pe_grid = get_yearly_PE_grid(datetime.now().date()-timedelta(365), datetime.now().date(), ativos_dict)

    message = {
        "status": 200,
        "message": "OK",
        "pe": pe_grid
    }

    response = jsonify(message)
    response.status_code = 200
    print(response)
    return response

@cache.memoize(86400)
def get_yearly_PE_grid(start_date, end_date, ativos_dict):
    return get_gold_PE_grid(start_date, end_date, ativos_dict)

if __name__ == '__main__': 
    app.run()