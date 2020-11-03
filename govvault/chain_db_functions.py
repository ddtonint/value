from web3 import Web3
import json
from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import WalletAddress, WalletBalance, Holder, VaultsPerformance, SeedPoolHolder, TrackingSetting

# Fill in your infura API key here
infura_url = "YOUR_INFURA_API_KEY_HERE"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Other tokens
burn_addr = web3.toChecksumAddress('0x0000000000000000000000000000000000000000')
value_addr = web3.toChecksumAddress('0x49E833337ECe7aFE375e44F4E3e8481029218E5c')
vusd_addr = web3.toChecksumAddress('0x1B8E12F839BD4e73A47adDF76cF7F0097d74c14C')
weth_addr = web3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
dai_addr = web3.toChecksumAddress('0x6B175474E89094C44Da98b954EedeAC495271d0F')
value_devs_addr = web3.toChecksumAddress('0x7Be4D5A99c903C437EC77A20CB6d0688cBB73c7f')

usdt_addr = web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
usdc_addr = web3.toChecksumAddress('0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48')
dai_addr = web3.toChecksumAddress('0x6B175474E89094C44Da98b954EedeAC495271d0F')

# VALUE contract
value_contract_abi = json.loads('[{"inputs":[{"internalType":"contract IERC20","name":"_yfv","type":"address"},{"internalType":"uint256","name":"_cap","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegator","type":"address"},{"indexed":true,"internalType":"address","name":"fromDelegate","type":"address"},{"indexed":true,"internalType":"address","name":"toDelegate","type":"address"}],"name":"DelegateChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegate","type":"address"},{"indexed":false,"internalType":"uint256","name":"previousBalance","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newBalance","type":"uint256"}],"name":"DelegateVotesChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"dst","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"src","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawal","type":"event"},{"inputs":[],"name":"DELEGATION_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_minter","type":"address"}],"name":"addMinter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint32","name":"","type":"uint32"}],"name":"checkpoints","outputs":[{"internalType":"uint32","name":"fromBlock","type":"uint32"},{"internalType":"uint256","name":"votes","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatee","type":"address"}],"name":"delegate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"delegateBySig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegator","type":"address"}],"name":"delegates","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getCurrentVotes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"getPriorVotes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"governance","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_token","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"governanceRecoverUnsupported","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"minters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"numCheckpoints","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_minter","type":"address"}],"name":"removeMinter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_cap","type":"uint256"}],"name":"setCap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_governance","type":"address"}],"name":"setGovernance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"yfv","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"yfvLockedBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
value_contract_addr = '0x49E833337ECe7aFE375e44F4E3e8481029218E5c'
value_contract = web3.eth.contract(address=value_contract_addr, abi=value_contract_abi)

# VALUE Gov Vault v2
govVault_ValueLiquid_contract_abi = json.loads('[{"inputs":[{"internalType":"contract ITokenInterface","name":"_yfvToken","type":"address"},{"internalType":"contract ITokenInterface","name":"_valueToken","type":"address"},{"internalType":"contract ITokenInterface","name":"_vUSD","type":"address"},{"internalType":"contract ITokenInterface","name":"_vETH","type":"address"},{"internalType":"uint256","name":"_valuePerBlock","type":"uint256"},{"internalType":"uint256","name":"_vusdPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"CommissionPaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_days","type":"uint256"}],"name":"Locked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"RewardPaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"FUND_CAP_DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"available","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"balance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"buyShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"chi","outputs":[{"internalType":"contract IFreeFromUpTo","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"controller","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_referrer","type":"address"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_referrer","type":"address"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"depositAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"depositAvailable","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_shares","type":"uint256"},{"internalType":"address","name":"_referrer","type":"address"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"depositShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_referrer","type":"address"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"depositYFV","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"earn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"earnLowerlimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fundCap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPricePerFullShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"getRewardAndDepositAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getStrategyCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"governance","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_to","type":"address"}],"name":"governanceRecoverUnsupported","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"governanceResetLocked","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"reserve","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"harvest","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"harvestAllStrategies","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_strategy","type":"address"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"harvestStrategy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_locked","type":"uint256"},{"internalType":"uint256","name":"_days","type":"uint256"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"lockShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"minStakingAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"pendingValue","outputs":[{"internalType":"uint256","name":"_pending","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"pendingVeth","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"pendingVusd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardReferral","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_controller","type":"address"}],"name":"setController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_earnLowerlimit","type":"uint256"}],"name":"setEarnLowerlimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_fundCap","type":"uint256"}],"name":"setFundCap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_governance","type":"address"}],"name":"setGovernance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxLockedDays","type":"uint256"}],"name":"setMaxLockedDays","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_minStakingAmount","type":"uint256"}],"name":"setMinStakingAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_rewardReferral","type":"address"}],"name":"setRewardReferral","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_totalDepositCap","type":"uint256"}],"name":"setTotalDepositCap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_unlockWithdrawFee","type":"uint256"}],"name":"setUnlockWithdrawFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_unstakingFrozenTime","type":"uint256"}],"name":"setUnstakingFrozenTime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_valueInsuranceFund","type":"address"}],"name":"setValueInsuranceFund","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_valuePerBlock","type":"uint256"}],"name":"setValuePerBlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_vusdPerBlock","type":"uint256"}],"name":"setVusdPerBlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"stakingPower","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalDepositCap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"unfrozenStakeTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlockWithdrawFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"unstake","outputs":[{"internalType":"uint256","name":"_actualWithdraw","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unstakingFrozenTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"updateReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_vETHContract","type":"address"}],"name":"upgradeVETHContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_vUSDContract","type":"address"}],"name":"upgradeVUSDContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"valueRewardDebt","type":"uint256"},{"internalType":"uint256","name":"vusdRewardDebt","type":"uint256"},{"internalType":"uint256","name":"lastStakeTime","type":"uint256"},{"internalType":"uint256","name":"accumulatedStakingPower","type":"uint256"},{"internalType":"uint256","name":"lockedAmount","type":"uint256"},{"internalType":"uint256","name":"lockedDays","type":"uint256"},{"internalType":"uint256","name":"boostedExtra","type":"uint256"},{"internalType":"uint256","name":"unlockedTime","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"vETH","outputs":[{"internalType":"contract ITokenInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"vETH_REWARD_FRACTION_RATE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"vUSD","outputs":[{"internalType":"contract ITokenInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"valueInsuranceFund","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"valuePerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"valueToken","outputs":[{"internalType":"contract ITokenInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"vusdPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_shares","type":"uint256"},{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint8","name":"_flag","type":"uint8"}],"name":"withdrawAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"yfvToken","outputs":[{"internalType":"contract ITokenInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')
govVault_ValueLiquid_contract_addr = web3.toChecksumAddress('0xceC03a960Ea678A2B6EA350fe0DbD1807B22D875')
govVault_ValueLiquid_contract = web3.eth.contract(address=govVault_ValueLiquid_contract_addr, abi=govVault_ValueLiquid_contract_abi)

# Seed pool v2
seedPool_contract_abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"Burned","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"CommissionPaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"RewardAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"RewardPaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Staked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"tokenAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawn","type":"event"},{"constant":true,"inputs":[],"name":"DAI_TOKEN_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DURATION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"EPOCH_REWARD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"NUMBER_EPOCHS","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"REFERRAL_COMMISSION_PERCENT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"SUPPORTED_STAKING_COIN_ADDRESSES","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"SUPPORTED_STAKING_COIN_WEI_MULTIPLE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"TOTAL_REWARD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"TUSD_TOKEN_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"USDC_TOKEN_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"USDT_TOKEN_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"accumulatedStakingPower","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"affiliate","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"claimVETHReward","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"claimedVETHRewards","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"currentEpochReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"exit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"getReward","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"initreward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"lastTimeRewardApplicable","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"lastUpdateTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"nextRewardMultiplier","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"reward","type":"uint256"}],"name":"notifyRewardAmount","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"periodFinish","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"referredCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"rewardPerToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rewardPerTokenStored","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rewardRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rewardReferral","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rewardVote","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"rewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_rewardDistribution","type":"address"}],"name":"setRewardDistribution","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_rewardReferral","type":"address"}],"name":"setRewardReferral","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_rewardVote","type":"address"}],"name":"setRewardVote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"referrer","type":"address"}],"name":"stake","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"stakingPower","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"starttime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"supportedStakingCoinWeiMultiple","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalAccumulatedReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"}],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userRewardPerTokenPaid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"vETH","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"vETHBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"vETH_REWARD_FRACTION_RATE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"vUSD","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"vUSDBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"vUSD_REWARD_FRACTION_RATE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"weiBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"weiTotalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"yfv","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]')
seedPool_contract_addr = web3.toChecksumAddress('0xC2D55CE14a8e04AEF9B6bCfD105079b63C6a0AC8')
seedPool_contract = web3.eth.contract(address=seedPool_contract_addr, abi=seedPool_contract_abi)

def process_gvValue_deposit_transactions(from_block, to_block):
    new_wallets_count = 0
    active_wallets_count = 0
    total_deposit = 0

    event_filter = govVault_ValueLiquid_contract.events.Deposit.createFilter(fromBlock=from_block, toBlock=to_block)
    txn_logs = event_filter.get_all_entries()
    print('Number of txn: ' + str(len(txn_logs)))

    for txn in txn_logs:
        deposit_addr = txn['args']['user']
        # check if this wallet is in database
        wallets_found = WalletAddress.objects.filter(wallet_address=deposit_addr).count()
        deposit_amount = txn['args']['amount']/1e18
        total_deposit += deposit_amount

        # if wallet not in database
        if (wallets_found == 0):
            print('New address deposited:' + deposit_addr)
            print('Amount: ' + '{:.2f}'.format(deposit_amount))
            if (deposit_amount > 0):
                print('Add it to database')
                new_wallets_count += 1
                # get value in this wallet from chain
                value_amount = value_contract.functions.balanceOf(deposit_addr).call()/1e18
                # add wallet to database
                wallet_addr = WalletAddress.objects.create(wallet_address=deposit_addr)
                # create new balance for this wallet
                WalletBalance.objects.create(address=wallet_addr, value=value_amount, gvValue=deposit_amount)
        else:
            print('Existing address:' + deposit_addr)
            print('Update its gvValue balance')
            active_wallets_count += 1
            # get its balance from chain and update database
            value_amount = value_contract.functions.balanceOf(deposit_addr).call()/1e18
            gvValue_staked_amount = govVault_ValueLiquid_contract.functions.userInfo(deposit_addr).call()[0]/1e18
            print('Hold: ' + str(value_amount))
            print('Staked amount: ' + str(gvValue_staked_amount))
            # update database
            wallet_found = WalletAddress.objects.get(wallet_address=deposit_addr)
            wallet_balance = WalletBalance.objects.get(address=wallet_found)
            wallet_balance.Value = value_amount
            wallet_balance.gvValue = gvValue_staked_amount
            wallet_balance.save()

    info = {
        'Txn count': len(txn_logs),
        'New wallets': new_wallets_count,
        'Active wallets': active_wallets_count,
        'Deposit amount': total_deposit
    }
    print(info)
    return info

def process_gvValue_withdraw_transactions(from_block, to_block):
    active_wallets_count = 0
    error_wallets_count = 0
    left_wallets_count = 0
    total_withdraw = 0

    event_filter = govVault_ValueLiquid_contract.events.Withdraw.createFilter(fromBlock=from_block, toBlock=to_block)
    txn_logs = event_filter.get_all_entries()
    print('Number of txn: ' + str(len(txn_logs)))

    for txn in txn_logs:
        withdraw_addr = txn['args']['user']
        # check if this wallet is in database
        wallets_found = WalletAddress.objects.filter(wallet_address=withdraw_addr).count()
        withdraw_amount = txn['args']['amount']/1e18
        total_withdraw += withdraw_amount

        # if wallet not in database
        if (wallets_found == 0):
            print('Seems wrong. Withdraw from new wallet?')
            error_wallets_count += 1
            # get its balance from chain and update database
            value_amount = value_contract.functions.balanceOf(withdraw_addr).call()/1e18
            gvValue_staked_amount = govVault_ValueLiquid_contract.functions.userInfo(withdraw_addr).call()[0]/1e18
            print('Hold: ' + str(value_amount))
            print('Staked amount: ' + str(gvValue_staked_amount))
            if (gvValue_staked_amount > 0):
                # create new balance for this wallet
                WalletBalance.objects.create(address=withdraw_addr, value=value_amount, gvValue=gvValue_staked_amount)
        else:
            print('Existing address:' + withdraw_addr)
            # get its balance from chain and update database
            value_amount = value_contract.functions.balanceOf(withdraw_addr).call()/1e18
            gvValue_staked_amount = govVault_ValueLiquid_contract.functions.userInfo(withdraw_addr).call()[0]/1e18
            print('Hold: ' + str(value_amount))
            print('Staked amount: ' + str(gvValue_staked_amount))
            if (gvValue_staked_amount > 0):
                # update database
                print('Update its balance')
                active_wallets_count += 1
                wallet_found = WalletAddress.objects.get(wallet_address=withdraw_addr)
                wallet_balance = WalletBalance.objects.get(address=wallet_found)
                wallet_balance.value = value_amount
                wallet_balance.gvValue = gvValue_staked_amount
                wallet_balance.save()
            else:
                print('Zero gvValue, remove from database')
                left_wallets_count += 1
                wallet_found = WalletAddress.objects.get(wallet_address=withdraw_addr)
                wallet_found_balance = WalletBalance.objects.get(address=wallet_found)
                wallet_found_balance.delete()
                wallet_found.delete()

    info = {
        'Txn count': len(txn_logs),
        'Error wallets': error_wallets_count,
        'Active wallets': active_wallets_count,
        'Left wallets': left_wallets_count,
        'Withdraw amount': total_withdraw
    }
    print(info)
    return info

def update_gvValue_holders_tables(from_block, to_block=None):
    if to_block is None:
        # get latest block number
        to_block_number = web3.eth.getBlock('latest')['number']
    else:
        to_block_number = to_block

    # get timestamp of to_block
    to_block_timestamp = web3.eth.getBlock(to_block_number)['timestamp']

    # keep track of last updated block
    settings = TrackingSetting.load()
    settings.gv_latest_update = datetime.fromtimestamp(to_block_timestamp, tz=timezone.utc)
    settings.gv_latest_block_number = to_block_number
    settings.save()

    # deposit
    deposit_info = process_gvValue_deposit_transactions(from_block, to_block_number)
    # withdraw
    withdraw_info = process_gvValue_withdraw_transactions(from_block, to_block_number)
    # total locked amount in gov vault
    gv_locked_amount = govVault_ValueLiquid_contract.functions.totalSupply().call()/1e18
    # holders
    existing_wallets_count = WalletBalance.objects.all().count()
    
    # update statistic ValueHolders table
    Holder.objects.create(
        timestamp = settings.gv_latest_update,
        from_block = from_block,
        to_block = to_block_number,
        deposits_count = deposit_info['Txn count'],
        withdraws_count = withdraw_info['Txn count'],
        new_wallets = deposit_info['New wallets'],
        left_wallets = withdraw_info['Left wallets'],
        total_wallets = existing_wallets_count,
        total_deposit = deposit_info['Deposit amount'],
        total_withdraw = withdraw_info['Withdraw amount'],
        total_locked = gv_locked_amount
    )

    info = {
        'Deposit count': deposit_info['Txn count'],
        'Withdraw count': withdraw_info['Txn count'],
        'Active wallets': deposit_info['Active wallets'] + withdraw_info['Active wallets'],
        'New wallets': deposit_info['New wallets'],
        'Left wallets': withdraw_info['Left wallets'],
        'Existing_wallets': existing_wallets_count,
        'Total deposit': deposit_info['Deposit amount'],
        'Total withdraw': withdraw_info['Withdraw amount'],
        'Total locked amount': gv_locked_amount,
        'gvValue flow': deposit_info['Deposit amount'] - withdraw_info['Withdraw amount']
    }
    return info

def update_gv_performance():
    gv_price_per_share = govVault_ValueLiquid_contract.functions.getPricePerFullShare().call()/1e18

    VaultsPerformance.objects.create(
        timestamp = timezone.now(),
        gov_vault = gv_price_per_share,
    )

    info = {
        'Current gvValue price per Share': gv_price_per_share
    }
    return info

def process_seedpool_staked_transactions(from_block, to_block=None):
    if to_block is None:
        # get latest block number
        to_block_number = web3.eth.getBlock('latest')['number']
    else:
        to_block_number = to_block

    event_filter = seedPool_contract.events.Staked.createFilter(fromBlock=from_block, toBlock=to_block_number)
    txn_logs = event_filter.get_all_entries()
    print('Number of staked txn: ' + str(len(txn_logs)))

    for txn in txn_logs:
        wallet_addr = txn['args']['user']
        wallets_cnt = SeedPoolHolder.objects.filter(wallet_address=wallet_addr).count()
        print('Wallet staked: ' + wallet_addr)
        # get its current stakes
        usdt_bal = seedPool_contract.functions.balanceOf(tokenAddress=usdt_addr, account=wallet_addr).call()/1e6
        usdc_bal = seedPool_contract.functions.balanceOf(tokenAddress=usdc_addr, account=wallet_addr).call()/1e6
        dai_bal = seedPool_contract.functions.balanceOf(tokenAddress=dai_addr, account=wallet_addr).call()/1e18

        # new wallet
        if (wallets_cnt == 0):
            print('New wallet')
            if (usdt_bal > 5) or (usdc_bal > 5) or (dai_bal > 5):
                print('With balance, add it')

                # create new object
                SeedPoolHolder.objects.create(
                    wallet_address = wallet_addr,
                    usdt_balance = usdt_bal,
                    usdc_balance = usdc_bal,
                    dai_balance = dai_bal
                )
            else:
                print('No balance, ignore it')
        else:
            print('Existing wallet')
            if (usdt_bal > 10) or (usdc_bal > 10) or (dai_bal > 10):
                print('With balance, update it')
                wallet = SeedPoolHolder.objects.get(wallet_address=wallet_addr)
                wallet.usdt_balance = usdt_bal
                wallet.usdc_balance = usdc_bal
                wallet.dai_balance = dai_bal
                wallet.save()
            else:
                print('No balance, delete it')
                wallet = SeedPoolHolder.objects.get(wallet_address=wallet_addr)
                wallet.delete()

def process_seedpool_withdrawn_transactions(from_block, to_block=None):
    if to_block is None:
        # get latest block number
        to_block_number = web3.eth.getBlock('latest')['number']
    else:
        to_block_number = to_block

    event_filter = seedPool_contract.events.Withdrawn.createFilter(fromBlock=from_block, toBlock=to_block_number)
    txn_logs = event_filter.get_all_entries()
    print('Number of withdrawn txn: ' + str(len(txn_logs)))

    for txn in txn_logs:
        wallet_addr = txn['args']['user']
        wallets_cnt = SeedPoolHolder.objects.filter(wallet_address=wallet_addr).count()
        print('Wallet withdrawn: ' + wallet_addr)
        # get its current stakes
        usdt_bal = seedPool_contract.functions.balanceOf(tokenAddress=usdt_addr, account=wallet_addr).call()/1e6
        usdc_bal = seedPool_contract.functions.balanceOf(tokenAddress=usdc_addr, account=wallet_addr).call()/1e6
        dai_bal = seedPool_contract.functions.balanceOf(tokenAddress=dai_addr, account=wallet_addr).call()/1e18

        # new wallet
        if (wallets_cnt == 0):
            print('Seem wrong, withdrawn from new wallet?')
            if (usdt_bal > 5) or (usdc_bal > 5) or (dai_bal > 5):
                print('With balance, add it')

                # create new object
                SeedPoolHolder.objects.create(
                    wallet_address = wallet_addr,
                    usdt_balance = usdt_bal,
                    usdc_balance = usdc_bal,
                    dai_balance = dai_bal
                )
            else:
                print('No balance, ignore it')
        else:
            print('Existing wallet')
            if (usdt_bal > 10) or (usdc_bal > 10) or (dai_bal > 10):
                print('With balance, update it')
                wallet = SeedPoolHolder.objects.get(wallet_address=wallet_addr)
                wallet.usdt_balance = usdt_bal
                wallet.usdc_balance = usdc_bal
                wallet.dai_balance = dai_bal
                wallet.save()
            else:
                print('No balance, delete it')
                wallet = SeedPoolHolder.objects.get(wallet_address=wallet_addr)
                wallet.delete()

def update_seedpool_holders_tables(from_block, to_block=None):
    if to_block is None:
        # get latest block number
        to_block_number = web3.eth.getBlock('latest')['number']
    else:
        to_block_number = to_block

    process_seedpool_staked_transactions(from_block, to_block_number)
    process_seedpool_withdrawn_transactions(from_block, to_block_number)
