# Teradeus

Trade cryptocurrencies using [0x Swap API](https://docs.0x.org/0x-api-swap/api-references) or [1inch Swap API](https://docs.1inch.io/docs/aggregation-protocol/introduction).

## Installation

Install `Teradeus` through [pip](https://pip.pypa.io/en/stable/):

``` bash
$ pip install -r requirements.txt
```

## Basic Usage

### Prerequisites

* Copy `.env.example`, paste it as `.env`, and supply the following empty variables below:

```
TERADEUS_ADDRESS=
TERADEUS_PRIVATE=
TERADEUS_SUCCESS=
TERADEUS_RPC=https://polygon-rpc.com
TERADEUS_SELLTOKEN=USDC
TERADEUS_API=0XAPI
TERADEUS_DEBUG=false

INCH_URL=https://api.1inch.io/v4.0
INCH_CHAIN=137

OXAPI_URL=https://polygon.api.0x.org
```

Wherein the `TERADEUS_ADDRESS` is the wallet address that will perform transactions and the `TERADEUS_PRIVATE` is the exported private key. To know on how to export a wallet's private key through Metamask, kindly check this [link](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key).

**Warning**: __EXPORTING YOUR ACCOUNT COULD BE RISKY AS IT DISPLAYS YOUR PRIVATE KEY IN CLEAR TEXT__. Therefore, you should make sure no one else sees, or otherwise is able to capture a screenshot while you retrieve your private key, to avoid possible loss of your Ether/tokens. Many phishing campaigns would ask for your private key, which would help them gain access to your accounts. You should never share your private key with anyone.

For `TERADEUS_SUCCESS`, it is an URL wherein Teradeus can pass data (e.g, `price`, `amount`, `value`) after the transaction is put to the network. It can be useful in collecting data such as getting average price per trade.

The `TERADEUS_API` specifies the implementation to be used when swapping assets. By default it uses the [0x Swap API](https://docs.0x.org/0x-api-swap/api-references) (`0XAPI`) but a [1inch Swap API](https://docs.1inch.io/docs/aggregation-protocol/introduction) implementation is also available (`1INCH`).

To specify a default token to sell, update the `TERADEUS_SELLTOKEN` variable. If not specified or empty, it will use the contract address of [USD Coin (PoS)](https://polygonscan.com/token/0x2791bca1f2de4661ed88a30c99a7a9449aa84174) by default.

For debugging purposes, the `TERADEUS_DEBUG` can be enabled to display JSON dump result from the swap implementations.

### Trading 

```
$ python swap.py [BUY_TOKEN] [AMOUNT] (SELL_TOKEN)
```

The code above will sell a certain amount (`[AMOUNT]`) of the specified `(SELL_TOKEN)` in order to buy the desired `[BUY_TOKEN]`. Putting `(SELL_TOKEN)` is optional, as the default value of `(SELL_TOKEN)` when not included is the contract address specified in the `TERADEUS_SELLTOKEN` variable in the `.env` file.