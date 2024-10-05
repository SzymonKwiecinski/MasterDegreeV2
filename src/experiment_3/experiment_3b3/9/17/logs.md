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

\textbf{Variables:} \\
Let \( x_i \) be the number of shares of stock \( i \) that the investor sells, where \( i = 1, 2, \ldots, N \).

\textbf{Parameters:} \\
Let:
\begin{itemize}
    \item \( \text{bought}_i \): Number of shares bought of stock \( i \) \\
    \item \( \text{buyPrice}_i \): Purchase price per share of stock \( i \) \\
    \item \( \text{currentPrice}_i \): Current price per share of stock \( i \) \\
    \item \( \text{futurePrice}_i \): Expected future price per share of stock \( i \) \\
    \item \( \text{transactionRate} \): Transaction cost rate in percentage \\
    \item \( \text{taxRate} \): Tax rate on capital gains in percentage \\
    \item \( K \): Net amount of money needed by the investor
\end{itemize}

\textbf{Objective Function:} \\
Maximize the expected future value of the portfolio:
\[
\max \sum_{i=1}^{N} \left( \text{futurePrice}_i \cdot \text{bought}_i - x_i \cdot \text{futurePrice}_i \right)
\]

\textbf{Constraints:} \\
The total amount raised from selling shares must cover the net amount needed:
\[
\sum_{i=1}^{N} \left( x_i \cdot \text{currentPrice}_i \cdot (1 - \frac{\text{transactionRate}}{100}) - (x_i \cdot \text{buyPrice}_i \cdot \frac{\text{taxRate}}{100}) \right) \geq K
\]
Additionally, we must ensure that the number of shares sold does not exceed the shares bought:
\[
0 \leq x_i \leq \text{bought}_i, \quad \forall i
\]

\textbf{Output:} \\
The output format will be:
\[
\text{sell} = [x_1, x_2, \ldots, x_N]
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

\textbf{Variables:} \\
Let \( x_i \) be the number of shares of stock \( i \) that the investor sells, where \( i = 1, 2, \ldots, N \).

\textbf{Parameters:} \\
Let:
\begin{itemize}
    \item \( \text{bought}_i \): Number of shares bought of stock \( i \) \\
    \item \( \text{buyPrice}_i \): Purchase price per share of stock \( i \) \\
    \item \( \text{currentPrice}_i \): Current price per share of stock \( i \) \\
    \item \( \text{futurePrice}_i \): Expected future price per share of stock \( i \) \\
    \item \( \text{transactionRate} \): Transaction cost rate in percentage \\
    \item \( \text{taxRate} \): Tax rate on capital gains in percentage \\
    \item \( K \): Net amount of money needed by the investor
\end{itemize}

\textbf{Objective Function:} \\
Maximize the expected future value of the portfolio:
\[
\max \sum_{i=1}^{N} \left( \text{futurePrice}_i \cdot \text{bought}_i - x_i \cdot \text{futurePrice}_i \right)
\]

\textbf{Constraints:} \\
The total amount raised from selling shares must cover the net amount needed:
\[
\sum_{i=1}^{N} \left( x_i \cdot \text{currentPrice}_i \cdot (1 - \frac{\text{transactionRate}}{100}) - (x_i \cdot \text{buyPrice}_i \cdot \frac{\text{taxRate}}{100}) \right) \geq K
\]
Additionally, we must ensure that the number of shares sold does not exceed the shares bought:
\[
0 \leq x_i \leq \text{bought}_i, \quad \forall i
\]

\textbf{Output:} \\
The output format will be:
\[
\text{sell} = [x_1, x_2, \ldots, x_N]
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

#### Extracting data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

#### Initializing the problem
problem = pulp.LpProblem("Stock_Selling_Optimization", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

#### Objective function
problem += pulp.lpSum((future_price[i] * bought[i] - x[i] * future_price[i]) for i in range(N))

#### Constraints
problem += pulp.lpSum(
    [x[i] * current_price[i] * (1 - transaction_rate / 100) - 
     x[i] * buy_price[i] * (tax_rate / 100) for i in range(N)]
) >= K

#### Solve the problem
problem.solve()

#### Output the solution
sell = [x[i].varValue for i in range(N)]
print(f'sell = {sell}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

