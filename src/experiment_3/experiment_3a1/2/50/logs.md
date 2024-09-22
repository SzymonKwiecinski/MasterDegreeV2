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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Variables}
Let:
\begin{itemize}
    \item $b_p$ = number of batches produced of part $p$ for $p = 1, \ldots, P$.
    \item $extra_m$ = additional hours purchased for machine $m$ for $m = 1, \ldots, M$.
\end{itemize}

\subsection*{Parameters}
The parameters are as follows:
\begin{itemize}
    \item $time_{m,p}$ = time required (in hours) for machine $m$ to produce a batch of part $p$.
    \item $cost_m$ = cost per hour for using machine $m$.
    \item $available_m$ = available hours per month for machine $m$.
    \item $price_p$ = price per batch for part $p$.
    \item $min\_batches_p$ = minimum number of batches required for part $p$.
    \item $extra\_costs_m$ = cost per hour for extra time on machine $m$.
    \item $max\_extra_m$ = maximum extra hours that can be purchased for machine $m$.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^P \left( price_p \cdot b_p - \sum_{m=1}^M (cost_m \cdot time_{m,p} \cdot b_p + extra\_costs_m \cdot extra_m) \right)
\]

\subsection*{Constraints}
1. **Production Requirement**: Each part must satisfy the minimum batch requirement:
\[
b_p \geq min\_batches_p \quad \forall p = 1, \ldots, P
\]

2. **Machine Time Availability**: The total time used on each machine must not exceed the available time plus any extra time purchased. For each machine $m$:
\[
\sum_{p=1}^P time_{m,p} \cdot b_p \leq available_m + extra_m \quad \forall m = 1, \ldots, M
\]

3. **Extra Time Limit**: The extra time purchased for each machine must not exceed the maximum extra hours allowed:
\[
extra_m \leq max\_extra_m \quad \forall m = 1, \ldots, M
\]

4. **Non-negativity**: The number of batches produced and extra time must be non-negative:
\[
b_p \geq 0 \quad \text{and} \quad extra_m \geq 0 \quad \forall p = 1, \ldots, P \text{ and } m = 1, \ldots, M
\]

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
Let:
\begin{itemize}
    \item $b_p$ = number of batches produced of part $p$ for $p = 1, \ldots, P$.
    \item $extra_m$ = additional hours purchased for machine $m$ for $m = 1, \ldots, M$.
\end{itemize}

\subsection*{Parameters}
The parameters are as follows:
\begin{itemize}
    \item $time_{m,p}$ = time required (in hours) for machine $m$ to produce a batch of part $p$.
    \item $cost_m$ = cost per hour for using machine $m$.
    \item $available_m$ = available hours per month for machine $m$.
    \item $price_p$ = price per batch for part $p$.
    \item $min\_batches_p$ = minimum number of batches required for part $p$.
    \item $extra\_costs_m$ = cost per hour for extra time on machine $m$.
    \item $max\_extra_m$ = maximum extra hours that can be purchased for machine $m$.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^P \left( price_p \cdot b_p - \sum_{m=1}^M (cost_m \cdot time_{m,p} \cdot b_p + extra\_costs_m \cdot extra_m) \right)
\]

\subsection*{Constraints}
1. **Production Requirement**: Each part must satisfy the minimum batch requirement:
\[
b_p \geq min\_batches_p \quad \forall p = 1, \ldots, P
\]

2. **Machine Time Availability**: The total time used on each machine must not exceed the available time plus any extra time purchased. For each machine $m$:
\[
\sum_{p=1}^P time_{m,p} \cdot b_p \leq available_m + extra_m \quad \forall m = 1, \ldots, M
\]

3. **Extra Time Limit**: The extra time purchased for each machine must not exceed the maximum extra hours allowed:
\[
extra_m \leq max\_extra_m \quad \forall m = 1, \ldots, M
\]

4. **Non-negativity**: The number of batches produced and extra time must be non-negative:
\[
b_p \geq 0 \quad \text{and} \quad extra_m \geq 0 \quad \forall p = 1, \ldots, P \text{ and } m = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

#### Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Define variables
P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Decision variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0)  #### b_p
extra_hours = pulp.LpVariable.dicts("extra", range(M), lowBound=0)  #### extra_m

#### Objective function
profit = pulp.lpSum((data['prices'][p] * batches[p] - 
                     pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * batches[p] 
                     for m in range(M)) - 
                     pulp.lpSum(data['extra_costs'][m] * extra_hours[m] for m in range(M))) 
                    for p in range(P))
problem += profit, "Total_Profit"

#### Constraints
#### Minimum batch requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}"

#### Machine time availability
for m in range(M):
    problem += (pulp.lpSum(data['time_required[m][p]'] * batches[p] for p in range(P)) <= 
                 data['availability'][m] + extra_hours[m]), f"Machine_Time_Availability_{m}"

#### Extra time limit
for m in range(M):
    problem += extra_hours[m] <= data['max_extra'][m], f"Extra_Time_Limit_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

