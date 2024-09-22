# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- Wild Sports produces \var{M} different products using \var{N} different raw materials.
- The company has \var{available_{i}} of raw material \var{i} available.
- Product \var{j} requires \var{req_{i,j}} units of material \var{i} per unit produced.
- Product \var{j} has a selling price of \var{price_j} per unit.
- Product \var{j} has a production cost of \var{cost_j} per unit produced.
- Product \var{j} has a forecasted maximum demand of \var{demand_j} for the month.

INPUT FORMAT: 

{
    "available": [available_{i} for i in 1, ..., N],
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M],
    "costs": [cost_{j} for j in 1, ..., M],
    "demands": [demand_{j} for j in 1, ..., M]
}

OBJECTIVE: How many of each product should the sports produce in order to maximize its profit for the month?

OUTPUT INFO:

- the amount of each product produced \var{amount_{j}}.
- \var{total_profit} shows the total profit of the company for the month.

OUTPUT FORMAT:

{
    "amount": [amount_{j} for j in 1, ..., M],
    "total_profit": total_profit
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( M \) be the number of different products.
    \item Let \( N \) be the number of different raw materials.
    \item Let \( \text{available}_{i} \) be the available quantity of raw material \( i \) for \( i = 1, \ldots, N \).
    \item Let \( \text{req}_{i,j} \) be the requirement of raw material \( i \) to produce one unit of product \( j \) for \( j = 1, \ldots, M \).
    \item Let \( \text{price}_{j} \) be the selling price per unit of product \( j \).
    \item Let \( \text{cost}_{j} \) be the production cost per unit of product \( j \).
    \item Let \( \text{demand}_{j} \) be the forecasted maximum demand for product \( j \).
\end{itemize}

\subsection*{Decision Variables}
Let \( x_j \) be the amount of product \( j \) produced, where \( j = 1, \ldots, M \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{j=1}^{M} ( \text{price}_{j} - \text{cost}_{j} ) x_j
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Raw Material Constraints:} 
    \[
    \sum_{j=1}^{M} \text{req}_{i,j} x_j \leq \text{available}_{i} \quad \text{for } i = 1, \ldots, N
    \]

    \item \textbf{Demand Constraints:} 
    \[
    x_j \leq \text{demand}_{j} \quad \text{for } j = 1, \ldots, M
    \]

    \item \textbf{Non-negativity Constraints:} 
    \[
    x_j \geq 0 \quad \text{for } j = 1, \ldots, M
    \]
\end{itemize}

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item The amount of each product produced \( x_j \).
    \item The total profit calculated from the objective function.
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

\section*{Linear Programming Model for Wild Sports}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( M \) be the number of different products.
    \item Let \( N \) be the number of different raw materials.
    \item Let \( \text{available}_{i} \) be the available quantity of raw material \( i \) for \( i = 1, \ldots, N \).
    \item Let \( \text{req}_{i,j} \) be the requirement of raw material \( i \) to produce one unit of product \( j \) for \( j = 1, \ldots, M \).
    \item Let \( \text{price}_{j} \) be the selling price per unit of product \( j \).
    \item Let \( \text{cost}_{j} \) be the production cost per unit of product \( j \).
    \item Let \( \text{demand}_{j} \) be the forecasted maximum demand for product \( j \).
\end{itemize}

\subsection*{Decision Variables}
Let \( x_j \) be the amount of product \( j \) produced, where \( j = 1, \ldots, M \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{j=1}^{M} ( \text{price}_{j} - \text{cost}_{j} ) x_j
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Raw Material Constraints:} 
    \[
    \sum_{j=1}^{M} \text{req}_{i,j} x_j \leq \text{available}_{i} \quad \text{for } i = 1, \ldots, N
    \]

    \item \textbf{Demand Constraints:} 
    \[
    x_j \leq \text{demand}_{j} \quad \text{for } j = 1, \ldots, M
    \]

    \item \textbf{Non-negativity Constraints:} 
    \[
    x_j \geq 0 \quad \text{for } j = 1, \ldots, M
    \]
\end{itemize}

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item The amount of each product produced \( x_j \).
    \item The total profit calculated from the objective function.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Number of products (M) and number of raw materials (N)
M = len(data['prices'])
N = len(data['available'])

#### Problem
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0) for j in range(M)]

#### Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * x[j] for j in range(M))
problem += profit

#### Raw material constraints
for i in range(N):
    problem += (
        pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i],
        f"Raw_Material_Constraint_{i}"
    )

#### Demand constraints
for j in range(M):
    problem += (
        x[j] <= data['demands'][j],
        f"Demand_Constraint_{j}"
    )

#### Solve the problem
problem.solve()

#### Output
product_amounts = {f'x_{j}': pulp.value(x[j]) for j in range(M)}
total_profit = pulp.value(problem.objective)

print("Amount of each product produced:")
for j in range(M):
    print(f"Product {j+1}: {product_amounts[f'x_{j}']}")

print(f"(Objective Value): <OBJ>{total_profit}</OBJ>")
```

