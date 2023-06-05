from core.clients_api import APIBaseClient


class MonoBankClient(APIBaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'

    def parse(self) -> list:
        # [ {'currencyCodeA': 840, 'currencyCodeB': 980, 'rateSell': 37.4406},
        #   {'currencyCodeA': 978, 'currencyCodeB': 980, 'rateSell': 41.8008},
        # ] ->
        # [ {'code': 'UAH', 'rate': '1.0000'},
        #   {'code': 'USD', 'rate': '37.4406'},
        #   {'code': 'EUR', 'rate': '41.8008'},
        # ]
        self._request('get')
        results = []
        if self.response:
            for i in self.response.json():
                if i['currencyCodeA'] == 840 and i['currencyCodeB'] == 980:
                    results.append({
                        'code': 'USD',
                        'rate': i['rateSell'],
                    })
                if i['currencyCodeA'] == 978 and i['currencyCodeB'] == 980:
                    results.append({
                        'code': 'EUR',
                        'rate': i['rateSell'],
                    })
            results.append({'code': 'UAH', 'rate': '1.0000'})
        return results


monobank_client = MonoBankClient()
