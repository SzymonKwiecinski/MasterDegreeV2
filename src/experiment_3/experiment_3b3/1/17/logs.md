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

\section*{Linear Programming Model for Stock Selling Optimization}

\textbf{Parameters:}
\begin{itemize}
    \item $N$: Number of different stocks.
    \item $bought_i$: Number of shares bought of stock $i$.
    \item $buyPrice_i$: Purchase price of stock $i$.
    \item $currentPrice_i$: Current price of stock $i$.
    \item $futurePrice_i$: Expected future price of stock $i$.
    \item $transactionRate$: Transaction cost percentage.
    \item $taxRate$: Tax rate on capital gains percentage.
    \item $K$: Desired amount of money net of capital gains and transaction costs.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $sell_i$: Number of shares of stock $i$ that the investor will sell.
\end{itemize}

\textbf{Objective Function:}
Maximize the expected value of the portfolio next year, given by:
\[
\text{Maximize } \sum_{i=1}^{N} futurePrice_i \cdot (bought_i - sell_i) 
\]

\textbf{Constraints:}
1. The net amount raised from selling shares must meet the requirement:
\[
\sum_{i=1}^{N} \left( (currentPrice_i \cdot sell_i) \cdot (1 - \frac{transactionRate}{100}) - (sell_i \cdot (currentPrice_i - buyPrice_i)) \cdot \frac{taxRate}{100} \right) \geq K
\]

2. The number of shares sold cannot exceed the number of shares bought:
\[
0 \leq sell_i \leq bought_i, \quad \forall i = 1, \ldots, N
\]

\textbf{Output Format:}
The solution will return:
\[
\{ "sell": [sell_1, sell_2, \ldots, sell_N] \}
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

\section*{Linear Programming Model for Stock Selling Optimization}

\textbf{Parameters:}
\begin{itemize}
    \item $N$: Number of different stocks.
    \item $bought_i$: Number of shares bought of stock $i$.
    \item $buyPrice_i$: Purchase price of stock $i$.
    \item $currentPrice_i$: Current price of stock $i$.
    \item $futurePrice_i$: Expected future price of stock $i$.
    \item $transactionRate$: Transaction cost percentage.
    \item $taxRate$: Tax rate on capital gains percentage.
    \item $K$: Desired amount of money net of capital gains and transaction costs.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $sell_i$: Number of shares of stock $i$ that the investor will sell.
\end{itemize}

\textbf{Objective Function:}
Maximize the expected value of the portfolio next year, given by:
\[
\text{Maximize } \sum_{i=1}^{N} futurePrice_i \cdot (bought_i - sell_i) 
\]

\textbf{Constraints:}
1. The net amount raised from selling shares must meet the requirement:
\[
\sum_{i=1}^{N} \left( (currentPrice_i \cdot sell_i) \cdot (1 - \frac{transactionRate}{100}) - (sell_i \cdot (currentPrice_i - buyPrice_i)) \cdot \frac{taxRate}{100} \right) \geq K
\]

2. The number of shares sold cannot exceed the number of shares bought:
\[
0 \leq sell_i \leq bought_i, \quad \forall i = 1, \ldots, N
\]

\textbf{Output Format:}
The solution will return:
\[
\{ "sell": [sell_1, sell_2, \ldots, sell_N] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

#### Define the problem
problem = pulp.LpProblem("Stock_Selling_Optimization", pulp.LpMaximize)

#### Decision variables
sell = [pulp.LpVariable(f'sell_{i}', 0, Bought[i], cat='Continuous') for i in range(N)]

#### Objective function
problem += pulp.lpSum([FuturePrice[i] * (Bought[i] - sell[i]) for i in range(N)])

#### Constraint 1: Net amount raised from selling shares must meet the requirement K
problem += pulp.lpSum([
    (CurrentPrice[i] * sell[i] * (1 - TransactionRate / 100))
    - (sell[i] * (CurrentPrice[i] - BuyPrice[i]) * TaxRate / 100) 
    for i in range(N)
]) >= K

#### Constraint 2: The number of shares sold cannot exceed the number of shares bought
#### Already implemented by bounds on decision variables

#### Solve the problem
problem.solve()

#### Output the solution
sell_values = [pulp.value(sell[i]) for i in range(N)]
solution = {"sell": sell_values}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

