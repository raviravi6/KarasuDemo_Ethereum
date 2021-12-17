from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import pytest
from brownie import network, exceptions
from scripts.deploy_badge import deploy_badge, mint_badge, burn_badge
from web3 import Web3


def test_deploy_badge():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    account = get_account()
    badge_name = "EXAMPLE"
    badge_symbol = "EXP"
    badge_token = deploy_badge(account, badge_name, badge_symbol)

    assert badge_token.name() == badge_name
    assert badge_token.symbol() == badge_symbol


def test_mint_badge():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    account = get_account()
    non_owner = get_account(index=1)
    badge_name = "EXAMPLE"
    badge_symbol = "EXP"
    token_id = 2
    badge_token = deploy_badge(account, badge_name, badge_symbol)
    mint_badge(badge_token, account, non_owner, token_id)

    assert badge_token.ownerOf(token_id) == non_owner
    assert badge_token.exists(token_id) == True


def test_burn_badge():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    owner = get_account()
    non_owner = get_account(index=1)
    badge_name = "EXAMPLE"
    badge_symbol = "EXP"
    token_id = 1
    badge_token = deploy_badge(owner, badge_name, badge_symbol)
    mint_badge(badge_token, owner, non_owner, token_id)
    burn_badge(badge_token, owner, token_id)

    assert badge_token.exists(token_id) == False
