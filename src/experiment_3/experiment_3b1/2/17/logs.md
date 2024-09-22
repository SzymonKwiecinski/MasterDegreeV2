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

\section*{Linear Programming Model}

Let:
\begin{itemize}
    \item $N$: Number of different stocks.
    \item $bought_i$: Number of shares bought for stock $i$.
    \item $buyPrice_i$: Purchase price per share of stock $i$.
    \item $currentPrice_i$: Current price per share of stock $i$.
    \item $futurePrice_i$: Expected future price per share of stock $i$.
    \item $transactionRate$: Transaction cost rate as a percentage.
    \item $taxRate$: Tax rate on capital gains as a percentage.
    \item $K$: Desired net amount of money to be raised.
    \item $sell_i$: Number of shares of stock $i$ that the investor should sell.
\end{itemize}

\subsection*{Objective Function}
We want to maximize the expected value of the portfolio next year after selling stocks, thus we need to maximize:
\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( futurePrice_i \cdot (bought_i - sell_i) \right)
\]

\subsection*{Constraints}
1. The total amount raised from selling stocks must be equal to the amount needed ($K$) net of transaction costs and taxes:

\[
\sum_{i=1}^{N} \left( currentPrice_i \cdot sell_i \cdot (1 - transactionRate/100) - (currentPrice_i - buyPrice_i) \cdot sell_i \cdot (taxRate/100) \right) \geq K
\]

2. The number of shares sold must not exceed the number of shares bought for each stock:

\[
0 \leq sell_i \leq bought_i, \quad \forall i = 1, \ldots, N
\]

3. Non-negativity constraint:

\[
sell_i \geq 0, \quad \forall i = 1, \ldots, N
\]

\subsection*{Output Format}
The output will consist of the number of shares that should be sold for each stock:

\[
\text{Output: } \{ "sell": [sell_1, sell_2, \ldots, sell_N] \}
\]

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

\section*{Linear Programming Model}

Let:
\begin{itemize}
    \item $N$: Number of different stocks.
    \item $bought_i$: Number of shares bought for stock $i$.
    \item $buyPrice_i$: Purchase price per share of stock $i$.
    \item $currentPrice_i$: Current price per share of stock $i$.
    \item $futurePrice_i$: Expected future price per share of stock $i$.
    \item $transactionRate$: Transaction cost rate as a percentage.
    \item $taxRate$: Tax rate on capital gains as a percentage.
    \item $K$: Desired net amount of money to be raised.
    \item $sell_i$: Number of shares of stock $i$ that the investor should sell.
\end{itemize}

\subsection*{Objective Function}
We want to maximize the expected value of the portfolio next year after selling stocks, thus we need to maximize:
\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( futurePrice_i \cdot (bought_i - sell_i) \right)
\]

\subsection*{Constraints}
1. The total amount raised from selling stocks must be equal to the amount needed ($K$) net of transaction costs and taxes:

\[
\sum_{i=1}^{N} \left( currentPrice_i \cdot sell_i \cdot (1 - transactionRate/100) - (currentPrice_i - buyPrice_i) \cdot sell_i \cdot (taxRate/100) \right) \geq K
\]

2. The number of shares sold must not exceed the number of shares bought for each stock:

\[
0 \leq sell_i \leq bought_i, \quad \forall i = 1, \ldots, N
\]

3. Non-negativity constraint:

\[
sell_i \geq 0, \quad \forall i = 1, \ldots, N
\]

\subsection*{Output Format}
The output will consist of the number of shares that should be sold for each stock:

\[
\text{Output: } \{ "sell": [sell_1, sell_2, \ldots, sell_N] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads("""{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}""")

#### Parameters
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

#### Problem definition
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

#### Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

#### Objective function
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

#### Constraint
problem += (pulp.lpSum(currentPrice[i] * sell[i] * (1 - transactionRate / 100) 
                         - (currentPrice[i] - buyPrice[i]) * sell[i] * (taxRate / 100) 
                         for i in range(N)) >= K), "Minimum_Amount_Raised")

#### Solve the problem
problem.solve()

#### Output
sell_shares = [pulp.value(sell[i]) for i in range(N)]
print(f'Output: {{"sell": {sell_shares}}}')
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
import json

#### Input data
data = json.loads("""{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}""")

#### Parameters
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

#### Problem definition
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

#### Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

#### Objective function
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

#### Constraint
problem += (pulp.lpSum(currentPrice[i] * sell[i] * (1 - transactionRate / 100) 
                         - (currentPrice[i] - buyPrice[i]) * sell[i] * (taxRate / 100) 
                         for i in range(N)) >= K), "Minimum_Amount_Raised")

#### Solve the problem
problem.solve()

#### Output
sell_shares = [pulp.value(sell[i]) for i in range(N)]
print(f'Output: {{"sell": {sell_shares}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/2/17/python_code0.py", line 29
    for i in range(N)) >= K), "Minimum_Amount_Raised")
                                                     ^
SyntaxError: unmatched ')'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads("""{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}""")

#### Parameters
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

#### Problem definition
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

#### Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

#### Objective function
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

#### Constraint
problem += (pulp.lpSum(currentPrice[i] * sell[i] * (1 - transactionRate / 100) 
                         - (currentPrice[i] - buyPrice[i]) * sell[i] * (taxRate / 100) 
                         for i in range(N)) >= K, "Minimum_Amount_Raised")

#### Solve the problem
problem.solve()

#### Output
sell_shares = [pulp.value(sell[i]) for i in range(N)]
print(f'Output: {{"sell": {sell_shares}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

