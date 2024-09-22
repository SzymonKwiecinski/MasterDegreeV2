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
\begin{itemize}
    \item Let \( b_p \) be the number of batches of part \( p \) produced (for \( p = 1, \ldots, P \)).
    \item Let \( e_m \) be the extra time purchased for machine \( m \) (for \( m = 1, \ldots, M \)).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): hours required on machine \( m \) to produce one batch of part \( p \).
    \item \( \text{cost}_{m} \): cost per hour for using machine \( m \).
    \item \( \text{available}_{m} \): available hours for machine \( m \) per month.
    \item \( \text{price}_{p} \): selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): minimum batches required for part \( p \) to fulfill contracts.
    \item \( \text{extra\_costs}_{m} \): cost of extra hours for machine \( m \).
    \item \( \text{max\_extra}_{m} \): maximum extra hours that can be purchased for machine \( m \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot b_p + e_m \right) \right) - \sum_{m=1}^{M} \left( \text{extra\_costs}_{m} \cdot e_m \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine time constraints:
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot b_p \leq \text{available}_{m} + e_m, \quad \forall m = 1, \ldots, M
    \]
    \item Minimum production constraints:
    \[
    b_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
    \]
    \item Extra time limits:
    \[
    e_m \leq \text{max\_extra}_{m}, \quad \forall m = 1, \ldots, M
    \]
    \item Non-negativity constraints:
    \[
    b_p \geq 0, \quad e_m \geq 0 \quad \forall p = 1, \ldots, P, \, m = 1, \ldots, M
    \]
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
\begin{itemize}
    \item Let \( b_p \) be the number of batches of part \( p \) produced (for \( p = 1, \ldots, P \)).
    \item Let \( e_m \) be the extra time purchased for machine \( m \) (for \( m = 1, \ldots, M \)).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): hours required on machine \( m \) to produce one batch of part \( p \).
    \item \( \text{cost}_{m} \): cost per hour for using machine \( m \).
    \item \( \text{available}_{m} \): available hours for machine \( m \) per month.
    \item \( \text{price}_{p} \): selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): minimum batches required for part \( p \) to fulfill contracts.
    \item \( \text{extra\_costs}_{m} \): cost of extra hours for machine \( m \).
    \item \( \text{max\_extra}_{m} \): maximum extra hours that can be purchased for machine \( m \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot b_p \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot b_p + e_m \right) \right) - \sum_{m=1}^{M} \left( \text{extra\_costs}_{m} \cdot e_m \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine time constraints:
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot b_p \leq \text{available}_{m} + e_m, \quad \forall m = 1, \ldots, M
    \]
    \item Minimum production constraints:
    \[
    b_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
    \]
    \item Extra time limits:
    \[
    e_m \leq \text{max\_extra}_{m}, \quad \forall m = 1, \ldots, M
    \]
    \item Non-negativity constraints:
    \[
    b_p \geq 0, \quad e_m \geq 0 \quad \forall p = 1, \ldots, P, \, m = 1, \ldots, M
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
num_parts = len(prices)
num_machines = len(machine_costs)

batches = [pulp.LpVariable(f'b_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(num_parts)]
extra_time = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(num_machines)]

#### Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)]) - \
         pulp.lpSum([machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) + extra_time[m]) for m in range(num_machines)]) - \
         pulp.lpSum([extra_costs[m] * extra_time[m] for m in range(num_machines)])

problem += profit

#### Constraints
#### Machine time constraints
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m] + extra_time[m]

#### Solve
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

