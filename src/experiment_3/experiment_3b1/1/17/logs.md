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

\section*{Linear Programming Model for Stock Selling Problem}

\subsection*{Indices}
Let \( i \) denote the index for stocks where \( i = 1, 2, \ldots, N \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{bought}_i \): Number of shares bought of stock \( i \)
    \item \( \text{buyPrice}_i \): Purchase price of stock \( i \)
    \item \( \text{currentPrice}_i \): Current price of stock \( i \)
    \item \( \text{futurePrice}_i \): Expected future price of stock \( i \)
    \item \( \text{transactionRate} \): Transaction cost percentage (as a fraction)
    \item \( \text{taxRate} \): Tax percentage on capital gains (as a fraction)
    \item \( K \): Net amount of money the investor wants to raise
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{sell}_i \) represent the number of shares of stock \( i \) that the investor sells.

\subsection*{Objective Function}
We aim to maximize the expected value of the portfolio next year, considering the future price of the stocks, which can be expressed as:

\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( \text{futurePrice}_i \cdot \left( \text{bought}_i - \text{sell}_i \right) \right)
\]

\subsection*{Constraints}
1. The amount raised from selling stocks must cover the desired amount \( K \) net of transaction costs and taxes:

\[
\sum_{i=1}^{N} \left( \text{currentPrice}_i \cdot \text{sell}_i \cdot (1 - \text{transactionRate}) - \text{taxRate} \cdot \left( \text{currentPrice}_i \cdot \text{sell}_i - \text{buyPrice}_i \cdot \text{sell}_i \right) \right) \geq K
\]

2. The number of shares sold must not exceed the number of shares bought:

\[
\text{sell}_i \leq \text{bought}_i \quad \forall i
\]

3. Non-negativity constraints:

\[
\text{sell}_i \geq 0 \quad \forall i
\]

\subsection*{Output}
The output will be the optimal number of shares to sell for each stock \( i \):

\[
\text{Output: } \{\text{sell} = [\text{sell}_1, \text{sell}_2, \ldots, \text{sell}_N]\}
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

\section*{Linear Programming Model for Stock Selling Problem}

\subsection*{Indices}
Let \( i \) denote the index for stocks where \( i = 1, 2, \ldots, N \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{bought}_i \): Number of shares bought of stock \( i \)
    \item \( \text{buyPrice}_i \): Purchase price of stock \( i \)
    \item \( \text{currentPrice}_i \): Current price of stock \( i \)
    \item \( \text{futurePrice}_i \): Expected future price of stock \( i \)
    \item \( \text{transactionRate} \): Transaction cost percentage (as a fraction)
    \item \( \text{taxRate} \): Tax percentage on capital gains (as a fraction)
    \item \( K \): Net amount of money the investor wants to raise
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{sell}_i \) represent the number of shares of stock \( i \) that the investor sells.

\subsection*{Objective Function}
We aim to maximize the expected value of the portfolio next year, considering the future price of the stocks, which can be expressed as:

\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( \text{futurePrice}_i \cdot \left( \text{bought}_i - \text{sell}_i \right) \right)
\]

\subsection*{Constraints}
1. The amount raised from selling stocks must cover the desired amount \( K \) net of transaction costs and taxes:

\[
\sum_{i=1}^{N} \left( \text{currentPrice}_i \cdot \text{sell}_i \cdot (1 - \text{transactionRate}) - \text{taxRate} \cdot \left( \text{currentPrice}_i \cdot \text{sell}_i - \text{buyPrice}_i \cdot \text{sell}_i \right) \right) \geq K
\]

2. The number of shares sold must not exceed the number of shares bought:

\[
\text{sell}_i \leq \text{bought}_i \quad \forall i
\]

3. Non-negativity constraints:

\[
\text{sell}_i \geq 0 \quad \forall i
\]

\subsection*{Output}
The output will be the optimal number of shares to sell for each stock \( i \):

\[
\text{Output: } \{\text{sell} = [\text{sell}_1, \text{sell}_2, \ldots, \text{sell}_N]\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}')

#### Extracting data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100  #### Convert percentage to fraction
taxRate = data['TaxRate'] / 100  #### Convert percentage to fraction
K = data['K']

#### Create a linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

#### Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

#### Objective function
problem += pulp.lpSum(futurePrice[i] * (bought[i] - sell[i]) for i in range(N)), "Objective"

#### Constraints
#### Constraint 1: The amount raised from selling stocks must cover the desired amount K
problem += (
    pulp.lpSum(currentPrice[i] * sell[i] * (1 - transactionRate) - 
                taxRate * (currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) for i in range(N)) >= K,
    "AmountRaisedConstraint"
)

#### Constraint 2: The number of shares sold must not exceed the number of shares bought
for i in range(N):
    problem += sell[i] <= bought[i], f"MaxSellConstraint_{i}"

#### Solve the problem
problem.solve()

#### Output results
sell_values = [sell[i].varValue for i in range(N)]
print(f'Output: {{"sell": {sell_values}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

