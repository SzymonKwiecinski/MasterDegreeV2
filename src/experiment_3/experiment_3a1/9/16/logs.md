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

\section*{Linear Programming Model for Oil Refinery}

\textbf{Parameters:}
\begin{itemize}
    \item $O$: Number of crude oil types
    \item $P$: Number of products
    \item $L$: Number of production processes
    \item $allocated_i$: Million barrels of crude oil type $i$ allocated for production
    \item $price_p$: Selling price per barrel of product $p$
    \item $input_{l,i}$: Barrels of crude oil type $i$ required by process $l$
    \item $output_{l,p}$: Barrels of product $p$ produced by process $l$
    \item $cost_l$: Cost per barrel of product produced by process $l$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $execute_l$: Number of times process $l$ is executed
    \item $revenue$: Total revenue for the month
\end{itemize}

\textbf{Objective Function:}
Maximize total revenue:
\[
\text{Maximize } Z = \sum_{p=1}^{P} price_p \cdot \sum_{l=1}^{L} output_{l,p} \cdot execute_l
\]

\textbf{Subject to:}
1. \textbf{Crude Oil Constraints:}
\[
\sum_{l=1}^{L} input_{l,i} \cdot execute_l \leq allocated_i \quad \forall i = 1, \ldots, O
\]
2. \textbf{Non-negativity Constraints:}
\[
execute_l \geq 0 \quad \forall l = 1, \ldots, L
\]

\textbf{Output Information:}
\begin{itemize}
    \item Total Revenue: $revenue = Z$
    \item Execution Plan: $execute = [execute_1, execute_2, \ldots, execute_L]$
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

\section*{Linear Programming Model for Oil Refinery}

\textbf{Parameters:}
\begin{itemize}
    \item $O$: Number of crude oil types
    \item $P$: Number of products
    \item $L$: Number of production processes
    \item $allocated_i$: Million barrels of crude oil type $i$ allocated for production
    \item $price_p$: Selling price per barrel of product $p$
    \item $input_{l,i}$: Barrels of crude oil type $i$ required by process $l$
    \item $output_{l,p}$: Barrels of product $p$ produced by process $l$
    \item $cost_l$: Cost per barrel of product produced by process $l$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $execute_l$: Number of times process $l$ is executed
    \item $revenue$: Total revenue for the month
\end{itemize}

\textbf{Objective Function:}
Maximize total revenue:
\[
\text{Maximize } Z = \sum_{p=1}^{P} price_p \cdot \sum_{l=1}^{L} output_{l,p} \cdot execute_l
\]

\textbf{Subject to:}
1. \textbf{Crude Oil Constraints:}
\[
\sum_{l=1}^{L} input_{l,i} \cdot execute_l \leq allocated_i \quad \forall i = 1, \ldots, O
\]
2. \textbf{Non-negativity Constraints:}
\[
execute_l \geq 0 \quad \forall l = 1, \ldots, L
\]

\textbf{Output Information:}
\begin{itemize}
    \item Total Revenue: $revenue = Z$
    \item Execution Plan: $execute = [execute_1, execute_2, \ldots, execute_L]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input as JSON
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

#### Parameters
O = data['O']  #### Number of crude oil types
P = data['P']  #### Number of products
L = data['L']  #### Number of production processes
allocated = data['Allocated']  #### Allocated crude oil
price = data['Price']  #### Selling price per product
input_matrix = data['Input']  #### Input matrix for crude oil
output_matrix = data['Output']  #### Output matrix for products
cost = data['Cost']  #### Cost per process

#### Create the LP problem
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

#### Decision Variables
execute = pulp.LpVariable.dicts("Execute", range(L), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(price[p] * pulp.lpSum(output_matrix[l][p] * execute[l] for l in range(L)) for p in range(P)), "Total_Revenue"

#### Constraints for crude oil allocations
for i in range(O):
    problem += pulp.lpSum(input_matrix[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_Oil_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Output the results
revenue = pulp.value(problem.objective)
execution_plan = [execute[l].varValue for l in range(L)]
print(f' (Objective Value): <OBJ>{revenue}</OBJ>')
print(f'Execution Plan: {execution_plan}')
```

