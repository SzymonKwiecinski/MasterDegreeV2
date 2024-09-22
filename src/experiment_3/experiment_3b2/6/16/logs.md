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
To solve the problem, we need to formulate a Linear Programming (LP) model that maximizes the revenue from producing oil products using given production processes and crude oil resources. Below is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\textbf{Sets:}
\begin{itemize}
    \item $O$: Set of crude oil types indexed by $i$.
    \item $P$: Set of products indexed by $p$.
    \item $L$: Set of production processes indexed by $l$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $\text{allocated}_i$: The amount of crude oil type $i$ allocated in million barrels.
    \item $\text{price}_p$: The selling price per barrel of product $p$.
    \item $\text{input}_{l,i}$: Barrels of crude oil type $i$ used per execution of process $l$.
    \item $\text{output}_{l,p}$: Barrels of product $p$ produced per execution of process $l$.
    \item $\text{cost}_l$: Cost per barrel of product produced by process $l$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $execute_l$: Number of times production process $l$ is executed.
\end{itemize}

\textbf{Objective Function:}

Maximize the revenue:
\[
\text{revenue} = \sum_{p \in P} \left( \text{price}_p \times \sum_{l \in L} \text{output}_{l,p} \times execute_l \right) - \sum_{l \in L} \left( \text{cost}_l \times \sum_{p \in P} \text{output}_{l,p} \times execute_l \right)
\]

\textbf{Constraints:}

1. Crude oil resource constraints:
\[
\sum_{l \in L} \text{input}_{l,i} \times execute_l \leq \text{allocated}_i, \quad \forall i \in O
\]

2. Non-negativity constraints:
\[
execute_l \geq 0, \quad \forall l \in L
\]

\end{document}
```

In this model:
- We maximize the total revenue by considering the price of each product produced and subtracting the process costs.
- We adhere to the constraints on the availability of each type of crude oil.
- We ensure that the decision variables, \(execute_l\), are non-negative. These variables represent the number of times each process is executed.


# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\textbf{Sets:}
\begin{itemize}
    \item $O$: Set of crude oil types indexed by $i$.
    \item $P$: Set of products indexed by $p$.
    \item $L$: Set of production processes indexed by $l$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $\text{allocated}_i$: The amount of crude oil type $i$ allocated in million barrels.
    \item $\text{price}_p$: The selling price per barrel of product $p$.
    \item $\text{input}_{l,i}$: Barrels of crude oil type $i$ used per execution of process $l$.
    \item $\text{output}_{l,p}$: Barrels of product $p$ produced per execution of process $l$.
    \item $\text{cost}_l$: Cost per barrel of product produced by process $l$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $execute_l$: Number of times production process $l$ is executed.
\end{itemize}

\textbf{Objective Function:}

Maximize the revenue:
\[
\text{revenue} = \sum_{p \in P} \left( \text{price}_p \times \sum_{l \in L} \text{output}_{l,p} \times execute_l \right) - \sum_{l \in L} \left( \text{cost}_l \times \sum_{p \in P} \text{output}_{l,p} \times execute_l \right)
\]

\textbf{Constraints:}

1. Crude oil resource constraints:
\[
\sum_{l \in L} \text{input}_{l,i} \times execute_l \leq \text{allocated}_i, \quad \forall i \in O
\]

2. Non-negativity constraints:
\[
execute_l \geq 0, \quad \forall l \in L
\]

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

#### Extracting the data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

#### Create the linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision variables
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0, cat='Continuous')

#### Objective Function
revenue = pulp.lpSum([price[p] * pulp.lpSum([output_matrix[l][p] * execute[l] for l in range(L)]) for p in range(P)]) \
                     - pulp.lpSum([cost[l] * pulp.lpSum([output_matrix[l][p] * execute[l] for p in range(P)]) for l in range(L)])
problem += revenue

#### Constraints
for i in range(O):
    problem += pulp.lpSum([input_matrix[l][i] * execute[l] for l in range(L)]) <= allocated[i], f"Crude_Oil_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

