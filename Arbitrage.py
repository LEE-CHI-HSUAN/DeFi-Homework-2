liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def getReserves(tokenA: str, tokenB: str) -> tuple[float, float]:
    (token0, token1) = (tokenA, tokenB) if tokenA < tokenB else (tokenB, tokenA)
    reserve0, reserve1 = liquidity.get((token0, token1))
    if (token0 == tokenA):
        return reserve0, reserve1
    else:
        return reserve1, reserve0

def getAmountOut(amountIn: float, tokenIn: str, tokenOut: str) -> float:
    assert amountIn > 0
    reserveIn, reserveOut = getReserves(tokenIn, tokenOut)
    assert reserveIn > 0 and reserveOut > 0

    amountInWithFee = amountIn * 997
    numerator = amountInWithFee * reserveOut
    denominator = reserveIn* 1000 + amountInWithFee
    amountOut = numerator / denominator
    return amountOut

def getAmountsOut(amountIn: float, path: list[str]):
    assert len(path) >= 2
    #amounts = [] * len(path)
    #amounts[0] = amountIn
    amount = amountIn
    for frm, to in zip(path[:-1], path[1:]):
        #amounts[i + 1] = getAmountOut(amounts[i], frm, to);
        amount = getAmountOut(amount, frm, to)
        # print(amount)
    return amount

def searchAllPath(path: list[str], candidates: list[str], amount: float) -> float:
    '''
    A DFS algorithm that search all possible path with no token visited twice
    It returns immediately once it finds a path that yields more than 20 units of tokenB.
    '''
    # Check whether the current path satisfies the termination policy
    if len(path) > 1:
        new_amount = getAmountOut(amount, path[-1], "tokenB")
        # print(path, new_amount)
        if new_amount >= 20:
            path.append("tokenB")
            return new_amount

    # Search for every outgoing edge
    for token in candidates:
        # if (path[-1] == token):
        #     continue
        new_amount = getAmountOut(amount, path[-1], token)
        new_candidates = candidates.copy()
        new_candidates.remove(token)
        path.append(token)
        finalAmount = searchAllPath(path, new_candidates, new_amount)
        if finalAmount > 0:
            return finalAmount
        path.pop()

    return 0


if __name__ == "__main__":
    candidates = ["tokenA", "tokenC", "tokenD"]
    path = ["tokenB"]
    finalAmount = searchAllPath(path, candidates, 5)
    print(f"path: {'->'.join(path)}, tokenB balance={finalAmount}")
