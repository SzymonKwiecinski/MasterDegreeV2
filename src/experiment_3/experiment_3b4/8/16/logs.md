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
To solve this problem, we need to develop a linear programming model that maximizes the total revenue for the oil refinery manager. The decision variables will represent how many times each production process should be executed. The objective is to maximize the revenue from selling the products minus the production costs. The constraints ensure that the use of crude oil resources does not exceed their allocated amounts. Here's the mathematical formulation for this problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item $i \in \{1, \ldots, O\}$: Index for crude oil types.
    \item $p \in \{1, \ldots, P\}$: Index for products.
    \item $l \in \{1, \ldots, L\}$: Index for production processes.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{allocated}_i$: Available barrels of crude oil type $i$.
    \item $\text{price}_p$: Selling price per barrel of product $p$.
    \item \(\text{input}_{l,i}\): Barrels of crude oil type $i$ used in process $l$.
    \item \(\text{output}_{l,p}\): Barrels of product $p$ produced by process $l$.
    \item \(\text{cost}_l\): Cost per barrel of product produced by process $l$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \(x_l\): Number of times to execute process $l$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{Maximize } z = \sum_{p=1}^{P} \sum_{l=1}^{L} \left( \text{output}_{l,p} \times \text{price}_p - \text{cost}_l \right) x_l
\]

\subsection*{Constraints}
\begin{itemize}
    \item Crude oil allocation constraints:
    \[
    \sum_{l=1}^{L} \text{input}_{l,i} \times x_l \leq \text{allocated}_i, \quad \forall i = 1, \ldots, O
    \]
    \item Non-negativity constraints:
    \[
    x_l \geq 0, \quad \forall l = 1, \ldots, L
    \]
\end{itemize}

\end{document}
```

This linear programming model captures the essence of the problem, where the objective function represents the net revenue from the production processes. The constraints ensure that the consumption of each type of crude oil does not exceed its available allocation, and the decision variables are non-negative, reflecting the nonnegative nature of process execution frequency.

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item $i \in \{1, \ldots, O\}$: Index for crude oil types.
    \item $p \in \{1, \ldots, P\}$: Index for products.
    \item $l \in \{1, \ldots, L\}$: Index for production processes.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{allocated}_i$: Available barrels of crude oil type $i$.
    \item $\text{price}_p$: Selling price per barrel of product $p$.
    \item \(\text{input}_{l,i}\): Barrels of crude oil type $i$ used in process $l$.
    \item \(\text{output}_{l,p}\): Barrels of product $p$ produced by process $l$.
    \item \(\text{cost}_l\): Cost per barrel of product produced by process $l$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \(x_l\): Number of times to execute process $l$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{Maximize } z = \sum_{p=1}^{P} \sum_{l=1}^{L} \left( \text{output}_{l,p} \times \text{price}_p - \text{cost}_l \right) x_l
\]

\subsection*{Constraints}
\begin{itemize}
    \item Crude oil allocation constraints:
    \[
    \sum_{l=1}^{L} \text{input}_{l,i} \times x_l \leq \text{allocated}_i, \quad \forall i = 1, \ldots, O
    \]
    \item Non-negativity constraints:
    \[
    x_l \geq 0, \quad \forall l = 1, \ldots, L
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON input
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

#### Create the linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(data['L'])]

#### Objective function
revenue_terms = [
    sum((data['Output'][l][p] * data['Price'][p] - data['Cost'][l]) * x[l] for l in range(data['L']))
    for p in range(data['P'])
]
problem += pulp.lpSum(revenue_terms)

#### Crude oil allocation constraints
for i in range(data['O']):
    problem += pulp.lpSum(data['Input'][l][i] * x[l] for l in range(data['L'])) <= data['Allocated'][i]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

