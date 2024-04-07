# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

1. tokenB->tokenA, amountIn = 5 amountOut = 5.655321988655322
2. tokenA->tokenD, amountIn = 5.655321988655322 amountOut = 2.4587813170979333
3. tokenD->tokenC, amountIn = 2.4587813170979333 amountOut = 5.0889272933015155
4. tokenC->tokenB, amountIn = 5.0889272933015155 amountOut = 20.129888944077443

Final reward (tokenB balance): 20.129888944077443
> There is a small discrepancy between the outputs of python and solidity due to variable types (float, uint).

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

Slippage refers to the discrepancy between the expected and the actual output amount of token in an exchange. The discrepancy arises from liquidity and other factors relating to the value of tokens.

To address this issue, we can set a slippage tolerance. Uniswap V2 Router01 provides functions that have the same mechanism, one of which is shown below.

```solidity
function swapExactTokensForTokens(
    uint amountIn,
    uint amountOutMin,
    address[] calldata path,
    address to,
    uint deadline
) external override ensure(deadline) returns (uint[] memory amounts);
```

The second argument `amountOutMin` is our slippage tolerance. If the real amountOut is less then `amountOutMin`, the transaction will revert. 

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

Since the value of a liquidity pool share was dependent on the ratio at which liquidity was initially deposited. The `MINIMUM_LIQUIDITY` sets a minimum threshold of liquidity. This can prevent attacker to let the value of share to grow too dramatically because the cost of attack is multiplied by `MINIMUM_LIQUIDITY`=1000.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

```solidity
liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
```

This formula first calculates the ratio of each token deposited in the pool, and only take the smaller one. If the ratios are not equal, the higher portion will be ignored. Therefore, the formula encourages people to deposit tokens proportional to the tokens in the pool.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

A victim wants to trade, say, token-A for token-B. The attacker then makes a transaction before the victim and raises the price of token-B. As a result, the slippage has increased and the victim has to trade at a higher price. The price of token-B will increase futher because of the second transaction; hence, the attack can sell token-B to make profit.

