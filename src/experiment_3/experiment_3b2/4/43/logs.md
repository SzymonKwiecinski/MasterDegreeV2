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
The problem described is a linear programming problem aimed at maximizing the profit for Wild Sports by deciding the number of each product to produce within the constraints of available raw materials and forecasted demands. Here's how you can formulate the problem as a linear program in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Wild Sports}

\subsection*{Sets}
\begin{itemize}
    \item Let \( M \) be the set of products, indexed by \( j \).
    \item Let \( N \) be the set of raw materials, indexed by \( i \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{available}_i \): The available amount of raw material \( i \).
    \item \( \text{req}_{i,j} \): The amount of raw material \( i \) required to produce one unit of product \( j \).
    \item \( \text{price}_j \): The selling price per unit of product \( j \).
    \item \( \text{cost}_j \): The production cost per unit of product \( j \).
    \item \( \text{demand}_j \): The maximum forecasted demand for product \( j \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{amount}_j \): The amount of product \( j \) to be produced.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit, given by:
\[
\text{maximize} \quad \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \cdot \text{amount}_j
\]

\subsection*{Constraints}
\begin{align*}
\text{Material Constraints:} \quad & \sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N \\
\text{Demand Constraints:} \quad & \text{amount}_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M \\
\text{Non-negativity:} \quad & \text{amount}_j \geq 0, \quad \forall j = 1, \ldots, M
\end{align*}

\end{document}
```

This model aims to maximize the company's profit by determining the optimal production levels for each product, considering raw material constraints and market demands.

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

\subsection*{Sets}
\begin{itemize}
    \item Let \( M \) be the set of products, indexed by \( j \).
    \item Let \( N \) be the set of raw materials, indexed by \( i \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{available}_i \): The available amount of raw material \( i \).
    \item \( \text{req}_{i,j} \): The amount of raw material \( i \) required to produce one unit of product \( j \).
    \item \( \text{price}_j \): The selling price per unit of product \( j \).
    \item \( \text{cost}_j \): The production cost per unit of product \( j \).
    \item \( \text{demand}_j \): The maximum forecasted demand for product \( j \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{amount}_j \): The amount of product \( j \) to be produced.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit, given by:
\[
\text{maximize} \quad \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \cdot \text{amount}_j
\]

\subsection*{Constraints}
\begin{align*}
\text{Material Constraints:} \quad & \sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N \\
\text{Demand Constraints:} \quad & \text{amount}_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M \\
\text{Non-negativity:} \quad & \text{amount}_j \geq 0, \quad \forall j = 1, \ldots, M
\end{align*}

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

#### Sets
M = range(len(data['prices']))  #### Products
N = range(len(data['available']))  #### Raw materials

#### Create the problem
problem = pulp.LpProblem("Wild_Sports_Optimization", pulp.LpMaximize)

#### Decision variables
amount = pulp.LpVariable.dicts("amount", M, lowBound=0)

#### Objective function
profit = pulp.lpSum([(data['prices'][j] - data['costs'][j]) * amount[j] for j in M])
problem += profit

#### Material constraints
for i in N:
    problem += pulp.lpSum([data['requirements'][i][j] * amount[j] for j in M]) <= data['available'][i]

#### Demand constraints
for j in M:
    problem += amount[j] <= data['demands'][j]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

