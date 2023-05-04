from currencies.api_client import APIBaseClient


class Monobank(APIBaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'

    def exchange(self) -> list:
        """
        [
            {"currencyCodeA":840,"currencyCodeB":980,"date":1683151274,"rateBuy":36.65,"rateCross":0,"rateSell":37.4406},
            {"currencyCodeA":978,"currencyCodeB":980,"date":1683181874,"rateBuy":40.61,"rateCross":0,"rateSell":41.8008},
            ...

        ]
        :return: dict
        [
            {'code': 'USD', 'rate': '37.4406'},
            {'code': 'EUR', 'rate': '41.8008'},

        ]
        """
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
        print(self.base_url, results)
        return results


mono = Monobank()
