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
To model the given problem as a linear program in LaTeX, we need to define decision variables, the objective function, and the constraints. 

Let's denote the decision variables as \( x_j \), representing the quantity of product \( j \) to be produced. The objective is to maximize the total profit, which is the difference between the total revenue and the total production cost.

Here is the LP model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports}

\subsection*{Decision Variables}
Let \( x_j \) be the number of units to produce for product \( j \).

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Profit} = \sum_{j=1}^{M} ( \text{price}_j \times x_j - \text{cost}_j \times x_j )
\]

which simplifies to:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} ( \text{price}_j - \text{cost}_j ) \times x_j
\]

\subsection*{Constraints}

1. Raw Material Availability:
   \[
   \sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i, \quad \text{for each raw material } i = 1, \dots, N
   \]

2. Demand Constraints:
   \[
   x_j \leq \text{demand}_j, \quad \text{for each product } j = 1, \dots, M
   \]

3. Non-negativity:
   \[
   x_j \geq 0, \quad \text{for each product } j = 1, \dots, M
   \]

\end{document}
```

In this model, the objective function seeks to maximize the profit, which is calculated as the sum of the revenue from each product minus the cost of producing each product. The constraints ensure that the use of raw materials does not exceed available amounts and that the production of each product does not exceed its forecasted demand. Additionally, all \( x_j \) are constrained to be non-negative, as negative production doesn't make sense in this context.

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

\subsection*{Decision Variables}
Let \( x_j \) be the number of units to produce for product \( j \).

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Profit} = \sum_{j=1}^{M} ( \text{price}_j \times x_j - \text{cost}_j \times x_j )
\]

which simplifies to:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} ( \text{price}_j - \text{cost}_j ) \times x_j
\]

\subsection*{Constraints}

1. Raw Material Availability:
   \[
   \sum_{j=1}^{M} \text{req}_{i,j} \times x_j \leq \text{available}_i, \quad \text{for each raw material } i = 1, \dots, N
   \]

2. Demand Constraints:
   \[
   x_j \leq \text{demand}_j, \quad \text{for each product } j = 1, \dots, M
   \]

3. Non-negativity:
   \[
   x_j \geq 0, \quad \text{for each product } j = 1, \dots, M
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

#### Define the problem
problem = pulp.LpProblem("Wild_Sports_Optimization", pulp.LpMaximize)

#### Define decision variables
M = len(data['prices'])
x = pulp.LpVariable.dicts("Units_Produced", range(M), lowBound=0)

#### Objective function
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M))

#### Constraints
N = len(data['available'])
#### Raw Material Availability Constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][j][i] * x[j] for j in range(M)) <= data['available'][i]

#### Demand Constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

