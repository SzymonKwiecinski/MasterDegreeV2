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

\subsection*{Variables}
Let \( x_j \) be the amount of product \( j \) produced, where \( j = 1, \ldots, M \). 

\subsection*{Parameters}
\begin{align*}
\text{available}_i & : \text{units of raw material } i \text{ available, for } i = 1, \ldots, N \\
\text{req}_{i,j} & : \text{units of material } i \text{ required to produce one unit of product } j \\
\text{price}_j & : \text{selling price of product } j \\
\text{cost}_j & : \text{production cost of product } j \\
\text{demand}_j & : \text{maximum forecasted demand for product } j
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Total Profit} = \sum_{j=1}^{M} ( \text{price}_j - \text{cost}_j ) x_j
\]

\subsection*{Constraints}
1. Raw material constraints:

\[
\sum_{j=1}^{M} \text{req}_{i,j} x_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
\]

2. Demand constraints:

\[
x_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M
\]

3. Non-negativity constraints:

\[
x_j \geq 0, \quad \forall j = 1, \ldots, M
\]

\subsection*{Output}
The solution to the LP will yield:
\begin{align*}
\text{amount} & : [x_1, x_2, \ldots, x_M] \\
\text{total\_profit} & : \text{Total Profit}
\end{align*}

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

\subsection*{Variables}
Let \( x_j \) be the amount of product \( j \) produced, where \( j = 1, \ldots, M \). 

\subsection*{Parameters}
\begin{align*}
\text{available}_i & : \text{units of raw material } i \text{ available, for } i = 1, \ldots, N \\
\text{req}_{i,j} & : \text{units of material } i \text{ required to produce one unit of product } j \\
\text{price}_j & : \text{selling price of product } j \\
\text{cost}_j & : \text{production cost of product } j \\
\text{demand}_j & : \text{maximum forecasted demand for product } j
\end{align*}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Total Profit} = \sum_{j=1}^{M} ( \text{price}_j - \text{cost}_j ) x_j
\]

\subsection*{Constraints}
1. Raw material constraints:

\[
\sum_{j=1}^{M} \text{req}_{i,j} x_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
\]

2. Demand constraints:

\[
x_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M
\]

3. Non-negativity constraints:

\[
x_j \geq 0, \quad \forall j = 1, \ldots, M
\]

\subsection*{Output}
The solution to the LP will yield:
\begin{align*}
\text{amount} & : [x_1, x_2, \ldots, x_M] \\
\text{total\_profit} & : \text{Total Profit}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extracting data from provided JSON format.
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

#### Number of products (M) and raw materials (N)
M = len(prices)
N = len(available)

#### Initialize the linear programming problem
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

#### Decision variables: amount of each product to produce
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

#### Objective function: Maximize total profit
profit = pulp.lpSum((prices[j] - costs[j]) * x[j] for j in range(M))
problem += profit

#### Constraints

#### 1. Raw material constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[i][j] * x[j] for j in range(M)) <= available[i])

#### 2. Demand constraints
for j in range(M):
    problem += (x[j] <= demands[j])

#### Solve the problem
problem.solve()

#### Results
amounts = [pulp.value(x[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

#### Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

