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

\section*{Mathematical Model for the Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item \( P \): Number of different parts.
    \item \( M \): Number of different machines.
    \item \( \text{time}_{m,p} \): Hours required on machine \( m \) to produce a batch of part \( p \).
    \item \( \text{cost}_{m} \): Cost per hour for using machine \( m \).
    \item \( \text{available}_{m} \): Available hours for machine \( m \) per month.
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum batches of part \( p \) to be produced each month.
    \item \( \text{extra\_costs}_{m} \): Extra cost per hour for machine \( m \).
    \item \( \text{max\_extra}_{m} \): Maximum extra hours that can be purchased for machine \( m \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{batches}_{p} \): Number of batches produced for part \( p \).
    \item \( \text{extra\_time}_{m} \): Additional hours purchased for machine \( m \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} + \text{extra\_time}_{m} \right) \right) - \sum_{m=1}^{M} \left( \text{extra\_costs}_{m} \cdot \text{extra\_time}_{m} \right)
\]

\subsection*{Constraints}
1. **Production Time for Each Machine:**
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} + \text{extra\_time}_{m} \leq \text{available}_{m} + \text{max\_extra}_{m}, \quad \forall m = 1, \ldots, M
\]

2. **Minimum Production Requirement:**
\[
\text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

3. **Non-negativity Constraints:**
\[
\text{batches}_{p} \geq 0, \quad \forall p = 1, \ldots, P
\]
\[
\text{extra\_time}_{m} \geq 0, \quad \forall m = 1, \ldots, M
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

\section*{Mathematical Model for the Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item \( P \): Number of different parts.
    \item \( M \): Number of different machines.
    \item \( \text{time}_{m,p} \): Hours required on machine \( m \) to produce a batch of part \( p \).
    \item \( \text{cost}_{m} \): Cost per hour for using machine \( m \).
    \item \( \text{available}_{m} \): Available hours for machine \( m \) per month.
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum batches of part \( p \) to be produced each month.
    \item \( \text{extra\_costs}_{m} \): Extra cost per hour for machine \( m \).
    \item \( \text{max\_extra}_{m} \): Maximum extra hours that can be purchased for machine \( m \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{batches}_{p} \): Number of batches produced for part \( p \).
    \item \( \text{extra\_time}_{m} \): Additional hours purchased for machine \( m \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} + \text{extra\_time}_{m} \right) \right) - \sum_{m=1}^{M} \left( \text{extra\_costs}_{m} \cdot \text{extra\_time}_{m} \right)
\]

\subsection*{Constraints}
1. **Production Time for Each Machine:**
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} + \text{extra\_time}_{m} \leq \text{available}_{m} + \text{max\_extra}_{m}, \quad \forall m = 1, \ldots, M
\]

2. **Minimum Production Requirement:**
\[
\text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

3. **Non-negativity Constraints:**
\[
\text{batches}_{p} \geq 0, \quad \forall p = 1, \ldots, P
\]
\[
\text{extra\_time}_{m} \geq 0, \quad \forall m = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'time_required': [
        [2, 1, 3, 2],
        [4, 2, 1, 2],
        [6, 2, 1, 2]
    ],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

#### Constants
P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

#### Objective Function
profit = pulp.lpSum(
    [data['prices'][p] * batches[p] for p in range(P)]
) - pulp.lpSum(
    [data['machine_costs'][m] * (pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) + extra_time[m]) for m in range(M)]
) - pulp.lpSum(
    [data['extra_costs'][m] * extra_time[m] for m in range(M)]
)
problem += profit

#### Constraints
#### 1. Production Time for Each Machine
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m] <= data['availability'][m] + data['max_extra'][m]

#### 2. Minimum Production Requirement
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

#### Solve the problem
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

