from dotenv import load_dotenv
from web3 import Web3
import json
import os
import requests
import sys

ox = 'https://polygon.api.0x.org'
rpc = 'https://polygon-rpc.com'

path = os.path.dirname(os.path.abspath(__file__))
file = path + '/erc20.json'
abi = json.loads(open(file, 'r').read())

w3 = Web3(Web3.HTTPProvider(rpc))

load_dotenv(dotenv_path = path + '/.env')
me = os.getenv('TERADEUS_ADDRESS')
key = os.getenv('TERADEUS_PRIVATE')
me = Web3.toChecksumAddress(me)

usdc = '0x2791bca1f2de4661ed88a30c99a7a9449aa84174'
usdc = Web3.toChecksumAddress(usdc)

if len(sys.argv[1:]) == 3:
    usdc = Web3.toChecksumAddress(sys.argv[3])

tokens = {}
tokens['KLIMA'] = '0x4e78011Ce80ee02d2c3e649Fb657E45898257815'
tokens['QI'] = '0x580A84C73811E1839F75d86d75d88cCa0c241fF4'
tokens['stMATIC'] = '0x3a58a54c066fdc0f2d55fc9c89f0415c92ebf3c4'
tokens['TETU'] = '0x255707B70BF90aa112006E1b07B9AeA6De021424'
tokens['WBTC'] = '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6'
tokens['WETH'] = '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619'
tokens['WMATIC'] = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'

if sys.argv[1] in tokens:
    token = Web3.toChecksumAddress(tokens[sys.argv[1]])
else:
    token = Web3.toChecksumAddress(sys.argv[1])

sell = w3.eth.contract(address = usdc, abi = abi)
num = sell.functions.decimals().call()
total = sell.functions.balanceOf(me).call()
amount = int(float(sys.argv[2]) * 10**num)

if total < amount:
    print('[FAIL]', 'Insufficient funds.')

    sys.exit()

data = {}
data['takerAddress'] = me
data['buyToken'] = token
data['sellAmount'] = amount
data['sellToken'] = usdc

link = ox + '/swap/v1/quote'
result = requests.get(link, data).json()

tx = {}
tx['chainId'] = result['chainId']
tx['data'] = result['data']
tx['from'] = Web3.toChecksumAddress(result['from'])
tx['gas'] = int(result['gas'])
tx['maxFeePerGas'] = int(result['gasPrice'])
tx['maxPriorityFeePerGas'] = int(result['gasPrice'])
tx['nonce'] = w3.eth.getTransactionCount(me)
tx['to'] = Web3.toChecksumAddress(result['to'])
tx['type'] = '0x2'
tx['value'] = int(result['value'])

signed = w3.eth.account.sign_transaction(tx, key)
w3.eth.send_raw_transaction(signed.rawTransaction)
hash = w3.toHex(w3.keccak(signed.rawTransaction))

buy = w3.eth.contract(address = token, abi = abi)
num = buy.functions.decimals().call()
buy = int(result['buyAmount'])
value = float(buy * 10**(num * -1))

if os.getenv('TERADEUS_SUCCESS'):
    data = {}
    data['buy'] = token
    data['sell'] = usdc
    data['amount'] = float(sys.argv[2])
    data['value'] = '{0:.18f}'.format(value)
    data['chain'] = int(result['chainId'])
    data['price'] = data['amount'] / value
    data['hash'] = hash

    link = os.getenv('TERADEUS_SUCCESS')

    requests.post(link, data)