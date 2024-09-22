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
To model the problem as a Linear Programming (LP) problem in LaTeX, we'll set up the objective function and the constraints. The objective is to maximize the total profit, which is the difference between the revenue from selling the products and the costs of producing them, subject to raw material constraints and demand constraints.

Here is the LaTeX code for this LP problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports Production}

\subsection*{Decision Variables}
Let \( x_j \) be the number of units of product \( j \) to produce, for \( j = 1, 2, \ldots, M \).

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{j=1}^{M} ( \text{price}_j \cdot x_j - \text{cost}_j \cdot x_j )
\]

which simplifies to:

\[
Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \cdot x_j
\]

\subsection*{Constraints}

1. \textbf{Raw Material Constraints:}

For each raw material \( i = 1, 2, \ldots, N \), the consumption should not exceed availability:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i \quad \text{for } i = 1, 2, \ldots, N
\]

2. \textbf{Demand Constraints:}

For each product \( j = 1, 2, \ldots, M \), the production should not exceed demand:

\[
x_j \leq \text{demand}_j \quad \text{for } j = 1, 2, \ldots, M
\]

3. \textbf{Non-negativity Constraints:}

\[
x_j \geq 0 \quad \text{for } j = 1, 2, \ldots, M
\]

\end{document}
```

This model defines the decision variables, objective function, and constraints necessary to solve the problem using linear programming techniques. You can use this LaTeX code to format the model in a professional manner.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports Production}

\subsection*{Decision Variables}
Let \( x_j \) be the number of units of product \( j \) to produce, for \( j = 1, 2, \ldots, M \).

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{j=1}^{M} ( \text{price}_j \cdot x_j - \text{cost}_j \cdot x_j )
\]

which simplifies to:

\[
Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \cdot x_j
\]

\subsection*{Constraints}

1. \textbf{Raw Material Constraints:}

For each raw material \( i = 1, 2, \ldots, N \), the consumption should not exceed availability:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i \quad \text{for } i = 1, 2, \ldots, N
\]

2. \textbf{Demand Constraints:}

For each product \( j = 1, 2, \ldots, M \), the production should not exceed demand:

\[
x_j \leq \text{demand}_j \quad \text{for } j = 1, 2, \ldots, M
\]

3. \textbf{Non-negativity Constraints:}

\[
x_j \geq 0 \quad \text{for } j = 1, 2, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Model Initialization
problem = pulp.LpProblem("WildSportsProduction", pulp.LpMaximize)

#### Decision Variables
M = len(data['prices'])
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

#### Objective Function
profit_per_unit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit_per_unit[j] * x[j] for j in range(M)), "Total_Profit"

#### Constraints
#### Raw Material Constraints
for i in range(len(data['available'])):
    problem += (pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]), f"Raw_Material_Constraint_{i+1}"

#### Demand Constraints
for j in range(M):
    problem += (x[j] <= data['demands'][j]), f"Demand_Constraint_{j+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

