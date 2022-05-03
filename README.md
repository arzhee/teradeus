# Oxtrade

Trade cryptocurrencies using the [0x Swap API](https://docs.0x.org/0x-api-swap/api-references).

## Installation

Install `Oxtrade` through [pip](https://pip.pypa.io/en/stable/):

``` bash
$ pip install -r requirements.txt
```

## Basic Usage

### Prerequisites

* Create a file named `.env` and supply the following variables:

```
OXTRADE_ADDRESS=
OXTRADE_PRIVATE=
```

Wherein the `OXTRADE_ADDRESS` is the wallet address that will perform transactions and the `OXTRADE_PRIVATE` is the exported private key. To know on how to export a wallet's private key through Metamask, kindly check this [link](https://metamask.zendesk.com/hc/en-us/articles/360015289632-How-to-Export-an-Account-Private-Key).

**Warning**: __EXPORTING YOUR ACCOUNT COULD BE RISKY AS IT DISPLAYS YOUR PRIVATE KEY IN CLEAR TEXT__. Therefore, you should make sure no one else sees, or otherwise is able to capture a screenshot while you retrieve your private key, to avoid possible loss of your Ether/tokens. Many phishing campaigns would ask for your private key, which would help them gain access to your accounts. You should never share your private key with anyone.

### Trading 

```
$ python trade.py [BUY_TOKEN] [AMOUNT] (SELL_TOKEN)
```

The code above will sell a certain amount (`[AMOUNT]`) of the specified `(SELL_TOKEN)` in order to buy the desired `[BUY_TOKEN]`. Putting `(SELL_TOKEN)` is optional, as the default value of `(SELL_TOKEN)` when not included is the contract address of [USD Coin (PoS)](https://polygonscan.com/token/0x2791bca1f2de4661ed88a30c99a7a9449aa84174).