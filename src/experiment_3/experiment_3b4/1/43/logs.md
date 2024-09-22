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
To solve the problem of maximizing the profit of Wild Sports by determining how many units of each product to produce, we can formulate it as a Linear Programming problem. The objective is to maximize the total profit, which is the sum of the profits for each product. The constraints include the availability of raw materials and the maximum forecasted demand for each product.

Below is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}

\begin{itemize}
    \item $N$: Number of raw materials
    \item $M$: Number of products
    \item $available_i$: Amount of raw material $i$ available, $i \in \{1, 2, \ldots, N\}$
    \item $req_{i,j}$: Units of raw material $i$ required per unit of product $j$, $i \in \{1, 2, \ldots, N\}$ and $j \in \{1, 2, \ldots, M\}$
    \item $price_j$: Selling price per unit of product $j$, $j \in \{1, 2, \ldots, M\}$
    \item $cost_j$: Production cost per unit of product $j$, $j \in \{1, 2, \ldots, M\}$
    \item $demand_j$: Maximum forecasted demand for product $j$, $j \in \{1, 2, \ldots, M\}$
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $amount_j$: Number of units of product $j$ to produce, $j \in \{1, 2, \ldots, M\}$
\end{itemize}

\subsection*{Objective Function}

Maximize the total profit:

\[
\max \sum_{j=1}^{M} \left((price_j - cost_j) \cdot amount_j \right)
\]

\subsection*{Constraints}

1. Raw material constraints for each raw material $i$:
   \[
   \sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i \quad \forall i \in \{1, 2, \ldots, N\}
   \]

2. Demand constraints for each product $j$:
   \[
   amount_j \leq demand_j \quad \forall j \in \{1, 2, \ldots, M\}
   \]

3. Non-negativity constraints:
   \[
   amount_j \geq 0 \quad \forall j \in \{1, 2, \ldots, M\}
   \]

\end{document}
```

This model includes decision variables for the number of each product to produce, an objective function to maximize the profit, and constraints to ensure that the raw material usage does not exceed availability and that the production does not exceed demand. The constraints also enforce the non-negativity of the production amounts.

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

\subsection*{Parameters}

\begin{itemize}
    \item $N$: Number of raw materials
    \item $M$: Number of products
    \item $available_i$: Amount of raw material $i$ available, $i \in \{1, 2, \ldots, N\}$
    \item $req_{i,j}$: Units of raw material $i$ required per unit of product $j$, $i \in \{1, 2, \ldots, N\}$ and $j \in \{1, 2, \ldots, M\}$
    \item $price_j$: Selling price per unit of product $j$, $j \in \{1, 2, \ldots, M\}$
    \item $cost_j$: Production cost per unit of product $j$, $j \in \{1, 2, \ldots, M\}$
    \item $demand_j$: Maximum forecasted demand for product $j$, $j \in \{1, 2, \ldots, M\}$
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $amount_j$: Number of units of product $j$ to produce, $j \in \{1, 2, \ldots, M\}$
\end{itemize}

\subsection*{Objective Function}

Maximize the total profit:

\[
\max \sum_{j=1}^{M} \left((price_j - cost_j) \cdot amount_j \right)
\]

\subsection*{Constraints}

1. Raw material constraints for each raw material $i$:
   \[
   \sum_{j=1}^{M} req_{i,j} \cdot amount_j \leq available_i \quad \forall i \in \{1, 2, \ldots, N\}
   \]

2. Demand constraints for each product $j$:
   \[
   amount_j \leq demand_j \quad \forall j \in \{1, 2, \ldots, M\}
   \]

3. Non-negativity constraints:
   \[
   amount_j \geq 0 \quad \forall j \in \{1, 2, \ldots, M\}
   \]

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
available = [240000, 8000, 75000]
requirements = [[48, 1, 10], [40, 1, 10], [0, 1, 2]]
prices = [40, 38, 9]
costs = [30, 26, 7]
demands = [10000, 2000, 10000]

#### Number of products
M = len(prices)
#### Number of raw materials
N = len(available)

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)]

#### Objective Function
profit_contrib = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum(profit_contrib[j] * amount[j] for j in range(M))

#### Constraints

#### Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amount[j] for j in range(M)) <= available[i]

#### Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

