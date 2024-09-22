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

\textbf{Variables:}
Let \( x_j \) be the amount of product \( j \) produced, where \( j = 1, \ldots, M \).

\textbf{Objective Function:}
We want to maximize the total profit, which can be expressed as:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (price_j - cost_j) \cdot x_j
\]

\textbf{Constraints:}

1. **Raw Material Constraints:**
For each raw material \( i \) (where \( i = 1, \ldots, N \)):
\[
\sum_{j=1}^{M} req_{i,j} \cdot x_j \leq available_i
\]
   
2. **Demand Constraints:**
For each product \( j \):
\[
0 \leq x_j \leq demand_j
\]

3. **Non-negativity Constraints:**
\[
x_j \geq 0 \quad \forall j = 1, \ldots, M
\]

\textbf{Model Summary:}

The complete linear programming model can be summarized as follows:

\[
\begin{aligned}
\text{Maximize } & Z = \sum_{j=1}^{M} (price_j - cost_j) \cdot x_j \\
\text{subject to } & \sum_{j=1}^{M} req_{i,j} \cdot x_j \leq available_i, \quad \forall i = 1, \ldots, N \\
& 0 \leq x_j \leq demand_j, \quad \forall j = 1, \ldots, M \\
& x_j \geq 0, \quad \forall j = 1, \ldots, M
\end{aligned}
\]

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

\textbf{Variables:}
Let \( x_j \) be the amount of product \( j \) produced, where \( j = 1, \ldots, M \).

\textbf{Objective Function:}
We want to maximize the total profit, which can be expressed as:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (price_j - cost_j) \cdot x_j
\]

\textbf{Constraints:}

1. **Raw Material Constraints:**
For each raw material \( i \) (where \( i = 1, \ldots, N \)):
\[
\sum_{j=1}^{M} req_{i,j} \cdot x_j \leq available_i
\]
   
2. **Demand Constraints:**
For each product \( j \):
\[
0 \leq x_j \leq demand_j
\]

3. **Non-negativity Constraints:**
\[
x_j \geq 0 \quad \forall j = 1, \ldots, M
\]

\textbf{Model Summary:}

The complete linear programming model can be summarized as follows:

\[
\begin{aligned}
\text{Maximize } & Z = \sum_{j=1}^{M} (price_j - cost_j) \cdot x_j \\
\text{subject to } & \sum_{j=1}^{M} req_{i,j} \cdot x_j \leq available_i, \quad \forall i = 1, \ldots, N \\
& 0 \leq x_j \leq demand_j, \quad \forall j = 1, \ldots, M \\
& x_j \geq 0, \quad \forall j = 1, \ldots, M
\end{aligned}
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

#### Number of products and raw materials
M = len(data['prices'])
N = len(data['available'])

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("Production", range(M), lowBound=0)

#### Objective function
profit_per_unit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit_per_unit[j] * x[j] for j in range(M)), "Total_Profit"

#### Constraints for raw materials
for i in range(N):
    problem += (
        pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i], 
        f"RawMaterialConstraint_{i}"
    )

#### Demand constraints
for j in range(M):
    problem += (x[j] <= data['demands'][j], f"DemandConstraint_{j}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

