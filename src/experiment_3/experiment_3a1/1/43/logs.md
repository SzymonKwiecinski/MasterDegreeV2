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

\subsection*{Parameters}
\begin{itemize}
    \item Let \( M \) be the number of different products.
    \item Let \( N \) be the number of different raw materials.
    \item Let \( \text{available}_i \) be the available units of raw material \( i \) for \( i = 1, \ldots, N \).
    \item Let \( \text{req}_{i,j} \) be the units of material \( i \) required to produce one unit of product \( j \) for \( j = 1, \ldots, M \).
    \item Let \( \text{price}_j \) be the selling price per unit of product \( j \).
    \item Let \( \text{cost}_j \) be the production cost per unit of product \( j \).
    \item Let \( \text{demand}_j \) be the forecasted maximum demand for product \( j \).
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{amount}_j \) be the amount of product \( j \) produced, where \( j = 1, \ldots, M \).

\subsection*{Objective Function}
The objective is to maximize the total profit, defined as:
\[
\text{total\_profit} = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \cdot \text{amount}_j
\]

\subsection*{Constraints}
1. Raw material constraints:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
\]

2. Demand constraints:
\[
\text{amount}_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
\text{amount}_j \geq 0, \quad \forall j = 1, \ldots, M
\]

\subsection*{Model Formulation}
The linear programming model can be summarized as follows:

\begin{align*}
\text{Maximize} & \quad \text{total\_profit} = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \cdot \text{amount}_j \\
\text{subject to} & \quad \sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i, \quad \forall i \\
                  & \quad \text{amount}_j \leq \text{demand}_j, \quad \forall j \\
                  & \quad \text{amount}_j \geq 0, \quad \forall j
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

\section*{Linear Programming Model for Wild Sports Production}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( M \) be the number of different products.
    \item Let \( N \) be the number of different raw materials.
    \item Let \( \text{available}_i \) be the available units of raw material \( i \) for \( i = 1, \ldots, N \).
    \item Let \( \text{req}_{i,j} \) be the units of material \( i \) required to produce one unit of product \( j \) for \( j = 1, \ldots, M \).
    \item Let \( \text{price}_j \) be the selling price per unit of product \( j \).
    \item Let \( \text{cost}_j \) be the production cost per unit of product \( j \).
    \item Let \( \text{demand}_j \) be the forecasted maximum demand for product \( j \).
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{amount}_j \) be the amount of product \( j \) produced, where \( j = 1, \ldots, M \).

\subsection*{Objective Function}
The objective is to maximize the total profit, defined as:
\[
\text{total\_profit} = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \cdot \text{amount}_j
\]

\subsection*{Constraints}
1. Raw material constraints:
\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i, \quad \forall i = 1, \ldots, N
\]

2. Demand constraints:
\[
\text{amount}_j \leq \text{demand}_j, \quad \forall j = 1, \ldots, M
\]

3. Non-negativity constraints:
\[
\text{amount}_j \geq 0, \quad \forall j = 1, \ldots, M
\]

\subsection*{Model Formulation}
The linear programming model can be summarized as follows:

\begin{align*}
\text{Maximize} & \quad \text{total\_profit} = \sum_{j=1}^{M} (\text{price}_j - \text{cost}_j) \cdot \text{amount}_j \\
\text{subject to} & \quad \sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i, \quad \forall i \\
                  & \quad \text{amount}_j \leq \text{demand}_j, \quad \forall j \\
                  & \quad \text{amount}_j \geq 0, \quad \forall j
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'available': [240000, 8000, 75000], 'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]], 'prices': [40, 38, 9], 'costs': [30, 26, 7], 'demands': [10000, 2000, 10000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data_json = '{"available": [240000, 8000, 75000], "requirements": [[48, 1, 10], [40, 1, 10], [0, 1, 2]], "prices": [40, 38, 9], "costs": [30, 26, 7], "demands": [10000, 2000, 10000]}'
data = json.loads(data_json)

#### Parameters
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  #### Number of products
N = len(available)  #### Number of raw materials

#### Decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

#### Problem definition
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

#### Objective function
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit, "Total_Profit"

#### Raw material constraints
for i in range(N):
    problem += pulp.lpSum(requirements[i][j] * amount[j] for j in range(M)) <= available[i], f"Raw_Material_Constraint_{i+1}"

#### Demand constraints
for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_Constraint_{j+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

