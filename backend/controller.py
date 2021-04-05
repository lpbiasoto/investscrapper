from flask import Flask, request, jsonify
from flask_caching import Cache
from flask_cors import CORS, cross_origin
from business.pe_analysis import *

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SECRET_KEY":"pipoca de caramelo",
    "CORS_HEADERS": 'Content-Type'
}
app = Flask(__name__)
app.config.from_mapping(config)

cors = CORS(app, resources={r"/gold_PE_grid": {"origins": "http://localhost:port"},r"/": {"origins": "http://localhost:port"}})
cache = Cache(app)

@app.route('/')
def main():
    return "API rodando"

@app.route('/gold_PE_grid/')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def gold_PE_grid():
    ativos_dict = {"Gold Futures": 8830, "GOLD": 13928, "Cobre Futuros": 8831}
    pe_grid = get_yearly_PE_grid(datetime.now().date()-timedelta(365), datetime.now().date(), ativos_dict)

    pe_grid_list = [x.to_dict() for x in pe_grid.get_elements_list()]

    message = {
        "status": 200,
        "message": "OK",
        "pe": pe_grid_list
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