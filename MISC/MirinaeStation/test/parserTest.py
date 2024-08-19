import json

json_data = '''
{
    "addresses": {
        "0xcfba3d06e44e4baeafacd17525c10ef687699443": {
            "secretKey": {
                "type": "Buffer",
                "data": [181,196,115,72,118,33,27,139,99,221,116,211,194,23,199,233,122,140,12,224,230,199,191,122,26,141,116,57,25,198,216,52]
            },
            "publicKey": {
                "type": "Buffer",
                "data": [161,29,81,248,17,116,8,135,233,53,72,90,31,147,191,16,12,162,38,165,185,80,48,115,143,242,218,223,69,155,52,5,96,44,224,39,29,207,57,243,51,53,17,116,199,34,183,83,213,109,137,59,43,121,71,192,232,20,60,175,3,25,12,79]
            },
            "address": "0xcfba3d06e44e4baeafacd17525c10ef687699443",
            "account": {
                "nonce": "0x",
                "balance": "0x06f05b59d3b20000",
                "stateRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
                "codeHash": "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
            }
        },
        "0x7a34be8d90e7d9e36dbd8fa8658cddebe0a1dd96": {
            "secretKey": {
                "type": "Buffer",
                "data": [226,240,164,202,2,52,117,193,243,35,68,196,98,115,159,5,149,210,191,15,164,18,234,10,204,239,91,140,39,67,1,215]
            },
            "publicKey": {
                "type": "Buffer",
                "data": [129,217,111,61,66,102,151,164,84,143,98,146,91,172,28,99,45,24,52,139,17,99,58,48,221,75,8,248,34,224,19,53,218,88,76,87,168,115,244,252,5,166,217,55,210,198,79,141,17,52,39,123,128,15,50,86,139,18,204,15,183,183,250,71]
            },
            "address": "0x7a34be8d90e7d9e36dbd8fa8658cddebe0a1dd96",
            "account": {
                "nonce": "0x",
                "balance": "0x06f05b59d3b20000",
                "stateRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
                "codeHash": "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
            }
        }
    }
}
'''

accounts_data = json.loads(json_data)

ganache_accounts = list(accounts_data["addresses"].keys())
private_keys = [bytes(value['secretKey']['data']).hex() for value in accounts_data["addresses"].values()]

#print("Extracted Addresses and Private Keys:")
#for addr, key in zip(ganache_accounts, private_keys):
#    print(f"Address: {addr}, Private Key: {key}")

