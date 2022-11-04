from uniswap_v3.reports.contracts import UniswapPoolContract, UniswapPoolContractPolygon, UniswapFactory
from uniswap_v3.reports.abis import abis


contracts = {}

# Factory
factory_address = '0x1F98431c8aD98523631AE4a59f267346ea31F984'
contracts['factory'] = UniswapFactory(factory_address, ABI=abis['factory'])

##

abi = abis['pool']

###

address = '0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8'
contracts['USDCWETH_0.3'] = UniswapPoolContract(address, ABI=abi)

###

address = '0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640'
contracts['USDCWETH_0.05'] = UniswapPoolContract(address, ABI=abi)

###

address = '0xCBCdF9626bC03E24f779434178A73a0B4bad62eD'
contracts['WETHWBTC_0.3'] = UniswapPoolContract(address, ABI=abi)

###

address = '0x290A6a7460B308ee3F19023D2D00dE604bcf5B42'
contracts['MATICWETH_0.3'] = UniswapPoolContract(address, ABI=abi)

###

address = '0x4585FE77225b41b697C938B018E2Ac67Ac5a20c0'
contracts['WETHWBTC_0.05'] = UniswapPoolContract(address, ABI=abi)

###

address = '0xc63B0708E2F7e69CB8A1df0e1389A98C35A76D52'
contracts['USDCFRAX_0.05'] = UniswapPoolContract(address, ABI=abi)

###

address = '0x97e7d56A0408570bA1a7852De36350f7713906ec'
contracts['DAIFRAX_0.05'] = UniswapPoolContract(address, ABI=abi)

###

address = '0xcB0C5d9D92f4F2F80cce7aa271a1E148c226e19D'
contracts['DAIRAI_0.05'] = UniswapPoolContract(address, ABI=abi)

###

address = '0x7F567cE133B0B69458fC318af06Eee27642865be'
contracts['USDCmiMATIC_0.05'] = UniswapPoolContractPolygon(address, ABI=abi)

###
