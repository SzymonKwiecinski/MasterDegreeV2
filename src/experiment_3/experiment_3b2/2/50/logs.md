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

\section*{Mathematical Model for Profit Maximization in Auto Parts Manufacturing}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts.
    \item $M$: Number of different machines.
    \item $time_{m,p}$: Time in hours required on machine $m$ to produce a batch of 100 parts $p$.
    \item $cost_{m}$: Cost in dollars per hour for using machine $m$.
    \item $available_{m}$: Maximum available hours per month for machine $m$.
    \item $price_{p}$: Selling price per batch of 100 parts $p$.
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ required to fulfill contract each month.
    \item $extra\_cost_{m}$: Cost in dollars per hour for extra availability of machine $m$.
    \item $max\_extra_{m}$: Maximum extra hours that can be purchased for machine $m$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to produce each month.
    \item $extra\_time_{m}$: Additional hours purchased for machine $m$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) + extra\_cost_{m} \cdot extra\_time_{m} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine time constraints for each machine $m$:
    \[
    \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m} + extra\_time_{m}, \quad \forall m \in \{1, \ldots, M\}
    \]
    \item Minimum batch production for each part $p$:
    \[
    batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, \ldots, P\}
    \]
    \item Limits on extra hours for each machine $m$:
    \[
    0 \leq extra\_time_{m} \leq max\_extra_{m}, \quad \forall m \in \{1, \ldots, M\}
    \]
    \item Non-negativity:
    \[
    batches_{p} \geq 0, \quad \forall p \in \{1, \ldots, P\}
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

\section*{Mathematical Model for Profit Maximization in Auto Parts Manufacturing}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts.
    \item $M$: Number of different machines.
    \item $time_{m,p}$: Time in hours required on machine $m$ to produce a batch of 100 parts $p$.
    \item $cost_{m}$: Cost in dollars per hour for using machine $m$.
    \item $available_{m}$: Maximum available hours per month for machine $m$.
    \item $price_{p}$: Selling price per batch of 100 parts $p$.
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ required to fulfill contract each month.
    \item $extra\_cost_{m}$: Cost in dollars per hour for extra availability of machine $m$.
    \item $max\_extra_{m}$: Maximum extra hours that can be purchased for machine $m$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to produce each month.
    \item $extra\_time_{m}$: Additional hours purchased for machine $m$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) + extra\_cost_{m} \cdot extra\_time_{m} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item Machine time constraints for each machine $m$:
    \[
    \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m} + extra\_time_{m}, \quad \forall m \in \{1, \ldots, M\}
    \]
    \item Minimum batch production for each part $p$:
    \[
    batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, \ldots, P\}
    \]
    \item Limits on extra hours for each machine $m$:
    \[
    0 \leq extra\_time_{m} \leq max\_extra_{m}, \quad \forall m \in \{1, \ldots, M\}
    \]
    \item Non-negativity:
    \[
    batches_{p} \geq 0, \quad \forall p \in \{1, \ldots, P\}
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from the provided JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

#### Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

#### Constants
P = len(prices)
M = len(machine_costs)

#### Create the problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

#### Objective Function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_costs[m] * extra_time[m] for m in range(M))

#### Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m], f"Machine_Time_Constraint_{m}"

for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batch_Constraint_{p}"

for m in range(M):
    problem += extra_time[m] <= max_extra[m], f"Max_Extra_Time_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

