from scripts.helpful_scripts import get_account, get_contract
from brownie import BadgeToken, config, network
from web3 import Web3



def deploy_badge(account, badge_name, badge_symbol):
    badge_token = BadgeToken.deploy(
        badge_name,
        badge_symbol,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print("Badge type created!")
    return badge_token


def mint_badge(badge_token, account, non_owner, token_id):
    mint_tx = badge_token.mint(non_owner, token_id, {"from": account})
    mint_tx.wait(1)


def burn_badge(badge_token, account, token_id):
    burn_tx = badge_token.burn(token_id)
    burn_tx.wait(1)


def main():
    account = get_account()
    #non_owner = get_account(index=1)
    non_owner = '0xA2BFc4B3653F3C6F91EFF29228f5e88A1De1f684'
    badge_name = "Validation Sample One"
    badge_symbol = "VSOne"
    badge_token = deploy_badge(account, badge_name, badge_symbol)
  #  badge_token = BadgeToken[0]
    token_id = 1
    mint_badge(badge_token, account, non_owner, token_id)
 #   burn_badge(badge_token, account, token_id)
