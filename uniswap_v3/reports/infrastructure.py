from uniswap_v3.reports.contracts import *
from uniswap_v3.reports.abis import abis


contracts = {}

###

abi = abis['position_NFT']

address = '0xC36442b4a4522E871399CD717aBDD847Ab11FE88'
contracts['Positions_NFT'] = UniswapPositionContract(address, ABI=abi)

###
