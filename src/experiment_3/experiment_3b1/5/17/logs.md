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

\section*{Linear Programming Model for Stock Selling}

\subsection*{Parameters}
\begin{align*}
N & : \text{Number of different stocks} \\
bought_i & : \text{Number of shares bought of stock } i \\
buyPrice_i & : \text{Price at which the shares of stock } i \text{ were bought} \\
currentPrice_i & : \text{Current price of one share of stock } i \\
futurePrice_i & : \text{Expected price of one share of stock } i \text{ in one year} \\
transactionRate & : \text{Transaction cost rate (\%)} \\
taxRate & : \text{Tax rate on capital gains (\%)} \\
K & : \text{Target amount of money to raise net of capital gains and transaction costs}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
sell_i & : \text{Number of shares to sell of stock } i 
\end{align*}

\subsection*{Objective Function}
Maximize the expected value of the portfolio next year, which can be formulated as:
\begin{align}
\text{Maximize } Z = \sum_{i=1}^{N} (futurePrice_i - currentPrice_i) \cdot (bought_i - sell_i)
\end{align}

\subsection*{Constraints}
1. The amount raised from selling shares, net of transaction costs and taxes, must meet or exceed the target amount \( K \):
\begin{align}
\sum_{i=1}^{N} \left( (currentPrice_i \cdot sell_i) - \left( transactionRate \cdot \frac{currentPrice_i \cdot sell_i}{100} \right) - \left( taxRate \cdot \frac{(currentPrice_i - buyPrice_i) \cdot sell_i}{100} \right) \right) \geq K
\end{align}

2. The number of shares sold cannot exceed the number of shares bought:
\begin{align}
sell_i \leq bought_i \quad \forall i = 1, ..., N
\end{align}

3. Non-negativity constraints:
\begin{align}
sell_i \geq 0 \quad \forall i = 1, ..., N
\end{align}

\subsection*{Output}
The output will consist of the number of shares to sell for each stock:
\begin{align*}
\text{Output} &: \{ sell : [sell_1, sell_2, ..., sell_N] \}
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

\section*{Linear Programming Model for Stock Selling}

\subsection*{Parameters}
\begin{align*}
N & : \text{Number of different stocks} \\
bought_i & : \text{Number of shares bought of stock } i \\
buyPrice_i & : \text{Price at which the shares of stock } i \text{ were bought} \\
currentPrice_i & : \text{Current price of one share of stock } i \\
futurePrice_i & : \text{Expected price of one share of stock } i \text{ in one year} \\
transactionRate & : \text{Transaction cost rate (\%)} \\
taxRate & : \text{Tax rate on capital gains (\%)} \\
K & : \text{Target amount of money to raise net of capital gains and transaction costs}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
sell_i & : \text{Number of shares to sell of stock } i 
\end{align*}

\subsection*{Objective Function}
Maximize the expected value of the portfolio next year, which can be formulated as:
\begin{align}
\text{Maximize } Z = \sum_{i=1}^{N} (futurePrice_i - currentPrice_i) \cdot (bought_i - sell_i)
\end{align}

\subsection*{Constraints}
1. The amount raised from selling shares, net of transaction costs and taxes, must meet or exceed the target amount \( K \):
\begin{align}
\sum_{i=1}^{N} \left( (currentPrice_i \cdot sell_i) - \left( transactionRate \cdot \frac{currentPrice_i \cdot sell_i}{100} \right) - \left( taxRate \cdot \frac{(currentPrice_i - buyPrice_i) \cdot sell_i}{100} \right) \right) \geq K
\end{align}

2. The number of shares sold cannot exceed the number of shares bought:
\begin{align}
sell_i \leq bought_i \quad \forall i = 1, ..., N
\end{align}

3. Non-negativity constraints:
\begin{align}
sell_i \geq 0 \quad \forall i = 1, ..., N
\end{align}

\subsection*{Output}
The output will consist of the number of shares to sell for each stock:
\begin{align*}
\text{Output} &: \{ sell : [sell_1, sell_2, ..., sell_N] \}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data_json = '''{
    "N": 3,
    "Bought": [100, 150, 80],
    "BuyPrice": [50, 40, 30],
    "CurrentPrice": [60, 35, 32],
    "FuturePrice": [65, 44, 34],
    "TransactionRate": 1.0,
    "TaxRate": 15.0,
    "K": 5000
}'''

data = json.loads(data_json)

#### Extracting data from JSON
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

#### Create the linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)

#### Objective Function
problem += pulp.lpSum((FuturePrice[i] - CurrentPrice[i]) * (Bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

#### Constraints
#### Constraint for raising enough money
problem += (pulp.lpSum((CurrentPrice[i] * sell[i])
                      - (TransactionRate * (CurrentPrice[i] * sell[i] / 100))
                      - (TaxRate * ((CurrentPrice[i] - BuyPrice[i]) * sell[i] / 100)) for i in range(N)) >= K), "Capital_Requirement"

#### Constraints to ensure sell does not exceed bought
for i in range(N):
    problem += (sell[i] <= Bought[i]), f"Max_Sell_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Output the results
sell_values = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_values}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

