from scripts.helpful_scripts import get_account, get_contract
from brownie import BadgeToken, config, network
from web3 import Web3

account = get_account()
badge_token = BadgeToken[0]

def getHolders(token_id=1):
    tx = badge_token.ownerOf(token_id, {"from": account})
    print(tx)