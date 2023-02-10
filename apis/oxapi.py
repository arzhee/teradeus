from web3 import Web3
import json
import requests

class OxApi:
    name = '0x API'

    def __init__(self, url, debug = False):
        self.url = url

        self.debug = debug

    def amount(self, amount):
        self.sellAmount = amount

        return self

    def buy(self, token):
        self.buyToken = token

        return self
    
    def buyDecimals(self, decimals):
        self.buyDecimals = decimals

        return self

    def generate(self):
        data = {}
        data['takerAddress'] = str(self.me)
        data['buyToken'] = self.buyToken
        data['sellAmount'] = self.sellAmount
        data['sellToken'] = self.sellToken

        try:
            link = self.url + '/swap/v1/quote'

            if self.debug:
                print('[INFO]', 'Accessing', link + '...')

            result = requests.get(link, data).json()

            if self.debug:
                print('[PASS]', 'Output from link:')
                print(json.dumps(result, indent = 2))

            if 'code' in result:
                error = result['values']['message']

                raise SystemError(str(error))
        except Exception as error:
            raise SystemError(str(error))

        tx = {}
        tx['chainId'] = int(result['chainId'])
        tx['data'] = result['data']
        tx['from'] = Web3.toChecksumAddress(result['from'])
        tx['gas'] = int(result['gas'])
        tx['maxFeePerGas'] = int(result['gasPrice'])
        tx['maxPriorityFeePerGas'] = int(result['gasPrice'])
        tx['to'] = Web3.toChecksumAddress(result['to'])
        tx['type'] = '0x2'
        tx['value'] = int(result['value'])

        data = {}
        data['chainId'] = result['chainId']
        data['buyAmount'] = result['buyAmount']
        data['tx'] = tx

        return data

    def sell(self, token):
        self.sellToken = token

        return self
    
    def sellDecimals(self, decimals):
        self.sellDecimals = decimals

        return self

    def wallet(self, address):
        self.me = address

        return self