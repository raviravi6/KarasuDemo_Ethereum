from scripts.helpful_scripts import get_account
from brownie import SimpleRFI

sample_token_uri = "https://ipfs.io/ipfs/QmejauJiE86AX1bN4JLtB91Vky8EEXGoXAAJuXv3ZJHwfv"


def deploy_simpleRFI(account):
    simple_rfi = SimpleRFI.deploy({"from": account})
    return simple_rfi


def mint_RFI(simple_rfi):
    account = get_account()
    tx = simple_rfi.createRFI(sample_token_uri, {"from": account})
    tx.wait(1)
    print(f"Awesome, you can view your NFT at {sample_token_uri}")


def main():
    account = get_account()
    simple_rfi = deploy_simpleRFI()
    createRFI(simple_rfi)
