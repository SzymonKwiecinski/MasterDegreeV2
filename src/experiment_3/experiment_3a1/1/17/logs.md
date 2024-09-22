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
    \item Let $x_i$ be the number of shares of stock $i$ that the investor sells, for $i = 1, 2, \ldots, N$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $bought_i$: Number of shares bought of stock $i$.
    \item $buyPrice_i$: Purchase price of stock $i$.
    \item $currentPrice_i$: Current price of stock $i$.
    \item $futurePrice_i$: Expected future price of stock $i$.
    \item $transactionRate$: Transaction cost rate (in percentage).
    \item $taxRate$: Tax rate on capital gains (in percentage).
    \item $K$: Amount of money the investor wants to raise net of capital gains and transaction costs.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } \sum_{i=1}^N (futurePrice_i \cdot bought_i - buyPrice_i \cdot bought_i) - \sum_{i=1}^N (transactionRate \cdot (\text{currentPrice_i} \cdot x_i)) - \sum_{i=1}^N \left( \frac{taxRate}{100} \cdot (currentPrice_i \cdot x_i - buyPrice_i \cdot x_i) \right)
\]

\textbf{Subject to:}
\begin{itemize}
    \item Total amount raised net of costs:
    \[
    \sum_{i=1}^N \left( currentPrice_i \cdot x_i \cdot (1 - \frac{transactionRate}{100}) - \frac{taxRate}{100} \cdot (currentPrice_i \cdot x_i - buyPrice_i \cdot x_i) \right) \geq K
    \]
    \item Non-negativity constraints:
    \[
    x_i \geq 0, \quad \forall i = 1, 2, \ldots, N
    \]
    \item The number of shares sold cannot exceed the number of shares bought:
    \[
    x_i \leq bought_i, \quad \forall i = 1, 2, \ldots, N
    \]
\end{itemize}

\textbf{Output:}
The solution will provide the number of shares to sell for each stock $i$ in the format:
\[
\{ "sell": [x_1, x_2, \ldots, x_N] \}
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
    \item Let $x_i$ be the number of shares of stock $i$ that the investor sells, for $i = 1, 2, \ldots, N$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $bought_i$: Number of shares bought of stock $i$.
    \item $buyPrice_i$: Purchase price of stock $i$.
    \item $currentPrice_i$: Current price of stock $i$.
    \item $futurePrice_i$: Expected future price of stock $i$.
    \item $transactionRate$: Transaction cost rate (in percentage).
    \item $taxRate$: Tax rate on capital gains (in percentage).
    \item $K$: Amount of money the investor wants to raise net of capital gains and transaction costs.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } \sum_{i=1}^N (futurePrice_i \cdot bought_i - buyPrice_i \cdot bought_i) - \sum_{i=1}^N (transactionRate \cdot (\text{currentPrice_i} \cdot x_i)) - \sum_{i=1}^N \left( \frac{taxRate}{100} \cdot (currentPrice_i \cdot x_i - buyPrice_i \cdot x_i) \right)
\]

\textbf{Subject to:}
\begin{itemize}
    \item Total amount raised net of costs:
    \[
    \sum_{i=1}^N \left( currentPrice_i \cdot x_i \cdot (1 - \frac{transactionRate}{100}) - \frac{taxRate}{100} \cdot (currentPrice_i \cdot x_i - buyPrice_i \cdot x_i) \right) \geq K
    \]
    \item Non-negativity constraints:
    \[
    x_i \geq 0, \quad \forall i = 1, 2, \ldots, N
    \]
    \item The number of shares sold cannot exceed the number of shares bought:
    \[
    x_i \leq bought_i, \quad \forall i = 1, 2, \ldots, N
    \]
\end{itemize}

\textbf{Output:}
The solution will provide the number of shares to sell for each stock $i$ in the format:
\[
\{ "sell": [x_1, x_2, \ldots, x_N] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

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

#### Variables
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

#### Problem definition
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)

#### Objective function
profit = pulp.lpSum((futurePrice[i] * bought[i] - buyPrice[i] * bought[i]) for i in range(N))
transaction_costs = pulp.lpSum(transactionRate * (currentPrice[i] * x[i]) for i in range(N))
taxes = pulp.lpSum(taxRate * (currentPrice[i] * x[i] - buyPrice[i] * x[i]) for i in range(N))

problem += profit - transaction_costs - taxes

#### Constraints
#### Total amount raised net of costs
total_net_sales = pulp.lpSum(
    (currentPrice[i] * x[i] * (1 - transactionRate) - taxRate * (currentPrice[i] * x[i] - buyPrice[i] * x[i]))
    for i in range(N)
)
problem += total_net_sales >= K

#### Non-negativity constraints and limit on shares sold
for i in range(N):
    problem += x[i] <= bought[i]

#### Solve the problem
problem.solve()

#### Output the result
sell = [x[i].varValue for i in range(N)]
print(json.dumps({"sell": sell}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

