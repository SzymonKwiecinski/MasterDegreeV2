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
To formulate this problem as a Linear Programming (LP) model, we need to define the decision variables, constraints, and the objective function based on the given problem description.

######### Decision Variables:
- Let \( x_i \) be the number of shares of stock \( i \) to sell.

######### Parameters:
- \( \text{bought}_i \): Number of shares initially bought for stock \( i \).
- \( \text{buyPrice}_i \): Initial buying price per share of stock \( i \).
- \( \text{currentPrice}_i \): Current price per share of stock \( i \).
- \( \text{futurePrice}_i \): Expected future price per share of stock \( i \).
- \( \text{transactionRate} \): Transaction cost rate in percentage.
- \( \text{taxRate} \): Tax rate on capital gains in percentage.
- \( K \): Required amount of money to be raised.

######### Objective:
Maximize the expected value of the portfolio next year, which is given by the sum of the expected future values of the remaining shares after selling:
\[
\text{maximize} \quad \sum_{i=1}^{N} (\text{bought}_i - x_i) \cdot \text{futurePrice}_i
\]

######### Constraints:
1. The amount raised after transaction costs and taxes must be at least \( K \):
   \[
   \sum_{i=1}^{N} \left[ x_i \cdot \text{currentPrice}_i \cdot \left(1 - \frac{\text{transactionRate}}{100}\right) - (x_i \cdot \text{currentPrice}_i - x_i \cdot \text{buyPrice}_i) \cdot \frac{\text{taxRate}}{100} \right] \geq K
   \]

2. The number of shares sold cannot exceed the number of shares owned:
   \[
   0 \leq x_i \leq \text{bought}_i \quad \text{for all } i = 1, 2, \ldots, N
   \]

######### Latex Representation:
Here is the mathematical model represented in LaTeX.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{maximize} \quad \sum_{i=1}^{N} (\text{bought}_i - x_i) \cdot \text{futurePrice}_i
\]

\textbf{Subject to:}

\[
\sum_{i=1}^{N} \left[ x_i \cdot \text{currentPrice}_i \cdot \left(1 - \frac{\text{transactionRate}}{100}\right) - (x_i \cdot \text{currentPrice}_i - x_i \cdot \text{buyPrice}_i) \cdot \frac{\text{taxRate}}{100} \right] \geq K
\]

\[
0 \leq x_i \leq \text{bought}_i \quad \text{for all } i = 1, 2, \ldots, N
\]

\end{document}
```

This model will help determine the optimal number of shares to sell from each stock to meet the required amount \( K \) while maximizing the expected portfolio value.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{maximize} \quad \sum_{i=1}^{N} (\text{bought}_i - x_i) \cdot \text{futurePrice}_i
\]

\textbf{Subject to:}

\[
\sum_{i=1}^{N} \left[ x_i \cdot \text{currentPrice}_i \cdot \left(1 - \frac{\text{transactionRate}}{100}\right) - (x_i \cdot \text{currentPrice}_i - x_i \cdot \text{buyPrice}_i) \cdot \frac{\text{taxRate}}{100} \right] \geq K
\]

\[
0 \leq x_i \leq \text{bought}_i \quad \text{for all } i = 1, 2, \ldots, N
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Future_Value", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, upBound=data['Bought'][i]) for i in range(data['N'])]

#### Objective Function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))

#### Constraints
problem += pulp.lpSum(
    x[i] * data['CurrentPrice'][i] * (1 - data['TransactionRate'] / 100) -
    (x[i] * data['CurrentPrice'][i] - x[i] * data['BuyPrice'][i]) * data['TaxRate'] / 100
    for i in range(data['N'])
) >= data['K']

#### Solve the problem
problem.solve()

#### Print Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

