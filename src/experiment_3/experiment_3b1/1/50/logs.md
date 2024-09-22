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
- Extra available time for machine \var{m} can be acquired at $\var{extra_costs_{m}}/hour. 
- Up to \var{max_extra_{m}} hours can be purchased for each machine \var{m}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "extra_costs": [extra_cost_{m} for m in 1, ..., M],
    "max_extra": [max_extra_{m} for m in 1, ..., M]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{extra_time} denotes the additional hours purchased for each machine \var{m}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "extra_time": [extra_time_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item \( b_p \) = number of batches produced for part \( p = 1, \ldots, P \)
    \item \( e_m \) = extra hours purchased for machine \( m = 1, \ldots, M \)
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \times b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \left( \sum_{p=1}^{P} \text{time}_{m,p} \times b_p \right) + \text{extra\_costs}_m \times e_m \right)
\]

\subsection*{Constraints}
1. Time availability constraints for each machine:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \times b_p + e_m \leq \text{available}_m + \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements for each part:
\[
b_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:
\[
b_p \geq 0, \quad \forall p = 1, \ldots, P
\]
\[
e_m \geq 0, \quad \forall m = 1, \ldots, M
\]

\subsection*{Output}
The output results will include:
\begin{itemize}
    \item The number of batches of each part produced: \( \{ b_p \, | \, p = 1, \ldots, P \} \)
    \item The extra time purchased for each machine: \( \{ e_m \, | \, m = 1, \ldots, M \} \)
    \item The total profit obtained: \( Z \)
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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item \( b_p \) = number of batches produced for part \( p = 1, \ldots, P \)
    \item \( e_m \) = extra hours purchased for machine \( m = 1, \ldots, M \)
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_p \times b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \times \left( \sum_{p=1}^{P} \text{time}_{m,p} \times b_p \right) + \text{extra\_costs}_m \times e_m \right)
\]

\subsection*{Constraints}
1. Time availability constraints for each machine:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \times b_p + e_m \leq \text{available}_m + \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements for each part:
\[
b_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:
\[
b_p \geq 0, \quad \forall p = 1, \ldots, P
\]
\[
e_m \geq 0, \quad \forall m = 1, \ldots, M
\]

\subsection*{Output}
The output results will include:
\begin{itemize}
    \item The number of batches of each part produced: \( \{ b_p \, | \, p = 1, \ldots, P \} \)
    \item The extra time purchased for each machine: \( \{ e_m \, | \, m = 1, \ldots, M \} \)
    \item The total profit obtained: \( Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

#### Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Define the Linear Programming problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

#### Decision Variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  #### Batches produced for each part
e = pulp.LpVariable.dicts("e", range(M), lowBound=0)  #### Extra hours for each machine

#### Objective Function
profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) + e[m]) + extra_costs[m] * e[m] for m in range(M))

problem += profit, "Total_Profit"

#### Constraints
#### Time availability constraints for each machine
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) + e[m] <= availability[m] + max_extra[m], f"Time_Availability_Constraint_{m}"

#### Minimum production requirements for each part
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Production_Requirement_Constraint_{p}"

#### Solve the problem
problem.solve()

#### Output Results
produced_batches = [b[p].varValue for p in range(P)]
extra_hours = [e[m].varValue for m in range(M)]

print(f'Produced batches: {produced_batches}')
print(f'Extra hours purchased: {extra_hours}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

