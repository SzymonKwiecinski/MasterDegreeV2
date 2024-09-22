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

\subsection*{Sets}
\begin{itemize}
    \item \( I = \{1, 2, \ldots, O\} \): set of crude oil types
    \item \( P = \{1, 2, \ldots, P\} \): set of products
    \item \( L = \{1, 2, \ldots, L\} \): set of production processes
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{allocated}_i \): allocated crude oil (in million barrels) for type \( i \)
    \item \( \text{price}_p \): selling price per barrel of product \( p \)
    \item \( \text{input}_{l,i} \): barrels of crude \( i \) needed for process \( l \)
    \item \( \text{output}_{l,p} \): barrels of product \( p \) produced by process \( l \)
    \item \( \text{cost}_l \): cost per barrel for process \( l \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{execute}_l \): number of times process \( l \) is executed
\end{itemize}

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{revenue} = \sum_{p \in P} \text{price}_p \cdot \left( \sum_{l \in L} \text{output}_{l,p} \cdot \text{execute}_l \right) - \sum_{l \in L} \text{cost}_l \cdot \left( \sum_{p \in P} \text{output}_{l,p} \cdot \text{execute}_l \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Supply constraints for each crude oil type:
    \[
    \sum_{l \in L} \text{input}_{l,i} \cdot \text{execute}_l \leq \text{allocated}_i, \quad \forall i \in I
    \]

    \item Non-negativity constraints:
    \[
    \text{execute}_l \geq 0, \quad \forall l \in L
    \]
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

\subsection*{Sets}
\begin{itemize}
    \item \( I = \{1, 2, \ldots, O\} \): set of crude oil types
    \item \( P = \{1, 2, \ldots, P\} \): set of products
    \item \( L = \{1, 2, \ldots, L\} \): set of production processes
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{allocated}_i \): allocated crude oil (in million barrels) for type \( i \)
    \item \( \text{price}_p \): selling price per barrel of product \( p \)
    \item \( \text{input}_{l,i} \): barrels of crude \( i \) needed for process \( l \)
    \item \( \text{output}_{l,p} \): barrels of product \( p \) produced by process \( l \)
    \item \( \text{cost}_l \): cost per barrel for process \( l \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{execute}_l \): number of times process \( l \) is executed
\end{itemize}

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{revenue} = \sum_{p \in P} \text{price}_p \cdot \left( \sum_{l \in L} \text{output}_{l,p} \cdot \text{execute}_l \right) - \sum_{l \in L} \text{cost}_l \cdot \left( \sum_{p \in P} \text{output}_{l,p} \cdot \text{execute}_l \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Supply constraints for each crude oil type:
    \[
    \sum_{l \in L} \text{input}_{l,i} \cdot \text{execute}_l \leq \text{allocated}_i, \quad \forall i \in I
    \]

    \item Non-negativity constraints:
    \[
    \text{execute}_l \geq 0, \quad \forall l \in L
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

#### Defining the sets
O = data['O']  #### Number of crude oil types
P = data['P']  #### Number of products
L = data['L']  #### Number of production processes

#### Defining the parameters
allocated = data['Allocated']  #### allocated crude oil
price = data['Price']  #### selling price per barrel of product
input_data = data['Input']  #### barrels of crude needed for process
output_data = data['Output']  #### barrels of product produced by process
cost = data['Cost']  #### cost per barrel for process

#### Create a problem variable
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

#### Decision variables
execute = pulp.LpVariable.dicts("execute", range(1, L + 1), lowBound=0)

#### Objective Function
total_revenue = pulp.lpSum(price[p - 1] * pulp.lpSum(output_data[l - 1][p - 1] * execute[l] for l in range(1, L + 1)) for p in range(1, P + 1))
total_cost = pulp.lpSum(cost[l - 1] * pulp.lpSum(output_data[l - 1][p - 1] * execute[l] for p in range(1, P + 1)) for l in range(1, L + 1))
problem += total_revenue - total_cost, "Total_Profit"

#### Supply constraints for each crude oil type
for i in range(1, O + 1):
    problem += (pulp.lpSum(input_data[l - 1][i - 1] * execute[l] for l in range(1, L + 1)) <= allocated[i - 1]), f"Supply_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

