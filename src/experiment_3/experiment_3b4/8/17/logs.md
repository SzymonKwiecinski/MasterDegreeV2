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
To formulate this problem as a linear programming model, we will define the decision variables, objective function, and constraints. The objective is to maximize the expected value of the investor's portfolio next year after selling certain shares to raise the required amount \(K\), net of transaction and tax costs.

**Decision Variables:**
- Let \( \text{sell}_i \) be the number of shares of stock \( i \) that the investor should sell, for each \( i = 1, \ldots, N \).

**Objective Function:**
- We aim to maximize the expected value of the portfolio next year:
  \[
  \sum_{i=1}^{N} (bought_i - \text{sell}_i) \cdot \text{futurePrice}_i
  \]

**Constraints:**
1. Capital raised from selling shares should meet or exceed \( K \) considering transaction costs and taxes:
   \[
   \sum_{i=1}^{N} \left( \text{sell}_i \cdot \text{currentPrice}_i \cdot (1 - \frac{\text{transactionRate}}{100}) - (\text{sell}_i \cdot (\text{currentPrice}_i - \text{buyPrice}_i) \cdot \frac{\text{taxRate}}{100}) \right) \geq K
   \]

2. The number of shares sold cannot exceed the number of shares owned:
   \[
   0 \leq \text{sell}_i \leq \text{bought}_i \quad \text{for all } i = 1, \ldots, N
   \]

Below is the LaTeX representation of the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model}

\textbf{Objective:} Maximize the expected value of the portfolio next year
\[
\max \sum_{i=1}^{N} (bought_i - \text{sell}_i) \cdot futurePrice_i
\]

\textbf{Subject to:}
\begin{align*}
& \sum_{i=1}^{N} \left( \text{sell}_i \cdot \text{currentPrice}_i \cdot \left(1 - \frac{\text{transactionRate}}{100}\right) - (\text{sell}_i \cdot (\text{currentPrice}_i - \text{buyPrice}_i) \cdot \frac{\text{taxRate}}{100}) \right) \geq K \\
& 0 \leq \text{sell}_i \leq bought_i, \quad \text{for all } i = 1, \ldots, N
\end{align*}

\end{document}
```

This mathematical model captures the decision of how many shares to sell while considering transaction costs and taxes, ensuring that the net amount raised meets the required amount \( K \), and maximizes the expected future value of the portfolio.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model}

\textbf{Objective:} Maximize the expected value of the portfolio next year
\[
\max \sum_{i=1}^{N} (bought_i - \text{sell}_i) \cdot futurePrice_i
\]

\textbf{Subject to:}
\begin{align*}
& \sum_{i=1}^{N} \left( \text{sell}_i \cdot \text{currentPrice}_i \cdot \left(1 - \frac{\text{transactionRate}}{100}\right) - (\text{sell}_i \cdot (\text{currentPrice}_i - \text{buyPrice}_i) \cdot \frac{\text{taxRate}}{100}) \right) \geq K \\
& 0 \leq \text{sell}_i \leq bought_i, \quad \text{for all } i = 1, \ldots, N
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

#### Problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

#### Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

#### Objective Function
objective = pulp.lpSum((bought[i] - sell[i]) * future_price[i] for i in range(N))
problem += objective

#### Constraints
constraint = pulp.lpSum(
    sell[i] * current_price[i] * (1 - transaction_rate / 100) - 
    (sell[i] * (current_price[i] - buy_price[i]) * tax_rate / 100)
    for i in range(N)
) >= K

problem += constraint

#### Solve the problem
problem.solve()

#### Print the results
print(f"Status: {pulp.LpStatus[problem.status]}")
for i in range(N):
    print(f"Sell Amount of Asset {i+1}: {pulp.value(sell[i])}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

