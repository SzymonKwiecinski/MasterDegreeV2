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

\subsection*{Parameters}
\begin{align*}
N & : \text{Number of different stocks} \\
bought_i & : \text{Number of shares bought of stock } i \\
buyPrice_i & : \text{Price per share bought of stock } i \\
currentPrice_i & : \text{Current price per share of stock } i \\
futurePrice_i & : \text{Expected future price per share of stock } i \\
transactionRate & : \text{Transaction cost rate (percentage)} \\
taxRate & : \text{Tax rate on capital gains (percentage)} \\
K & : \text{Desired net amount to raise}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
sell_i & : \text{Number of shares of stock } i \text{ to sell}
\end{align*}

\subsection*{Objective Function}
We need to maximize the expected value of the portfolio next year, given by:

\begin{align*}
\text{Maximize } & \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i)) - \sum_{i=1}^{N} (currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (sell_i \cdot (currentPrice_i - buyPrice_i) \cdot \frac{taxRate}{100}))
\end{align*}

\subsection*{Constraints}
To ensure that the investor raises at least the desired amount \( K \), we have the following constraint:

\begin{align*}
\sum_{i=1}^{N} (currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (sell_i \cdot (currentPrice_i - buyPrice_i) \cdot \frac{taxRate}{100})) & \geq K
\end{align*}

Additionally, the number of shares sold must not exceed the number of shares bought:

\begin{align*}
sell_i & \leq bought_i, \quad \text{for } i = 1, \ldots, N
\end{align*}

And the number of shares sold must be non-negative:

\begin{align*}
sell_i & \geq 0, \quad \text{for } i = 1, \ldots, N
\end{align*}

\subsection*{Output Format}
The output will consist of the number of shares to sell for each stock:

\begin{align*}
\text{Output: } & \{ "sell": [sell_1, sell_2, \ldots, sell_N] \}
\end{align*}

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

\subsection*{Parameters}
\begin{align*}
N & : \text{Number of different stocks} \\
bought_i & : \text{Number of shares bought of stock } i \\
buyPrice_i & : \text{Price per share bought of stock } i \\
currentPrice_i & : \text{Current price per share of stock } i \\
futurePrice_i & : \text{Expected future price per share of stock } i \\
transactionRate & : \text{Transaction cost rate (percentage)} \\
taxRate & : \text{Tax rate on capital gains (percentage)} \\
K & : \text{Desired net amount to raise}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
sell_i & : \text{Number of shares of stock } i \text{ to sell}
\end{align*}

\subsection*{Objective Function}
We need to maximize the expected value of the portfolio next year, given by:

\begin{align*}
\text{Maximize } & \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i)) - \sum_{i=1}^{N} (currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (sell_i \cdot (currentPrice_i - buyPrice_i) \cdot \frac{taxRate}{100}))
\end{align*}

\subsection*{Constraints}
To ensure that the investor raises at least the desired amount \( K \), we have the following constraint:

\begin{align*}
\sum_{i=1}^{N} (currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (sell_i \cdot (currentPrice_i - buyPrice_i) \cdot \frac{taxRate}{100})) & \geq K
\end{align*}

Additionally, the number of shares sold must not exceed the number of shares bought:

\begin{align*}
sell_i & \leq bought_i, \quad \text{for } i = 1, \ldots, N
\end{align*}

And the number of shares sold must be non-negative:

\begin{align*}
sell_i & \geq 0, \quad \text{for } i = 1, \ldots, N
\end{align*}

\subsection*{Output Format}
The output will consist of the number of shares to sell for each stock:

\begin{align*}
\text{Output: } & \{ "sell": [sell_1, sell_2, \ldots, sell_N] \}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data_json = '{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}'
data = json.loads(data_json)

#### Parameters
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

#### Create the linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

#### Decision variables: number of shares to sell
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum((futurePrice[i] * (bought[i] - sell[i]) for i in range(N))) - \
    pulp.lpSum((currentPrice[i] * sell[i] * (1 - transactionRate / 100) - \
    (sell[i] * (currentPrice[i] - buyPrice[i]) * taxRate / 100) for i in range(N)))

#### Constraints
problem += pulp.lpSum((currentPrice[i] * sell[i] * (1 - transactionRate / 100) - \
    (sell[i] * (currentPrice[i] - buyPrice[i]) * taxRate / 100) for i in range(N))) >= K

for i in range(N):
    problem += sell[i] <= bought[i]

#### Solve the problem
problem.solve()

#### Output results
sell_values = [sell[i].varValue for i in range(N)]
output = {"sell": sell_values}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(output)
```

