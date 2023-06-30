import json
from web3 import Web3
import time
from decimal import Decimal
import random
import os
from datetime import datetime

time_ot = 120
time_do = 500

# ABI
with open('api.json') as f:
    abi = json.load(f)

# Контракт NFT
contr_bsc_address = '0xCCED48E6fe655E5F28e8C4e56514276ba8b34C09'  # Изменить адрес контракта минта

with open("privates.txt", "r") as f:
    keys_list = [row.strip() for row in f if row.strip()]
    numbered_keys = list(enumerate(keys_list, start=1))
    random.shuffle(numbered_keys)  # Перемешивание кошельков, можно закомментировать

message = f"Будет обработано {len(numbered_keys)} кошельков"
print(message)

wallets_prob = []
for wallet_number, PRIVATE_KEY in numbered_keys:
    web3 = Web3(Web3.HTTPProvider('https://rpc-core.icecreamswap.com'))
    w3 = Web3(Web3.HTTPProvider('https://rpc-core.icecreamswap.com'))

    account = w3.eth.account.from_key(PRIVATE_KEY)
    address = account.address
    contract = w3.eth.contract(address=w3.to_checksum_address(contr_bsc_address), abi=abi)
    
    message = f"{datetime.now().strftime('%H:%M:%S')} \n [{wallet_number}] - {address}"
    print(message, flush=True)

    try:
        valueRandom = Decimal(round(random.uniform(0.01, 0.02), 7))
        gasPriceRandom = Decimal(random.uniform(30, 50))
        swap_txn = contract.functions.swapExactETHForTokens(0, [Web3.to_checksum_address('0x191e94fa59739e188dce837f7f6978d84727ad01'), Web3.to_checksum_address('0x900101d06a7426441ae63e9ab3b9b0f63be145f1')], address, (int(time.time()) + 3000000)).build_transaction({
            'from': address,
            'value': web3.to_wei(valueRandom,'ether'),
            'gasPrice': Web3.to_wei(gasPriceRandom, 'gwei'),
            'nonce': web3.eth.get_transaction_count(address),
        })
        signed_swap_txn = w3.eth.account.sign_transaction(swap_txn, PRIVATE_KEY)
        swap_txn_hash = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        transaction_url = f"Transaction: https://scan.coredao.org/tx/{swap_txn_hash.hex()}"
        print(transaction_url)

        wait_time = random.randint(time_ot, time_do)
        time.sleep(wait_time)
        print(f"Время до следующей транзакции: {wait_time} секунд")
    except Exception as err:
        error_message = f"Неожиданная {err=}"
        print(error_message)
        wallets_prob.append(address)

if len(wallets_prob) > 0:
    error_message = "Есть проблемки\n" + "\n".join(wallets_prob)
    print(error_message)

    with open('failed.txt', 'w') as file:
        for wallet in wallets_prob:
            file.write(f"{wallet}\n")
else:
    print("Закончили без ошибок")
