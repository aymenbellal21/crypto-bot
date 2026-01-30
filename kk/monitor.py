import logging
import time
import json
import os
from exchange_manager import ExchangeManager

class Monitor:
    def __init__(self, exchange_manager: ExchangeManager, history_file="history.json"):
        self.exchange_manager = exchange_manager
        self.history_file = history_file
        self.active = False
        self.logs = self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Error loading history: {e}")
                return []
        return []

    def _save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.logs, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving history: {e}")

    def start_monitoring(self, interval: int = 60):
        """Starts a polling-based monitor."""
        self.active = True
        logging.info("Security Monitoring started...")
        
        while self.active:
            for ex_name in self.exchange_manager.exchanges:
                logging.info(f"Scanning {ex_name} for new transactions...")
                txs = self.exchange_manager.fetch_recent_transactions(ex_name)
                
                # In a real scenario, we would filter for ONLY new txs here
                entry = {
                    "timestamp": time.time(),
                    "exchange": ex_name,
                    "status": "Scan completed",
                    "data": txs
                }
                self.logs.append(entry)
                self._save_history() # Persist immediately
                
            time.sleep(interval)

    def stop_monitoring(self):
        self.active = False
        logging.info("Security Monitoring stopped.")

    def get_summary(self):
        return self.logs
