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
To solve this problem, we will set up a linear programming model using the PuLP library in Python. Our goal is to determine how many shares the investor should sell in order to raise the required amount `K` while maximizing the expected future value of the portfolio.

First, let's outline the steps for the formulation:

1. **Decision Variables**: Let `sell_i` represent the number of shares to sell of stock `i`.

2. **Objective Function**: We aim to maximize the expected future value, which is the sum of:
   \[
   \text{Expected Future Value} = \sum (bought_i - sell_i) \times \text{futurePrice}_i
   \]

3. **Constraints**:
   - **Sell Non-Negativity and Limits**: \(0 \leq sell_i \leq bought_i\)
   - **Raise Required Amount**:
     \[
     \sum \left((\text{currentPrice}_i \times sell_i) - \left(\text{taxRate} \times \text{gain}_i + \text{transactionRate} \times \text{currentPrice}_i \times sell_i\right)\right) \geq K
     \]
     where \(\text{gain}_i = (\text{currentPrice}_i - \text{buyPrice}_i) \times sell_i\).

Let's implement the solution in Python using PuLP:

```python
import pulp

#### Data input
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

#### Parameters
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100.0
tax_rate = data['TaxRate'] / 100.0
K = data['K']

#### Define the linear programming problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

#### Decision variables
sell = [pulp.LpVariable(f"sell_{i}", 0, bought[i]) for i in range(N)]

#### Objective function: Maximize future portfolio value
problem += pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N)), "Maximize_Future_Value"

#### Constraint: Raise at least K after transaction costs and taxes
problem += pulp.lpSum(
    (current_price[i] * sell[i] - 
     tax_rate * (current_price[i] - buy_price[i]) * sell[i] - 
     transaction_rate * current_price[i] * sell[i]) for i in range(N)
) >= K, "Raise_Amount_K"

#### Solve the problem
problem.solve()

#### Extract the results
sell_values = [pulp.value(sell[i]) for i in range(N)]

#### Output format
output = {
    "sell": sell_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This code solves the optimization problem by defining the linear program using PuLP, setting up the decision variables, objective, and constraints, and then solving the problem. The results are printed in the required output format.

