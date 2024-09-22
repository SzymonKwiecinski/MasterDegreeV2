# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this problem as a linear programming (LP) problem, we need to define decision variables, an objective function, and constraints. Let's break down the requirements and formulate the LP model.

######### Decision Variables
- Let \( \text{sell}_i \) be the number of shares of stock \( i \) that the investor should sell.

######### Objective Function
The investor wants to maximize the expected value of his portfolio next year. Therefore, the objective function is:

\[
\text{maximize} \quad \sum_{i=1}^{N} (bought_i - \text{sell}_i) \times \text{futurePrice}_i
\]

######### Constraints
1. **Capital Requirement Constraint:** The investor wants to raise an amount \( K \) net of capital gains and transaction costs. The total amount raised from selling shares of stock \( i \) is:

   \[
   \text{Amount received after selling } i = \text{sell}_i \times \text{currentPrice}_i \times (1 - \text{transactionRate}) 
   \]

   The capital gain for stock \( i \) is:

   \[
   \text{Capital Gain for } i = \left(\text{sell}_i \times \text{currentPrice}_i\right) - \left(\text{sell}_i \times \text{buyPrice}_i\right)
   \]

   The tax paid on the capital gain is:

   \[
   \text{Tax on } i = \text{Capital Gain for } i \times \text{taxRate}
   \]

   The net amount received after transaction costs and taxes for stock \( i \) is:

   \[
   \text{Net Amount for } i = \text{Amount received after selling } i - \text{Tax on } i
   \]

   Summing this over all \( i \), we must have:

   \[
   \sum_{i=1}^{N} \left(\text{sell}_i \times \text{currentPrice}_i \times (1 - \text{transactionRate}) - \left(\left(\text{sell}_i \times \text{currentPrice}_i - \text{sell}_i \times \text{buyPrice}_i\right) \times \text{taxRate}\right)\right) \geq K
   \]

2. **Non-negativity and Stock Limits:**

   \[
   0 \leq \text{sell}_i \leq \text{bought}_i \quad \text{for all } i
   \]

Now we can write the LP model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{maximize} \quad & \sum_{i=1}^{N} (bought_i - \text{sell}_i) \times \text{futurePrice}_i \\
\text{subject to} \quad 
& \sum_{i=1}^{N} \left(\text{sell}_i \times \text{currentPrice}_i \times (1 - \text{transactionRate}) - \left(\left(\text{sell}_i \times \text{currentPrice}_i - \text{sell}_i \times \text{buyPrice}_i\right) \times \text{taxRate}\right)\right) \geq K, \\
& 0 \leq \text{sell}_i \leq \text{bought}_i \quad \text{for all } i.
\end{align*}

\end{document}
```

This representation captures the objective of maximizing the expected portfolio value after selling the necessary shares while adhering to the financial constraints imposed by transaction costs, taxes, and the capital requirement \( K \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{maximize} \quad & \sum_{i=1}^{N} (bought_i - \text{sell}_i) \times \text{futurePrice}_i \\
\text{subject to} \quad 
& \sum_{i=1}^{N} \left(\text{sell}_i \times \text{currentPrice}_i \times (1 - \text{transactionRate}) - \left(\left(\text{sell}_i \times \text{currentPrice}_i - \text{sell}_i \times \text{buyPrice}_i\right) \times \text{taxRate}\right)\right) \geq K, \\
& 0 \leq \text{sell}_i \leq \text{bought}_i \quad \text{for all } i.
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
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

#### Variables
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

#### Objective function
profit = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += profit, "Total_Profit"

#### Constraints
problem += (pulp.lpSum(sell[i] * current_price[i] * (1 - transaction_rate) -
                       ((sell[i] * current_price[i] - sell[i] * buy_price[i]) * (tax_rate / 100))
                       for i in range(N)) >= K), "Minimum_Value_Constraint"

#### Upper bound constraints
for i in range(N):
    problem += (sell[i] <= bought[i], f"Upper_Bound_Sell_{i}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

