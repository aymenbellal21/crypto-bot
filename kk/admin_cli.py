import json
import os
import sys

CLIENTS_FILE = "clients.json"

def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        return []
    with open(CLIENTS_FILE, 'r') as f:
        return json.load(f)

def save_clients(clients):
    with open(CLIENTS_FILE, 'w') as f:
        json.dump(clients, f, indent=4)

def add_client(client_id, client_name, dev_auth_token):
    clients = load_clients()
    clients.append({
        "client_id": client_id,
        "client_name": client_name,
        "api_keys": {},
        "dev_auth_token": dev_auth_token
    })
    save_clients(clients)
    print(f"Client {client_name} added successfully.")

def add_api_key(client_id, exchange_name, api_key, secret):
    clients = load_clients()
    for client in clients:
        if client['client_id'] == client_id:
            client['api_keys'][exchange_name] = {
                "apiKey": api_key,
                "secret": secret
            }
            save_clients(clients)
            print(f"API key for {exchange_name} added to client {client_id}.")
            return
    print(f"Client {client_id} not found.")

def list_clients():
    clients = load_clients()
    for client in clients:
        print(f"ID: {client['client_id']}, Name: {client['client_name']}, Exchanges: {list(client['api_keys'].keys())}")

from exchange_manager import ExchangeManager
from automation import AutomationEngine

def manual_withdraw(client_id, exchange_name, code, amount, address):
    clients = load_clients()
    for client in clients:
        if client['client_id'] == client_id:
            ex_manager = ExchangeManager(client['api_keys'])
            engine = AutomationEngine(ex_manager)
            # Use the client's own dev_auth_token for the manual trace
            result = engine.automated_withdraw(client['dev_auth_token'], exchange_name, code, float(amount), address)
            print(f"Withdrawal result: {result}")
            return
    print(f"Client {client_id} not found.")

def show_history():
    if os.path.exists("history.json"):
        with open("history.json", 'r') as f:
            history = json.load(f)
            for entry in history[-20:]: # Show last 20 entries
                print(f"[{entry['timestamp']}] {entry['exchange']}: {entry['status']}")
    else:
        print("No history found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python admin_cli.py [list|add_client|add_key|withdraw|history]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        list_clients()
    elif cmd == "add_client":
        add_client(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "add_key":
        add_api_key(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "withdraw":
        # python admin_cli.py withdraw [client_id] [exchange] [symbol] [amount] [address]
        manual_withdraw(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif cmd == "history":
        show_history()
