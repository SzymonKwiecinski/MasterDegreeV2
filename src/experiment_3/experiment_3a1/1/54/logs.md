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
    \item \( \text{time}_{m,p} \): Time required (in hours) on machine \( m \) to produce a batch of part \( p \).
    \item \( \text{cost}_{m} \): Cost per hour of using machine \( m \).
    \item \( \text{available}_{m} \): Availability of machine \( m \) (in hours) per month.
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum number of batches required for part \( p \) to fulfill a contract.
    \item \( \text{standard\_cost} \): Standard labor cost per hour for machine 1.
    \item \( \text{overtime\_cost} \): Overtime labor cost per hour for machine 1.
    \item \( \text{overtime\_hour} \): Number of hours before overtime costs are incurred.
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{batches}_{p} \) be the number of batches produced for part \( p \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \text{time}_{m,p} \cdot \sum_{p=1}^{P} \text{batches}_{p} \right) - \left( \text{labor cost for machine 1} \right)
\]

Where labor cost for machine 1 is defined as:
\[
\text{labor cost for machine 1} = \begin{cases}
\text{standard\_cost} \times \text{hours} & \text{if } \text{hours} \leq \text{overtime\_hour} \\
\text{standard\_cost} \times \text{overtime\_hour} + \text{overtime\_cost} \times (\text{hours} - \text{overtime\_hour}) & \text{if } \text{hours} > \text{overtime\_hour}
\end{cases}
\]

\subsection*{Subject to the Constraints}
1. Machine time constraint for machine \( m \):
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirement:
\[
\text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:
\[
\text{batches}_{p} \geq 0, \quad \forall p = 1, \ldots, P
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

\subsection*{Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item \( \text{time}_{m,p} \): Time required (in hours) on machine \( m \) to produce a batch of part \( p \).
    \item \( \text{cost}_{m} \): Cost per hour of using machine \( m \).
    \item \( \text{available}_{m} \): Availability of machine \( m \) (in hours) per month.
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum number of batches required for part \( p \) to fulfill a contract.
    \item \( \text{standard\_cost} \): Standard labor cost per hour for machine 1.
    \item \( \text{overtime\_cost} \): Overtime labor cost per hour for machine 1.
    \item \( \text{overtime\_hour} \): Number of hours before overtime costs are incurred.
\end{itemize}

\subsection*{Decision Variables}
Let \( \text{batches}_{p} \) be the number of batches produced for part \( p \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \text{time}_{m,p} \cdot \sum_{p=1}^{P} \text{batches}_{p} \right) - \left( \text{labor cost for machine 1} \right)
\]

Where labor cost for machine 1 is defined as:
\[
\text{labor cost for machine 1} = \begin{cases}
\text{standard\_cost} \times \text{hours} & \text{if } \text{hours} \leq \text{overtime\_hour} \\
\text{standard\_cost} \times \text{overtime\_hour} + \text{overtime\_cost} \times (\text{hours} - \text{overtime\_hour}) & \text{if } \text{hours} > \text{overtime\_hour}
\end{cases}
\]

\subsection*{Subject to the Constraints}
1. Machine time constraint for machine \( m \):
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot \text{batches}_{p} \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirement:
\[
\text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:
\[
\text{batches}_{p} \geq 0, \quad \forall p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load the data
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

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

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])  #### Total revenue
machine_cost = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])  #### Total machine cost
labor_cost = pulp.lpSum([pulp.lpSum([standard_cost * min(availability[m] / sum(time_required[m][p] * batches[p] for p in range(P)), overtime_hour[m]) + \
                                       overtime_cost * (availability[m] / sum(time_required[m][p] * batches[p] for p in range(P)) - overtime_hour[m])
                                       for m in range(M)])])

problem += profit - machine_cost - labor_cost, "Total_Profit"

#### Constraints
#### Machine time constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_Availability_{m}"

#### Minimum production requirement
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

