import os
import json
import time
import threading
from dataclasses import dataclass
from typing import Optional
import uuid
from datetime import datetime, timedelta

import aiohttp
from flask import Flask, jsonify, request
from web3 import Web3
from web3.middleware import geth_poa_middleware

app = Flask(__name__)

rpc_url = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")

web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_abi = '[{"inputs":[{"internalType":"address","name":"_wallet","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"buyTicket","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"buy_token","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"isChallSolved","outputs":[{"internalType":"bool","name":"solved","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint48","name":"amount","type":"uint48"}],"name":"loan","outputs":[],"stateMutability":"payable","type":"function"}]'
contract_bytecode = '6080604052600080556001805466ffffffffffffff1916905534801561002457600080fd5b506040516104253803806104258339818101604052602081101561004757600080fd5b5051600180546001600160a01b0390921667010000000000000002600160381b600160d81b031990921691909117905561039f806100866000396000f3fe60806040526004361061003f5760003560e01c80634728fd4814610044578063ed7e286b1461006b578063edca914c14610094578063ede56d88146100a9575b600080fd5b6100696004803603602081101561005a57600080fd5b503565ffffffffffff166100c6565b005b34801561007757600080fd5b50610080610182565b604080519115158252519081900360200190f35b3480156100a057600080fd5b506100696101bd565b610069600480360360208110156100bf57600080fd5b503561027e565b600154600160381b90046001600160a01b031633146101165760405162461bcd60e51b81526004018080602001828103825260258152602001806103456025913960400191505060405180910390fd5b6001805465ffffffffffff19811665ffffffffffff91821684018216179091556040513391831690600081818185875af1925050503d8060008114610177576040519150601f19603f3d011682016040523d82523d6000602084013e61017c565b606091505b50505050565b6001546000906601000000000000900460ff1680156101a9575060015465ffffffffffff16155b156101b6575060016101ba565b5060005b90565b600154600160381b90046001600160a01b0316331461020d5760405162461bcd60e51b81526004018080602001828103825260258152602001806103456025913960400191505060405180910390fd5b60005465ffffffffffff11156102545760405162461bcd60e51b81526004018080602001828103825260228152602001806103236022913960400191505060405180910390fd5b6000805465fffffffffffe190190556001805466ff00000000000019166601000000000000179055565b600154600160381b90046001600160a01b031633146102ce5760405162461bcd60e51b81526004018080602001828103825260258152602001806103456025913960400191505060405180910390fd5b60405133908290600081818185875af1925050503d806000811461030e576040519150601f19603f3d011682016040523d82523d6000602084013e610313565b606091505b5050600080549092019091555056fe4e6f7420656e6f7567682066756e647320746f2062757920746865207469636b6574506c6561736520757365207468652077616c6c65742070726f766964656420746f20796f75a2646970667358221220cdef8d8dafe75eec2631c38a474a57c96bd321db65f6d8745e3efbb185dea7ba64736f6c63430007000033'


@dataclass
class RPCError:
    code: int
    message: str

PARSE_ERROR = RPCError(code=-32700, message="Parse error")
INVALID_REQUEST = RPCError(code=-32600, message="Invalid request")
METHOD_NOT_SUPPORTED = RPCError(code=-32004, message="Method not supported")
RESULT_UNAVAILABLE = RPCError(code=-32002, message="Resource unavailable")

ALLOWED_METHODS = frozenset(
    [
        "eth_blockNumber",
        "eth_call",
        "eth_chainId",
        "eth_estimateGas",
        "eth_gasPrice",
        "eth_getBalance",
        "eth_getBlockByHash",
        "eth_getBlockByNumber",
        "eth_getCode",
        "eth_getStorageAt",
        "eth_getTransactionByHash",
        "eth_getTransactionCount",
        "eth_getTransactionReceipt",
        "eth_sendRawTransaction",
        "net_version",
        "rpc_modules",
        "web3_clientVersion",
    ]
)

def error_response(error: RPCError, status_code: int, request_id: Optional[int] = None):
    return jsonify({
        "jsonrpc": "2.0",
        "error": {
            "code": error.code,
            "message": error.message,
        },
        "id": request_id,
    }), status_code

async def dispatch_request(provider: str, body: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(provider, json=body) as response:
            return await response.json()

user_data = {}

cnt = 0

def deploy_contract_for_user(user_id):
    global cnt

    while not os.path.exists("/shared/accounts.json"):
        time.sleep(1)

    with open("/shared/accounts.json") as f:
        accounts_data = json.load(f)

    ganache_accounts = accounts_data["addresses"]
    private_keys = accounts_data["private_keys"]
    # If you use 'ganache-cli', use the code below
    #ganache_accounts = list(accounts_data["addresses"].keys())
    #private_keys = [bytes(value['secretKey']['data']).hex() for value in accounts_data["addresses"].values()]

    if user_id not in user_data:
        deployer = list(ganache_accounts.keys())[cnt]
        private_key = private_keys[deployer]
        deployer = Web3.to_checksum_address(deployer)

        MirinaeStation = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        try:
            transaction = MirinaeStation.constructor(deployer).build_transaction({
                'from': deployer,
                'nonce': web3.eth.get_transaction_count(deployer),
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei')
            })

            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            rpc_url = f"http://RPC_URL/interact/{user_id}"

            deployment_info = {
                "contractAddress": tx_receipt.contractAddress,
                "walletAddress": deployer,
                "privateKey": private_key,
                "rpcUrl": rpc_url,
                "user_id": user_id
            }

            user_data[user_id] = deployment_info
            cnt += 1

        except Exception as e:
            print(f"Error in transaction: {e}")
            return str(e), deployer, private_key

    return user_data[user_id]

def gen_uuid():
    rand_uuid = str(uuid.uuid4())
    while rand_uuid in user_data:
        rand_uuid = str(uuid.uuid4())
    return rand_uuid


@app.route('/info', methods=['GET'])
def info():
    user_id = gen_uuid()
    deployment_info = deploy_contract_for_user(user_id)
    return jsonify({"user_id": user_id})

@app.route('/info/<user_id>', methods=['GET'])
def info_with_id(user_id):
    if user_id not in user_data:
        return error_response(RESULT_UNAVAILABLE, 400)

    deployment_info = user_data[user_id]
    return jsonify(deployment_info)

@app.route('/flag/<user_id>', methods=['GET'])
def flag(user_id):
    if user_id not in user_data:
        return error_response(RESULT_UNAVAILABLE, 400)

    deployment_info = deploy_contract_for_user(user_id)
    contract_address = deployment_info['contractAddress']
    wallet_address = deployment_info['walletAddress']

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    solved = contract.functions.isChallSolved().call({'from': wallet_address})

    flag = open("./flag.txt", "r").read()

    result = f"Challenge Solved!! {flag}" if solved else "Challenge Not Solved"
    with open(f'result_{user_id}.txt', 'w') as f:
        f.write(result)

    return result

@app.route('/interact/<user_id>', methods=['POST'])
async def interact(user_id):
    if user_id not in user_data:
        return error_response(RESULT_UNAVAILABLE, 400)

    try:
        body = request.get_json()
    except ValueError:
        return error_response(PARSE_ERROR, 415)

    request_id = body.get("id")
    body_keys = [key.lower() for key in body.keys()]
    if body_keys.count("method") != 1 or not isinstance(body["method"], str):
        return error_response(INVALID_REQUEST, 401, request_id)

    if body["method"] not in ALLOWED_METHODS:
        return error_response(METHOD_NOT_SUPPORTED, 401, request_id)

    try:
        if body["method"] == "eth_sendRawTransaction":
            raw_tx = body["params"][0]
            tx_hash = web3.eth.send_raw_transaction(raw_tx)
            response = {"jsonrpc": "2.0", "result": tx_hash.hex(), "id": request_id}
        else:
            #if body["method"] == "eth_call" or body["method"] == "eth_sendTransaction":
            #    if "gasPrice" not in body["params"][0]:
            #        body["params"][0]["gasPrice"] = web3.to_wei('20', 'gwei')
            response = await dispatch_request(
                os.getenv("WEB3_PROVIDER_URI", rpc_url), body
            )
            if (
                body["method"] in ("eth_getBlockByHash", "eth_getBlockByNumber")
                and "result" in response
            ):
                response["result"]["transactions"] = []
        return jsonify(response)
    except Exception as e:
        print(f"Exception: {e}")
        return error_response(RESULT_UNAVAILABLE, 500, request_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
