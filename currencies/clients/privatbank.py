from currencies.api_client import APIBaseClient


class PrivatBank(APIBaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def exchange(self) -> list:
        """
        [
            {"ccy":"EUR","base_ccy":"UAH","buy":"40.55000","sale":"41.55000"},
            {"ccy":"USD","base_ccy":"UAH","buy":"37.22000","sale":"37.72000"}
        ]
        :return: dict
        [
            {'code': 'EUR', "rate":"41.55000"},
            {'code': 'USD', "rate":"37.72000"},
        ]

        """
        self._request(
            'get',
            params={
                'json': '',
                'exchange': '',
                'coursid': 5
            }
        )
        results = []
        if self.response:
            for i in self.response.json():
                results.append({
                    'code': i['ccy'],
                    'rate': i['sale'],
                })
        return results


privat = PrivatBank()
