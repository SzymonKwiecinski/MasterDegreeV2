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

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time (in hours) required on machine $m$ to produce a batch of part $p$
    \item $cost_{m}$: Cost (per hour) for using machine $m$
    \item $available_{m}$: Availability (in hours) of machine $m$ per month
    \item $price_{p}$: Selling price (per batch) of part $p$
    \item $min\_batches_{p}$: Minimum batches of part $p$ required to fulfill the contract
    \item $extra\_costs_{m}$: Cost (per hour) for acquiring extra time for machine $m$
    \item $max\_extra_{m}$: Maximum extra hours that can be purchased for machine $m$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ produced (for $p = 1, \ldots, P$)
    \item $extra\_time_{m}$: Additional hours purchased for machine $m$ (for $m = 1, \ldots, M$)
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot batches_p) - \sum_{m=1}^{M} (cost_m \cdot (available_m + extra\_time_m)) - \sum_{m=1}^{M} (extra\_costs_m \cdot extra\_time_m)
\]

\subsection*{Constraints}
1. Production Constraints:
\[
batches_p \geq min\_batches_p \quad \forall p \in \{1, \ldots, P\}
\]

2. Machine Availability Constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_p) \leq available_m + extra\_time_m \quad \forall m \in \{1, \ldots, M\}
\]

3. Extra Time Purchase Constraints:
\[
extra\_time_m \leq max\_extra_m \quad \forall m \in \{1, \ldots, M\}
\]

4. Non-negativity Constraints:
\[
batches_p \geq 0 \quad \forall p \in \{1, \ldots, P\}
\]
\[
extra\_time_m \geq 0 \quad \forall m \in \{1, \ldots, M\}
\]

\subsection*{Output Variables}
The solution will include:
\begin{itemize}
    \item Batches produced for each part: $batches = [batches_p \text{ for } p = 1, \ldots, P]$
    \item Extra time purchased for each machine: $extra\_time = [extra\_time_m \text{ for } m = 1, \ldots, M]$
    \item Total profit obtained: $total\_profit = Z$
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

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time (in hours) required on machine $m$ to produce a batch of part $p$
    \item $cost_{m}$: Cost (per hour) for using machine $m$
    \item $available_{m}$: Availability (in hours) of machine $m$ per month
    \item $price_{p}$: Selling price (per batch) of part $p$
    \item $min\_batches_{p}$: Minimum batches of part $p$ required to fulfill the contract
    \item $extra\_costs_{m}$: Cost (per hour) for acquiring extra time for machine $m$
    \item $max\_extra_{m}$: Maximum extra hours that can be purchased for machine $m$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ produced (for $p = 1, \ldots, P$)
    \item $extra\_time_{m}$: Additional hours purchased for machine $m$ (for $m = 1, \ldots, M$)
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_p \cdot batches_p) - \sum_{m=1}^{M} (cost_m \cdot (available_m + extra\_time_m)) - \sum_{m=1}^{M} (extra\_costs_m \cdot extra\_time_m)
\]

\subsection*{Constraints}
1. Production Constraints:
\[
batches_p \geq min\_batches_p \quad \forall p \in \{1, \ldots, P\}
\]

2. Machine Availability Constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_p) \leq available_m + extra\_time_m \quad \forall m \in \{1, \ldots, M\}
\]

3. Extra Time Purchase Constraints:
\[
extra\_time_m \leq max\_extra_m \quad \forall m \in \{1, \ldots, M\}
\]

4. Non-negativity Constraints:
\[
batches_p \geq 0 \quad \forall p \in \{1, \ldots, P\}
\]
\[
extra\_time_m \geq 0 \quad \forall m \in \{1, \ldots, M\}
\]

\subsection*{Output Variables}
The solution will include:
\begin{itemize}
    \item Batches produced for each part: $batches = [batches_p \text{ for } p = 1, \ldots, P]$
    \item Extra time purchased for each machine: $extra\_time = [extra\_time_m \text{ for } m = 1, \ldots, M]$
    \item Total profit obtained: $total\_profit = Z$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

P = len(data['min_batches'])
M = len(data['machine_costs'])

#### Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, cat='Continuous') for m in range(M)]

#### Objective Function
total_profit = (
    pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) 
    - pulp.lpSum(data['machine_costs'][m] * (data['availability'][m] + extra_time[m]) for m in range(M))
    - pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))
)
problem += total_profit

#### Constraints
#### Production Constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

#### Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]

#### Extra Time Purchase Constraints
for m in range(M):
    problem += extra_time[m] <= data['max_extra'][m]

#### Solve the problem
problem.solve()

#### Output
print("Batches produced for each part:")
for p in range(P):
    print(f"Part {p + 1}: {batches[p].varValue}")

print("\nExtra time purchased for each machine:")
for m in range(M):
    print(f"Machine {m + 1}: {extra_time[m].varValue}")

print(f"\nTotal Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

