import json
import base64

from abc import ABC
from web3 import Web3

from uniswap_v3.tokens import tokens


class ProviderInitException(Exception):
    pass


class AbstractContract(ABC):
    # class Contract is a template for any
    # EVM based contract and initializing with contract address and ABI.
    # Address and ABI can be found on blockchain explorer sush as https://etherscan.io

    provider = None

    def __init__(self, address: str, ABI: str):

        if self.provider is not None:
            w3 = Web3(Web3.HTTPProvider(self.provider))
        else:
            raise ProviderInitException

        try:
            self.contract = w3.eth.contract(address, abi=ABI)
        except Exception as e:
            print(f'{e} in contract {address}')

    @property
    def address(self):
        return self.contract.address

    @property
    def abi(self):
        return self.contract.abi

    def get_functions_list(self) -> list:
        return self.contract.all_functions()


class Contract(AbstractContract):
    provider = 'https://node'


class UniswapPoolContract(Contract):
    
    def get_tick(self) -> int:
        return self.contract.functions.slot0().call()[1]
    
    def get_token0(self) -> str:
        return self.contract.functions.token0().call()
    
    def get_token1(self) -> str:
        return self.contract.functions.token1().call()

    def get_price(self, notional_token_address) -> float:
        token0_address = self.get_token0()
        token1_address = self.get_token1()
        token0 = tokens[token0_address]
        token1 = tokens[token1_address]
        x96price = int(self.contract.functions.slot0().call()[0])

        # Price according to https://docs.uniswap.org/sdk/guides/fetching-prices
        price_in_token1 = x96price ** 2 * 10 ** token0['decimals'] / 10 ** token1['decimals'] / 2 ** 192
        if notional_token_address == token1_address:
            price = price_in_token1
        elif notional_token_address == token0_address:
            price = 1 / price_in_token1
        else:
            raise Exception(f'Wrong notional for this pool ({notional_token_address}).'
                            f'Should be either "{token0_address}" or "{token1_address}"')
        return price


class UniswapPositionContract(Contract):
    
    def get_position(self, token_id: int) -> list:
        return self.contract.functions.positions(token_id).call()
    
    def get_positions_number(self, address: str) -> int:
        return self.contract.functions.balanceOf(address).call()
    
    def get_token_id(self, address: str, index: int) -> int:
        return self.contract.functions.tokenOfOwnerByIndex(address, index).call()
    
    def get_pool_symbol(self, token_id: str) -> str:
        uri = self.contract.functions.tokenURI(token_id).call().split(',')[1]
        decoded = base64.b64decode(uri).decode('utf-8')
        name = json.loads(decoded)['name']
        pool = name.split('-')[2].strip().replace('/', '')
        fee = name.split('-')[1].strip()
        return pool + '_' + fee.replace('%', '')


class UniswapFactory(Contract):

    def get_pool(self, token0_address, token1_address, fee) -> str:
        return self.contract.functions.getPool(token0_address, token1_address, fee).call()


class FeesCalculator:
    """ Uniswap V3 functions """

    def __init__(self, pool):
        self.pool = pool

    def fo0(self, tick):
        return self.pool.contract.functions.ticks(tick).call()[2]

    def fo1(self, tick):
        return self.pool.contract.functions.ticks(tick).call()[3]

    @staticmethod
    def fa(tick, tick_c, fg, fo):
        if tick_c >= tick:
            return fg - fo(tick)
        return fo(tick)

    @staticmethod
    def fb(tick, tick_c, fg, fo):
        if tick_c >= tick:
            return fo(tick)
        return fg - fo(tick)

    def fr(self, fg, fo, tick_c, tick_u, tick_l):
        return fg - self.fb(tick_l, tick_c, fg, fo) - self.fa(tick_u, tick_c, fg, fo)

    def fu(self, l, fg, fo, tick_c, tick_u, tick_l, fr_t0):
        dfr = (self.fr(fg, fo, tick_c, tick_u, tick_l) - fr_t0)

        # fancy maths
        if dfr < 0:
            dfr += 2 ** 256

        return l * dfr
