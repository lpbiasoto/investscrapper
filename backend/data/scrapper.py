import pandas as pd
from bs4 import BeautifulSoup
import requests
import pytz
from datetime import datetime, timedelta
from lxml.html import fromstring

class HistoricalDataScrapper():

    def get_data(self,start_date,end_date,ativos_dict):
        index = pd.date_range(start_date, end = end_date, freq='D')
        columns = [ativo for ativo in ativos_dict]
        df_ = pd.DataFrame(index=index, columns=columns)

        for ativo in ativos_dict:
            params = {
                "curr_id": ativos_dict[ativo],
                "smlID": 300004,
                'header': ativo+' Historical Data',
                'st_date': start_date.strftime("%m/%d/%Y"),
                'end_date': end_date.strftime("%m/%d/%Y"),
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
                raise ConnectionError("Erro" + str(r.status_code) + ", tente novamente mais tarde.")
            root_ = fromstring(r.text)
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()
            if path_:
                for elements_ in path_:
                    if elements_.xpath(".//td")[0].text_content() == 'No results found':
                        raise IndexError("Dados do ativo não disponíveis ou não encontrados.")
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.get('data-real-value'))
                    date = datetime.strptime(str(datetime.fromtimestamp(int(info[0]), tz=pytz.timezone('GMT')).date()), '%Y-%m-%d')
                    
                    close = float(info[1].replace(',', ''))
                    open = float(info[2].replace(',', ''))
                    high = float(info[3].replace(',', ''))
                    low = float(info[4].replace(',', ''))
                    volume = int(info[5])
                    result.insert(len(result),{'Data':date,ativo:close})
                    result = result[::-1]
                    df = pd.DataFrame.from_records([value for value in result])
                    df.set_index("Data", inplace=True)
            else:
                raise RuntimeError("Erro ao tentar obter os dados.")
            df_[ativo] = df[ativo].fillna(method='ffill')
        return df_.dropna()