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

\section*{Mathematical Model for Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce a batch of 100 parts $p$
    \item $cost_{m}$: Cost per hour for using machine $m$
    \item $available_{m}$: Availability of machine $m$ (in hours per month)
    \item $price_{p}$: Selling price per batch of part $p$
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ to be produced
    \item $standard\_cost$: Standard labor cost per hour
    \item $overtime\_cost$: Overtime labor cost per hour
    \item $overtime\_hour$: Overtime limit in hours
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ produced
    \item $overtime\_hours$: Overtime hours used
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} - \sum_{m=1}^{M} (cost_{m} \cdot time_{m,p} \cdot batches_{p}) \right) - (standard\_cost \cdot overtime\_hours + overtime\_cost \cdot max(0, overtime\_hours - overtime\_hour))
\]

\subsection*{Constraints}
\begin{itemize}
    \item Production constraints for each part:
    \[
    batches_{p} \geq min\_batches_{p} \quad \forall p \in \{1, \ldots, P\}
    \]
    \item Machine availability constraints:
    \[
    \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} \leq available_{m} \quad \forall m \in \{1, \ldots, M\}
    \]
\end{itemize}

\subsection*{Output}
The output consists of:
\begin{itemize}
    \item The number of batches produced of each part: $batches_{p}$
    \item The total profit: $total\_profit = Z$
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

\section*{Mathematical Model for Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required (in hours) on machine $m$ to produce a batch of 100 parts $p$
    \item $cost_{m}$: Cost per hour for using machine $m$
    \item $available_{m}$: Availability of machine $m$ (in hours per month)
    \item $price_{p}$: Selling price per batch of part $p$
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ to be produced
    \item $standard\_cost$: Standard labor cost per hour
    \item $overtime\_cost$: Overtime labor cost per hour
    \item $overtime\_hour$: Overtime limit in hours
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ produced
    \item $overtime\_hours$: Overtime hours used
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} - \sum_{m=1}^{M} (cost_{m} \cdot time_{m,p} \cdot batches_{p}) \right) - (standard\_cost \cdot overtime\_hours + overtime\_cost \cdot max(0, overtime\_hours - overtime\_hour))
\]

\subsection*{Constraints}
\begin{itemize}
    \item Production constraints for each part:
    \[
    batches_{p} \geq min\_batches_{p} \quad \forall p \in \{1, \ldots, P\}
    \]
    \item Machine availability constraints:
    \[
    \sum_{p=1}^{P} time_{m,p} \cdot batches_{p} \leq available_{m} \quad \forall m \in \{1, \ldots, M\}
    \]
\end{itemize}

\subsection*{Output}
The output consists of:
\begin{itemize}
    \item The number of batches produced of each part: $batches_{p}$
    \item The total profit: $total\_profit = Z$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

#### Parameters
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour_limits = data['OvertimeHour']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')
overtime_hours = pulp.LpVariable("Overtime_Hours", lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) \
         - pulp.lpSum(costs[m] * time_required[m][p] * batches[p] for p in range(P) for m in range(M)) \
         - (standard_cost * overtime_hours + overtime_cost * pulp.max(0, overtime_hours - pulp.lpSum(overtime_hour_limits)))
problem += profit, "Total_Profit"

#### Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m}"

#### Solve the problem
problem.solve()

#### Output results
for p in range(P):
    print(f'Batches produced for part {p}: {batches[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

