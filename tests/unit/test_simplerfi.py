from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import pytest
from brownie import network, exceptions
from scripts.data_management.deploy_rfi import mint_RFI, deploy_simpleRFI


def test_upload_rfi():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.slip("Only for local testing")
    account = get_account()
    simplerfi = deploy_simpleRFI(account)
    mint_RFI(simplerfi)
