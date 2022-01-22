from functools import lru_cache
from typing import Union

import brownie
from eth_typing.evm import Address, BlockNumber
from y.constants import STABLECOINS
from y.contracts import Contract

from ypricemagic.price_modules import *
from ypricemagic.price_modules.aave import aave
from ypricemagic.price_modules.compound import compound
from ypricemagic.price_modules.balancer.balancer import balancer
from ypricemagic.price_modules.chainlink.chainlink import chainlink
from ypricemagic.price_modules.curve import curve
from ypricemagic.price_modules.uniswap.uniswap import uniswap


@lru_cache(maxsize=None)
def check_bucket(
    token_address: Union[str, Address, brownie.Contract, Contract]
    ):

    if type(token_address) != str:
        token_address = str(token_address)

    # these require neither calls to the chain nor contract initialization
    if token_address == "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":       return 'wrapped gas coin'
    elif token_address in STABLECOINS:                                      return 'stable usd'

    elif wsteth.is_wsteth(token_address):                                   return 'wsteth'
    elif cream.is_creth(token_address):                                     return 'creth'
    elif belt.is_belt_lp(token_address):                                    return 'belt lp'

    elif froyo.is_froyo(token_address):                                     return 'froyo'
    elif aave.is_atoken(token_address):                                     return 'atoken' 

    # these just require calls
    elif balancer.is_balancer_pool(token_address):                          return 'balancer pool'
    elif yearn.is_yearn_vault(token_address):                               return 'yearn or yearn-like'
    elif ib.is_ib_token(token_address):                                     return 'ib token'

    elif gelato.is_gelato_pool(token_address):                              return 'gelato'
    elif piedao.is_pie(token_address):                                      return 'piedao lp'
    elif tokensets.is_token_set(token_address):                             return 'token set'

    elif ellipsis.is_eps_rewards_pool(token_address):                       return 'ellipsis lp'
    elif mstablefeederpool.is_mstable_feeder_pool(token_address):           return 'mstable feeder pool'

    # these require both calls and contract initializations
    elif uniswap.is_uniswap_pool(token_address):                            return 'uni or uni-like lp'
    elif mooniswap.is_mooniswap_pool(token_address):                        return 'mooniswap lp'
    elif token_address in compound:                                         return 'compound'
    elif token_address in curve:                                            return 'curve lp'
    elif token_address in chainlink:                                        return 'chainlink feed'