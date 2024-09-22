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

\subsection*{Variables}
Let:
\begin{itemize}
    \item $batches_p$ be the number of batches produced of part $p$, for $p = 1, 2, \ldots, P$.
\end{itemize}

\subsection*{Parameters}
Given:
\begin{itemize}
    \item $time_{m,p}$: time required in hours on machine $m$ to produce one batch of part $p$.
    \item $cost_m$: cost per hour for using machine $m$.
    \item $available_m$: availability in hours per month for machine $m$.
    \item $price_p$: selling price per batch of part $p$.
    \item $min\_batches_p$: minimum number of batches of part $p$ that must be produced.
    \item $standard\_cost$: cost per hour for standard labor.
    \item $overtime\_cost$: cost per hour for overtime labor.
    \item $overtime\_hour$: maximum hours of standard labor before overtime rates apply.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_p \cdot batches_p - \sum_{m=1}^{M} (time_{m,p} \cdot batches_p \cdot cost_m) \right) - \text{Labor Costs}
\]

Where Labor Costs for machine 1 can be calculated as:

\[
\text{Labor Costs} = 
\begin{cases}
standard\_cost \cdot hours & \text{if } hours \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (hours - overtime\_hour) & \text{if } hours > overtime\_hour
\end{cases}
\]

with \( hours = time_{1,p} \cdot batches_p \).

\subsection*{Constraints}
1. Capacity constraints for each machine \( m \):

\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_p) \leq available_m, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements for each part:

\[
batches_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:

\[
batches_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Output}
The output will be:

\begin{itemize}
    \item \( batches_p \): number of batches produced for each part \( p \).
    \item \( total\_profit = Z \): total profit obtained for the month.
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
Let:
\begin{itemize}
    \item $batches_p$ be the number of batches produced of part $p$, for $p = 1, 2, \ldots, P$.
\end{itemize}

\subsection*{Parameters}
Given:
\begin{itemize}
    \item $time_{m,p}$: time required in hours on machine $m$ to produce one batch of part $p$.
    \item $cost_m$: cost per hour for using machine $m$.
    \item $available_m$: availability in hours per month for machine $m$.
    \item $price_p$: selling price per batch of part $p$.
    \item $min\_batches_p$: minimum number of batches of part $p$ that must be produced.
    \item $standard\_cost$: cost per hour for standard labor.
    \item $overtime\_cost$: cost per hour for overtime labor.
    \item $overtime\_hour$: maximum hours of standard labor before overtime rates apply.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_p \cdot batches_p - \sum_{m=1}^{M} (time_{m,p} \cdot batches_p \cdot cost_m) \right) - \text{Labor Costs}
\]

Where Labor Costs for machine 1 can be calculated as:

\[
\text{Labor Costs} = 
\begin{cases}
standard\_cost \cdot hours & \text{if } hours \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (hours - overtime\_hour) & \text{if } hours > overtime\_hour
\end{cases}
\]

with \( hours = time_{1,p} \cdot batches_p \).

\subsection*{Constraints}
1. Capacity constraints for each machine \( m \):

\[
\sum_{p=1}^{P} (time_{m,p} \cdot batches_p) \leq available_m, \quad \forall m = 1, \ldots, M
\]

2. Minimum production requirements for each part:

\[
batches_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraints:

\[
batches_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Output}
The output will be:

\begin{itemize}
    \item \( batches_p \): number of batches produced for each part \( p \).
    \item \( total\_profit = Z \): total profit obtained for the month.
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
data = json.loads('''{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}''')

#### Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

#### Variables
batches = pulp.LpVariable.dicts("Batches", range(data['NumParts']), lowBound=0, cat='Continuous')

#### Objective function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) \
         - pulp.lpSum(pulp.lpSum(data['TimeRequired'][m][p] * batches[p] * data['MachineCosts'][m]
                                   for p in range(data['NumParts'])) for m in range(data['NumMachines']))

#### Labor costs
labor_costs = []
for p in range(data['NumParts']):
    hours = pulp.lpSum(data['TimeRequired'][0][p] * batches[p])
    labor_cost = pulp.lpSum([
        data['StandardCost'] * hours if hours <= data['OvertimeHour'][0] else
        data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (hours - data['OvertimeHour'][0])
    ])
    labor_costs.append(labor_cost)

#### Add labor costs to objective
total_labor_costs = pulp.lpSum(labor_costs)
problem += profit - total_labor_costs, "Total_Profit"

#### Capacity constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Capacity_Constraint_{m+1}"

#### Minimum production requirements
for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p], f"Min_Batches_Constraint_{p+1}"

#### Solve the problem
problem.solve()

#### Output results
for p in range(data['NumParts']):
    print(f'Batches produced for part {p+1}: {batches[p].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

