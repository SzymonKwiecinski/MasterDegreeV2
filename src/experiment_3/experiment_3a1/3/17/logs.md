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

Let:
\begin{itemize}
    \item $N$: Number of different stocks.
    \item $bought_i$: Number of shares bought of stock $i$.
    \item $buyPrice_i$: Purchase price per share of stock $i$.
    \item $currentPrice_i$: Current price per share of stock $i$.
    \item $futurePrice_i$: Expected price per share of stock $i$ in one year.
    \item $transactionRate$: Transaction cost rate (percentage) of the amount transacted.
    \item $taxRate$: Tax rate (percentage) on capital gains.
    \item $K$: Amount of money to be raised net of capital gains and transaction costs.
    \item $sell_i$: Number of shares of stock $i$ to sell.
\end{itemize}

The objective is to maximize the expected value of the portfolio while ensuring that the net amount raised from selling shares meets or exceeds $K$.

\subsection*{Objective Function}
Maximize the expected value of the portfolio next year:
\[
\text{Maximize } Z = \sum_{i=1}^{N} futurePrice_i \cdot (bought_i - sell_i)
\]

\subsection*{Constraints}
The amount raised from selling shares, net of transaction costs and taxes on capital gains, should be greater than or equal to $K$:
\[
\sum_{i=1}^{N} \left( (currentPrice_i \cdot sell_i) - \left( transactionRate \cdot (currentPrice_i \cdot sell_i) + taxRate \cdot \left( (currentPrice_i - buyPrice_i) \cdot sell_i \right) \right) \right) \geq K
\]
This simplifies to:
\[
\sum_{i=1}^{N} \left( (1 - transactionRate) \cdot currentPrice_i \cdot sell_i - taxRate \cdot (currentPrice_i - buyPrice_i) \cdot sell_i \right) \geq K
\]

\subsection*{Non-negativity Constraint}
\[
sell_i \geq 0 \quad \forall i \in \{1, 2, \ldots, N\}
\]

\subsection*{Variable Definition}
\begin{itemize}
    \item $sell_i$: Number of shares of stock $i$ to sell, where $i = 1, 2, \ldots, N$.
\end{itemize}

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

Let:
\begin{itemize}
    \item $N$: Number of different stocks.
    \item $bought_i$: Number of shares bought of stock $i$.
    \item $buyPrice_i$: Purchase price per share of stock $i$.
    \item $currentPrice_i$: Current price per share of stock $i$.
    \item $futurePrice_i$: Expected price per share of stock $i$ in one year.
    \item $transactionRate$: Transaction cost rate (percentage) of the amount transacted.
    \item $taxRate$: Tax rate (percentage) on capital gains.
    \item $K$: Amount of money to be raised net of capital gains and transaction costs.
    \item $sell_i$: Number of shares of stock $i$ to sell.
\end{itemize}

The objective is to maximize the expected value of the portfolio while ensuring that the net amount raised from selling shares meets or exceeds $K$.

\subsection*{Objective Function}
Maximize the expected value of the portfolio next year:
\[
\text{Maximize } Z = \sum_{i=1}^{N} futurePrice_i \cdot (bought_i - sell_i)
\]

\subsection*{Constraints}
The amount raised from selling shares, net of transaction costs and taxes on capital gains, should be greater than or equal to $K$:
\[
\sum_{i=1}^{N} \left( (currentPrice_i \cdot sell_i) - \left( transactionRate \cdot (currentPrice_i \cdot sell_i) + taxRate \cdot \left( (currentPrice_i - buyPrice_i) \cdot sell_i \right) \right) \right) \geq K
\]
This simplifies to:
\[
\sum_{i=1}^{N} \left( (1 - transactionRate) \cdot currentPrice_i \cdot sell_i - taxRate \cdot (currentPrice_i - buyPrice_i) \cdot sell_i \right) \geq K
\]

\subsection*{Non-negativity Constraint}
\[
sell_i \geq 0 \quad \forall i \in \{1, 2, \ldots, N\}
\]

\subsection*{Variable Definition}
\begin{itemize}
    \item $sell_i$: Number of shares of stock $i$ to sell, where $i = 1, 2, \ldots, N$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Input data
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
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

#### Variables
sell = pulp.LpVariable.dicts("Sell", range(data['N']), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(data['N'])), "Total_Expected_Value"

#### Constraints
problem += pulp.lpSum((1 - data['TransactionRate'] / 100) * data['CurrentPrice'][i] * sell[i] - 
                      (data['TaxRate'] / 100) * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * sell[i] 
                      for i in range(data['N'])) >= data['K'], "Capital_Gains_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

