# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of different shares (constant)
    \item $Bought_i$: Amount of each share $i$ initially bought, for $i = 1, 2, \ldots, N$
    \item $BuyPrice_i$: Purchase price of each share $i$, for $i = 1, 2, \ldots, N$
    \item $CurrentPrice_i$: Current market price of each share $i$, for $i = 1, 2, \ldots, N$
    \item $FuturePrice_i$: Expected future market price of each share $i$, for $i = 1, 2, \ldots, N$
    \item $TransactionRate$: Transaction cost rate per share sold (constant)
    \item $TaxRate$: Capital gains tax rate on the profit from selling shares (constant)
    \item $K$: Amount of money the investor needs to raise (constant)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Number of shares $i$ sold, for $i = 1, 2, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Maximize the expected value of the investor's portfolio next year:
\[
\text{Maximize} \quad \sum_{i=1}^{N} (Bought_i - x_i) \cdot FuturePrice_i
\]

\subsection*{Constraints}
\begin{align}
    & x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, N \quad \text{(Non-negativity constraint)} \\
    & x_i \leq Bought_i \quad \text{for } i = 1, 2, \ldots, N \quad \text{(Cannot sell more than bought)} \\
    & \sum_{i=1}^{N} \left[ x_i \cdot CurrentPrice_i - x_i \cdot (CurrentPrice_i - BuyPrice_i) \cdot TaxRate - x_i \cdot CurrentPrice_i \cdot TransactionRate \right] \geq K \quad \text{(Amount raised constraint)}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0 / 100,  #### Convert percentage to a rate
    'TaxRate': 15.0 / 100,         #### Convert percentage to a rate
    'K': 5000
}

#### Problem definition
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x{i}", lowBound=0, upBound=data['Bought'][i]) for i in range(data['N'])]

#### Objective function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))

#### Constraints
#### Amount raised constraint
problem += pulp.lpSum(
    x[i] * data['CurrentPrice'][i] - 
    x[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] - 
    x[i] * data['CurrentPrice'][i] * data['TransactionRate'] 
    for i in range(data['N'])
) >= data['K']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```


