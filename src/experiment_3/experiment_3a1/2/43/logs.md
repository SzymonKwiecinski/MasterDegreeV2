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

\section*{Linear Programming Model for Wild Sports Production}

\subsection*{Variables}
Let:
\begin{itemize}
    \item $M$: Number of products
    \item $N$: Number of raw materials
    \item $amount_{j}$: Amount of product $j$ produced (for $j = 1, \ldots, M$)
    \item $available_{i}$: Available units of raw material $i$ (for $i = 1, \ldots, N$)
    \item $req_{i,j}$: Units of raw material $i$ required to produce one unit of product $j$
    \item $price_{j}$: Selling price per unit of product $j$
    \item $cost_{j}$: Production cost per unit of product $j$
    \item $demand_{j}$: Forecasted maximum demand for product $j$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (price_{j} - cost_{j}) \cdot amount_{j}
\]

\subsection*{Constraints}
1. Raw material constraints:
\[
\sum_{j=1}^{M} req_{i,j} \cdot amount_{j} \leq available_{i} \quad \text{for } i = 1, \ldots, N
\]
2. Demand constraints:
\[
amount_{j} \leq demand_{j} \quad \text{for } j = 1, \ldots, M
\]
3. Non-negativity constraints:
\[
amount_{j} \geq 0 \quad \text{for } j = 1, \ldots, M
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item Amount of each product produced: $amount = [amount_{1}, amount_{2}, \ldots, amount_{M}]$
    \item Total profit: $total\_profit = Z$
\end{itemize}

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

\section*{Linear Programming Model for Wild Sports Production}

\subsection*{Variables}
Let:
\begin{itemize}
    \item $M$: Number of products
    \item $N$: Number of raw materials
    \item $amount_{j}$: Amount of product $j$ produced (for $j = 1, \ldots, M$)
    \item $available_{i}$: Available units of raw material $i$ (for $i = 1, \ldots, N$)
    \item $req_{i,j}$: Units of raw material $i$ required to produce one unit of product $j$
    \item $price_{j}$: Selling price per unit of product $j$
    \item $cost_{j}$: Production cost per unit of product $j$
    \item $demand_{j}$: Forecasted maximum demand for product $j$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{j=1}^{M} (price_{j} - cost_{j}) \cdot amount_{j}
\]

\subsection*{Constraints}
1. Raw material constraints:
\[
\sum_{j=1}^{M} req_{i,j} \cdot amount_{j} \leq available_{i} \quad \text{for } i = 1, \ldots, N
\]
2. Demand constraints:
\[
amount_{j} \leq demand_{j} \quad \text{for } j = 1, \ldots, M
\]
3. Non-negativity constraints:
\[
amount_{j} \geq 0 \quad \text{for } j = 1, \ldots, M
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item Amount of each product produced: $amount = [amount_{1}, amount_{2}, \ldots, amount_{M}]$
    \item Total profit: $total\_profit = Z$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON format
data_json = '{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}'
data = json.loads(data_json)

#### Extracting data
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  #### Number of products
N = len(available)  #### Number of raw materials

#### Initialize the problem
problem = pulp.LpProblem("WildSportsProduction", pulp.LpMaximize)

#### Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

#### Objective function
profit = [prices[j] - costs[j] for j in range(M)]
problem += pulp.lpSum(profit[j] * amount[j] for j in range(M)), "Total_Profit"

#### Constraints
#### Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * amount[j] for j in range(M)) <= available[i], f"RawMaterialConstraint_{i}"

#### Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j], f"DemandConstraint_{j}"

#### Solve the problem
problem.solve()

#### Output the results
amount_produced = [amount[j].varValue for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f'Amount of each product produced: {amount_produced}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

