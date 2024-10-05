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
To address the given linear programming problem for Wild Sports, we need to maximize the profit by determining how many of each product should be produced, considering the constraints on raw material availability, production costs, and demand limitations. The problem can be formulated as follows:

Let:
- \( x_j \) represent the number of units of product \( j \) produced.

Objective Function:
- Maximize the total profit, which is the total revenue minus total cost:
\[ \text{Profit} = \sum_{j=1}^{M} ( \text{price}_j - \text{cost}_j ) \times x_j \]

Subject to:
- Material availability constraints:
\[ \sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N \]
- Demand constraints:
\[ x_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M \]
- Non-negativity constraints:
\[ x_j \geq 0, \quad \forall j = 1, \ldots, M \]

Here is the complete mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Maximize} \quad \text{Profit} = \sum_{j=1}^{M} ( \text{price}_j - \text{cost}_j ) \times x_j
\]

\textbf{Subject to:}

Material availability constraints:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
\]

Demand constraints:
\[
x_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M
\]

Non-negativity constraints:
\[
x_j \geq 0, \quad \forall j = 1, \ldots, M
\]

\end{document}
```

This model will allow you to determine the optimal production levels of each product that maximizes profit while respecting raw material limits and demand constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Maximize} \quad \text{Profit} = \sum_{j=1}^{M} ( \text{price}_j - \text{cost}_j ) \times x_j
\]

\textbf{Subject to:}

Material availability constraints:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
\]

Demand constraints:
\[
x_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M
\]

Non-negativity constraints:
\[
x_j \geq 0, \quad \forall j = 1, \ldots, M
\]

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

#### Number of products
M = len(data['prices'])

#### Number of materials
N = len(data['available'])

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

#### Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * x[j] for j in range(M))
problem += profit

#### Material availability constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]

#### Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

