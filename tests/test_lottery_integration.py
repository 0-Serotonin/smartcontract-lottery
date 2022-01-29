from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_DEVELOPMENT,
    fund_with_link,
    get_account,
)


from brownie import network
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_DEVELOPMENT
from scripts.deploy_lottery import deploy_lottery, get_account
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(120)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
