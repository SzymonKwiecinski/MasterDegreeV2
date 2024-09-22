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

\section*{Investor's Stock Selling Problem}

\subsection*{Parameters}

Let:
\begin{itemize}
    \item \( N \): number of different stocks.
    \item \( bought_i \): number of shares bought of stock \( i \).
    \item \( buyPrice_i \): purchase price of stock \( i \).
    \item \( currentPrice_i \): current price of stock \( i \).
    \item \( futurePrice_i \): expected price of stock \( i \) in one year.
    \item \( transactionRate \): transaction cost as a percentage of the amount transacted.
    \item \( taxRate \): tax on capital gains as a percentage.
    \item \( K \): required net money to raise.
\end{itemize}

\subsection*{Decision Variables}

Let:
\[
sell_i \quad \text{for } i = 1, \ldots, N
\]
denote the number of shares of stock \( i \) that the investor should sell.

\subsection*{Objective Function}

The objective is to maximize the expected value of the portfolio in one year while ensuring the net proceeds from selling shares cover the required amount \( K \). Thus, we formulate the optimization problem as follows:

\[
\text{Maximize } \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i)) - \sum_{i=1}^{N} (currentPrice_i \cdot sell_i \cdot (1 + \frac{transactionRate}{100})) - \sum_{i=1}^{N} \left( \frac{(currentPrice_i - buyPrice_i)}{currentPrice_i} \cdot taxRate \cdot sell_i \right)
\]

\subsection*{Constraints}

The primary constraint ensuring that the investor raises at least \( K \) net of transaction costs and taxes is given by:

\[
\sum_{i=1}^{N} (currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (currentPrice_i - buyPrice_i) \cdot taxRate \cdot sell_i) \geq K
\]

Additionally, the shares sold cannot exceed the shares bought:

\[
0 \leq sell_i \leq bought_i \quad \text{for } i = 1, \ldots, N
\]

\subsection*{Final Formulation}

We can summarize the linear programming problem as follows:

\[
\begin{align*}
\text{Maximize} & \quad \sum_{i=1}^{N} \left( futurePrice_i \cdot (bought_i - sell_i) \right) - \sum_{i=1}^{N} \left( currentPrice_i \cdot sell_i \cdot (1 + \frac{transactionRate}{100}) \right) \\
& \quad - \sum_{i=1}^{N} \left( \frac{(currentPrice_i - buyPrice_i)}{currentPrice_i} \cdot taxRate \cdot sell_i \right) \\
\text{subject to} & \quad \sum_{i=1}^{N} \left( currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (currentPrice_i - buyPrice_i) \cdot taxRate \cdot sell_i \right) \geq K \\
& \quad 0 \leq sell_i \leq bought_i \quad \text{for } i = 1, \ldots, N \\
\end{align*}
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

\section*{Investor's Stock Selling Problem}

\subsection*{Parameters}

Let:
\begin{itemize}
    \item \( N \): number of different stocks.
    \item \( bought_i \): number of shares bought of stock \( i \).
    \item \( buyPrice_i \): purchase price of stock \( i \).
    \item \( currentPrice_i \): current price of stock \( i \).
    \item \( futurePrice_i \): expected price of stock \( i \) in one year.
    \item \( transactionRate \): transaction cost as a percentage of the amount transacted.
    \item \( taxRate \): tax on capital gains as a percentage.
    \item \( K \): required net money to raise.
\end{itemize}

\subsection*{Decision Variables}

Let:
\[
sell_i \quad \text{for } i = 1, \ldots, N
\]
denote the number of shares of stock \( i \) that the investor should sell.

\subsection*{Objective Function}

The objective is to maximize the expected value of the portfolio in one year while ensuring the net proceeds from selling shares cover the required amount \( K \). Thus, we formulate the optimization problem as follows:

\[
\text{Maximize } \sum_{i=1}^{N} (futurePrice_i \cdot (bought_i - sell_i)) - \sum_{i=1}^{N} (currentPrice_i \cdot sell_i \cdot (1 + \frac{transactionRate}{100})) - \sum_{i=1}^{N} \left( \frac{(currentPrice_i - buyPrice_i)}{currentPrice_i} \cdot taxRate \cdot sell_i \right)
\]

\subsection*{Constraints}

The primary constraint ensuring that the investor raises at least \( K \) net of transaction costs and taxes is given by:

\[
\sum_{i=1}^{N} (currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (currentPrice_i - buyPrice_i) \cdot taxRate \cdot sell_i) \geq K
\]

Additionally, the shares sold cannot exceed the shares bought:

\[
0 \leq sell_i \leq bought_i \quad \text{for } i = 1, \ldots, N
\]

\subsection*{Final Formulation}

We can summarize the linear programming problem as follows:

\[
\begin{align*}
\text{Maximize} & \quad \sum_{i=1}^{N} \left( futurePrice_i \cdot (bought_i - sell_i) \right) - \sum_{i=1}^{N} \left( currentPrice_i \cdot sell_i \cdot (1 + \frac{transactionRate}{100}) \right) \\
& \quad - \sum_{i=1}^{N} \left( \frac{(currentPrice_i - buyPrice_i)}{currentPrice_i} \cdot taxRate \cdot sell_i \right) \\
\text{subject to} & \quad \sum_{i=1}^{N} \left( currentPrice_i \cdot sell_i \cdot (1 - \frac{transactionRate}{100}) - (currentPrice_i - buyPrice_i) \cdot taxRate \cdot sell_i \right) \geq K \\
& \quad 0 \leq sell_i \leq bought_i \quad \text{for } i = 1, \ldots, N \\
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
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

#### Problem Definition
problem = pulp.LpProblem("Investor_Stock_Selling_Problem", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0)

#### Objective Function
profit_from_future = pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(data['N']))
cost_of_selling = pulp.lpSum(data['CurrentPrice'][i] * sell[i] * (1 + data['TransactionRate'] / 100) for i in range(data['N']))
tax_cost = pulp.lpSum(((data['CurrentPrice'][i] - data['BuyPrice'][i]) / data['CurrentPrice'][i]) * data['TaxRate'] / 100 * sell[i] for i in range(data['N']))

problem += profit_from_future - cost_of_selling - tax_cost, "Total_Profit"

#### Constraints
net_proceeds = pulp.lpSum((data['CurrentPrice'][i] * sell[i] * (1 - data['TransactionRate'] / 100)) - 
                          ((data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] / 100) * sell[i] 
                          for i in range(data['N']))

problem += net_proceeds >= data['K'], "Net_Proceeds_Constraint"

#### Constraints to limit sells to the amount bought
for i in range(data['N']):
    problem += sell[i] <= data['Bought'][i], f"Limit_Sell_{i}"
    
#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

