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

\section*{Problem Description}

The investor wants to decide how many shares of stock \(i\) to sell (\( \text{sell}_i \)) in order to raise a specified net amount of money \(K\), net of capital gains taxes and transaction costs. The goal is to maximize the expected value of the portfolio at the end of the year.

\section*{Mathematical Model}

Let:
\begin{itemize}
    \item \(N\) be the number of different stocks.
    \item \(\text{bought}_i\) be the number of shares bought of stock \(i\).
    \item \(\text{buyPrice}_i\) be the price at which stock \(i\) was bought.
    \item \(\text{currentPrice}_i\) be the current price of stock \(i\).
    \item \(\text{futurePrice}_i\) be the expected price of stock \(i\) in one year.
    \item \(\text{transactionRate}\) be the transaction cost rate (as a percentage).
    \item \(\text{taxRate}\) be the tax rate on capital gains (as a percentage).
    \item \(K\) be the amount of money the investor wants to raise net of costs.
\end{itemize}

We introduce the variables:
\begin{itemize}
    \item \(\text{sell}_i\) is the number of shares of stock \(i\) to sell.
\end{itemize}

The goal is to choose \(\text{sell}_i\) to maximize the expected value of the portfolio at the end of the year, which is given by:
\[ 
\text{max} \sum_{i=1}^{N} \left( \text{bought}_i - \text{sell}_i \right) \cdot \text{futurePrice}_i 
\]

Subject to the following constraints:
\begin{align*}
    &\sum_{i=1}^{N} \bigg[ \text{sell}_i \cdot \text{currentPrice}_i - \left( \frac{\text{taxRate}}{100} \cdot \max(0, \left( \text{sell}_i \cdot \text{currentPrice}_i - \text{sell}_i \cdot \text{buyPrice}_i \right)) \right) \\
    &\quad - \left( \frac{\text{transactionRate}}{100} \cdot \text{sell}_i \cdot \text{currentPrice}_i \right) \bigg] \geq K, \\
    &0 \leq \text{sell}_i \leq \text{bought}_i, \quad \forall i = 1, \ldots, N.
\end{align*}

Where:
- The first constraint ensures that the net amount raised after taxes and transaction costs is at least \(K\).
- The second set of constraints ensures that the investor can't sell more shares than they own.

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

\section*{Problem Description}

The investor wants to decide how many shares of stock \(i\) to sell (\( \text{sell}_i \)) in order to raise a specified net amount of money \(K\), net of capital gains taxes and transaction costs. The goal is to maximize the expected value of the portfolio at the end of the year.

\section*{Mathematical Model}

Let:
\begin{itemize}
    \item \(N\) be the number of different stocks.
    \item \(\text{bought}_i\) be the number of shares bought of stock \(i\).
    \item \(\text{buyPrice}_i\) be the price at which stock \(i\) was bought.
    \item \(\text{currentPrice}_i\) be the current price of stock \(i\).
    \item \(\text{futurePrice}_i\) be the expected price of stock \(i\) in one year.
    \item \(\text{transactionRate}\) be the transaction cost rate (as a percentage).
    \item \(\text{taxRate}\) be the tax rate on capital gains (as a percentage).
    \item \(K\) be the amount of money the investor wants to raise net of costs.
\end{itemize}

We introduce the variables:
\begin{itemize}
    \item \(\text{sell}_i\) is the number of shares of stock \(i\) to sell.
\end{itemize}

The goal is to choose \(\text{sell}_i\) to maximize the expected value of the portfolio at the end of the year, which is given by:
\[ 
\text{max} \sum_{i=1}^{N} \left( \text{bought}_i - \text{sell}_i \right) \cdot \text{futurePrice}_i 
\]

Subject to the following constraints:
\begin{align*}
    &\sum_{i=1}^{N} \bigg[ \text{sell}_i \cdot \text{currentPrice}_i - \left( \frac{\text{taxRate}}{100} \cdot \max(0, \left( \text{sell}_i \cdot \text{currentPrice}_i - \text{sell}_i \cdot \text{buyPrice}_i \right)) \right) \\
    &\quad - \left( \frac{\text{transactionRate}}{100} \cdot \text{sell}_i \cdot \text{currentPrice}_i \right) \bigg] \geq K, \\
    &0 \leq \text{sell}_i \leq \text{bought}_i, \quad \forall i = 1, \ldots, N.
\end{align*}

Where:
- The first constraint ensures that the net amount raised after taxes and transaction costs is at least \(K\).
- The second set of constraints ensures that the investor can't sell more shares than they own.

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

#### Decision variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0)

#### Objective function
problem += pulp.lpSum(
    (data['Bought'][i] - sell[i]) * data['FuturePrice'][i] for i in range(data['N'])
), "Total Portfolio Value"

#### Constraints
problem += (
    pulp.lpSum(
        sell[i] * data['CurrentPrice'][i] - 
        (data['TaxRate'] / 100) * pulp.lpSum(
            pulp.lpMax(0, (sell[i] * data['CurrentPrice'][i] - sell[i] * data['BuyPrice'][i])) for i in range(data['N'])
        ) - 
        (data['TransactionRate'] / 100) * sell[i] * data['CurrentPrice'][i]
        for i in range(data['N'])) 
    ) >= data['K'], "NetAmountRaised"
)

for i in range(data['N']):
    problem += (sell[i] <= data['Bought'][i], f"MaxSell_{i}")

#### Solve the problem
problem.solve()

#### Output the objective value
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

#### Data from the provided JSON format
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
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

#### Decision variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0)

#### Objective function
problem += pulp.lpSum(
    (data['Bought'][i] - sell[i]) * data['FuturePrice'][i] for i in range(data['N'])
), "Total Portfolio Value"

#### Constraints
problem += (
    pulp.lpSum(
        sell[i] * data['CurrentPrice'][i] - 
        (data['TaxRate'] / 100) * pulp.lpSum(
            pulp.lpMax(0, (sell[i] * data['CurrentPrice'][i] - sell[i] * data['BuyPrice'][i])) for i in range(data['N'])
        ) - 
        (data['TransactionRate'] / 100) * sell[i] * data['CurrentPrice'][i]
        for i in range(data['N'])) 
    ) >= data['K'], "NetAmountRaised"
)

for i in range(data['N']):
    problem += (sell[i] <= data['Bought'][i], f"MaxSell_{i}")

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b2/10/17/python_code0.py", line 36
    )
    ^
SyntaxError: unmatched ')'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

#### Decision variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0)

#### Objective function
problem += pulp.lpSum(
    (data['Bought'][i] - sell[i]) * data['FuturePrice'][i] for i in range(data['N'])
), "Total Portfolio Value"

#### Constraints
problem += (
    pulp.lpSum(
        sell[i] * data['CurrentPrice'][i] - 
        (data['TaxRate'] / 100) * pulp.lpSum(
            pulp.lpMax(0, (sell[i] * data['CurrentPrice'][i] - sell[i] * data['BuyPrice'][i])) for i in range(data['N'])
        ) - 
        (data['TransactionRate'] / 100) * sell[i] * data['CurrentPrice'][i]
    for i in range(data['N'])) 
    ) >= data['K'], "NetAmountRaised"
)

for i in range(data['N']):
    problem += (sell[i] <= data['Bought'][i], f"MaxSell_{i}")

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

