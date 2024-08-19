import json
from web3 import Web3

with open("./accounts.json") as f:
    accounts_data = json.load(f)



ganache_accounts = list(accounts_data["addresses"].keys())

private_keys = [bytes(value['secretKey']['data']).hex() for value in accounts_data["addresses"].values()]

#print("Extracted Addresses and Private Keys:")
#for addr, key in zip(ganache_accounts, private_keys):
#    print(f"Address: {addr}, Private Key: 0x{key}")

print(f"Address: {ganache_accounts[0]}, Private Key: 0x{private_keys[0]}")