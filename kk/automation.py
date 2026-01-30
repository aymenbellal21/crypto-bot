import logging
from exchange_manager import ExchangeManager
from config import config

class SecurityLayer:
    @staticmethod
    def authorize_action(dev_token: str):
        """Checks if the provided developer token is valid."""
        if config.verify_auth(dev_token):
            logging.info("Developer authorization successful.")
            return True
        logging.warning("UNAUTHORIZED ATTEMPT: Developer token invalid.")
        return False

class AutomationEngine:
    def __init__(self, exchange_manager: ExchangeManager):
        self.exchange_manager = exchange_manager

    def automated_withdraw(self, dev_token: str, exchange_name: str, code: str, amount: float, address: str):
        """Executes a transfer but ONLY if developer token is provided."""
        if not SecurityLayer.authorize_action(dev_token):
            return {"status": "error", "message": "Unauthorized: Developer token required"}
        
        try:
            result = self.exchange_manager.execute_transfer(exchange_name, code, amount, address)
            return {"status": "success", "data": result}
        except Exception as e:
            logging.error(f"Transfer failed: {e}")
            return {"status": "error", "message": str(e)}
