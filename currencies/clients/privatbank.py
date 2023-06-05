from core.clients_api import APIBaseClient


class PrivatBankClient(APIBaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def parse(self) -> list:
        # [ { 'ccy': 'EUR', 'sale': '41.55000'},
        #   { 'ccy': 'USD', 'sale': '37.72000'}
        # ] ->
        # [ {'code': 'UAH', 'rate': '1.00000'},
        #   {'code': 'EUR', 'rate': '41.55000'},
        #   {'code': 'USD', 'rate': '37.72000'},
        # ]
        self._request('get', params={'json': '', 'exchange': '', 'coursid': 5}) # noqa
        results = []
        if self.response:
            for i in self.response.json():
                results.append({
                    'code': i['ccy'],
                    'rate': i['sale'],
                })
            results.append({'code': 'UAH', 'rate': '1.0000'})
        return results


privatbank_client = PrivatBankClient()
