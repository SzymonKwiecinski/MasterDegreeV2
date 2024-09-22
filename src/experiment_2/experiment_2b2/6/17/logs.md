# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- An investor has a portfolio of \var{N} different stocks.
- He has bought \var{bought_i} shares of stock \var{i} at price \var{buyPrice_i}. 
- The current price of one share of stock \var{i} is \var{currentPrice_i}.
- The investor expects that the price of one share of stock \var{i} in one year will be \var{futurePrice_i}.
- If he sells shares, the investor pays transaction costs at the rate of \var{transactionRate} % of the amount transacted.
- In addition, the investor pays taxes at the rate of \var{taxRate} % on capital gains (i.e., the difference between the amount received from selling shares and the amount paid to buy them).
- Both transaction costs and taxes are numbers between 0 and 100.
- The investor wants to raise an amount of money \var{K} net of capital gains and transaction costs.
- You can assume that the investor can sell floating point numbers of shares.

INPUT FORMAT: 

{
    "bought": [bought_i, for i in 1, ..., N],
    "buyPrice": [buyPrice_i, for i in 1, ..., N],
    "currentPrice": [currentPrice_i, for i in 1, ..., N],
    "futurePrice": [futurePrice_i, for i in 1, ..., N],
    "transactionRate": transactionRate,
    "taxRate": taxRate,
    "K": K
}

OBJECTIVE: We want to know how many shares the investor needs to sell in order to raise the needed money, net of capital gains and transaction costs, while maximizing the expected value of his portfolio next year.

OUTPUT INFO:

- \var{sell_i} is the number of shares of stock \var{i} that the investor should sell.

OUTPUT FORMAT:

{
    "sell": [sell_i, for i in 1, ..., N],
}

</DESCRIPTION>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Transform the input data into variables
data = {
    "N": 3,
    "Bought": [100, 150, 80],
    "BuyPrice": [50, 40, 30],
    "CurrentPrice": [60, 35, 32],
    "FuturePrice": [65, 44, 34],
    "TransactionRate": 1.0,
    "TaxRate": 15.0,
    "K": 5000
}

N = data["N"]
Bought = data["Bought"]
BuyPrice = data["BuyPrice"]
CurrentPrice = data["CurrentPrice"]
FuturePrice = data["FuturePrice"]
TransactionRate = data["TransactionRate"] / 100
TaxRate = data["TaxRate"] / 100
K = data["K"]

#### Define the problem
problem = pulp.LpProblem("Investor_Portfolio", pulp.LpMaximize)

#### Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

#### Objective function: Maximize the expected value of the portfolio next year
expected_value = pulp.lpSum((Bought[i] - sell[i]) * FuturePrice[i] for i in range(N))
problem += expected_value

#### Add the financial constraints
#### Constraint: Amount raised must be at least K, considering transaction costs and taxes
price_after_transaction = [CurrentPrice[i] * (1 - TransactionRate) for i in range(N)]
capital_gain = [pulp.lpSum((CurrentPrice[i] - BuyPrice[i]) * sell[i]) for i in range(N)]
tax_on_capital_gain = [TaxRate * capital_gain[i] for i in range(N)]
net_amount_received = [pulp.lpSum(price_after_transaction[i] * sell[i] - tax_on_capital_gain[i]) for i in range(N)]

problem += (pulp.lpSum(net_amount_received) >= K, "Net_Amount_Required")

#### Solve the problem
problem.solve()

#### Prepare the output
output = {
    "sell": [pulp.value(sell[i]) for i in range(N)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

