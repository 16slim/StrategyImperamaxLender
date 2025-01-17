import brownie
from brownie import Contract
from brownie import config
import math


def test_remove_from_withdrawal_queue(
    gov,
    token,
    vault,
    whale,
    strategy,
    chain,
    amount,
):
    ## deposit to the vault after approving
    startingWhale = token.balanceOf(whale)
    token.approve(vault, 2**256 - 1, {"from": whale})
    vault.deposit(amount, {"from": whale})
    chain.sleep(1)
    strategy.harvest({"from": gov})
    chain.sleep(1)

    # simulate 1 day of earnings
    chain.sleep(86400)
    strategy.harvest({"from": gov})
    chain.sleep(1)
    before = strategy.estimatedTotalAssets()

    # set emergency and exit, then confirm that the strategy has no funds
    vault.removeStrategyFromQueue(strategy, {"from": gov})
    after = strategy.estimatedTotalAssets()
    assert before == after

    # check that our strategy is no longer in the withdrawal queue's 20 addresses
    addresses = []
    for x in range(19):
        address = vault.withdrawalQueue(x)
        addresses.append(address)
    print(
        "Strategy Address: ",
        strategy.address,
        "\nWithdrawal Queue Addresses: ",
        addresses,
    )
    assert not strategy.address in addresses
