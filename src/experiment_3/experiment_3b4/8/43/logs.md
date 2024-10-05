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
To create a mathematical model for the given problem in LATEX format, we'll represent it as a linear programming (LP) problem. The goal is to maximize the profit by determining the number of each product to produce, given resource constraints and market demand.

Here's how you can formulate the problem in LATEX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports}

\subsection*{Parameters}
Let:
\begin{itemize}
    \item $N$ be the number of raw materials.
    \item $M$ be the number of products.
    \item $available_i$ be the availability of raw material $i$, for $i = 1, \ldots, N$.
    \item $req_{i,j}$ be the units of raw material $i$ required to produce one unit of product $j$, for $i = 1, \ldots, N$ and $j = 1, \ldots, M$.
    \item $price_j$ be the selling price per unit of product $j$.
    \item $cost_j$ be the production cost per unit of product $j$.
    \item $demand_j$ be the forecasted maximum demand for product $j$.
\end{itemize}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item $amount_j$ be the amount of product $j$ produced, for $j = 1, \ldots, M$.
\end{itemize}

\subsection*{Objective Function}
Maximize the profit, which is the total revenue minus the total production cost:
\[
\text{Maximize } \quad \sum_{j=1}^{M} (price_j - cost_j) \cdot amount_j
\]

\subsection*{Constraints}
\begin{itemize}
    \item Raw Material Constraints: For each raw material $i$,
    \[
    \sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i, \quad \text{for } i = 1, \ldots, N
    \]
    \item Demand Constraints: For each product $j$,
    \[
    amount_j \leq demand_j, \quad \text{for } j = 1, \ldots, M
    \]
    \item Non-negativity Constraints:
    \[
    amount_j \geq 0, \quad \text{for } j = 1, \ldots, M
    \]
\end{itemize}

\end{document}
```

This LATEX file sets up the LP problem with parameters, decision variables, objective function, and constraints clearly defined. You can compile this LATEX document to generate a formatted representation of the LP problem.

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
Let:
\begin{itemize}
    \item $N$ be the number of raw materials.
    \item $M$ be the number of products.
    \item $available_i$ be the availability of raw material $i$, for $i = 1, \ldots, N$.
    \item $req_{i,j}$ be the units of raw material $i$ required to produce one unit of product $j$, for $i = 1, \ldots, N$ and $j = 1, \ldots, M$.
    \item $price_j$ be the selling price per unit of product $j$.
    \item $cost_j$ be the production cost per unit of product $j$.
    \item $demand_j$ be the forecasted maximum demand for product $j$.
\end{itemize}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item $amount_j$ be the amount of product $j$ produced, for $j = 1, \ldots, M$.
\end{itemize}

\subsection*{Objective Function}
Maximize the profit, which is the total revenue minus the total production cost:
\[
\text{Maximize } \quad \sum_{j=1}^{M} (price_j - cost_j) \cdot amount_j
\]

\subsection*{Constraints}
\begin{itemize}
    \item Raw Material Constraints: For each raw material $i$,
    \[
    \sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i, \quad \text{for } i = 1, \ldots, N
    \]
    \item Demand Constraints: For each product $j$,
    \[
    amount_j \leq demand_j, \quad \text{for } j = 1, \ldots, M
    \]
    \item Non-negativity Constraints:
    \[
    amount_j \geq 0, \quad \text{for } j = 1, \ldots, M
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Number of raw materials and products
N = len(data['available'])
M = len(data['prices'])

#### LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
amount = {j: pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)}

#### Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * amount[j] for j in range(M))
problem += profit

#### Constraints
#### Raw material constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * amount[j] for j in range(M)) <= data['available'][i]

#### Demand constraints
for j in range(M):
    problem += amount[j] <= data['demands'][j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

