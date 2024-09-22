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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the time required in hours on machine \( m \) to produce a batch of part \( p \).
    \item Let \( \text{cost}_{m} \) be the cost per hour for using machine \( m \).
    \item Let \( \text{available}_{m} \) be the available hours per month for machine \( m \).
    \item Let \( \text{price}_{p} \) be the selling price per batch of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) that must be produced each month.
    \item Let \( \text{standard\_cost} \) be the standard labor cost per hour for machine 1.
    \item Let \( \text{overtime\_cost} \) be the labor cost per hour for overtime.
    \item Let \( \text{overtime\_hour} \) be the number of hours after which overtime applies.
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{batches}_{p} \) be the number of batches of part \( p \) produced each month, for \( p = 1, \ldots, P \).

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \right) - \text{Labor Cost}
\]

Where:
\[
\text{Labor Cost} = \begin{cases}
    \text{standard\_cost} \cdot \text{hours\_used}_{1} & \text{if } \text{hours\_used}_{1} \leq \text{overtime\_hour} \\
    \text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{hours\_used}_{1} - \text{overtime\_hour}) & \text{otherwise}
\end{cases}
\]
with \( \text{hours\_used}_{1} = \sum_{p=1}^{P} \text{time}_{1,p} \cdot \text{batches}_{p} \).

\subsection*{Constraints}
\begin{itemize}
    \item Machine capacity constraints for all machines \( m \):
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
    \]
    
    \item Minimum production constraints for all parts \( p \):
    \[
    \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
    \]
    
    \item Non-negativity constraints:
    \[
    \text{batches}_{p} \geq 0, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The number of batches of each part produced, \( \text{batches}_{p} \).
    \item The total profit obtained for the month, \( \text{total\_profit} \).
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
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the time required in hours on machine \( m \) to produce a batch of part \( p \).
    \item Let \( \text{cost}_{m} \) be the cost per hour for using machine \( m \).
    \item Let \( \text{available}_{m} \) be the available hours per month for machine \( m \).
    \item Let \( \text{price}_{p} \) be the selling price per batch of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) that must be produced each month.
    \item Let \( \text{standard\_cost} \) be the standard labor cost per hour for machine 1.
    \item Let \( \text{overtime\_cost} \) be the labor cost per hour for overtime.
    \item Let \( \text{overtime\_hour} \) be the number of hours after which overtime applies.
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{batches}_{p} \) be the number of batches of part \( p \) produced each month, for \( p = 1, \ldots, P \).

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \right) - \text{Labor Cost}
\]

Where:
\[
\text{Labor Cost} = \begin{cases}
    \text{standard\_cost} \cdot \text{hours\_used}_{1} & \text{if } \text{hours\_used}_{1} \leq \text{overtime\_hour} \\
    \text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{hours\_used}_{1} - \text{overtime\_hour}) & \text{otherwise}
\end{cases}
\]
with \( \text{hours\_used}_{1} = \sum_{p=1}^{P} \text{time}_{1,p} \cdot \text{batches}_{p} \).

\subsection*{Constraints}
\begin{itemize}
    \item Machine capacity constraints for all machines \( m \):
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
    \]
    
    \item Minimum production constraints for all parts \( p \):
    \[
    \text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
    \]
    
    \item Non-negativity constraints:
    \[
    \text{batches}_{p} \geq 0, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The number of batches of each part produced, \( \text{batches}_{p} \).
    \item The total profit obtained for the month, \( \text{total\_profit} \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = '''{
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

#### Load the data
data = json.loads(data)

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
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective Function
hours_used_1 = pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])

labor_cost = pulp.lpSum([
    standard_cost * hours_used_1 if hours_used_1 <= overtime_hour[m]
    else standard_cost * overtime_hour[m] + overtime_cost * (hours_used_1 - overtime_hour[m])
    for m in range(M)
])

total_profit = (pulp.lpSum([prices[p] * batches[p] for p in range(P)]) 
                 - pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]) 
                 - labor_cost)

problem += total_profit, "Total_Profit"

#### Constraints
#### Machine capacity constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], 
                           f"Machine_Capacity_Constraint_{m}")

#### Minimum production constraints
for p in range(P):
    problem += (batches[p] >= min_batches[p], f"Min_Batches_Constraint_{p}")

#### Solve the problem
problem.solve()

#### Output
for p in range(P):
    print(f'Batches of part {p + 1}: {batches[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

