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

\section*{Linear Programming Model for Maximizing Profit in Auto Parts Manufacturing}

\subsection*{Sets and Indices}
\begin{description}
    \item[$P$] Set of parts, indexed by $p = 1, 2, \ldots, P$.
    \item[$M$] Set of machines, indexed by $m = 1, 2, \ldots, M$.
\end{description}

\subsection*{Parameters}
\begin{align*}
    & \text{time\_required}_{m,p}: \text{Time in hours required on machine } m \text{ for one batch of part } p. \\
    & \text{cost}_{m}: \text{Cost per hour for operating machine } m. \\
    & \text{available}_{m}: \text{Maximum available hours per month for machine } m. \\
    & \text{price}_{p}: \text{Price per batch of part } p. \\
    & \text{min\_batches}_{p}: \text{Minimum number of batches required for part } p. \\
    & \text{extra\_cost}_{m}: \text{Cost per additional hour for machine } m. \\
    & \text{max\_extra}_{m}: \text{Maximum extra hours purchasable for machine } m.
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & \text{batches}_{p}: \text{Number of batches produced for part } p. \\
    & \text{extra\_time}_{m}: \text{Additional hours purchased for machine } m.
\end{align*}

\subsection*{Objective Function}
Maximize the total profit, which is the total revenue minus the total cost:
\[
\max \sum_{p=1}^{P} (\text{price}_{p} \times \text{batches}_{p}) - 
\sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} (\text{time\_required}_{m,p} \times \text{batches}_{p}) + \text{extra\_cost}_{m} \cdot \text{extra\_time}_{m} \right)
\]

\subsection*{Constraints}
\begin{align*}
    & \text{Machine Time Constraints:} \\
    & \sum_{p=1}^{P} (\text{time\_required}_{m,p} \times \text{batches}_{p}) \leq \text{available}_{m} + \text{extra\_time}_{m}, \quad \forall m = 1, 2, \ldots, M \\
    & \text{Minimum Batch Constraints:} \\
    & \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P \\
    & \text{Extra Time Constraints:} \\
    & 0 \leq \text{extra\_time}_{m} \leq \text{max\_extra}_{m}, \quad \forall m = 1, 2, \ldots, M \\
    & \text{Non-negativity Constraints:} \\
    & \text{batches}_{p} \geq 0, \quad \forall p = 1, 2, \ldots, P
\end{align*}

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

\section*{Linear Programming Model for Maximizing Profit in Auto Parts Manufacturing}

\subsection*{Sets and Indices}
\begin{description}
    \item[$P$] Set of parts, indexed by $p = 1, 2, \ldots, P$.
    \item[$M$] Set of machines, indexed by $m = 1, 2, \ldots, M$.
\end{description}

\subsection*{Parameters}
\begin{align*}
    & \text{time\_required}_{m,p}: \text{Time in hours required on machine } m \text{ for one batch of part } p. \\
    & \text{cost}_{m}: \text{Cost per hour for operating machine } m. \\
    & \text{available}_{m}: \text{Maximum available hours per month for machine } m. \\
    & \text{price}_{p}: \text{Price per batch of part } p. \\
    & \text{min\_batches}_{p}: \text{Minimum number of batches required for part } p. \\
    & \text{extra\_cost}_{m}: \text{Cost per additional hour for machine } m. \\
    & \text{max\_extra}_{m}: \text{Maximum extra hours purchasable for machine } m.
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & \text{batches}_{p}: \text{Number of batches produced for part } p. \\
    & \text{extra\_time}_{m}: \text{Additional hours purchased for machine } m.
\end{align*}

\subsection*{Objective Function}
Maximize the total profit, which is the total revenue minus the total cost:
\[
\max \sum_{p=1}^{P} (\text{price}_{p} \times \text{batches}_{p}) - 
\sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} (\text{time\_required}_{m,p} \times \text{batches}_{p}) + \text{extra\_cost}_{m} \cdot \text{extra\_time}_{m} \right)
\]

\subsection*{Constraints}
\begin{align*}
    & \text{Machine Time Constraints:} \\
    & \sum_{p=1}^{P} (\text{time\_required}_{m,p} \times \text{batches}_{p}) \leq \text{available}_{m} + \text{extra\_time}_{m}, \quad \forall m = 1, 2, \ldots, M \\
    & \text{Minimum Batch Constraints:} \\
    & \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, 2, \ldots, P \\
    & \text{Extra Time Constraints:} \\
    & 0 \leq \text{extra\_time}_{m} \leq \text{max\_extra}_{m}, \quad \forall m = 1, 2, \ldots, M \\
    & \text{Non-negativity Constraints:} \\
    & \text{batches}_{p} \geq 0, \quad \forall p = 1, 2, \ldots, P
\end{align*}

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

#### Constants
P = len(data['prices'])  #### number of parts
M = len(data['machine_costs'])  #### number of machines

#### Problem
problem = pulp.LpProblem("Maximize_Profit_Auto_Parts", pulp.LpMaximize)

#### Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=data['max_extra'][m], cat='Continuous') for m in range(M)]

#### Objective Function
revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
machine_costs = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))
extra_time_costs = pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))
profit = revenue - machine_costs - extra_time_costs

problem += profit

#### Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]

#### Solve the problem
problem.solve()

#### Output Results
print(f'Optimal Value (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

