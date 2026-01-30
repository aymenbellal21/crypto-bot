import ccxt
import logging
from typing import Dict, List

class ExchangeManager:
    def __init__(self, exchange_configs: Dict):
        self.exchanges: Dict[str, ccxt.Exchange] = {}
        for name, config in exchange_configs.items():
            if hasattr(ccxt, name):
                exchange_class = getattr(ccxt, name)
                self.exchanges[name] = exchange_class({
                    'apiKey': config.get('apiKey'),
                    'secret': config.get('secret'),
                    'enableRateLimit': True,
                })
                logging.info(f"Initialized exchange: {name}")
            else:
                logging.error(f"Exchange {name} not supported by CCXT")

    def get_balance(self, exchange_name: str):
        if exchange_name in self.exchanges:
            return self.exchanges[exchange_name].fetch_balance()
        return None

    def fetch_recent_transactions(self, exchange_name: str, symbol: str = None):
        """Fetches recent deposits and withdrawals."""
        if exchange_name not in self.exchanges:
            return []
        
        exchange = self.exchanges[exchange_name]
        try:
            # Note: Not all exchanges support fetch_deposits/fetch_withdrawals
            deposits = exchange.fetch_deposits() if exchange.has['fetchDeposits'] else []
            withdrawals = exchange.fetch_withdrawals() if exchange.has['fetchWithdrawals'] else []
            return {"deposits": deposits, "withdrawals": withdrawals}
        except Exception as e:
            logging.error(f"Error fetching transactions from {exchange_name}: {e}")
            return {"deposits": [], "withdrawals": []}

    def execute_transfer(self, exchange_name: str, code: str, amount: float, address: str, tag: str = None):
        """Executes a withdrawal with security checks handled by the calling layer."""
        if exchange_name not in self.exchanges:
            raise ValueError(f"Exchange {exchange_name} not found")
        
        exchange = self.exchanges[exchange_name]
        if not exchange.has['withdraw']:
            raise NotImplementedError(f"Exchange {exchange_name} does not support withdrawals via API")
        
        return exchange.withdraw(code, amount, address, tag)
