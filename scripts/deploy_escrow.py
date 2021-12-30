from scripts.helpful_scripts import get_account, get_contract, get_contract_address
from brownie import MainERC20Escrow, config, network
from web3 import Web3
import time


def deploy_mainERC20Escrow(account, token):
    main_ERC20escrow = MainERC20Escrow.deploy(
        token,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    return main_ERC20escrow


def approve_token_transfer(token, sender, account, amount):
    # approve token transfer
    approve_tx = token.approve(sender, amount, {"from": account})
    approve_tx.wait(1)
    print("Token transfer approved!")


def deposit_to_escrow(main_escrow, account, non_owner, amount, expiration_sec):
    # make deposit
    deposit_tx = main_escrow.deposit(
        non_owner, amount, expiration_sec, {"from": account}
    )
    deposit_tx.wait(1)
    print("Deposit made!")


def withdraw_from_escrow(main_escrow, account, non_owner, amount):
    # withdraw from escrow
    withdraw_tx = main_escrow.withdraw(non_owner, amount, {"from": account})
    withdraw_tx.wait(1)
    print("Withdrawal complete!")


def refund_escrow(main_escrow, account, non_owner):
    # refund escrow back to owner
    refund_tx = main_escrow.refund(non_owner, {"from": account})
    refund_tx.wait(1)
    print("Refund complete!")


def main():
    account = get_account()
    #non_owner = get_account(index=1)
    non_owner = "0xA2BFc4B3653F3C6F91EFF29228f5e88A1De1f684"
    token = get_contract("usdc_token", "interface")


 #   main_ERC20escrow = deploy_mainERC20Escrow(account, token)
    main_ERC20escrow = MainERC20Escrow[-1]
    amount = Web3.toWei(10, "ether")
    expiration_sec = 600

    approve_token_transfer(token, main_ERC20escrow.address, account, amount)
    deposit_to_escrow(main_ERC20escrow, account, non_owner, amount, expiration_sec)
    #withdraw_from_escrow(main_ERC20escrow, account, non_owner, amount)

    #time.sleep(expiration_sec)
    #refund_escrow(main_ERC20escrow, account, non_owner)
