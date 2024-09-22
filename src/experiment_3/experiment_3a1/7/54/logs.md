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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Sets and Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the time required on machine \( m \) to produce a batch of part \( p \) (in hours).
    \item Let \( \text{cost}_{m} \) be the cost per hour of using machine \( m \).
    \item Let \( \text{available}_{m} \) be the available hours for machine \( m \) per month.
    \item Let \( \text{price}_{p} \) be the selling price per batch of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) that must be produced.
    \item Let \( \text{standard\_cost} \) be the standard labor cost per hour.
    \item Let \( \text{overtime\_cost} \) be the overtime labor cost per hour.
    \item Let \( \text{overtime\_hour} \) be the number of hours before overtime rates apply.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{batches}_{p} \) be the number of batches produced for part \( p \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \text{hours}_{m} \right)
\]

where
\[
\text{hours}_{m} = \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot \text{batches}_{p} \right)
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot \text{batches}_{p} \right) \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements:
\[
\text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

3. Labor cost considerations for Machine 1:
\[
\text{Labor Cost} =
\begin{cases} 
\text{standard\_cost} \cdot \text{hours}_{1}, & \text{if } \text{hours}_{1} \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{hours}_{1} - \text{overtime\_hour}), & \text{if } \text{hours}_{1} > \text{overtime\_hour}
\end{cases}
\]

4. Non-negativity constraints:
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

\section*{Linear Programming Model for Auto Parts Manufacturing}

\subsection*{Sets and Parameters}
\begin{itemize}
    \item Let \( P \) be the number of different parts.
    \item Let \( M \) be the number of different machines.
    \item Let \( \text{time}_{m,p} \) be the time required on machine \( m \) to produce a batch of part \( p \) (in hours).
    \item Let \( \text{cost}_{m} \) be the cost per hour of using machine \( m \).
    \item Let \( \text{available}_{m} \) be the available hours for machine \( m \) per month.
    \item Let \( \text{price}_{p} \) be the selling price per batch of part \( p \).
    \item Let \( \text{min\_batches}_{p} \) be the minimum number of batches of part \( p \) that must be produced.
    \item Let \( \text{standard\_cost} \) be the standard labor cost per hour.
    \item Let \( \text{overtime\_cost} \) be the overtime labor cost per hour.
    \item Let \( \text{overtime\_hour} \) be the number of hours before overtime rates apply.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{batches}_{p} \) be the number of batches produced for part \( p \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot \text{batches}_{p} \right) - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \text{hours}_{m} \right)
\]

where
\[
\text{hours}_{m} = \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot \text{batches}_{p} \right)
\]

\subsection*{Constraints}
1. Machine availability constraints:
\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot \text{batches}_{p} \right) \leq \text{available}_{m}, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements:
\[
\text{batches}_{p} \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

3. Labor cost considerations for Machine 1:
\[
\text{Labor Cost} =
\begin{cases} 
\text{standard\_cost} \cdot \text{hours}_{1}, & \text{if } \text{hours}_{1} \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (\text{hours}_{1} - \text{overtime\_hour}), & \text{if } \text{hours}_{1} > \text{overtime\_hour}
\end{cases}
\]

4. Non-negativity constraints:
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

#### Data
data = {
    'NumMachines': 3, 
    'NumParts': 4, 
    'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'MachineCosts': [160, 10, 15], 
    'Availability': [200, 300, 500], 
    'Prices': [570, 250, 585, 430], 
    'MinBatches': [10, 10, 10, 10], 
    'StandardCost': 20, 
    'OvertimeCost': 30, 
    'OvertimeHour': [400, 400, 300]
}

#### Initialize the problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(data['NumParts']), lowBound=0)

#### Objective Function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) 
cost = pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines']))
problem += profit - cost

#### Constraints
#### Machine availability constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]

#### Minimum production requirements
for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p]

#### Define labor cost for Machine 1
hours_m1 = pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(data['NumParts']))
labor_cost_m1 = data['StandardCost'] * hours_m1

#### Handling overtime
overtime_hours_m1 = hours_m1 - data['OvertimeHour'][0]
problem += labor_cost_m1 <= (data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (overtime_hours_m1)) if hours_m1 > data['OvertimeHour'][0] else data['StandardCost'] * hours_m1

#### Solve the problem
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

