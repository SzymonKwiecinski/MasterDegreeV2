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

\textbf{Parameters:}
\begin{itemize}
    \item Let $O$ be the number of crude oil types.
    \item Let $P$ be the number of products.
    \item Let $L$ be the number of production processes.
    \item Let $allocated_i$ be the number of million barrels of crude oil type $i$ allocated for production.
    \item Let $price_p$ be the selling price per barrel for product $p$.
    \item Let $input_{l,i}$ be the number of barrels of crude oil type $i$ needed for process $l$.
    \item Let $output_{l,p}$ be the number of barrels of product $p$ produced from process $l$.
    \item Let $cost_l$ be the cost per barrel of product produced from process $l$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $execute_l$ be the number of times process $l$ is executed.
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
    \text{Maximize } revenue = \sum_{p=1}^{P} price_p \cdot \sum_{l=1}^{L} output_{l,p} \cdot execute_l
\end{equation}

\textbf{Subject to:}
\begin{equation}
    \sum_{l=1}^{L} input_{l,i} \cdot execute_l \leq allocated_i \quad \forall i = 1, \ldots, O
\end{equation}
\begin{equation}
    revenue - \sum_{l=1}^{L} cost_l \cdot \sum_{p=1}^{P} output_{l,p} \cdot execute_l \geq 0
\end{equation}
\begin{equation}
    execute_l \geq 0 \quad \forall l = 1, \ldots, L
\end{equation}

\textbf{Output:}
\begin{itemize}
    \item $revenue$: The total revenue for the month.
    \item $execute$: The optimal number of times each process should be executed, represented as $[execute_1, execute_2, \ldots, execute_L]$.
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

\textbf{Parameters:}
\begin{itemize}
    \item Let $O$ be the number of crude oil types.
    \item Let $P$ be the number of products.
    \item Let $L$ be the number of production processes.
    \item Let $allocated_i$ be the number of million barrels of crude oil type $i$ allocated for production.
    \item Let $price_p$ be the selling price per barrel for product $p$.
    \item Let $input_{l,i}$ be the number of barrels of crude oil type $i$ needed for process $l$.
    \item Let $output_{l,p}$ be the number of barrels of product $p$ produced from process $l$.
    \item Let $cost_l$ be the cost per barrel of product produced from process $l$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item Let $execute_l$ be the number of times process $l$ is executed.
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
    \text{Maximize } revenue = \sum_{p=1}^{P} price_p \cdot \sum_{l=1}^{L} output_{l,p} \cdot execute_l
\end{equation}

\textbf{Subject to:}
\begin{equation}
    \sum_{l=1}^{L} input_{l,i} \cdot execute_l \leq allocated_i \quad \forall i = 1, \ldots, O
\end{equation}
\begin{equation}
    revenue - \sum_{l=1}^{L} cost_l \cdot \sum_{p=1}^{P} output_{l,p} \cdot execute_l \geq 0
\end{equation}
\begin{equation}
    execute_l \geq 0 \quad \forall l = 1, \ldots, L
\end{equation}

\textbf{Output:}
\begin{itemize}
    \item $revenue$: The total revenue for the month.
    \item $execute$: The optimal number of times each process should be executed, represented as $[execute_1, execute_2, \ldots, execute_L]$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data_json = '{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}'
data = json.loads(data_json)

#### Parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

#### Create the problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

#### Decision Variables
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0)

#### Objective Function
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_data[l][p] * execute[l] for l in range(L)) for p in range(P))
problem += revenue

#### Constraints
#### Constraint for allocated crude oil types
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * execute[l] for l in range(L)) <= allocated[i]

#### Constraint for revenue - costs
problem += revenue - pulp.lpSum(cost[l] * pulp.lpSum(output_data[l][p] * execute[l] for p in range(P)) for l in range(L)) >= 0

#### Solve the problem
problem.solve()

#### Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
execute_values = [execute[l].varValue for l in range(L)]
print(f'Optimal execution of processes: {execute_values}')
```

