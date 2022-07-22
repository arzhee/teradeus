from web3 import Web3
import json

class Teradeus:
    def __init__(self, rpc, debug = False):
        self.abi = json.loads(open('erc20.json', 'r').read())

        self.debug = debug

        self.tokens = json.loads(open('tokens.json', 'r').read())

        self.w3 = Web3(Web3.HTTPProvider(rpc))

    def __decimal__(self, token):
        contract = self.w3.eth.contract(address = token, abi = self.abi)

        return contract.functions.decimals().call()

    def __total__(self, token):
        contract = self.w3.eth.contract(address = token, abi = self.abi)

        return contract.functions.balanceOf(self.me).call()

    def amount(self, amount):
        self.realAmount = float(amount)

        decimals = self.__decimal__(self.sellToken)

        amount = float(amount) * 10**decimals

        self.sellAmount = int(amount)

        return self

    def buy(self, token):
        self.buyToken = self.__checkToken(token)

        return self

    def execute(self, api):
        if self.debug:
            print('[INFO]', 'Performing swap using', api.name + '...')

        if self.__total__(self.sellToken) < self.sellAmount:
            raise SystemError('Insufficient funds.')

        api.wallet(str(self.me))
        api.buy(self.buyToken)
        api.amount(self.sellAmount)
        api.sell(self.sellToken)

        result = api.generate()

        result['tx']['nonce'] = self.w3.eth.getTransactionCount(self.me)

        signed = self.w3.eth.account.sign_transaction(result['tx'], self.private)
        self.w3.eth.send_raw_transaction(signed.rawTransaction)
        hash = self.w3.toHex(self.w3.keccak(signed.rawTransaction))

        decimals = self.__decimal__(self.buyToken)
        buyAmount = int(result['buyAmount'])
        value = float(buyAmount * 10**(decimals * -1))

        data = {}
        data['buy'] = self.buyToken
        data['sell'] = self.sellToken
        data['amount'] = self.realAmount
        data['value'] = '{0:.18f}'.format(value)
        data['chain'] = int(result['chainId'])
        data['price'] = data['amount'] / value
        data['hash'] = hash

        if self.debug:
            print('[PASS]', 'Output from API:')
            print(json.dumps(data, indent = 2))

        return data

    def key(self, key):
        self.private = key

        return self

    def sell(self, token):
        self.sellToken = self.__checkToken(token)

        return self

    def __checkToken(self, token):
        if token in self.tokens:
            token = self.tokens[token]

        return Web3.toChecksumAddress(token)

    def wallet(self, address):
        self.me = self.__checkToken(address)

        return self