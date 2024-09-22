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
- Machine \var{1} is being outsourced so that the manufacturer must pay for the labor.
- The labor costs $\var{standard_cost}/h up to \var{overtime_hour} hours, after which it costs $\var{overtime_cost}/h due to overtime.
- Individual availability conditions for Machine \var{1} can be disregarded.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour
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

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( time_{m,p} \) be the hours required on machine \( m \) to produce a batch of 100 parts of type \( p \).
    \item Let \( cost_{m} \) be the cost per hour of using machine \( m \).
    \item Let \( available_{m} \) be the maximum available hours per month for machine \( m \).
    \item Let \( price_{p} \) be the selling price per batch of part \( p \).
    \item Let \( min\_batches_{p} \) be the minimum number of batches of part \( p \) that must be produced each month.
    \item Let \( standard\_cost \) be the standard labor cost per hour.
    \item Let \( overtime\_cost \) be the overtime labor cost per hour.
    \item Let \( overtime\_hour \) be the number of hours after which overtime costs apply.
\end{itemize}

\subsection*{Decision Variables}
Let \( batches_{p} \) be the number of batches produced for part \( p \).

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}))
\]

\subsection*{Constraints}
1. Production constraints for each part:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, \ldots, P\}
\]

2. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m \in \{2, \ldots, M\}
\]

3. Labor cost constraints for Machine 1:
\begin{align*}
\text{Let } T & = \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) \\
\text{If } T & \leq overtime\_hour: \\
\text{Cost} & = standard\_cost \cdot T \\
\text{If } T & > overtime\_hour: \\
\text{Cost} & = standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (T - overtime\_hour)
\end{align*}

\subsection*{Non-negativity Constraints}
\[
batches_{p} \geq 0, \quad \forall p \in \{1, \ldots, P\}
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item \( batches_{p} \) for \( p \in \{1, \ldots, P\} \)
    \item \( total\_profit \) defined as:
\[
total\_profit = Z
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

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( time_{m,p} \) be the hours required on machine \( m \) to produce a batch of 100 parts of type \( p \).
    \item Let \( cost_{m} \) be the cost per hour of using machine \( m \).
    \item Let \( available_{m} \) be the maximum available hours per month for machine \( m \).
    \item Let \( price_{p} \) be the selling price per batch of part \( p \).
    \item Let \( min\_batches_{p} \) be the minimum number of batches of part \( p \) that must be produced each month.
    \item Let \( standard\_cost \) be the standard labor cost per hour.
    \item Let \( overtime\_cost \) be the overtime labor cost per hour.
    \item Let \( overtime\_hour \) be the number of hours after which overtime costs apply.
\end{itemize}

\subsection*{Decision Variables}
Let \( batches_{p} \) be the number of batches produced for part \( p \).

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}))
\]

\subsection*{Constraints}
1. Production constraints for each part:
\[
batches_{p} \geq min\_batches_{p}, \quad \forall p \in \{1, \ldots, P\}
\]

2. Machine availability constraints:
\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m \in \{2, \ldots, M\}
\]

3. Labor cost constraints for Machine 1:
\begin{align*}
\text{Let } T & = \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) \\
\text{If } T & \leq overtime\_hour: \\
\text{Cost} & = standard\_cost \cdot T \\
\text{If } T & > overtime\_hour: \\
\text{Cost} & = standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (T - overtime\_hour)
\end{align*}

\subsection*{Non-negativity Constraints}
\[
batches_{p} \geq 0, \quad \forall p \in \{1, \ldots, P\}
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item \( batches_{p} \) for \( p \in \{1, \ldots, P\} \)
    \item \( total\_profit \) defined as:
\[
total\_profit = Z
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data_json = '''{
    "NumMachines": 3,
    "NumParts": 4,
    "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "MachineCosts": [160, 10, 15],
    "Availability": [200, 300, 500],
    "Prices": [570, 250, 585, 430],
    "MinBatches": [10, 10, 10, 10],
    "StandardCost": 20,
    "OvertimeCost": 30,
    "OvertimeHour": [400, 400, 300]
}'''
data = json.loads(data_json)

#### Parameters
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += profit

#### Constraints
#### Production constraints for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_constraint_part_{p}"

#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_constraint_machine_{m}"

#### Labor cost constraints for Machine 1
T = pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])
problem += (T <= overtime_hour[0]) | (standard_cost * T + overtime_cost * (T - overtime_hour[0]) >= 0), "Machine_1_Cost_Constraint"

#### Solve the problem
problem.solve()

#### Output results
batches_solution = {p: batches[p].varValue for p in range(P)}
total_profit = pulp.value(problem.objective)

print("Batches Produced:", batches_solution)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

