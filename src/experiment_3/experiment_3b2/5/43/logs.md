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
To solve this problem, we need to formulate a linear programming (LP) model to maximize the profit for Wild Sports. The decision variables, objective function, and constraints can be defined as follows:

**Decision Variables:**
- Let \( x_j \) be the number of units of product \( j \) to be produced, for \( j = 1, \ldots, M \).

**Objective Function:**
- We aim to maximize the total profit, which is the revenue from sales minus the production costs. The objective function can be written as:
  
  \[
  \text{Maximize} \quad Z = \sum_{j=1}^{M} ( \text{price}_j \cdot x_j - \text{cost}_j \cdot x_j )
  \]

  Simplified further, the profit is:
  
  \[
  Z = \sum_{j=1}^{M} ( (\text{price}_j - \text{cost}_j) \cdot x_j )
  \]

**Constraints:**
1. **Raw Material Constraints:**
   - For each raw material \( i \), the sum of materials used by all products cannot exceed the available amount:
   
   \[
   \sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
   \]

2. **Demand Constraints:**
   - The production of each product cannot exceed its forecasted maximum demand:
   
   \[
   x_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M
   \]

3. **Non-negativity Constraints:**
   - The number of units produced must be non-negative:
   
   \[
   x_j \geq 0, \quad \forall j = 1, \ldots, M
   \]

Here is the corresponding LaTeX code for the LP model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports}

\subsection*{Objective Function}
Maximize:
\[
Z = \sum_{j=1}^{M} ((\text{price}_j - \text{cost}_j) \cdot x_j)
\]

\subsection*{Constraints}
\begin{align*}
\text{1. Raw Material Constraints:} & \\
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j & \leq \text{available}_i, \quad \forall i = 1, \ldots, N \\

\text{2. Demand Constraints:} & \\
x_j & \leq \text{demand}_j, \quad \forall j = 1, \ldots, M \\

\text{3. Non-negativity Constraints:} & \\
x_j & \geq 0, \quad \forall j = 1, \ldots, M
\end{align*}

\end{document}
```

This LP model aims to find the optimal production levels \( x_j \) for each product \( j \) that maximizes Wild Sports' total profit while not exceeding raw material availability or forecasted demand.

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

\subsection*{Objective Function}
Maximize:
\[
Z = \sum_{j=1}^{M} ((\text{price}_j - \text{cost}_j) \cdot x_j)
\]

\subsection*{Constraints}
\begin{align*}
\text{1. Raw Material Constraints:} & \\
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j & \leq \text{available}_i, \quad \forall i = 1, \ldots, N \\

\text{2. Demand Constraints:} & \\
x_j & \leq \text{demand}_j, \quad \forall j = 1, \ldots, M \\

\text{3. Non-negativity Constraints:} & \\
x_j & \geq 0, \quad \forall j = 1, \ldots, M
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Define the problem
problem = pulp.LpProblem("Wild_Sports_Optimization", pulp.LpMaximize)

#### Number of products and resources
M = len(data['prices'])
N = len(data['available'])

#### Decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

#### Objective Function
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum([profit[j] * x[j] for j in range(M)]), "Total_Profit"

#### Constraints
#### Raw Material Constraints
for i in range(N):
    problem += pulp.lpSum([data['requirements'][i][j] * x[j] for j in range(M)]) <= data['available'][i], f"Raw_Material_Constraint_{i}"

#### Demand Constraints
for j in range(M):
    problem += x[j] <= data['demands'][j], f"Demand_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

