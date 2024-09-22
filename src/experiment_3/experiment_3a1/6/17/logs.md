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

Let:
\begin{itemize}
    \item \( N \) be the number of different stocks.
    \item \( bought_i \) be the number of shares bought of stock \( i \).
    \item \( buyPrice_i \) be the purchase price of one share of stock \( i \).
    \item \( currentPrice_i \) be the current price of one share of stock \( i \).
    \item \( futurePrice_i \) be the expected future price of one share of stock \( i \) in one year.
    \item \( transactionRate \) be the transaction cost rate (percentage).
    \item \( taxRate \) be the capital gains tax rate (percentage).
    \item \( K \) be the amount of net money to be raised.
    \item \( sell_i \) be the number of shares of stock \( i \) to sell.
\end{itemize}

\textbf{Objective:}
Maximize the expected future value of the portfolio after selling shares, defined as:
\[
\text{maximize } Z = \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i)) 
\]

\textbf{Subject to the constraints:}

1. The net amount raised from selling shares must meet or exceed \( K \):
\[
\sum_{i=1}^{N} \left( (currentPrice_i - transactionRate/100 \cdot currentPrice_i)sell_i - taxRate/100 \cdot (currentPrice_i - buyPrice_i)sell_i \right) \geq K
\]

2. The number of shares sold must not exceed the number of shares bought:
\[
0 \leq sell_i \leq bought_i \quad \text{for } i = 1, \ldots, N
\]

3. Non-negativity constraints:
\[
sell_i \geq 0 \quad \text{for } i = 1, \ldots, N
\]

\textbf{Output:}
Find the optimal \( sell_i \) such that:
\[
\text{output } \{ "sell": [sell_1, sell_2, \ldots, sell_N] \}
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

\section*{Linear Programming Model for Stock Selling}

Let:
\begin{itemize}
    \item \( N \) be the number of different stocks.
    \item \( bought_i \) be the number of shares bought of stock \( i \).
    \item \( buyPrice_i \) be the purchase price of one share of stock \( i \).
    \item \( currentPrice_i \) be the current price of one share of stock \( i \).
    \item \( futurePrice_i \) be the expected future price of one share of stock \( i \) in one year.
    \item \( transactionRate \) be the transaction cost rate (percentage).
    \item \( taxRate \) be the capital gains tax rate (percentage).
    \item \( K \) be the amount of net money to be raised.
    \item \( sell_i \) be the number of shares of stock \( i \) to sell.
\end{itemize}

\textbf{Objective:}
Maximize the expected future value of the portfolio after selling shares, defined as:
\[
\text{maximize } Z = \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i)) 
\]

\textbf{Subject to the constraints:}

1. The net amount raised from selling shares must meet or exceed \( K \):
\[
\sum_{i=1}^{N} \left( (currentPrice_i - transactionRate/100 \cdot currentPrice_i)sell_i - taxRate/100 \cdot (currentPrice_i - buyPrice_i)sell_i \right) \geq K
\]

2. The number of shares sold must not exceed the number of shares bought:
\[
0 \leq sell_i \leq bought_i \quad \text{for } i = 1, \ldots, N
\]

3. Non-negativity constraints:
\[
sell_i \geq 0 \quad \text{for } i = 1, \ldots, N
\]

\textbf{Output:}
Find the optimal \( sell_i \) such that:
\[
\text{output } \{ "sell": [sell_1, sell_2, \ldots, sell_N] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

#### Extracting data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

#### Define the problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

#### Define decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

#### Objective Function
problem += pulp.lpSum(future_price[i] * (bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

#### Constraints
problem += (pulp.lpSum(((current_price[i] - (transaction_rate / 100) * current_price[i]) * sell[i] - 
                         (tax_rate / 100) * (current_price[i] - buy_price[i]) * sell[i]) 
                        for i in range(N)) >= K, "Net_Money_Raised")

#### Constraints for selling shares
for i in range(N):
    problem += sell[i] <= bought[i], f"Max_Sell_Constraint_{i+1}"
    
#### Solve the problem
problem.solve()

#### Output results
sell_values = [sell[i].varValue for i in range(N)]
output = {"sell": sell_values}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

