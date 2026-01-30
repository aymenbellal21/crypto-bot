import os
import json
from dotenv import load_dotenv

class Config:
    def __init__(self, clients_file="clients.json"):
        load_dotenv()
        self.clients_file = clients_file
        self.dev_auth_token = os.getenv("DEVELOPER_AUTH_TOKEN")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.report_auto_generate = os.getenv("REPORT_AUTO_GENERATE", "true").lower() == "true"
        
        self.clients = self._load_clients()

    def _load_clients(self):
        """Loads all client configurations from the JSON file."""
        if not os.path.exists(self.clients_file):
            return []
        with open(self.clients_file, 'r') as f:
            return json.load(f)

    def verify_auth(self, token: str) -> bool:
        """Verifies if the provided token matches the global Developer Auth Token."""
        if not self.dev_auth_token:
            return False
        return token == self.dev_auth_token

config = Config()
