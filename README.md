# Value project

Django app to track $VALUE contracts.

## Edit `settings.py`

Edit this file to run the code on your own server:

- Update `SECRET_KEY` and `ALLOWED_HOSTS` in `settings.py`.
- To connect to your database, edit `DATABASES` to include database name, username and password.

## Gov Vault app

The main app to track gov vault transactions, update database, and create views and charts.

### Infura API

The app uses Infura to access ETH network. Update `infura_url` in `govvault/chain_db_functions.py` with your API key.

## Commands

Commands to update database can be found in `govvault/management/commands/`.
