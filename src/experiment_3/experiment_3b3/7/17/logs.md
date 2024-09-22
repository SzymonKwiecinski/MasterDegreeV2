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

\textbf{Variables:}
\begin{itemize}
    \item Let \( s_i \) be the number of shares of stock \( i \) to sell, where \( i = 1, \ldots, N \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{bought}_i \): number of shares bought of stock \( i \)
    \item \( \text{buyPrice}_i \): price at which shares of stock \( i \) were bought
    \item \( \text{currentPrice}_i \): current price of shares of stock \( i \)
    \item \( \text{futurePrice}_i \): expected future price of shares of stock \( i \)
    \item \( \text{transactionRate} \): transaction cost percentage 
    \item \( \text{taxRate} \): tax rate on capital gains percentage
    \item \( K \): net amount of money needed 
\end{itemize}

\textbf{Objective Function:}
Maximize the expected value of the portfolio next year after selling shares:
\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( \left( \text{futurePrice}_i - \text{buyPrice}_i \right) \cdot \text{bought}_i - \left( \text{transactionRate} / 100 \cdot \left( \text{currentPrice}_i \cdot s_i \right) + \text{taxRate} / 100 \cdot \left( \text{currentPrice}_i \cdot s_i - \text{buyPrice}_i \cdot s_i \right) \right) \right)
\]

\textbf{Constraints:}
1. The amount raised after transaction costs and taxes must be at least \( K \):
\[
\sum_{i=1}^{N} \left( \text{currentPrice}_i \cdot s_i - \left( \text{transactionRate} / 100 \cdot \left( \text{currentPrice}_i \cdot s_i \right) + \text{taxRate} / 100 \cdot \left( \text{currentPrice}_i \cdot s_i - \text{buyPrice}_i \cdot s_i \right) \right) \right) \geq K
\]

2. The number of shares sold should not exceed the number of shares bought:
\[
s_i \leq \text{bought}_i \quad \forall i
\]

3. Non-negativity constraints:
\[
s_i \geq 0 \quad \forall i
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

\textbf{Variables:}
\begin{itemize}
    \item Let \( s_i \) be the number of shares of stock \( i \) to sell, where \( i = 1, \ldots, N \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{bought}_i \): number of shares bought of stock \( i \)
    \item \( \text{buyPrice}_i \): price at which shares of stock \( i \) were bought
    \item \( \text{currentPrice}_i \): current price of shares of stock \( i \)
    \item \( \text{futurePrice}_i \): expected future price of shares of stock \( i \)
    \item \( \text{transactionRate} \): transaction cost percentage 
    \item \( \text{taxRate} \): tax rate on capital gains percentage
    \item \( K \): net amount of money needed 
\end{itemize}

\textbf{Objective Function:}
Maximize the expected value of the portfolio next year after selling shares:
\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( \left( \text{futurePrice}_i - \text{buyPrice}_i \right) \cdot \text{bought}_i - \left( \text{transactionRate} / 100 \cdot \left( \text{currentPrice}_i \cdot s_i \right) + \text{taxRate} / 100 \cdot \left( \text{currentPrice}_i \cdot s_i - \text{buyPrice}_i \cdot s_i \right) \right) \right)
\]

\textbf{Constraints:}
1. The amount raised after transaction costs and taxes must be at least \( K \):
\[
\sum_{i=1}^{N} \left( \text{currentPrice}_i \cdot s_i - \left( \text{transactionRate} / 100 \cdot \left( \text{currentPrice}_i \cdot s_i \right) + \text{taxRate} / 100 \cdot \left( \text{currentPrice}_i \cdot s_i - \text{buyPrice}_i \cdot s_i \right) \right) \right) \geq K
\]

2. The number of shares sold should not exceed the number of shares bought:
\[
s_i \leq \text{bought}_i \quad \forall i
\]

3. Non-negativity constraints:
\[
s_i \geq 0 \quad \forall i
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extracting data from the JSON format
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

N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

#### Define the problem
problem = pulp.LpProblem("Stock_Selling", pulp.LpMaximize)

#### Define the decision variables
s = [pulp.LpVariable(f's_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

#### Define the objective function
objective = pulp.lpSum(
    (futurePrice[i] - buyPrice[i]) * bought[i] - 
    (transactionRate / 100 * currentPrice[i] * s[i] + 
     taxRate / 100 * (currentPrice[i] * s[i] - buyPrice[i] * s[i])) 
    for i in range(N)
)
problem += objective

#### Define the constraints
#### Constraint 1: Amount raised must be at least K
problem += pulp.lpSum(
    (currentPrice[i] * s[i] - (
        transactionRate / 100 * currentPrice[i] * s[i] +
        taxRate / 100 * (currentPrice[i] * s[i] - buyPrice[i] * s[i])
    )) for i in range(N)
) >= K

#### Constraint 2 and 3: Each s_i must be non-negative and can not exceed bought_i (handled by LpVariable definition)

#### Solve the problem
problem.solve()

#### Print the results
print("Status:", pulp.LpStatus[problem.status])
for i in range(N):
    print(f's_{i} (Shares to sell for stock {i+1}): {s[i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

