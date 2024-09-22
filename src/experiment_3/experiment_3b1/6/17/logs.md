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

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( N \) = number of different stocks
    \item \( bought_i \) = number of shares bought of stock \( i \)
    \item \( buyPrice_i \) = price per share of stock \( i \) when bought
    \item \( currentPrice_i \) = current price per share of stock \( i \)
    \item \( futurePrice_i \) = expected price per share of stock \( i \) in one year
    \item \( transactionRate \) = transaction cost rate (as a percentage)
    \item \( taxRate \) = tax rate on capital gains (as a percentage)
    \item \( K \) = amount of money the investor wants to raise net of capital gains and transaction costs
    \item \( sell_i \) = number of shares of stock \( i \) that the investor should sell
\end{itemize}

\subsection*{Objective}
Maximize the expected value of the portfolio next year:
\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( futurePrice_i \cdot (bought_i - sell_i) \right)
\]

\subsection*{Constraints}
1. The amount received from selling shares, net of transaction costs and taxes, should be at least \( K \):
\[
\sum_{i=1}^{N} \left( currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (currentPrice_i - buyPrice_i) \cdot sell_i \cdot \frac{taxRate}{100} \right) \geq K
\]

2. The number of shares sold cannot exceed the number of shares owned:
\[
sell_i \leq bought_i, \quad \forall i \in \{1, \ldots, N\}
\]

3. The number of shares sold must be non-negative:
\[
sell_i \geq 0, \quad \forall i \in \{1, \ldots, N\}
\]

\subsection*{Output}
The solution will yield the optimal number of shares to sell for each stock \( i \):
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

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( N \) = number of different stocks
    \item \( bought_i \) = number of shares bought of stock \( i \)
    \item \( buyPrice_i \) = price per share of stock \( i \) when bought
    \item \( currentPrice_i \) = current price per share of stock \( i \)
    \item \( futurePrice_i \) = expected price per share of stock \( i \) in one year
    \item \( transactionRate \) = transaction cost rate (as a percentage)
    \item \( taxRate \) = tax rate on capital gains (as a percentage)
    \item \( K \) = amount of money the investor wants to raise net of capital gains and transaction costs
    \item \( sell_i \) = number of shares of stock \( i \) that the investor should sell
\end{itemize}

\subsection*{Objective}
Maximize the expected value of the portfolio next year:
\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( futurePrice_i \cdot (bought_i - sell_i) \right)
\]

\subsection*{Constraints}
1. The amount received from selling shares, net of transaction costs and taxes, should be at least \( K \):
\[
\sum_{i=1}^{N} \left( currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (currentPrice_i - buyPrice_i) \cdot sell_i \cdot \frac{taxRate}{100} \right) \geq K
\]

2. The number of shares sold cannot exceed the number of shares owned:
\[
sell_i \leq bought_i, \quad \forall i \in \{1, \ldots, N\}
\]

3. The number of shares sold must be non-negative:
\[
sell_i \geq 0, \quad \forall i \in \{1, \ldots, N\}
\]

\subsection*{Output}
The solution will yield the optimal number of shares to sell for each stock \( i \):
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

#### Problem definition
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

#### Variables
N = data['N']
bought = data['Bought']
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, upBound=None, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(data['FuturePrice'][i] * (bought[i] - sell[i]) for i in range(N)), "Expected_Portfolio_Value"

#### Constraints
#### Constraint 1: Amount received from selling shares must be at least K
problem += pulp.lpSum(((data['CurrentPrice'][i] * sell[i] * (1 - data['TransactionRate'] / 100)) - 
                        ((data['CurrentPrice'][i] - data['BuyPrice'][i]) * sell[i] * (data['TaxRate'] / 100))) 
                       for i in range(N)) >= data['K'], "Capital_Gains_Constraint"

#### Constraint 2: Cannot sell more than bought
for i in range(N):
    problem += sell[i] <= bought[i], f"Max_Sell_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Output
sell_results = [sell[i].varValue for i in range(N)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output: {{ "sell": {sell_results} }}')
```

