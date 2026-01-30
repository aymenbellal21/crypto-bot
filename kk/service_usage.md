# Crypto Security Bot Service Guide

## Overview
This bot is a professional security and monitoring tool designed for crypto platforms and enterprises. It provides real-time transaction tracking, automated fund management, and developer-authorized transfers.

## Commercial Features
- **Multi-tenancy**: Manage multiple clients from a single instance using `clients.json`.
- **Admin CLI**: Manage your business with `admin_cli.py`.

## Administration Tasks
- **List Clients**: `python admin_cli.py list`
- **Add New Client**: `python admin_cli.py add_client company_b "Company Beta" beta_dev_token`
- **Add API Key**: `python admin_cli.py add_key company_b binance YOUR_KEY YOUR_SECRET`
- **Trigger Manual Withdrawal**: `python admin_cli.py withdraw [client_id] [exchange] [symbol] [amount] [address]`
- **View Transaction History**: `python admin_cli.py history`

## Setup for Clients
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `clients.json` using the Admin CLI or manually.
3. Run the bot: `python bot.py`

## Developer Authorization
Critical actions like `automated_withdraw` in `automation.py` will always check for the `DEVELOPER_AUTH_TOKEN` before execution.

---
*Developed as a premium service/product.*
