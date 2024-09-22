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

\subsection*{Variables}
Let:
\begin{itemize}
    \item $N$: Number of different stocks
    \item $bought_i$: Number of shares bought of stock $i$
    \item $buyPrice_i$: Price at which stock $i$ was bought
    \item $currentPrice_i$: Current price of stock $i$
    \item $futurePrice_i$: Expected price of stock $i$ in one year
    \item $transactionRate$: Transaction cost rate (in percentage)
    \item $taxRate$: Tax rate on capital gains (in percentage)
    \item $K$: Target net amount to raise
    \item $sell_i$: Number of shares to sell of stock $i$
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the expected value of the portfolio next year, while ensuring that the net amount raised is at least $K$:

\[
\text{maximize} \quad \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i)) - \sum_{i=1}^{N} (sell_i \cdot currentPrice_i)
\]

\subsection*{Constraints}
The constraints include the need to raise a net amount of at least $K$ after transaction costs and taxes:

The amount raised from selling shares $i$ is given by:

\[
\text{Amount\_Raised}_i = sell_i \cdot currentPrice_i
\]

The capital gains from selling shares is given by:

\[
\text{Capital\_Gains}_i = (currentPrice_i - buyPrice_i) \cdot sell_i
\]

The transaction cost for selling shares is:

\[
\text{Transaction\_Cost}_i = transactionRate \cdot \text{Amount\_Raised}_i
\]

The net amount raised after considering transaction costs and taxes on capital gains can be expressed as:

\[
\text{Net\_Amount} = \sum_{i=1}^{N} \left( \text{Amount\_Raised}_i - \text{Transaction\_Cost}_i - (taxRate \cdot \text{Capital\_Gains}_i) \right)
\]

Thus, the constraint can be formulated as:

\[
\sum_{i=1}^{N} \left( sell_i \cdot currentPrice_i - transactionRate \cdot (sell_i \cdot currentPrice_i) - taxRate \cdot ((currentPrice_i - buyPrice_i) \cdot sell_i) \right) \geq K
\]

\subsection*{Non-negativity Constraints}
Additionally, we impose that the number of shares to sell cannot be negative:

\[
sell_i \geq 0 \quad \text{for all } i \in \{1, 2, \ldots, N\}
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

\subsection*{Variables}
Let:
\begin{itemize}
    \item $N$: Number of different stocks
    \item $bought_i$: Number of shares bought of stock $i$
    \item $buyPrice_i$: Price at which stock $i$ was bought
    \item $currentPrice_i$: Current price of stock $i$
    \item $futurePrice_i$: Expected price of stock $i$ in one year
    \item $transactionRate$: Transaction cost rate (in percentage)
    \item $taxRate$: Tax rate on capital gains (in percentage)
    \item $K$: Target net amount to raise
    \item $sell_i$: Number of shares to sell of stock $i$
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the expected value of the portfolio next year, while ensuring that the net amount raised is at least $K$:

\[
\text{maximize} \quad \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i)) - \sum_{i=1}^{N} (sell_i \cdot currentPrice_i)
\]

\subsection*{Constraints}
The constraints include the need to raise a net amount of at least $K$ after transaction costs and taxes:

The amount raised from selling shares $i$ is given by:

\[
\text{Amount\_Raised}_i = sell_i \cdot currentPrice_i
\]

The capital gains from selling shares is given by:

\[
\text{Capital\_Gains}_i = (currentPrice_i - buyPrice_i) \cdot sell_i
\]

The transaction cost for selling shares is:

\[
\text{Transaction\_Cost}_i = transactionRate \cdot \text{Amount\_Raised}_i
\]

The net amount raised after considering transaction costs and taxes on capital gains can be expressed as:

\[
\text{Net\_Amount} = \sum_{i=1}^{N} \left( \text{Amount\_Raised}_i - \text{Transaction\_Cost}_i - (taxRate \cdot \text{Capital\_Gains}_i) \right)
\]

Thus, the constraint can be formulated as:

\[
\sum_{i=1}^{N} \left( sell_i \cdot currentPrice_i - transactionRate \cdot (sell_i \cdot currentPrice_i) - taxRate \cdot ((currentPrice_i - buyPrice_i) \cdot sell_i) \right) \geq K
\]

\subsection*{Non-negativity Constraints}
Additionally, we impose that the number of shares to sell cannot be negative:

\[
sell_i \geq 0 \quad \text{for all } i \in \{1, 2, \ldots, N\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from JSON format
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

#### Problem definition
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

#### Variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0, cat='Continuous')

#### Objective function
profit = pulp.lpSum([data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) - sell[i] * data['CurrentPrice'][i] for i in range(data['N'])])
problem += profit

#### Constraints
net_amount = pulp.lpSum([
    (sell[i] * data['CurrentPrice'][i] -
     data['TransactionRate'] * (sell[i] * data['CurrentPrice'][i]) -
     data['TaxRate'] / 100 * ((data['CurrentPrice'][i] - data['BuyPrice'][i]) * sell[i]))
    for i in range(data['N'])
])

problem += net_amount >= data['K'], "NetAmountConstraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

