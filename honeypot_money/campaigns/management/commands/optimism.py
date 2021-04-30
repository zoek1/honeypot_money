import json

from django.core.management.base import BaseCommand, CommandError
from web3 import Web3

from honeypot_money.settings import BASE_DIR
import os.path

class Command(BaseCommand):
    help = 'Check and transfer optimism balances from given address'

    def add_arguments(self, parser):
        parser.add_argument('from_address')
        parser.add_argument('to_address')

    def handle(self, *args, **options):
        abi_path_contract = os.path.join(BASE_DIR, 'data/contracts/OVM_L1ETHGateway.json')
        optimism_gateway = json.load(open(abi_path_contract))
        optimism_abi = optimism_gateway['abi']
        optimism_address = optimism_gateway['address']

        from_addr = options['from_address']
        to_addr = options['to_address']

        w3_kovan = Web3(Web3.HTTPProvider('https://kovan.infura.io/v3/'))
        w3_optimism_kovan = Web3(Web3.HTTPProvider('https://kovan.optimism.io/'))

        nonce = w3_kovan.eth.getTransactionCount(from_addr)
        nonce_optimism = w3_optimism_kovan.eth.getTransactionCount(from_addr)

        print(w3_kovan.eth.getBalance(from_addr))
        print(w3_optimism_kovan.eth.getBalance(from_addr))
        print(w3_optimism_kovan.eth.getBalance(to_addr))

        gateway_contract = w3_kovan.eth.contract(address=optimism_address, abi=optimism_abi)

        private_key = '' # Read from file

        # deposit_tx = self.move_funds_to_l2(gateway_contract, nonce, w3_kovan, private_key)
        self.faucet(to_addr, w3_optimism_kovan, nonce_optimism, 1, private_key, Web3.toWei(1, 'gwei'))
        # print(deposit_tx)
        # w3.eth.contract(address=optimism_addr, abi=)

    def faucet(self, to_addr, w3, nonce, gas, pk, value):
        abi_path_contract = os.path.join(BASE_DIR, 'data/contracts/ERC20.json')
        optimism_abi = json.load(open(abi_path_contract))
        WETH_ADDRESS = '0x4200000000000000000000000000000000000006'
        erc20_contract = w3.eth.contract(address=WETH_ADDRESS, abi=optimism_abi)

        faucet_tx = erc20_contract.functions.transfer(to_addr, value).buildTransaction({
            'nonce': nonce,
            'gas': gas,
            'chainId': 69,
        })
        print(faucet_tx)
        # print(w3.eth.estimateGas(faucet_tx))
        signed_txn = w3.eth.account.signTransaction(faucet_tx, private_key=pk)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)


    def move_funds_to_l2(self, contract, nonce, w3, pk):
        deposit_tx = contract.functions.deposit().buildTransaction({
            'chainId': 42,
            'nonce': nonce,
            'gas': 327127,
            'value': Web3.toWei(1, 'gwei'),
        })


        signed_txn = w3.eth.account.signTransaction(deposit_tx, private_key=pk)
        w3.eth.sendRawTransaction(signed_txn.rawTransaction)