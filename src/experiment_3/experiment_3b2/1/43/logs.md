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
To model this problem as a linear programming (LP) problem, we need to define our decision variables, objective function, and constraints. We'll determine how many units of each product to produce to maximize total profit subject to raw material and demand constraints.

Let's define the decision variables:
- \( x_j \): Number of units of product \( j \) to be produced, for \( j = 1, \ldots, M \).

The objective function, which is to maximize profit, is given by:
\[
\text{Profit} = \sum_{j=1}^{M} (price_j - cost_j) \times x_j
\]

The constraints are:
1. Raw materials constraints:
   \[
   \sum_{j=1}^{M} req_{i,j} \times x_j \leq available_i, \quad \text{for each } i = 1, \ldots, N
   \]
2. Demand constraints:
   \[
   x_j \leq demand_j, \quad \text{for each } j = 1, \ldots, M
   \]
3. Non-negativity constraints:
   \[
   x_j \geq 0, \quad \text{for each } j = 1, \ldots, M
   \]

Here's the LaTeX code for the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Wild Sports Production}

\subsection*{Decision Variables}

Let \( x_j \) be the number of units of product \( j \) to be produced, where \( j = 1, \ldots, M \).

\subsection*{Objective Function}

Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} (price_j - cost_j) \times x_j
\]

\subsection*{Constraints}

\begin{enumerate}
    \item Raw materials constraints:
    \[
    \sum_{j=1}^{M} req_{i,j} \times x_j \leq available_i, \quad \text{for each } i = 1, \ldots, N
    \]
    
    \item Demand constraints:
    \[
    x_j \leq demand_j, \quad \text{for each } j = 1, \ldots, M
    \]
    
    \item Non-negativity constraints:
    \[
    x_j \geq 0, \quad \text{for each } j = 1, \ldots, M
    \]
\end{enumerate}

\end{document}
```

This linear programming model can be solved using optimization software to determine the optimal production quantities for each product that maximizes the company's profit, given the constraints on raw materials and market demand.

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

Let \( x_j \) be the number of units of product \( j \) to be produced, where \( j = 1, \ldots, M \).

\subsection*{Objective Function}

Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} (price_j - cost_j) \times x_j
\]

\subsection*{Constraints}

\begin{enumerate}
    \item Raw materials constraints:
    \[
    \sum_{j=1}^{M} req_{i,j} \times x_j \leq available_i, \quad \text{for each } i = 1, \ldots, N
    \]
    
    \item Demand constraints:
    \[
    x_j \leq demand_j, \quad \text{for each } j = 1, \ldots, M
    \]
    
    \item Non-negativity constraints:
    \[
    x_j \geq 0, \quad \text{for each } j = 1, \ldots, M
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

#### Extract data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  #### Number of products
N = len(available)  #### Number of raw materials

#### Create the linear programming problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

#### Objective function
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M)), "Total_Profit"

#### Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i+1}"

#### Constraints for demand
for j in range(M):
    problem += x[j] <= demands[j], f"Demand_Constraint_{j+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

