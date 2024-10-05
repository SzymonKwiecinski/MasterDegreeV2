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
To solve this linear programming problem, we'll define the decision variables, constraints, and objective function in a mathematical model using LaTeX. 

Let's denote:
- \( x_j \) as the number of units of product \( j \) to be produced.

Here's the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\[
x_j \geq 0 \quad \text{for } j = 1, 2, \ldots, M
\]

\textbf{Objective Function:}

Maximize the profit, which is calculated as the total revenue minus the total production cost:

\[
\text{Maximize } Z = \sum_{j=1}^{M} (price_j - cost_j) \cdot x_j
\]

\textbf{Constraints:}

1. Raw Material Constraints: The total amount of each raw material used cannot exceed the available amount.

\[
\sum_{j=1}^{M} req_{i,j} \cdot x_j \leq available_i \quad \text{for } i = 1, 2, \ldots, N
\]

2. Demand Constraints: The production of each product cannot exceed its forecasted maximum demand.

\[
x_j \leq demand_j \quad \text{for } j = 1, 2, \ldots, M
\]

3. Non-negativity Constraints:

\[
x_j \geq 0 \quad \text{for } j = 1, 2, \ldots, M
\]

\end{document}
```

This LaTeX code represents our linear programming model for the problem. The objective function aims to maximize the company's profit by choosing the optimal number of each product to produce, considering the constraints on raw material availability and forecasted demand for each product.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}
\[
x_j \geq 0 \quad \text{for } j = 1, 2, \ldots, M
\]

\textbf{Objective Function:}

Maximize the profit, which is calculated as the total revenue minus the total production cost:

\[
\text{Maximize } Z = \sum_{j=1}^{M} (price_j - cost_j) \cdot x_j
\]

\textbf{Constraints:}

1. Raw Material Constraints: The total amount of each raw material used cannot exceed the available amount.

\[
\sum_{j=1}^{M} req_{i,j} \cdot x_j \leq available_i \quad \text{for } i = 1, 2, \ldots, N
\]

2. Demand Constraints: The production of each product cannot exceed its forecasted maximum demand.

\[
x_j \leq demand_j \quad \text{for } j = 1, 2, \ldots, M
\]

3. Non-negativity Constraints:

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

#### Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [
        [48, 1, 10],
        [40, 1, 10],
        [0, 1, 2]
    ],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Extracting data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

#### Number of products
M = len(prices)
#### Number of raw materials
N = len(available)

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x_vars = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

#### Objective Function
profit = pulp.lpSum((prices[j] - costs[j]) * x_vars[j] for j in range(M))
problem += profit

#### Raw Material Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x_vars[j] for j in range(M)) <= available[i]

#### Demand Constraints
for j in range(M):
    problem += x_vars[j] <= demands[j]

#### Solve
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

