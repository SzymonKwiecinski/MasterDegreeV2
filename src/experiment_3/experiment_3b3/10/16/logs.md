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

\section*{Linear Programming Model}

\textbf{Indices:} 
\begin{itemize}
    \item \( i \): index for crude types (1 to \( O \))
    \item \( p \): index for product types (1 to \( P \))
    \item \( l \): index for production processes (1 to \( L \))
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{allocated}_i \): million barrels of crude oil type \( i \) allocated for production
    \item \( \text{price}_p \): selling price per barrel of product \( p \)
    \item \( \text{input}_{l,i} \): barrels of crude type \( i \) required for process \( l \)
    \item \( \text{output}_{l,p} \): barrels of product \( p \) produced by process \( l \)
    \item \( \text{cost}_l \): cost per barrel of product produced by process \( l \)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_l \): number of times process \( l \) is executed
\end{itemize}

\textbf{Objective Function:} 
Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \text{price}_p \cdot \left( \sum_{l=1}^{L} \text{output}_{l,p} \cdot x_l \right) - \sum_{l=1}^{L} \text{cost}_l \cdot \left( \sum_{p=1}^{P} \text{output}_{l,p} \cdot x_l \right)
\]

\textbf{Subject to:}
\begin{equation}
\sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i \quad \forall i = 1, \ldots, O
\end{equation}

\textbf{Non-negativity Constraints:}
\begin{equation}
x_l \geq 0 \quad \forall l = 1, \ldots, L
\end{equation}

\textbf{Output:}
The solution will provide:
\begin{itemize}
    \item \( \text{revenue} \): Total revenue for the month
    \item \( \text{execute}_l \): Number of times that process \( l \) should be executed
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

\section*{Linear Programming Model}

\textbf{Indices:} 
\begin{itemize}
    \item \( i \): index for crude types (1 to \( O \))
    \item \( p \): index for product types (1 to \( P \))
    \item \( l \): index for production processes (1 to \( L \))
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{allocated}_i \): million barrels of crude oil type \( i \) allocated for production
    \item \( \text{price}_p \): selling price per barrel of product \( p \)
    \item \( \text{input}_{l,i} \): barrels of crude type \( i \) required for process \( l \)
    \item \( \text{output}_{l,p} \): barrels of product \( p \) produced by process \( l \)
    \item \( \text{cost}_l \): cost per barrel of product produced by process \( l \)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_l \): number of times process \( l \) is executed
\end{itemize}

\textbf{Objective Function:} 
Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \text{price}_p \cdot \left( \sum_{l=1}^{L} \text{output}_{l,p} \cdot x_l \right) - \sum_{l=1}^{L} \text{cost}_l \cdot \left( \sum_{p=1}^{P} \text{output}_{l,p} \cdot x_l \right)
\]

\textbf{Subject to:}
\begin{equation}
\sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i \quad \forall i = 1, \ldots, O
\end{equation}

\textbf{Non-negativity Constraints:}
\begin{equation}
x_l \geq 0 \quad \forall l = 1, \ldots, L
\end{equation}

\textbf{Output:}
The solution will provide:
\begin{itemize}
    \item \( \text{revenue} \): Total revenue for the month
    \item \( \text{execute}_l \): Number of times that process \( l \) should be executed
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
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
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output = data['Output']
cost = data['Cost']

#### Define the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(L)]

#### Objective Function
revenue = pulp.lpSum(price[p] * pulp.lpSum(output[l][p] * x[l] for l in range(L)) for p in range(P))
cost_total = pulp.lpSum(cost[l] * pulp.lpSum(output[l][p] * x[l] for p in range(P)) for l in range(L))
problem += revenue - cost_total, "Total Revenue"

#### Constraints
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * x[l] for l in range(L)) <= allocated[i], f"Crude_Allocation_{i}"

#### Solve the problem
problem.solve()

#### Output results
execute_times = {f'Process_{l+1}': pulp.value(x[l]) for l in range(L)}
total_revenue = pulp.value(problem.objective)

print("Execute times for each process:")
for process, times in execute_times.items():
    print(f"{process}: {times}")

print(f"Total Revenue (Objective Value): <OBJ>{total_revenue}</OBJ>")
```

