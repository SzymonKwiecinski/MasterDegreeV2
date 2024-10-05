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
To solve this problem, we need to create a linear programming model that maximizes the expected value of the investor's portfolio next year while ensuring that the net proceeds from selling shares meet or exceed the required amount \(K\). 

Let's outline the LP model:

1. **Decision Variables**:
   - \( x_i \): Number of shares of stock \(i\) to sell.

2. **Objective Function**:
   - Maximize the expected value of the portfolio next year:
   
   \[
   \text{maximize} \quad \sum_{i=1}^{N} \left(bought_i - x_i\right) \times futurePrice_i
   \]

3. **Constraints**:
   
   - Non-negativity and availability constraint:
     \[
     0 \leq x_i \leq bought_i \quad \forall \, i = 1, \ldots, N
     \]
   
   - Net proceeds requirement:
     \[
     \sum_{i=1}^{N} \left( \text{currentPrice}_i \times x_i - \left(\text{currentPrice}_i \times x_i - \text{buyPrice}_i \times x_i\right) \times \frac{\text{taxRate}}{100} - \text{currentPrice}_i \times x_i \times \frac{\text{transactionRate}}{100} \right) \geq K
     \]

Now, let's write this in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Portfolio Optimization}

\subsection*{Objective:}
Maximize the expected value of the portfolio next year:
\[
\text{maximize} \quad \sum_{i=1}^{N} \left(bought_i - x_i\right) \times futurePrice_i
\]

\subsection*{Constraints:}

\begin{align*}
& 0 \leq x_i \leq bought_i, \quad \forall \, i = 1, \ldots, N \\
& \sum_{i=1}^{N} \left( \text{currentPrice}_i \times x_i - \left(\text{currentPrice}_i \times x_i - \text{buyPrice}_i \times x_i\right) \times \frac{\text{taxRate}}{100} - \text{currentPrice}_i \times x_i \times \frac{\text{transactionRate}}{100} \right) \geq K
\end{align*}

\subsection*{Variables:}
\begin{itemize}
    \item \( x_i \): Number of shares of stock \(i\) to sell, \(i = 1, \ldots, N\)
\end{itemize}

\end{document}
```

This LaTeX code generates the mathematical model for the problem, specifying the objective and the constraints we need to solve in order to determine the number of shares to sell for each stock.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Portfolio Optimization}

\subsection*{Objective:}
Maximize the expected value of the portfolio next year:
\[
\text{maximize} \quad \sum_{i=1}^{N} \left(bought_i - x_i\right) \times futurePrice_i
\]

\subsection*{Constraints:}

\begin{align*}
& 0 \leq x_i \leq bought_i, \quad \forall \, i = 1, \ldots, N \\
& \sum_{i=1}^{N} \left( \text{currentPrice}_i \times x_i - \left(\text{currentPrice}_i \times x_i - \text{buyPrice}_i \times x_i\right) \times \frac{\text{taxRate}}{100} - \text{currentPrice}_i \times x_i \times \frac{\text{transactionRate}}{100} \right) \geq K
\end{align*}

\subsection*{Variables:}
\begin{itemize}
    \item \( x_i \): Number of shares of stock \(i\) to sell, \(i = 1, \ldots, N\)
\end{itemize}

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

#### Problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=data['Bought'][i]) for i in range(data['N'])]

#### Objective function
objective = sum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))
problem += objective

#### Constraints
constraint = sum(
    data['CurrentPrice'][i] * x[i] -
    (data['CurrentPrice'][i] * x[i] - data['BuyPrice'][i] * x[i]) * (data['TaxRate'] / 100) -
    data['CurrentPrice'][i] * x[i] * (data['TransactionRate'] / 100)
    for i in range(data['N'])
) >= data['K']
problem += constraint

#### Solve
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

