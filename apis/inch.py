from web3 import Web3
import json
import requests

class OneInch:
    name = '1inch API'

    def __init__(self, url, chain, debug = False):
        self.chain = chain

        self.url = url + '/' + str(chain)

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
        data['fromAddress'] = str(self.me)
        data['toTokenAddress'] = self.buyToken
        data['amount'] = self.sellAmount
        data['fromTokenAddress'] = self.sellToken
        data['slippage'] = 1

        try:
            link = self.url + '/swap'

            if self.debug:
                print('[INFO]', 'Accessing', link + '...')

            result = requests.get(link, data).json()

            if self.debug:
                print('[PASS]', 'Output from link:')
                print(json.dumps(result, indent = 2))

            if 'statusCode' in result:
                error = result['description']

                raise SystemError(str(error))
        except Exception as error:
            raise SystemError(str(error))

        tx = {}
        tx['chainId'] = int(self.chain)
        tx['data'] = result['tx']['data']
        tx['from'] = Web3.toChecksumAddress(result['tx']['from'])
        tx['gas'] = int(result['tx']['gas'])
        tx['maxFeePerGas'] = int(result['tx']['gasPrice'])
        tx['maxPriorityFeePerGas'] = int(result['tx']['gasPrice'])
        tx['to'] = Web3.toChecksumAddress(result['tx']['to'])
        tx['type'] = '0x2'
        tx['value'] = int(result['tx']['value'])

        data = {}
        data['chainId'] = self.chain
        data['buyAmount'] = result['toTokenAmount']
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