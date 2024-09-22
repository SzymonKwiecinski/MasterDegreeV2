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
To solve the problem using the PuLP python library, we will formulate the linear programming model to maximize the expected value of the investor's portfolio next year while ensuring that the net amount raised is at least \( K \). We will incorporate the constraints on transaction costs and taxes.

Here's the code:

```python
import pulp

#### Data from JSON
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,
    'TaxRate': 15.0,
    'K': 5000
}

#### Extracting data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

#### Define the LP problem
problem = pulp.LpProblem("Maximize_Future_Value", pulp.LpMaximize)

#### Decision variables
sell = [pulp.LpVariable(f'sell_{i}', 0, bought[i]) for i in range(N)]

#### Objective function
problem += pulp.lpSum([
    future_price[i] * (bought[i] - sell[i]) for i in range(N)
]), "Maximize Future Value"

#### Constraint for net money raised
net_money_constraints = []
for i in range(N):
    sell_value = sell[i] * current_price[i]
    transaction_cost = sell_value * transaction_rate
    capital_gains = sell[i] * (current_price[i] - buy_price[i])
    tax_on_gains = capital_gains * tax_rate
    net_proceeds = sell_value - transaction_cost - tax_on_gains
    net_money_constraints.append(net_proceeds)

problem += pulp.lpSum(net_money_constraints) >= K, "Net Money Constraint"

#### Solve the problem
problem.solve()

#### Output the result
sell_result = [pulp.value(sell[i]) for i in range(N)]

output = {
    "sell": sell_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

The above script will calculate how many shares the investor should sell for each stock to raise the required net amount \( K \), while also maximizing the expected future value of the portfolio next year. The final result will provide both the number of shares to sell and the objective value, i.e., the expected future value of the portfolio.

