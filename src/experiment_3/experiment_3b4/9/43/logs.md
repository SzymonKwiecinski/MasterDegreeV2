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
To solve this linear programming problem, we will model the situation where Wild Sports wants to maximize its profit given the constraints of available raw materials and the maximum demand for each product. 

We define the decision variables as follows:
- Let \( x_j \) be the number of units of product \( j \) to produce.

The objective function is to maximize the total profit, which is the total revenue minus the total production costs:
- Total Revenue: \(\sum_{j=1}^{M} \text{price}_j \times x_j\)
- Total Cost: \(\sum_{j=1}^{M} \text{cost}_j \times x_j\)

Thus, the objective function is:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \times x_j
\]

The constraints are:
1. Raw material constraints: For each raw material \( i \), the total usage across all products should not exceed the available quantity:
   \[
   \sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i \quad \text{for each } i = 1, \ldots, N
   \]

2. Demand constraints: The production of each product \( j \) should not exceed its forecasted demand:
   \[
   x_j \leq \text{demand}_j \quad \text{for each } j = 1, \ldots, M
   \]

3. Non-negativity constraints: 
   \[
   x_j \geq 0 \quad \text{for each } j = 1, \ldots, M
   \]

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize profit

\[
Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \times x_j
\]

\textbf{Subject to:}

\[
\sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i \quad \text{for each } i = 1, \ldots, N
\]

\[
x_j \leq \text{demand}_j \quad \text{for each } j = 1, \ldots, M
\]

\[
x_j \geq 0 \quad \text{for each } j = 1, \ldots, M
\]

\end{document}
```

With this mathematical model, you can use linear programming software or solvers to determine the optimal values for \( x_j \), which represent the number of units of each product to produce in order to maximize the profit while satisfying all constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize profit

\[
Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \times x_j
\]

\textbf{Subject to:}

\[
\sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i \quad \text{for each } i = 1, \ldots, N
\]

\[
x_j \leq \text{demand}_j \quad \text{for each } j = 1, \ldots, M
\]

\[
x_j \geq 0 \quad \text{for each } j = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the problem
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Number of products
M = len(data['prices'])

#### Number of resources
N = len(data['available'])

#### Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective function
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M))

#### Constraints
#### Resource constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]

#### Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

