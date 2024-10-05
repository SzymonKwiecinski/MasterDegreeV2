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
To model the given problem as a linear programming problem, we need to define an objective function and a set of constraints. The objective is to maximize the total profit, which is the difference between the total sales revenue and the total production cost.

Let's define the decision variables:
- \( x_j \): Number of units of product \( j \) to be produced for \( j = 1, \ldots, M \).

Objective function:
- Maximize total profit: 
  \[
  \text{Total Profit} = \sum_{j=1}^{M} (price_j \times x_j - cost_j \times x_j)
  \]
  Simplified to:
  \[
  \text{Maximize} \quad \sum_{j=1}^{M} (price_j - cost_j) \times x_j
  \]

Constraints:
1. Raw material constraints:
   \[
   \sum_{j=1}^{M} req_{i,j} \times x_j \leq available_i \quad \text{for } i = 1, \ldots, N
   \]
2. Demand constraints:
   \[
   x_j \leq demand_j \quad \text{for } j = 1, \ldots, M
   \]
3. Non-negativity constraints:
   \[
   x_j \geq 0 \quad \text{for } j = 1, \ldots, M
   \]

Let's write the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Maximize} \quad \sum_{j=1}^{M} (price_j - cost_j) \times x_j
\]

\textbf{Subject to:}
\begin{align*}
& \sum_{j=1}^{M} req_{i,j} \times x_j \leq available_i, \quad \text{for } i = 1, \ldots, N \\
& x_j \leq demand_j, \quad \text{for } j = 1, \ldots, M \\
& x_j \geq 0, \quad \text{for } j = 1, \ldots, M
\end{align*}

\end{document}
```

This model will help Wild Sports determine the optimal number of units to produce for each product to maximize profit while not exceeding material availability and meeting the forecasted demand.

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
\text{Maximize} \quad \sum_{j=1}^{M} (price_j - cost_j) \times x_j
\]

\textbf{Subject to:}
\begin{align*}
& \sum_{j=1}^{M} req_{i,j} \times x_j \leq available_i, \quad \text{for } i = 1, \ldots, N \\
& x_j \leq demand_j, \quad \text{for } j = 1, \ldots, M \\
& x_j \geq 0, \quad \text{for } j = 1, \ldots, M
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}')

#### Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  #### Number of products
N = len(available)  #### Number of resources

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

#### Objective function
problem += pulp.lpSum([(prices[j] - costs[j]) * x[j] for j in range(M)]), "Total_Profit"

#### Constraints
#### Resource constraints
for i in range(N):
    problem += (pulp.lpSum([requirements[i][j] * x[j] for j in range(M)]) <= available[i]), f"Resource_Constraint_{i+1}"

#### Demand constraints
for j in range(M):
    problem += (x[j] <= demands[j]), f"Demand_Constraint_{j+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

