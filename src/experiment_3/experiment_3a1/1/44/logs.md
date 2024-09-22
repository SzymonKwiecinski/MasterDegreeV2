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
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): Time required (in hours) on machine \( m \) to produce one batch of part \( p \).
    \item \( \text{cost}_{m} \): Cost per hour for using machine \( m \).
    \item \( \text{available}_{m} \): Total hours available on machine \( m \) per month.
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum number of batches of part \( p \) required per month.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \right)
\]

\subsection*{Constraints}
1. Machine availability constraints:

\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements:

\[
b_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:

\[
b_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Output}
The output will include:
\begin{itemize}
    \item \( \text{batches} = [b_p \text{ for } p = 1, \ldots, P] \)
    \item \( \text{total\_profit} \)
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
Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): Time required (in hours) on machine \( m \) to produce one batch of part \( p \).
    \item \( \text{cost}_{m} \): Cost per hour for using machine \( m \).
    \item \( \text{available}_{m} \): Total hours available on machine \( m \) per month.
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum number of batches of part \( p \) required per month.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \right)
\]

\subsection*{Constraints}
1. Machine availability constraints:

\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot b_p \right) \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements:

\[
b_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:

\[
b_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Output}
The output will include:
\begin{itemize}
    \item \( \text{batches} = [b_p \text{ for } p = 1, \ldots, P] \)
    \item \( \text{total\_profit} \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

#### Number of parts and machines
P = len(prices)
M = len(machine_costs)

#### Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Decision variables
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective function
profit = pulp.lpSum([prices[p] * b[p] for p in range(P)]) - pulp.lpSum(
    [
        machine_costs[m] * pulp.lpSum([time_required[m][p] * b[p] for p in range(P)])
        for m in range(M)
    ]
)

problem += profit

#### Constraints for machine availability
for m in range(M):
    problem += (
        pulp.lpSum([time_required[m][p] * b[p] for p in range(P)]) <= availability[m]
    )

#### Constraints for minimum production requirements
for p in range(P):
    problem += b[p] >= min_batches[p]

#### Solve the problem
problem.solve()

#### Output results
batches = [b[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'batches = {batches}')
print(f'total_profit = {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

