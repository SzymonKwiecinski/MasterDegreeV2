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
To model the given problem as a Linear Programming (LP) problem, we define the decision variables, objective function, and constraints based on the provided information.

######### Decision Variables:
Let \( x_j \) be the number of units of product \( j \) to be produced, where \( j = 1, 2, \ldots, M \).

######### Objective Function:
The objective is to maximize the total profit, which is the total revenue minus the total production cost.

The revenue from product \( j \) is \( \text{price}_j \times x_j \).
The production cost for product \( j \) is \( \text{cost}_j \times x_j \).

Therefore, the profit from product \( j \) is \((\text{price}_j - \text{cost}_j) \times x_j\).

The total profit is the sum of profits from all products:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) x_j
\]

######### Constraints:
1. **Raw Material Constraints:**
   For each raw material \( i \), the total amount used cannot exceed the available amount:
   \[
   \sum_{j=1}^{M} \text{req}_{i,j} x_j \leq \text{available}_i \quad \text{for } i = 1, 2, \ldots, N
   \]

2. **Demand Constraints:**
   The production of each product cannot exceed the forecasted demand:
   \[
   x_j \leq \text{demand}_j \quad \text{for } j = 1, 2, \ldots, M
   \]

3. **Non-negativity Constraints:**
   The number of units produced for each product must be non-negative:
   \[
   x_j \geq 0 \quad \text{for } j = 1, 2, \ldots, M
   \]

Here is the complete Linear Programming model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Wild Sports}
\author{}
\date{}
\maketitle

\section*{Objective}

Maximize the total profit \( Z \):

\[
Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) x_j
\]

\section*{Constraints}

\begin{itemize}
    \item Raw Material Constraints:
    \[
    \sum_{j=1}^{M} \text{req}_{i,j} x_j \leq \text{available}_i \quad \text{for } i = 1, 2, \ldots, N
    \]

    \item Demand Constraints:
    \[
    x_j \leq \text{demand}_j \quad \text{for } j = 1, 2, \ldots, M
    \]

    \item Non-negativity Constraints:
    \[
    x_j \geq 0 \quad \text{for } j = 1, 2, \ldots, M
    \]
\end{itemize}

\section*{Decision Variables}

\( x_j \) represents the number of units to produce of product \( j \), where \( j = 1, 2, \ldots, M \).

\end{document}
```

This LaTeX document outlines the LP formulation of the problem. The objective function, constraints, and decision variables are clearly stated, providing a comprehensive model for maximizing the profit of Wild Sports.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Wild Sports}
\author{}
\date{}
\maketitle

\section*{Objective}

Maximize the total profit \( Z \):

\[
Z = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) x_j
\]

\section*{Constraints}

\begin{itemize}
    \item Raw Material Constraints:
    \[
    \sum_{j=1}^{M} \text{req}_{i,j} x_j \leq \text{available}_i \quad \text{for } i = 1, 2, \ldots, N
    \]

    \item Demand Constraints:
    \[
    x_j \leq \text{demand}_j \quad \text{for } j = 1, 2, \ldots, M
    \]

    \item Non-negativity Constraints:
    \[
    x_j \geq 0 \quad \text{for } j = 1, 2, \ldots, M
    \]
\end{itemize}

\section*{Decision Variables}

\( x_j \) represents the number of units to produce of product \( j \), where \( j = 1, 2, \ldots, M \).

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

#### Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

#### Number of products and raw materials
M = len(prices)
N = len(available)

#### Problem
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat='Continuous') for j in range(M)]

#### Objective Function
problem += pulp.lpSum((prices[j] - costs[j]) * x[j] for j in range(M))

#### Constraints

#### Raw Material Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i]

#### Demand Constraints
for j in range(M):
    problem += x[j] <= demands[j]

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

