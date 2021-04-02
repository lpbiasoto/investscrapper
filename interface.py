import pandas as pd
from bs4 import BeautifulSoup
import requests
import pytz
from datetime import datetime, timedelta
from lxml.html import fromstring

class Interface():

    def get_data(self, ativos_dict):
        todays_date = datetime.now().date()
        index = pd.date_range(start = todays_date-timedelta(365), end = todays_date, freq='D')
        columns = [ativo for ativo in ativos_dict]
        df_ = pd.DataFrame(index=index, columns=columns)

        for ativo in ativos_dict:
            params = {
                "curr_id": ativos_dict[ativo],
                "smlID": 300004,
                'header': ativo+' Historical Data',
                'st_date': '04/01/2020',
                'end_date': '04/01/2021',
                'interval_sec': 'Daily',
                "sort_col": "date",
                "sort_ord": "DESC",
                "action": "historical_data"
            }
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
            url = "https://www.investing.com/instruments/HistoricalDataAjax"
            r = requests.post(url, headers=head, data=params)
            if r.status_code != 200:
                raise ConnectionError("ERR#0015: error " + str(r.status_code) + ", try again later.")
            root_ = fromstring(r.text)
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()
            if path_:
                for elements_ in path_:
                    if elements_.xpath(".//td")[0].text_content() == 'No results found':
                        raise IndexError("ERR#0080: commodity information unavailable or not found.")
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.get('data-real-value'))
                    commodity_date = datetime.strptime(str(datetime.fromtimestamp(int(info[0]), tz=pytz.timezone('GMT')).date()), '%Y-%m-%d')
                    
                    commodity_close = float(info[1].replace(',', ''))
                    commodity_open = float(info[2].replace(',', ''))
                    commodity_high = float(info[3].replace(',', ''))
                    commodity_low = float(info[4].replace(',', ''))
                    commodity_volume = int(info[5])
                    # result.insert(len(result),
                    #               Data(commodity_date, commodity_open, commodity_high, commodity_low,
                    #                    commodity_close, commodity_volume, currency, None))
                    result.insert(len(result),{'Data':commodity_date,ativo:commodity_close})
                # if order in ['ascending', 'asc']:
                    result = result[::-1]
                # elif order in ['descending', 'desc']:
                #     result = result
                # if as_json is True:
                #     json_ = {
                #         'name': name,
                #         'recent':
                #             [value.commodity_as_json() for value in result]
                #     }
                #     print(json.dumps(json_, sort_keys=False))
                # elif as_json is False:
                    df = pd.DataFrame.from_records([value for value in result])
                    df.set_index("Data", inplace=True)
            else:
                raise RuntimeError("ERR#0004: data retrieval error while scraping.")
            df_[ativo] = df[ativo].fillna(method='ffill')

        return df_.dropna()


