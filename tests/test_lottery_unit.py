from brownie import Lottery, network, accounts, config, exceptions
from toolz.itertoolz import get
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_DEVELOPMENT,
    get_account,
    fund_with_link,
    get_contract,
)
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip()
    lottery = deploy_lottery()
    # 3314 eth / usd
    # usdEntranceFee is 50
    # expected entrance fee is 50/3314 eth
    expected_entrance_fee = Web3.toWei(0.015, "ether")
    entrance_fee = lottery.getEntranceFee()
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip()
    lottery = deploy_lottery()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_end_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip()
    lottery = deploy_lottery()

    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip()
    lottery = deploy_lottery()

    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_lottery_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    starting_account_balance = account.balance()
    balance_of_lottery = lottery.balance()
    transasction = lottery.endLottery()
    request_Id = transasction.events["RequestRandom"]["requestID"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_Id, STATIC_RNG, lottery.address, {"from": account}
    )
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_account_balance + balance_of_lottery
