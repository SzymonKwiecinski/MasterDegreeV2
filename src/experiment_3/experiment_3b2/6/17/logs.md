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
To model this problem as a linear programming problem, we will define the decision variables, objective function, and constraints. Let's assume that the decision variable \( x_i \) represents the number of shares of stock \( i \) that the investor sells. The objective is to maximize the expected value of the investor's portfolio in one year, subject to the constraint that the investor raises an amount \( K \) net of capital gains and transaction costs.

Here is the mathematical formulation:

1. **Decision Variables:**
   - \( x_i \): Number of shares of stock \( i \) to sell, \( i = 1, \ldots, N \).

2. **Objective Function:**
   - Maximize the expected value of the portfolio in one year:
   \[
   \text{Maximize} \quad \sum_{i=1}^{N} (bought_i - x_i) \times futurePrice_i
   \]

3. **Constraints:**
   - Raise at least amount \( K \), net of transaction costs and capital gains tax:
   \[
   \sum_{i=1}^{N} \left( (1 - \frac{\text{transactionRate}}{100}) \times currentPrice_i \times x_i - \frac{\text{taxRate}}{100} \times (currentPrice_i - buyPrice_i) \times x_i \right) \geq K
   \]
   - Cannot sell more shares than owned:
   \[
   0 \leq x_i \leq bought_i, \quad i = 1, \ldots, N
   \]

Now, let's put this model into a LaTeX document:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( x_i \) be the number of shares of stock \( i \) to sell, where \( i = 1, \ldots, N \).

\subsection*{Objective Function}
Maximize the expected future value of the portfolio:
\[
\text{Maximize} \quad \sum_{i=1}^{N} (bought_i - x_i) \times futurePrice_i
\]

\subsection*{Constraints}
1. The amount raised is at least \( K \), net of transaction costs and taxes:
\[
\sum_{i=1}^{N} \left( (1 - \frac{\text{transactionRate}}{100}) \times currentPrice_i \times x_i - \frac{\text{taxRate}}{100} \times (currentPrice_i - buyPrice_i) \times x_i \right) \geq K
\]

2. Do not sell more shares than owned:
\[
0 \leq x_i \leq bought_i, \quad i = 1, \ldots, N
\]

\end{document}
```

This model captures the essential elements of the problem, including the objective of maximizing future portfolio value while meeting the net cash requirement \( K \) after accounting for transaction costs and capital gains taxes.

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

\subsection*{Decision Variables}
Let \( x_i \) be the number of shares of stock \( i \) to sell, where \( i = 1, \ldots, N \).

\subsection*{Objective Function}
Maximize the expected future value of the portfolio:
\[
\text{Maximize} \quad \sum_{i=1}^{N} (bought_i - x_i) \times futurePrice_i
\]

\subsection*{Constraints}
1. The amount raised is at least \( K \), net of transaction costs and taxes:
\[
\sum_{i=1}^{N} \left( (1 - \frac{\text{transactionRate}}{100}) \times currentPrice_i \times x_i - \frac{\text{taxRate}}{100} \times (currentPrice_i - buyPrice_i) \times x_i \right) \geq K
\]

2. Do not sell more shares than owned:
\[
0 \leq x_i \leq bought_i, \quad i = 1, \ldots, N
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

#### Create the linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("shares_to_sell", range(data['N']), lowBound=0)

#### Objective Function
problem += pulp.lpSum([(data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N'])]), "Total_Expected_Future_Value"

#### Constraints
#### Constraint 1: Amount raised is at least K, net of transaction costs and taxes
problem += pulp.lpSum([(1 - data['TransactionRate'] / 100) * data['CurrentPrice'][i] * x[i] -
                        (data['TaxRate'] / 100) * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * x[i]
                        for i in range(data['N'])]) >= data['K'], "Minimum_Amount_Raised"

#### Constraint 2: Do not sell more shares than owned
for i in range(data['N']):
    problem += x[i] <= data['Bought'][i], f"Max_Shares_Sold_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

