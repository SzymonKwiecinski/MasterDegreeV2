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
To solve this problem, we will create a linear programming model using the Pulp Python library. We will define the decision variables, constraints, and the objective function. The task is to determine how many shares should be sold to raise the required amount of money \( K \), while maximizing the expected future value of the portfolio.

Let's break it down step-by-step in the code below:

```python
import pulp

#### Parse the data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

#### Define the LP problem
problem = pulp.LpProblem("Maximize_Future_Portfolio_Value", pulp.LpMaximize)

#### Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

#### Objective: maximize expected future value of the portfolio
future_value = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += future_value

#### Constraint: raise at least K amount after costs and taxes
#### Net proceeds from selling stock i = sell_i * currentPrice_i * (1 - transactionRate)
#### Net capital gains from selling stock i = max(0, (currentPrice_i - buyPrice_i) * sell_i)
net_proceeds = pulp.lpSum(sell[i] * current_price[i] * (1 - transaction_rate) for i in range(N))
capital_gains = pulp.lpSum(pulp.lpSum((current_price[i] - buy_price[i]) * sell[i] for i in range(N) if current_price[i] > buy_price[i]))
net_capital_gains = capital_gains * (1 - tax_rate)

#### Required to raise at least K amount
problem += (net_proceeds - net_capital_gains) >= K

#### Solve the problem
problem.solve()

#### Prepare the output
sell_shares = [pulp.value(sell[i]) for i in range(N)]

output = {
    "sell": sell_shares
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This code defines a linear program to maximize the expected future value of the investment portfolio, subject to the constraint that the investor needs to raise a specific amount \( K \) after accounting for transaction costs and taxes on capital gains. We use decision variables to represent the number of shares to sell from each stock.

