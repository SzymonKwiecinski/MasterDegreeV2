# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- The division must produce at least \var{min_batches_{p}} batches of part \var{p} each month to fulfill a contract.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): time required on machine \( m \) to produce one batch of part \( p \) (in hours).
    \item \( cost_m \): cost per hour of using machine \( m \).
    \item \( available_m \): available hours of machine \( m \) per month.
    \item \( price_p \): selling price per batch of part \( p \).
    \item \( min\_batches_p \): minimum batches of part \( p \) required to fulfill a contract.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \right)
\]

\subsection*{Constraints}

1. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_m \quad \forall m = 1, 2, \ldots, M
\]

2. Minimum production requirements:
\[
b_p \geq min\_batches_p \quad \forall p = 1, 2, \ldots, P
\]

3. Non-negativity constraints:
\[
b_p \geq 0 \quad \forall p = 1, 2, \ldots, P
\]

\subsection*{Output}
The output will be:
\begin{itemize}
    \item Number of batches produced for each part: \( \{batches_p\} \)
    \item Total profit for the month: \( total\_profit \)
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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Variables}
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{m,p} \): time required on machine \( m \) to produce one batch of part \( p \) (in hours).
    \item \( cost_m \): cost per hour of using machine \( m \).
    \item \( available_m \): available hours of machine \( m \) per month.
    \item \( price_p \): selling price per batch of part \( p \).
    \item \( min\_batches_p \): minimum batches of part \( p \) required to fulfill a contract.
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \right)
\]

\subsection*{Constraints}

1. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot b_p) \leq available_m \quad \forall m = 1, 2, \ldots, M
\]

2. Minimum production requirements:
\[
b_p \geq min\_batches_p \quad \forall p = 1, 2, \ldots, P
\]

3. Non-negativity constraints:
\[
b_p \geq 0 \quad \forall p = 1, 2, \ldots, P
\]

\subsection*{Output}
The output will be:
\begin{itemize}
    \item Number of batches produced for each part: \( \{batches_p\} \)
    \item Total profit for the month: \( total\_profit \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

#### Number of parts and machines
P = len(prices)
M = len(machine_costs)

#### Problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Variables
batches = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit - costs

#### Constraints

#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

#### Minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Output results
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced for each part: {batches_produced}')
print(f'Total Profit (Objective Value): <OBJ>{total_profit}</OBJ>')
```

