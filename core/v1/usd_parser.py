from typing import Set

import requests
from bs4 import BeautifulSoup, element
from bs4.element import AttributeValueList
from faker import Faker
from websockets.headers import parse_extension

fake = Faker()
URL = "https://minfin.com.ua/ua/currency/converter/usd-uah/?val1=1&val2=40.8"

def getFakeUserAgent():
    return fake.user_agent()


def parseCurrency() -> list[float]|None: # parse 1 to many currency (1 dollar for many uah)
    userAgent = {
        'User-agent': getFakeUserAgent()
    }

    req = requests.get(URL, headers=userAgent)

    if req.status_code != 200: return None

    soup = BeautifulSoup(req.text, 'html.parser')
    parsing_result: list[element.Tag] = soup.find_all('input', class_='cNCStF')

    if len(parsing_result) != 2: return None

    from_usd_k = float(parsing_result[0].get('value'))
    to_usd_k = float(parsing_result[1].get('value'))

    uah2uad_k: float = float(from_usd_k) / float(to_usd_k)

    return [
        from_usd_k, to_usd_k, uah2uad_k
    ]


# test for parser
def test():
    _, uah_to_usd, currencyK = parseCurrency()

    # convert 1000 uah to usd
    uah2usd_1000 = 1000 * currencyK
    usd2uah_1000 = 1000 / currencyK

    print(f'1 USD is {uah_to_usd} UAH now')
    print('1000 UAH in USD: ', uah2usd_1000)
    print('1000 USD in UAH: ', usd2uah_1000)


if __name__ == '__main__': test()