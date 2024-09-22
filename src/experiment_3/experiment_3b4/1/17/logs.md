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
To address the given problem, we need to set up a linear programming model. Our objective is to determine how many shares of each stock the investor should sell in order to raise the required amount \( K \) net of transaction costs and taxes. Additionally, the investor wants to maximize the expected value of the portfolio in the following year.

Here's the mathematical model for the problem:

######### Decision Variables:
- Let \( \text{sell}_i \) denote the number of shares of stock \( i \) to sell.

######### Parameters:
- \( \text{bought}_i \): Number of shares of stock \( i \) bought.
- \( \text{buyPrice}_i \): Purchase price per share of stock \( i \).
- \( \text{currentPrice}_i \): Current price per share of stock \( i \).
- \( \text{futurePrice}_i \): Expected future price per share of stock \( i \).
- \( \text{transactionRate} \): Transaction cost rate (as a percentage).
- \( \text{taxRate} \): Tax rate on capital gains (as a percentage).
- \( K \): Amount of money to be raised.

######### Objective Function:
Maximize the expected value of the portfolio in one year:
\[
\max \sum_{i=1}^{N} \left(\text{bought}_i - \text{sell}_i\right) \times \text{futurePrice}_i
\]

######### Constraints:
1. **Net Amount Raised Constraint:**
   \[
   \sum_{i=1}^{N} \left(\text{sell}_i \times \text{currentPrice}_i \times \left(1 - \frac{\text{transactionRate}}{100}\right) - \max(0, \text{sell}_i \times (\text{currentPrice}_i - \text{buyPrice}_i)) \times \frac{\text{taxRate}}{100}\right) \geq K
   \]
   
2. **Stock Limit Constraint:**
   \[
   0 \leq \text{sell}_i \leq \text{bought}_i \quad \text{for all } i
   \]

Now, let's write this model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{itemize}
    \item $\text{sell}_i$: Number of shares of stock $i$ to sell.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{bought}_i$: Number of shares of stock $i$ bought.
    \item $\text{buyPrice}_i$: Purchase price per share of stock $i$.
    \item $\text{currentPrice}_i$: Current price per share of stock $i$.
    \item $\text{futurePrice}_i$: Expected future price per share of stock $i$.
    \item $\text{transactionRate}$: Transaction cost rate (percentage).
    \item $\text{taxRate}$: Tax rate on capital gains (percentage).
    \item $K$: Amount of money to be raised.
\end{itemize}

\subsection*{Objective Function}
\begin{equation}
    \max \sum_{i=1}^{N} \left(\text{bought}_i - \text{sell}_i\right) \times \text{futurePrice}_i
\end{equation}

\subsection*{Constraints}
\begin{align}
    &\sum_{i=1}^{N} \left(\text{sell}_i \times \text{currentPrice}_i \times \left(1 - \frac{\text{transactionRate}}{100}\right) - \max(0, \text{sell}_i \times (\text{currentPrice}_i - \text{buyPrice}_i)) \times \frac{\text{taxRate}}{100}\right) \geq K \\
    &0 \leq \text{sell}_i \leq \text{bought}_i \quad \text{for all } i
\end{align}

\end{document}
```

This LaTeX code describes the linear programming formulation for the problem, where we maximize the expected portfolio value subject to constraints related to raising the required money and limited share sales.

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

\subsection*{Decision Variables}
\begin{itemize}
    \item $\text{sell}_i$: Number of shares of stock $i$ to sell.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{bought}_i$: Number of shares of stock $i$ bought.
    \item $\text{buyPrice}_i$: Purchase price per share of stock $i$.
    \item $\text{currentPrice}_i$: Current price per share of stock $i$.
    \item $\text{futurePrice}_i$: Expected future price per share of stock $i$.
    \item $\text{transactionRate}$: Transaction cost rate (percentage).
    \item $\text{taxRate}$: Tax rate on capital gains (percentage).
    \item $K$: Amount of money to be raised.
\end{itemize}

\subsection*{Objective Function}
\begin{equation}
    \max \sum_{i=1}^{N} \left(\text{bought}_i - \text{sell}_i\right) \times \text{futurePrice}_i
\end{equation}

\subsection*{Constraints}
\begin{align}
    &\sum_{i=1}^{N} \left(\text{sell}_i \times \text{currentPrice}_i \times \left(1 - \frac{\text{transactionRate}}{100}\right) - \max(0, \text{sell}_i \times (\text{currentPrice}_i - \text{buyPrice}_i)) \times \frac{\text{taxRate}}{100}\right) \geq K \\
    &0 \leq \text{sell}_i \leq \text{bought}_i \quad \text{for all } i
\end{align}

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

#### Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

#### Initialize the problem
problem = pulp.LpProblem("MaximizeFutureValue", pulp.LpMaximize)

#### Decision variables
sell_vars = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i]) for i in range(N)]

#### Objective function
problem += pulp.lpSum((Bought[i] - sell_vars[i]) * FuturePrice[i] for i in range(N))

#### Constraint: amount of money to be raised
problem += (
    pulp.lpSum(
        sell_vars[i] * CurrentPrice[i] * (1 - TransactionRate / 100) -
        max(0, sell_vars[i] * (CurrentPrice[i] - BuyPrice[i])) * TaxRate / 100
        for i in range(N)
    ) >= K
)

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

#### Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

#### Initialize the problem
problem = pulp.LpProblem("MaximizeFutureValue", pulp.LpMaximize)

#### Decision variables
sell_vars = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i]) for i in range(N)]

#### Objective function
problem += pulp.lpSum((Bought[i] - sell_vars[i]) * FuturePrice[i] for i in range(N))

#### Constraint: amount of money to be raised
problem += (
    pulp.lpSum(
        sell_vars[i] * CurrentPrice[i] * (1 - TransactionRate / 100) -
        max(0, sell_vars[i] * (CurrentPrice[i] - BuyPrice[i])) * TaxRate / 100
        for i in range(N)
    ) >= K
)

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b4/1/17/python_code0.py", line 36, in <module>
    pulp.lpSum(
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 2233, in lpSum
    return LpAffineExpression().addInPlace(vector)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 867, in addInPlace
    for e in other:
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b4/1/17/python_code0.py", line 38, in <genexpr>
    max(0, sell_vars[i] * (CurrentPrice[i] - BuyPrice[i])) * TaxRate / 100
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: '>' not supported between instances of 'LpAffineExpression' and 'int'
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

#### Parameters
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

#### Initialize the problem
problem = pulp.LpProblem("MaximizeFutureValue", pulp.LpMaximize)

#### Decision variables
sell_vars = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=Bought[i]) for i in range(N)]

#### Objective function
problem += pulp.lpSum((Bought[i] - sell_vars[i]) * FuturePrice[i] for i in range(N))

#### Constraint: amount of money to be raised
problem += (
    pulp.lpSum(
        sell_vars[i] * CurrentPrice[i] * (1 - TransactionRate / 100) -
        (pulp.lpSum([sell_vars[i] * (CurrentPrice[i] - BuyPrice[i])]) * TaxRate / 100)
        ) for i in range(N)
    ) >= K
)

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```

