from scripts.helpful_scripts import get_account, get_contract, get_contract_address
from brownie import ERC20EscrowCloneFactory, config, network, interface
from web3 import Web3
import time




def deploy_escrow_contract(account):
    escrow_contract = ERC20EscrowCloneFactory.deploy( 
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    return escrow_contract

def clone_escrow_contract(account, escrow_clone, og_escrow_contract):
    clone_contract = escrow_clone.createERC20EscrowCounter(og_escrow_contract, {"from": account})
    return clone_contract

def approve_token_transfer(token, sender, account, amount):
    # approve token transfer
    approve_tx = token.approve(sender, amount, {"from": account})
    approve_tx.wait(1)
    print("Token transfer approved!")


def deposit_to_escrow(escrow_clone, account, amount, expiration_sec, token, cid):
    # make deposit
    customGasLimit = 500000000000
    deposit_tx = escrow_clone.deposit(
        cid, amount, expiration_sec, token, {"from": account}
    )

    deposit_tx.wait(1)
    print("Deposit made!")

def set_payee(escrow_contract, account, payee, depositId, cid):
    tx = escrow_contract.setPayee(
        depositId, cid, payee, {"from": account}
    )


def withdraw_from_escrow(escrow_contract, account, non_owner, amount):
    # withdraw from escrow
    withdraw_tx = escrow_contract.withdraw(non_owner, amount, {"from": account})
    withdraw_tx.wait(1)
    print("Withdrawal complete!")


def refund_escrow(escrow_contract, account, non_owner):
    # refund escrow back to owner
    refund_tx = escrow_contract.refund(non_owner, {"from": account})
    refund_tx.wait(1)
    print("Refund complete!")


def main():
    account = get_account()
    #non_owner = get_account(index=1)
    non_owner = "0xA2BFc4B3653F3C6F91EFF29228f5e88A1De1f684"
   # contract_name = 'link_token'
   # contract_address = config["networks"][network.show_active()][contract_name]
   # token = interface.IERC20(contract_address)
   # cid = "bafybeig2w3jz4y2ps2tf5u42p3l5p4v73wp7zbem3xsn6efb56mlaqd4yq"
    og_escrow_contract = "0x0123310121F72cdFC327d20b1b0BA323877389Fb"
  #  cid = 'hello'

    escrow_clone = deploy_escrow_contract(account)
   # escrow_clone = ERC20EscrowCloneFactory[-1]
 
    clone_contract = clone_escrow_contract(account, escrow_clone, og_escrow_contract)

    amount = Web3.toWei(2, "ether")
    expiration_sec = 60

    #approve_token_transfer(token, escrow_clone.address, account, amount)
   # deposit_to_escrow(escrow_clone, account, amount, expiration_sec, token, cid)
  #  set_payee(escrow_clone, account, non_owner, 1, cid)
    #withdraw_from_escrow(escrow_clone, account, non_owner, amount)

    #time.sleep(expiration_sec)
    #refund_escrow(escrow_clone, account, non_owner)
