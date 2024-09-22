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

\section*{Linear Programming Model for Investor's Portfolio}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( N \) = number of different stocks
    \item \( bought_i \) = number of shares bought of stock \( i \)
    \item \( buyPrice_i \) = price at which the investor bought stock \( i \)
    \item \( currentPrice_i \) = current price of stock \( i \)
    \item \( futurePrice_i \) = expected future price of stock \( i \)
    \item \( transactionRate \) = transaction cost rate (in percentage)
    \item \( taxRate \) = tax rate on capital gains (in percentage)
    \item \( K \) = amount of money the investor wants to raise
    \item \( sell_i \) = number of shares of stock \( i \) that the investor should sell
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the expected value of the portfolio next year after selling shares. Therefore, the objective function can be expressed as:

\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( futurePrice_i \cdot (bought_i - sell_i) \right)
\]

\subsection*{Constraints}
1. The net amount raised from selling the shares must be at least \( K \):

\[
\sum_{i=1}^{N} \left( \left( currentPrice_i \cdot sell_i \right) \cdot \left( 1 - \frac{transactionRate}{100} \right) - \left( \left( currentPrice_i - buyPrice_i \right) \cdot sell_i \right) \cdot \frac{taxRate}{100} \right) \geq K
\]

2. The number of shares sold cannot exceed the number of shares bought:

\[
0 \leq sell_i \leq bought_i \quad \forall i
\]

3. Non-negativity constraints:

\[
sell_i \geq 0 \quad \forall i
\]

\subsection*{Input Format}
The input is given by:
\begin{verbatim}
{
    "bought": [bought_i, for i in 1, ..., N],
    "buyPrice": [buyPrice_i, for i in 1, ..., N],
    "currentPrice": [currentPrice_i, for i in 1, ..., N],
    "futurePrice": [futurePrice_i, for i in 1, ..., N],
    "transactionRate": transactionRate,
    "taxRate": taxRate,
    "K": K
}
\end{verbatim}

\subsection*{Output Format}
The output will provide the shares to sell as follows:
\begin{verbatim}
{
    "sell": [sell_i, for i in 1, ..., N],
}
\end{verbatim}

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

\section*{Linear Programming Model for Investor's Portfolio}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( N \) = number of different stocks
    \item \( bought_i \) = number of shares bought of stock \( i \)
    \item \( buyPrice_i \) = price at which the investor bought stock \( i \)
    \item \( currentPrice_i \) = current price of stock \( i \)
    \item \( futurePrice_i \) = expected future price of stock \( i \)
    \item \( transactionRate \) = transaction cost rate (in percentage)
    \item \( taxRate \) = tax rate on capital gains (in percentage)
    \item \( K \) = amount of money the investor wants to raise
    \item \( sell_i \) = number of shares of stock \( i \) that the investor should sell
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the expected value of the portfolio next year after selling shares. Therefore, the objective function can be expressed as:

\[
\text{Maximize } Z = \sum_{i=1}^{N} \left( futurePrice_i \cdot (bought_i - sell_i) \right)
\]

\subsection*{Constraints}
1. The net amount raised from selling the shares must be at least \( K \):

\[
\sum_{i=1}^{N} \left( \left( currentPrice_i \cdot sell_i \right) \cdot \left( 1 - \frac{transactionRate}{100} \right) - \left( \left( currentPrice_i - buyPrice_i \right) \cdot sell_i \right) \cdot \frac{taxRate}{100} \right) \geq K
\]

2. The number of shares sold cannot exceed the number of shares bought:

\[
0 \leq sell_i \leq bought_i \quad \forall i
\]

3. Non-negativity constraints:

\[
sell_i \geq 0 \quad \forall i
\]

\subsection*{Input Format}
The input is given by:
\begin{verbatim}
{
    "bought": [bought_i, for i in 1, ..., N],
    "buyPrice": [buyPrice_i, for i in 1, ..., N],
    "currentPrice": [currentPrice_i, for i in 1, ..., N],
    "futurePrice": [futurePrice_i, for i in 1, ..., N],
    "transactionRate": transactionRate,
    "taxRate": taxRate,
    "K": K
}
\end{verbatim}

\subsection*{Output Format}
The output will provide the shares to sell as follows:
\begin{verbatim}
{
    "sell": [sell_i, for i in 1, ..., N],
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Define the data
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,
    'TaxRate': 15.0,
    'K': 5000,
}

#### Extract data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

#### Define the problem
problem = pulp.LpProblem("InvestorPortfolio", pulp.LpMaximize)

#### Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

#### Objective Function
problem += pulp.lpSum([futurePrice[i] * (bought[i] - sell[i]) for i in range(N)])

#### Constraint 1: Net amount raised from selling shares
problem += pulp.lpSum([
    (currentPrice[i] * sell[i]) * (1 - transactionRate / 100) - ((currentPrice[i] - buyPrice[i]) * sell[i]) * (taxRate / 100)
    for i in range(N)
]) >= K

#### Solve the problem
problem.solve()

#### Output the solution
sell_values = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_values}
print(output)

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

