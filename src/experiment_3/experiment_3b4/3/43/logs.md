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
To address the problem using Linear Programming, we need to formulate a mathematical model. The goal is to maximize the total profit given the constraints on raw materials and demand.

Let's define:
- \( x_j \): the number of units of product \( j \) to be produced, for \( j = 1, \ldots, M \).

**Objective Function:**
Maximize the total profit, which is defined as the difference between total sales revenue and total production cost. The objective function can be written as:

\[
\text{Maximize } Z = \sum_{j=1}^{M} ( \text{price}_j \times x_j - \text{cost}_j \times x_j )
\]

Alternatively, simplify to:

\[
\text{Maximize } Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \times x_j
\]

**Constraints:**

1. Raw material constraints: For each raw material \( i \), the total units used by all products should not exceed the available units.
   \[
   \sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i, \quad \text{for } i = 1, \ldots, N
   \]

2. Demand constraints: The production of each product should not exceed its demand.
   \[
   x_j \leq \text{demand}_j, \quad \text{for } j = 1, \ldots, M
   \]

3. Non-negativity constraints:
   \[
   x_j \geq 0, \quad \text{for } j = 1, \ldots, M
   \]

Below is the mathematical model formulated in \(\LaTeX\):

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \times x_j
\]

\subsection*{Constraints}
1. Raw Material Constraints:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i, \quad \text{for } i = 1, \ldots, N
\]

2. Demand Constraints:
\[
x_j \leq \text{demand}_j, \quad \text{for } j = 1, \ldots, M
\]

3. Non-negativity Constraints:
\[
x_j \geq 0, \quad \text{for } j = 1, \ldots, M
\]

\end{document}
```

This setup provides a comprehensive mathematical model for solving the given problem using Linear Programming techniques. By solving this model, you can determine the optimal number of each product to produce to maximize the profit while respecting the constraints.

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

\subsection*{Objective}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \times x_j
\]

\subsection*{Constraints}
1. Raw Material Constraints:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i, \quad \text{for } i = 1, \ldots, N
\]

2. Demand Constraints:
\[
x_j \leq \text{demand}_j, \quad \text{for } j = 1, \ldots, M
\]

3. Non-negativity Constraints:
\[
x_j \geq 0, \quad \text{for } j = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']
M = len(prices)
N = len(available)

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

#### Objective function
profit = [(prices[j] - costs[j]) * x[j] for j in range(M)]
problem += pulp.lpSum(profit), "Total_Profit"

#### Raw Material Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i}"

#### Demand Constraints
for j in range(M):
    problem += x[j] <= demands[j], f"Demand_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

