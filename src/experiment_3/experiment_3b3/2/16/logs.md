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

\subsection*{Indices}
\begin{itemize}
    \item $i$: Index for crude oil types ($i = 1, 2, \ldots, O$)
    \item $p$: Index for products ($p = 1, 2, \ldots, P$)
    \item $l$: Index for production processes ($l = 1, 2, \ldots, L$)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $allocated_i$: Million barrels of crude oil type $i$ allocated for production
    \item $price_p$: Selling price per barrel of product $p$
    \item $input_{l,i}$: Barrels of crude oil type $i$ required for process $l$
    \item $output_{l,p}$: Barrels of product $p$ produced by process $l$
    \item $cost_l$: Cost per barrel of product produced by process $l$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $execute_l$: Number of times process $l$ is executed (can be a floating point number)
\end{itemize}

\subsection*{Objective Function}
We want to maximize the total revenue:

\[
\text{Maximize } Z = \sum_{p=1}^{P} price_p \cdot \left( \sum_{l=1}^{L} output_{l,p} \cdot execute_l \right) - \sum_{l=1}^{L} cost_l \cdot \left( \sum_{p=1}^{P} output_{l,p} \cdot execute_l \right)
\]

\subsection*{Constraints}
1. Crude oil allocation constraint for each type $i$:

\[
\sum_{l=1}^{L} input_{l,i} \cdot execute_l \leq allocated_i \quad \forall i = 1, \ldots, O
\]

2. Non-negativity constraint for processes:

\[
execute_l \geq 0 \quad \forall l = 1, \ldots, L
\]

\subsection*{Output Information}
The output of the model will provide:
\begin{itemize}
    \item $revenue$: Total revenue for the month
    \item $execute$: Array of numbers of times each process should be executed, $[execute_1, execute_2, \ldots, execute_L]$
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

\subsection*{Indices}
\begin{itemize}
    \item $i$: Index for crude oil types ($i = 1, 2, \ldots, O$)
    \item $p$: Index for products ($p = 1, 2, \ldots, P$)
    \item $l$: Index for production processes ($l = 1, 2, \ldots, L$)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $allocated_i$: Million barrels of crude oil type $i$ allocated for production
    \item $price_p$: Selling price per barrel of product $p$
    \item $input_{l,i}$: Barrels of crude oil type $i$ required for process $l$
    \item $output_{l,p}$: Barrels of product $p$ produced by process $l$
    \item $cost_l$: Cost per barrel of product produced by process $l$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $execute_l$: Number of times process $l$ is executed (can be a floating point number)
\end{itemize}

\subsection*{Objective Function}
We want to maximize the total revenue:

\[
\text{Maximize } Z = \sum_{p=1}^{P} price_p \cdot \left( \sum_{l=1}^{L} output_{l,p} \cdot execute_l \right) - \sum_{l=1}^{L} cost_l \cdot \left( \sum_{p=1}^{P} output_{l,p} \cdot execute_l \right)
\]

\subsection*{Constraints}
1. Crude oil allocation constraint for each type $i$:

\[
\sum_{l=1}^{L} input_{l,i} \cdot execute_l \leq allocated_i \quad \forall i = 1, \ldots, O
\]

2. Non-negativity constraint for processes:

\[
execute_l \geq 0 \quad \forall l = 1, \ldots, L
\]

\subsection*{Output Information}
The output of the model will provide:
\begin{itemize}
    \item $revenue$: Total revenue for the month
    \item $execute$: Array of numbers of times each process should be executed, $[execute_1, execute_2, \ldots, execute_L]$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse data
data = {
    'O': 2, 'P': 2, 'L': 3,
    'Allocated': [8000, 5000],
    'Price': [38, 33],
    'Input': [[3, 5], [1, 1], [5, 3]],
    'Output': [[4, 3], [1, 1], [3, 4]],
    'Cost': [51, 11, 40]
}

#### Initialize the Problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

#### Decision Variables
execute = [pulp.LpVariable(f"execute_{l+1}", lowBound=0, cat='Continuous') for l in range(data['L'])]

#### Objective Function
revenue_terms = [
    sum(data['Output'][l][p] * data['Price'][p] * execute[l] for l in range(data['L']))
    for p in range(data['P'])
]
cost_terms = [
    data['Cost'][l] * sum(data['Output'][l][p] * execute[l] for p in range(data['P']))
    for l in range(data['L'])
]
problem += sum(revenue_terms) - sum(cost_terms)

#### Constraints
#### Crude oil allocation constraint for each type
for i in range(data['O']):
    problem += sum(data['Input'][l][i] * execute[l] for l in range(data['L'])) <= data['Allocated'][i]

#### Solve the Problem
problem.solve()

#### Outputs
revenue = pulp.value(problem.objective)
execution_values = [pulp.value(execute[l]) for l in range(data['L'])]

#### Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


