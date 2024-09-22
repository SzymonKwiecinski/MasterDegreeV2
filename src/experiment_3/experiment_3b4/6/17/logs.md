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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Investor's Portfolio Optimization}

We define the following parameters and decision variables:

\begin{itemize}
    \item $N$: Number of different stocks.
    \item $bought_i$: Number of shares initially bought for stock $i$, for $i = 1, \ldots, N$.
    \item $buyPrice_i$: Initial buying price per share for stock $i$, for $i = 1, \ldots, N$.
    \item $currentPrice_i$: Current price per share for stock $i$, for $i = 1, \ldots, N$.
    \item $futurePrice_i$: Expected price per share for stock $i$ in one year, for $i = 1, \ldots, N$.
    \item $transactionRate$: Transaction cost rate as a percentage.
    \item $taxRate$: Tax rate on capital gains as a percentage.
    \item $K$: The amount of money the investor wants to raise.
    \item $sell_i$: Number of shares to sell for stock $i$, for $i = 1, \ldots, N$ (decision variables).
\end{itemize}

\subsection*{Objective Function}

Maximize the expected value of the portfolio next year:

\[
\text{Maximize} \quad \sum_{i=1}^{N} (bought_i - sell_i) \cdot futurePrice_i
\]

\subsection*{Constraints}

1. Non-negativity and selling constraints:
   \[
   0 \leq sell_i \leq bought_i, \quad \forall i = 1, \ldots, N
   \]

2. Raise the required money $K$:
   \[
   \sum_{i=1}^{N} \left( (1 - \frac{\text{transactionRate}}{100}) \cdot currentPrice_i \cdot sell_i - \frac{\text{taxRate}}{100} \cdot \max(0, (currentPrice_i - buyPrice_i) \cdot sell_i) \right) \geq K
   \]

Here, the term $\max(0, (currentPrice_i - buyPrice_i) \cdot sell_i)$ ensures that we only tax positive capital gains.

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Investor's Portfolio Optimization}

We define the following parameters and decision variables:

\begin{itemize}
    \item $N$: Number of different stocks.
    \item $bought_i$: Number of shares initially bought for stock $i$, for $i = 1, \ldots, N$.
    \item $buyPrice_i$: Initial buying price per share for stock $i$, for $i = 1, \ldots, N$.
    \item $currentPrice_i$: Current price per share for stock $i$, for $i = 1, \ldots, N$.
    \item $futurePrice_i$: Expected price per share for stock $i$ in one year, for $i = 1, \ldots, N$.
    \item $transactionRate$: Transaction cost rate as a percentage.
    \item $taxRate$: Tax rate on capital gains as a percentage.
    \item $K$: The amount of money the investor wants to raise.
    \item $sell_i$: Number of shares to sell for stock $i$, for $i = 1, \ldots, N$ (decision variables).
\end{itemize}

\subsection*{Objective Function}

Maximize the expected value of the portfolio next year:

\[
\text{Maximize} \quad \sum_{i=1}^{N} (bought_i - sell_i) \cdot futurePrice_i
\]

\subsection*{Constraints}

1. Non-negativity and selling constraints:
   \[
   0 \leq sell_i \leq bought_i, \quad \forall i = 1, \ldots, N
   \]

2. Raise the required money $K$:
   \[
   \sum_{i=1}^{N} \left( (1 - \frac{\text{transactionRate}}{100}) \cdot currentPrice_i \cdot sell_i - \frac{\text{taxRate}}{100} \cdot \max(0, (currentPrice_i - buyPrice_i) \cdot sell_i) \right) \geq K
   \]

Here, the term $\max(0, (currentPrice_i - buyPrice_i) \cdot sell_i)$ ensures that we only tax positive capital gains.

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

#### Extract data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate'] / 100
TaxRate = data['TaxRate'] / 100
K = data['K']

#### Problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

#### Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

#### Objective
problem += pulp.lpSum((Bought[i] - sell[i]) * FuturePrice[i] for i in range(N)), "Expected_Future_Value"

#### Constraints
#### Constraint 1: Non-negativity and selling constraints are handled in variable bounds
#### Constraint 2: Raise the required money K
problem += pulp.lpSum(
    ((1 - TransactionRate) * CurrentPrice[i] * sell[i] -
     TaxRate * pulp.lpSum([pulp.lpMax(0, (CurrentPrice[i] - BuyPrice[i]) * sell[i])]))
    for i in range(N)
) >= K, "Raise_Required_Money"

#### Solve
problem.solve()

#### Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
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

#### Extract data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate'] / 100
TaxRate = data['TaxRate'] / 100
K = data['K']

#### Problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

#### Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

#### Objective
problem += pulp.lpSum((Bought[i] - sell[i]) * FuturePrice[i] for i in range(N)), "Expected_Future_Value"

#### Constraints
#### Constraint 1: Non-negativity and selling constraints are handled in variable bounds
#### Constraint 2: Raise the required money K
problem += pulp.lpSum(
    ((1 - TransactionRate) * CurrentPrice[i] * sell[i] -
     TaxRate * pulp.lpSum([pulp.lpMax(0, (CurrentPrice[i] - BuyPrice[i]) * sell[i])]))
    for i in range(N)
) >= K, "Raise_Required_Money"

#### Solve
problem.solve()

#### Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b4/6/17/python_code0.py", line 37, in <module>
    problem += pulp.lpSum(
               ^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 2233, in lpSum
    return LpAffineExpression().addInPlace(vector)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 867, in addInPlace
    for e in other:
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b4/6/17/python_code0.py", line 39, in <genexpr>
    TaxRate * pulp.lpSum([pulp.lpMax(0, (CurrentPrice[i] - BuyPrice[i]) * sell[i])]))
                          ^^^^^^^^^^
AttributeError: module 'pulp' has no attribute 'lpMax'
</CODE_ERROR>


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

#### Extract data
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate'] / 100
TaxRate = data['TaxRate'] / 100
K = data['K']

#### Problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

#### Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i], cat='Continuous') for i in range(N)]

#### Objective
problem += pulp.lpSum((Bought[i] - sell[i]) * FuturePrice[i] for i in range(N)), "Expected_Future_Value"

#### Constraints
#### Constraint 1: Non-negativity and selling constraints are handled in variable bounds
#### Constraint 2: Raise the required money K
problem += pulp.lpSum(
    ((1 - TransactionRate) * CurrentPrice[i] * sell[i] -
     TaxRate * pulp.lpSum(pulp.lpMax(0, (CurrentPrice[i] - BuyPrice[i]) * sell[i]) for i in range(N)))
    ) for i in range(N)
) >= K, "Raise_Required_Money"

#### Solve
problem.solve()

#### Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

