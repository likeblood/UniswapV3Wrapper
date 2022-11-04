from datetime import datetime

import pandas as pd

from uniswap_v3.reports.contracts import FeesCalculator
from uniswap_v3.reports.infrastructure import contracts as infrastructure_contracts
from uniswap_v3.reports.pools import contracts as pools

from uniswap_v3.utils import get_symbol_price
from uniswap_v3.tokens import tokens

def get_report_uniswap_v3(address: str, pool_symbol=None, notional='USDT', get_symbol_price=get_symbol_price) -> pd.DataFrame:
    
    UTCNOW = datetime.utcnow()
    df = pd.DataFrame()
    TICK_BASE = 1.0001 # whitepaper
    
    positions = infrastructure_contracts['Positions_NFT']
    N_placements = positions.get_positions_number(address)
    
    # get all UNI-POS NFT id by address
    placements = []
    for i in range(N_placements):
        placements.append(positions.get_token_id(address, i))
    
    for token_id in placements:
        
        try:
            symbol = positions.get_pool_symbol(token_id)
            pool = pools[symbol]
            
            # position info
            token0 = pool.get_token0()
            token1 = pool.get_token1()

            symbol = tokens[token0]['symbol'] + tokens[token1]['symbol'] + '_' +\
                        str(pool.contract.functions.fee().call() / 10**4)
            
            if symbol != pool_symbol:
                continue
            
            decimal0 = tokens[token0]['decimals']
            decimal1 = tokens[token1]['decimals']
            
            tick = pool.get_tick()
            position = positions.get_position(token_id)
            tick_lower = position[5]
            tick_upper = position[6]
            liquidity = position[7]
        
            sqrt_price = TICK_BASE ** (tick / 2)
            sqrt_price_l = TICK_BASE ** (tick_lower / 2)
            sqrt_price_u = TICK_BASE ** (tick_upper / 2)
            
            if tick < tick_lower:
                token0_amount = liquidity * (1 / sqrt_price_l - 1 / sqrt_price_u)
                token1_amount = 0
            elif tick > tick_upper:
                token0_amount = 0
                token1_amount = liquidity * (sqrt_price_u - sqrt_price_l)
            else:
                token0_amount = liquidity * (1 / sqrt_price - 1 / sqrt_price_u)
                token1_amount = liquidity * (sqrt_price - sqrt_price_l)
        
            token0_amount /= (10 ** decimal0)
            token1_amount /= (10 ** decimal1)
            
            # fees info
            fees_calculator = FeesCalculator(pool)

            scaler = (1 << 128)

            fg0 = pool.contract.functions.feeGrowthGlobal0X128().call()
            fg1 = pool.contract.functions.feeGrowthGlobal1X128().call()
            
            fr0_t0 = position[8]
            fr1_t0 = position[9]
            
            fees0_amount = fees_calculator.fu(liquidity, fg0, fees_calculator.fo0,
                                              tick, tick_upper, tick_lower, fr0_t0) / scaler / (10 ** decimal0)
            fees1_amount = fees_calculator.fu(liquidity, fg1, fees_calculator.fo1,
                                              tick, tick_upper, tick_lower, fr1_t0) / scaler / (10 ** decimal1)
            
                        
            token0_price = get_symbol_price(tokens[token0]['symbol'] + notional)
            token1_price = get_symbol_price(tokens[token1]['symbol'] + notional)
            
            if token0_amount or token1_amount or fees0_amount or fees1_amount:
                df = df.append({'pool': symbol,
                                'token_id': token_id,
                                'range_lower': 10**(decimal1-decimal0) * (1/sqrt_price_u)**2,
                                'range_upper': 10**(decimal1-decimal0) * (1/sqrt_price_l)**2,
                                'token1_quantity': token0_amount,
                                'token2_quantity': token1_amount,
                                'position_in_pool': token0_amount * token0_price +\
                                                    token1_amount * token1_price,
                                'fees1_quantity': fees0_amount,
                                'fees2_quantity': fees1_amount,
                                'fees': fees0_amount * token0_price +\
                                        fees1_amount * token1_price,
                                'notional': notional,
                                'protocol': 'uniswap_v3'
                               }, ignore_index=True)

            df['token'] = None
            df['token_quantity'] = None
            df['token_in_notional'] = None
                                
        except Exception as e:
            print(e)
            continue
            
    df['timestamp'] = UTCNOW
    
    return df
