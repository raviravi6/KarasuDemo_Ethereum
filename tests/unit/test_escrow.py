from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import pytest
from brownie import network, exceptions
from scripts.deploy_escrow import (
    deploy_mainEscrow,
    approve_token_transfer,
    deposit_to_escrow,
    withdraw_from_escrow,
    refund_escrow,
)
from web3 import Web3
import time


def test_deploy_escrow():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    account = get_account()
    token = get_contract("dai_token")
    main_escrow = deploy_mainEscrow(account, token)


def test_approve_token_transfer():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    account = get_account()
    amount = Web3.toWei(10, "ether")
    token = get_contract("dai_token")
    main_escrow = deploy_mainEscrow(account, token)
    approve_token_transfer(token, main_escrow.address, account, amount)
    assert token.allowance(account, main_escrow.address) == amount


def test_deposit_to_escrow():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    account = get_account()
    non_owner = get_account(index=1)
    amount = Web3.toWei(10, "ether")
    token = get_contract("dai_token")
    main_escrow = deploy_mainEscrow(account, token)
    approve_token_transfer(token, main_escrow.address, account, amount)
    deposit_to_escrow(main_escrow, account, non_owner, amount, 10)
    assert token.balanceOf(main_escrow.address) == amount


def test_withdraw_from_escrow():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    account = get_account()
    non_owner = get_account(index=1)
    amount = Web3.toWei(10, "ether")
    token = get_contract("dai_token")
    main_escrow = deploy_mainEscrow(account, token)
    approve_token_transfer(token, main_escrow.address, account, amount)
    deposit_to_escrow(main_escrow, account, non_owner, amount, 10)

    amount_w = Web3.toWei(5, "ether")

    withdraw_from_escrow(main_escrow, account, non_owner, amount_w)

    assert token.balanceOf(non_owner.address) == amount_w
    assert token.balanceOf(main_escrow.address) == amount - amount_w


def test_refund_escrow():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    account = get_account()
    non_owner = get_account(index=1)
    amount = Web3.toWei(10, "ether")
    token = get_contract("dai_token")
    main_escrow = deploy_mainEscrow(account, token)
    approve_token_transfer(token, main_escrow.address, account, amount)
    deposit_to_escrow(main_escrow, account, non_owner, amount, 1)
    time.sleep(10)
    refund_escrow(main_escrow, account, non_owner)

    assert token.balanceOf(main_escrow.address) == 0
