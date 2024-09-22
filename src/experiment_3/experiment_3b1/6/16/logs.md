# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A manager of an oil refinery has \var{allocated_i} million barrels of crude oil type \var{i} allocated for production during the coming month. 
- These resources can be used to make \var{P} different products. product \var{p} sells for $ \var{price_p} per barrel.
- There are \var{L} production processes. Process \var{l} uses \var{input_l_i} barrels of each crude \var{i}, and produces \var{output_l_p} barrels of each product \var{p}. 
- Process \var{l} has a cost of \var{cost_l} per barrel of product produced.
- All \var{input_l_i} quantities and \var{output_l_p} quanitites are in barrels. 
- There are no separate cost items for the cost of the crudes, as they have already been allocated.

INPUT FORMAT: 

{
    "allocated": [allocated_i for i in 1, ..., O],
    "price": [price_p for p in 1, ..., P],
    "input": [[input_l_i for i in 1, ..., O] for l in 1, ..., L],
    "output": [[output_l_p for p in 1, ..., P] for l in 1, ..., L],
    "cost": [cost_l for l in 1, ..., L]
}

OBJECTIVE: We want to know how many times should we execute each process to maximize the revenue for the next month (you can assume that the number of times that each process is executed is a floating point number)

OUTPUT INFO:

- \var{revenue} is the total revenue for the month.
- \var{execute_l} is the number of times that process \var{l} should be executed.

OUTPUT FORMAT:

{
    "revenue": revenue,
    "execute": [execute_l for l in 1, ..., L]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Oil Refinery Production}

Let:
\begin{itemize}
    \item $O$: Number of crude oil types
    \item $P$: Number of products
    \item $L$: Number of production processes
    \item $\text{allocated}_i$: Amount of crude oil type $i$ allocated (in million barrels)
    \item $\text{price}_p$: Selling price of product $p$ per barrel
    \item $\text{input}_{l,i}$: Amount of crude oil type $i$ required for process $l$ (in barrels)
    \item $\text{output}_{l,p}$: Amount of product $p$ produced per execution of process $l$ (in barrels)
    \item $\text{cost}_l$: Cost of process $l$ per barrel of product produced
    \item $x_l$: Number of times process $l$ is executed
\end{itemize}

\subsection*{Objective Function}
We want to maximize the revenue minus the cost:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \text{price}_p \sum_{l=1}^{L} \text{output}_{l,p} x_l - \sum_{l=1}^{L} \text{cost}_l \left( \sum_{p=1}^{P} \text{output}_{l,p} x_l \right)
\]

\subsection*{Constraints}

1. Crude oil constraints:
\[
\sum_{l=1}^{L} \text{input}_{l,i} x_l \leq \text{allocated}_i \quad \forall i = 1, \ldots, O
\]

2. Non-negativity constraints:
\[
x_l \geq 0 \quad \forall l = 1, \ldots, L
\]

\subsection*{Outputs}
The output will provide:
\begin{itemize}
    \item $\text{revenue}$: Total revenue for the month
    \item $\text{execute}_l$: Number of times process $l$ should be executed
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

\section*{Linear Programming Model for Oil Refinery Production}

Let:
\begin{itemize}
    \item $O$: Number of crude oil types
    \item $P$: Number of products
    \item $L$: Number of production processes
    \item $\text{allocated}_i$: Amount of crude oil type $i$ allocated (in million barrels)
    \item $\text{price}_p$: Selling price of product $p$ per barrel
    \item $\text{input}_{l,i}$: Amount of crude oil type $i$ required for process $l$ (in barrels)
    \item $\text{output}_{l,p}$: Amount of product $p$ produced per execution of process $l$ (in barrels)
    \item $\text{cost}_l$: Cost of process $l$ per barrel of product produced
    \item $x_l$: Number of times process $l$ is executed
\end{itemize}

\subsection*{Objective Function}
We want to maximize the revenue minus the cost:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \text{price}_p \sum_{l=1}^{L} \text{output}_{l,p} x_l - \sum_{l=1}^{L} \text{cost}_l \left( \sum_{p=1}^{P} \text{output}_{l,p} x_l \right)
\]

\subsection*{Constraints}

1. Crude oil constraints:
\[
\sum_{l=1}^{L} \text{input}_{l,i} x_l \leq \text{allocated}_i \quad \forall i = 1, \ldots, O
\]

2. Non-negativity constraints:
\[
x_l \geq 0 \quad \forall l = 1, \ldots, L
\]

\subsection*{Outputs}
The output will provide:
\begin{itemize}
    \item $\text{revenue}$: Total revenue for the month
    \item $\text{execute}_l$: Number of times process $l$ should be executed
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

#### Extracting data from the JSON
O = data['O']  #### number of crude oil types
P = data['P']  #### number of products
L = data['L']  #### number of production processes
allocated = data['Allocated']  #### amount of crude oil allocated
price = data['Price']  #### selling price of products
input_data = data['Input']  #### input crude oil required for processes
output_data = data['Output']  #### output products from processes
cost = data['Cost']  #### cost per barrel of product produced

#### Creating the LP problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

#### Decision variables: number of times each process is executed
x = pulp.LpVariable.dicts("x", range(L), lowBound=0)

#### Objective function: Maximize revenue - cost
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_data[l][p] * x[l] for l in range(L)) for p in range(P))
total_cost = pulp.lpSum(cost[l] * pulp.lpSum(output_data[l][p] * x[l] for p in range(P)) for l in range(L))
problem += revenue - total_cost

#### Constraints: Crude oil constraints
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * x[l] for l in range(L)) <= allocated[i], f"CrudeOilConstraint_{i}"

#### Non-negativity constraints are handled by defining the lowBound=0 in the variables

#### Solving the problem
problem.solve()

#### Output the results
revenue_value = pulp.value(problem.objective)
execution_plan = {l: x[l].varValue for l in range(L)}

print(f' (Objective Value): <OBJ>{revenue_value}</OBJ>')
print('Execution Plan:', execution_plan)
```

