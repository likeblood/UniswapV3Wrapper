from dataclasses import dataclass


@dataclass
class Token:
    """
    Token data structure
    """
    address: str
    decimals: str
    symbol: str
    chain: str
        

def symbol_to_token(symbol: str) -> Token:
    tokens = {
                'BUSD': Token('0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56', 18, 'BUSD', 'bsc'),
                'USDT': Token('0x55d398326f99059fF775485246999027B3197955', 18, 'BUSD', 'bsc'),
             }
    return tokens[symbol]