import requests
import time

RPC_URL = "https://testnet-rpc.monad.xyz"
MIN_BALANCE_WEI = 2 * 10**18     # Min 2 MONAD
MAX_BALANCE_WEI = 100 * 10**18   # Max 100 MONAD
MIN_NONCE = 700                 # Min 1000 transaksi
MAX_NONCE = 10000                # Max 10000 transaksi

# Daftar token untuk filter
TOKEN_CONTRACTS = {
    "YAKI": "0xfe140e1dCe99Be9F4F15d657CD9b7BF622270C50",
    "CHOG": "0xE0590015A873bF326bd645c3E1266d4db41C4E6B",
    "DAK":  "0x0F0BDEbF0F83cD1EE3974779Bcb7315f9808c714",
    "APR":  "0xb2f82D0f38dc453D596Ad40A37799446Cc89274A",
    "GMO":  "0xaEef2f6B429Cb59C9B2D7bB2141ADa993E8571c3"
}

def get_latest_block_number():
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        result = response.json().get("result")
        return int(result, 16)
    except Exception as e:
        print(f"❌ Error ambil latest block: {e}")
        return None

def get_block_by_number(block_number):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "id": 1
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        return response.json().get("result")
    except Exception as e:
        print(f"❌ Error ambil block {block_number}: {e}")
        return None

def is_contract(address, cache):
    if address in cache:
        return cache[address]
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getCode",
        "params": [address, "latest"],
        "id": 1
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        result = response.json().get("result")
        is_sc = result != "0x"
        cache[address] = is_sc
        return is_sc
    except Exception as e:
        print(f"❌ Error cek address {address}: {e}")
        cache[address] = True
        return True

def get_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        result = response.json().get("result")
        return int(result, 16)
    except Exception as e:
        print(f"❌ Error cek balance {address}: {e}")
        return 0

def get_nonce(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionCount",
        "params": [address, "latest"],
        "id": 1
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        result = response.json().get("result")
        return int(result, 16)
    except Exception as e:
        print(f"❌ Error cek nonce {address}: {e}")
        return 0

def get_token_balance(address, token_address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": token_address,
                "data": "0x70a08231000000000000000000000000" + address[2:].lower()
            },
            "latest"
        ],
        "id": 1
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10)
        result = response.json().get("result")
        return int(result, 16)
    except Exception as e:
        print(f"❌ Error cek token balance {token_address} - {address}: {e}")
        return 0

def collect_eoa_addresses(target_count, start_block):
    addresses = set()
    block_number = start_block
    cache_contract_check = {}

    print(f"\n🔍 Mulai scanning dari block {start_block} cari {target_count} wallet EOA...\n")

    while len(addresses) < target_count:
        block = get_block_by_number(block_number)
        if block:
            tx_list = block.get("transactions", [])
            print(f"📦 Block {block_number}: {len(tx_list)} transaksi")

            for tx in tx_list:
                for addr in [tx["from"].lower(), tx["to"].lower() if tx["to"] else None]:
                    if not addr or addr in addresses or is_contract(addr, cache_contract_check):
                        continue

                    balance = get_balance(addr)
                    nonce = get_nonce(addr)

                    if (MIN_BALANCE_WEI <= balance <= MAX_BALANCE_WEI) and (MIN_NONCE <= nonce <= MAX_NONCE):
                        # Cek apakah punya salah satu token
                        punya_token = False
                        for token_name, token_addr in TOKEN_CONTRACTS.items():
                            token_bal = get_token_balance(addr, token_addr)
                            if token_bal > 0:
                                punya_token = True
                                break

                        if not punya_token:
                            continue

                        addresses.add(addr)
                        print(f"✅ {addr} | Balance: {balance / 1e18:.2f} MONAD | TxCount: {nonce} | Total: {len(addresses)}/{target_count}")

                        if len(addresses) >= target_count:
                            break
        else:
            print(f"❌ Block {block_number} tidak ditemukan")

        block_number -= 1
        time.sleep(0.25)

    filename = f"wallet_{target_count}_eoa_filtered.txt"
    with open(filename, "w") as f:
        for addr in addresses:
            f.write(f"{addr}\n")

    print(f"\n🎉 Selesai! {target_count} wallet EOA tersaring disimpan di {filename}")

# Mulai scanning
latest_block = get_latest_block_number()
if latest_block:
    print(f"🔥 Latest block: {latest_block}")
    collect_eoa_addresses(500, latest_block)
else:
    print("❌ Gagal ambil latest block")
