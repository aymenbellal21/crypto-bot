import logging
import sys
from config import config
from exchange_manager import ExchangeManager
from monitor import Monitor
from automation import AutomationEngine
from reporter import Reporter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class CryptoSecurityBot:
    def __init__(self):
        self.clients = []
        for client_config in config.clients:
            logging.info(f"Setting up bot for client: {client_config['client_name']}")
            ex_manager = ExchangeManager(client_config['api_keys'])
            self.clients.append({
                "config": client_config,
                "ex_manager": ex_manager,
                "monitor": Monitor(ex_manager),
                "automation": AutomationEngine(ex_manager)
            })

    def run(self):
        logging.info("Bot is starting for all clients...")
        try:
            for client in self.clients:
                client['monitor'].start_monitoring(interval=5)
            
            # In a real scenario, this would be non-blocking or multi-threaded
            # For this MVP, we'll just simulate a run
        except KeyboardInterrupt:
            for client in self.clients:
                client['monitor'].stop_monitoring()
            self.generate_final_reports()

    def generate_final_reports(self):
        logging.info("Generating final reports for all clients...")
        for client in self.clients:
            client_id = client['config']['client_id']
            data = client['monitor'].get_summary()
            Reporter.generate_csv_report(data, filename=f"report_{client_id}.csv")
            Reporter.generate_pdf_report(data, filename=f"report_{client_id}.pdf")
            logging.info(f"Reports generated for {client_id}")

if __name__ == "__main__":
    bot = CryptoSecurityBot()
    bot.run()
