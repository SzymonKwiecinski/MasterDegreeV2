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

\subsection*{Parameters}
\begin{itemize}
    \item Let $O$ be the number of crude oil types.
    \item Let $P$ be the number of products.
    \item Let $L$ be the number of production processes.
    \item Let \texttt{allocated\_i} be the allocated amount of crude oil type $i$ (in million barrels).
    \item Let \texttt{price\_p} be the selling price of product $p$ (in dollars).
    \item Let \texttt{input\_l\_i} be the input requirement of crude oil type $i$ for process $l$ (in barrels).
    \item Let \texttt{output\_l\_p} be the output produced of product $p$ by process $l$ (in barrels).
    \item Let \texttt{cost\_l} be the cost per barrel for process $l$ (in dollars).
\end{itemize}

\subsection*{Decision Variables}
Let $x_l$ be the number of times that process $l$ should be executed.

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \texttt{price\_p} \left( \sum_{l=1}^{L} \texttt{output\_l\_p} x_l \right) - \sum_{l=1}^{L} \texttt{cost\_l} \left( \sum_{p=1}^{P} \texttt{output\_l\_p} x_l \right)
\]

\subsection*{Constraints}
1. **Resource Allocation Constraints**:
\[
\sum_{l=1}^{L} \texttt{input\_l\_i} x_l \leq \texttt{allocated\_i}, \quad \forall i \in \{1, \ldots, O\}
\]

2. **Non-negativity Constraints**:
\[
x_l \geq 0, \quad \forall l \in \{1, \ldots, L\}
\]

\subsection*{Output}
Let $\text{revenue}$ be the total revenue for the month, and $\text{execute}_l$ be the number of times that process $l$ should be executed.

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

\subsection*{Parameters}
\begin{itemize}
    \item Let $O$ be the number of crude oil types.
    \item Let $P$ be the number of products.
    \item Let $L$ be the number of production processes.
    \item Let \texttt{allocated\_i} be the allocated amount of crude oil type $i$ (in million barrels).
    \item Let \texttt{price\_p} be the selling price of product $p$ (in dollars).
    \item Let \texttt{input\_l\_i} be the input requirement of crude oil type $i$ for process $l$ (in barrels).
    \item Let \texttt{output\_l\_p} be the output produced of product $p$ by process $l$ (in barrels).
    \item Let \texttt{cost\_l} be the cost per barrel for process $l$ (in dollars).
\end{itemize}

\subsection*{Decision Variables}
Let $x_l$ be the number of times that process $l$ should be executed.

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \texttt{price\_p} \left( \sum_{l=1}^{L} \texttt{output\_l\_p} x_l \right) - \sum_{l=1}^{L} \texttt{cost\_l} \left( \sum_{p=1}^{P} \texttt{output\_l\_p} x_l \right)
\]

\subsection*{Constraints}
1. **Resource Allocation Constraints**:
\[
\sum_{l=1}^{L} \texttt{input\_l\_i} x_l \leq \texttt{allocated\_i}, \quad \forall i \in \{1, \ldots, O\}
\]

2. **Non-negativity Constraints**:
\[
x_l \geq 0, \quad \forall l \in \{1, \ldots, L\}
\]

\subsection*{Output}
Let $\text{revenue}$ be the total revenue for the month, and $\text{execute}_l$ be the number of times that process $l$ should be executed.

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'O': 2, 
    'P': 2, 
    'L': 3, 
    'Allocated': [8000, 5000], 
    'Price': [38, 33], 
    'Input': [[3, 5], [1, 1], [5, 3]], 
    'Output': [[4, 3], [1, 1], [3, 4]], 
    'Cost': [51, 11, 40]
}

O = data['O']
P = data['P']
L = data['L']
Allocated = data['Allocated']
Price = data['Price']
Input = data['Input']
Output = data['Output']
Cost = data['Cost']

#### Define the problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(L)]

#### Objective Function
objective = sum(Price[p] * sum(Output[l][p] * x[l] for l in range(L)) for p in range(P)) - \
            sum(Cost[l] * sum(Output[l][p] * x[l] for p in range(P)) for l in range(L))

problem += objective

#### Constraints
#### Resource Allocation Constraints
for i in range(O):
    problem += sum(Input[l][i] * x[l] for l in range(L)) <= Allocated[i]
    
#### Non-negativity Constraints are automatically handled by lowerBound in variable definition

#### Solve the problem
problem.solve()

#### Output the solution
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

