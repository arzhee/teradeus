from web3 import Web3
import json
import requests

class Pswap:
    name = 'Paraswap API'

    def __init__(self, url, chain, debug = False):
        self.chain = chain

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
        data['srcToken'] = self.sellToken
        data['srcDecimals'] = self.sellDecimals
        data['destToken'] = self.buyToken
        data['destDecimals'] = self.buyDecimals
        data['amount'] = self.sellAmount
        data['userAddress'] = str(self.me)
        data['network'] = int(self.chain)

        try:
            # Get first a price from the /price endpoint --------
            link = self.url + '/prices'

            if self.debug:
                print('[INFO]', 'Getting price (' + link + ')...')

                print('[INFO]', 'Data:')

                print(json.dumps(data, indent = 2))

            result = requests.get(link, data).json()

            if self.debug:
                print('[PASS]', 'Output from link:')
                print(json.dumps(result, indent = 2))

            if 'error' in result:
                raise SystemError(str(result['error']))
            # ---------------------------------------------------

            priceRoute = result['priceRoute']
            buyAmount = priceRoute['destAmount']

            # Generate web3 object through /transaction -------
            link = self.url + '/transactions/' + self.chain

            if self.debug:
                print('[INFO]', 'Creating tx [', link + ']...')

                print('[INFO]', 'Data:')

                print(json.dumps(data, indent = 2))

            data = {}
            data['srcToken'] = self.sellToken
            data['srcDecimals'] = self.sellDecimals
            data['destToken'] = self.buyToken
            data['destDecimals'] = self.buyDecimals
            data['srcAmount'] = self.sellAmount
            data['userAddress'] = str(self.me)
            data['priceRoute'] = priceRoute
            data['slippage'] = 50

            result = requests.post(link, json = data).json()

            if self.debug:
                print('[PASS]', 'Output from link:')
                print(json.dumps(result, indent = 2))

            if 'error' in result:
                raise SystemError(str(result['error']))
            # -------------------------------------------------
        except Exception as error:
            raise SystemError(str(error))

        tx = {}
        tx['chainId'] = int(self.chain)
        tx['data'] = result['data']
        tx['from'] = Web3.toChecksumAddress(result['from'])
        tx['gas'] = int(result['gas'])
        tx['maxFeePerGas'] = int(result['gasPrice'])
        tx['maxPriorityFeePerGas'] = int(result['gasPrice'])
        tx['to'] = Web3.toChecksumAddress(result['to'])
        tx['type'] = '0x2'
        tx['value'] = int(result['value'])

        data = {}
        data['chainId'] = self.chain
        data['buyAmount'] = buyAmount
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