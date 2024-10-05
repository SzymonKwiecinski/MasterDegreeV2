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
To model the given problem using Linear Programming, we need to establish the objective function and constraints based on the provided information.

**Objective Function**: The investor aims to maximize the expected value of his portfolio next year. The expected value of one share of stock \(i\) in one year is given by \( \text{futurePrice}_i \). Therefore, for maximizing the portfolio's expected value, we consider:

\[ \text{maximize} \quad \sum_{i=1}^{N} (\text{bought}_i - \text{sell}_i) \times \text{futurePrice}_i \]

**Constraints**:

1. To meet the requirement of raising an amount \(K\) net of capital gains and transaction costs, the following constraint must be satisfied:

   \[
   \sum_{i=1}^{N} \left( \text{sell}_i \times \text{currentPrice}_i \right) - \sum_{i=1}^{N} \left( \text{sell}_i \times \text{buyPrice}_i \right) \times \frac{\text{taxRate}}{100} - \sum_{i=1}^{N} \left( \text{sell}_i \times \text{currentPrice}_i \right) \times \frac{\text{transactionRate}}{100} \geq K
   \]

2. No more shares can be sold than those available:

   \[
   \text{sell}_i \leq \text{bought}_i \quad \text{for all } i = 1, \ldots, N
   \]

3. Non-negativity constraint, as the number of shares being sold cannot be negative:

   \[
   \text{sell}_i \geq 0 \quad \text{for all } i = 1, \ldots, N
   \]

Here is the complete Linear Programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective Function}
Maximize the expected value of the portfolio next year:
\[
\text{maximize} \quad \sum_{i=1}^{N} (\text{bought}_i - \text{sell}_i) \times \text{futurePrice}_i
\]

\subsection*{Constraints}

1. Raise amount \(K\) net of capital gains and transaction costs:
\[
\sum_{i=1}^{N} \left( \text{sell}_i \times \text{currentPrice}_i \right) - \sum_{i=1}^{N} \left( \text{sell}_i \times \text{buyPrice}_i \right) \times \frac{\text{taxRate}}{100} - \sum_{i=1}^{N} \left( \text{sell}_i \times \text{currentPrice}_i \right) \times \frac{\text{transactionRate}}{100} \geq K
\]

2. Limit on maximum shares sold:
\[
\text{sell}_i \leq \text{bought}_i \quad \text{for all } i = 1, \ldots, N
\]

3. Non-negativity of shares sold:
\[
\text{sell}_i \geq 0 \quad \text{for all } i = 1, \ldots, N
\]

\end{document}
```

This model will help determine the optimal number of shares to sell (\( \text{sell}_i \)) for each stock \(i\), such that the investor can raise the required amount \(K\) while maximizing the expected value of the portfolio next year.

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

\subsection*{Objective Function}
Maximize the expected value of the portfolio next year:
\[
\text{maximize} \quad \sum_{i=1}^{N} (\text{bought}_i - \text{sell}_i) \times \text{futurePrice}_i
\]

\subsection*{Constraints}

1. Raise amount \(K\) net of capital gains and transaction costs:
\[
\sum_{i=1}^{N} \left( \text{sell}_i \times \text{currentPrice}_i \right) - \sum_{i=1}^{N} \left( \text{sell}_i \times \text{buyPrice}_i \right) \times \frac{\text{taxRate}}{100} - \sum_{i=1}^{N} \left( \text{sell}_i \times \text{currentPrice}_i \right) \times \frac{\text{transactionRate}}{100} \geq K
\]

2. Limit on maximum shares sold:
\[
\text{sell}_i \leq \text{bought}_i \quad \text{for all } i = 1, \ldots, N
\]

3. Non-negativity of shares sold:
\[
\text{sell}_i \geq 0 \quad \text{for all } i = 1, \ldots, N
\]

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
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

#### Number of assets
N = data['N']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

#### Define decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')
bought = data['Bought']

#### Objective function
problem += pulp.lpSum((bought[i] - sell[i]) * data['FuturePrice'][i] for i in range(N)), "Total Expected Value"

#### Constraints
#### Constraint 1: raise amount K
problem += (pulp.lpSum(sell[i] * data['CurrentPrice'][i] for i in range(N)) - 
             pulp.lpSum(sell[i] * data['BuyPrice'][i] for i in range(N)) * (data['TaxRate'] / 100) - 
             pulp.lpSum(sell[i] * data['CurrentPrice'][i] for i in range(N)) * (data['TransactionRate'] / 100) >= data['K']), "Capital Gains Constraint"

#### Constraint 2: limit on maximum shares sold
for i in range(N):
    problem += (sell[i] <= bought[i]), f"Max_Sold_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

