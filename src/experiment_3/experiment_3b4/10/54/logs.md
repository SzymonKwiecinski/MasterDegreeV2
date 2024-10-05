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

\section*{Linear Programming Model for Maximizing Profit in Auto Parts Manufacturing}

\subsection*{Sets and Indices}
\begin{align*}
P & : \text{Set of parts produced, indexed by } p = 1, 2, \ldots, P \\
M & : \text{Set of machines used, indexed by } m = 1, 2, \ldots, M
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{time\_required}_{m,p} & : \text{Time in hours required by machine } m \text{ to produce 100 parts of part } p \\
\text{machine\_cost}_{m} & : \text{Cost per hour of operating machine } m \\
\text{availability}_{m} & : \text{Total working hours available for machine } m \text{ per month} \\
\text{prices}_{p} & : \text{Selling price per batch (100 parts) of part } p \\
\text{min\_batches}_{p} & : \text{Minimum number of batches required for part } p \text{ per month} \\
\text{standard\_cost} & : \text{Standard labor cost per hour for machine 1} \\
\text{overtime\_cost} & : \text{Overtime labor cost per hour for machine 1} \\
\text{overtime\_hour} & : \text{Threshold hours for overtime on machine 1}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{batches}_{p} & : \text{Number of batches of part } p \text{ to be produced monthly} \quad \forall p \in P \\
\text{hours\_machine1\_standard} & : \text{Standard operational hours for machine 1} \\
\text{hours\_machine1\_overtime} & : \text{Overtime operational hours for machine 1}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit, which is the revenue from selling the parts minus the cost of production:
\begin{align*}
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{prices}_{p} \times \text{batches}_{p} - \left( \sum_{m=2}^{M} \text{machine\_cost}_{m} \times \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_{p} + \text{standard\_cost} \times \text{hours\_machine1\_standard} + \text{overtime\_cost} \times \text{hours\_machine1\_overtime} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{1. Machine Time Constraint for } m = 2, \ldots, M: \\
& \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_{p} \leq \text{availability}_{m} \quad \forall m = 2, \ldots, M \\

\text{2. Machine 1 Time Partitioning:} \\
& \sum_{p=1}^{P} \text{time\_required}_{1,p} \times \text{batches}_{p} = \text{hours\_machine1\_standard} + \text{hours\_machine1\_overtime} \\

\text{3. Overtime Constraint for Machine 1:} \\
& \text{hours\_machine1\_standard} \leq \text{overtime\_hour} \\

\text{4. Contractual Minimum Production:} \\
& \text{batches}_{p} \geq \text{min\_batches}_{p} \quad \forall p = 1, \ldots, P \\

\text{5. Non-negativity:} \\
& \text{batches}_{p} \geq 0, \quad \text{hours\_machine1\_standard} \geq 0, \quad \text{hours\_machine1\_overtime} \geq 0
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
\begin{align*}
P & : \text{Set of parts produced, indexed by } p = 1, 2, \ldots, P \\
M & : \text{Set of machines used, indexed by } m = 1, 2, \ldots, M
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{time\_required}_{m,p} & : \text{Time in hours required by machine } m \text{ to produce 100 parts of part } p \\
\text{machine\_cost}_{m} & : \text{Cost per hour of operating machine } m \\
\text{availability}_{m} & : \text{Total working hours available for machine } m \text{ per month} \\
\text{prices}_{p} & : \text{Selling price per batch (100 parts) of part } p \\
\text{min\_batches}_{p} & : \text{Minimum number of batches required for part } p \text{ per month} \\
\text{standard\_cost} & : \text{Standard labor cost per hour for machine 1} \\
\text{overtime\_cost} & : \text{Overtime labor cost per hour for machine 1} \\
\text{overtime\_hour} & : \text{Threshold hours for overtime on machine 1}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{batches}_{p} & : \text{Number of batches of part } p \text{ to be produced monthly} \quad \forall p \in P \\
\text{hours\_machine1\_standard} & : \text{Standard operational hours for machine 1} \\
\text{hours\_machine1\_overtime} & : \text{Overtime operational hours for machine 1}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit, which is the revenue from selling the parts minus the cost of production:
\begin{align*}
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{prices}_{p} \times \text{batches}_{p} - \left( \sum_{m=2}^{M} \text{machine\_cost}_{m} \times \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_{p} + \text{standard\_cost} \times \text{hours\_machine1\_standard} + \text{overtime\_cost} \times \text{hours\_machine1\_overtime} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{1. Machine Time Constraint for } m = 2, \ldots, M: \\
& \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_{p} \leq \text{availability}_{m} \quad \forall m = 2, \ldots, M \\

\text{2. Machine 1 Time Partitioning:} \\
& \sum_{p=1}^{P} \text{time\_required}_{1,p} \times \text{batches}_{p} = \text{hours\_machine1\_standard} + \text{hours\_machine1\_overtime} \\

\text{3. Overtime Constraint for Machine 1:} \\
& \text{hours\_machine1\_standard} \leq \text{overtime\_hour} \\

\text{4. Contractual Minimum Production:} \\
& \text{batches}_{p} \geq \text{min\_batches}_{p} \quad \forall p = 1, \ldots, P \\

\text{5. Non-negativity:} \\
& \text{batches}_{p} \geq 0, \quad \text{hours\_machine1\_standard} \geq 0, \quad \text{hours\_machine1\_overtime} \geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

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
    'OvertimeHour': 400
}

#### Indices
P = range(data['NumParts'])
M = range(data['NumMachines'])

#### Decision Variables
batches = {p: pulp.LpVariable(f'batches_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in P}
hours_machine1_standard = pulp.LpVariable('hours_machine1_standard', lowBound=0, cat='Continuous')
hours_machine1_overtime = pulp.LpVariable('hours_machine1_overtime', lowBound=0, cat='Continuous')

#### Problem
problem = pulp.LpProblem("Maximize_Profit_Auto_Parts", pulp.LpMaximize)

#### Objective Function
revenue = pulp.lpSum(data['Prices'][p] * batches[p] for p in P)
cost_machines = (pulp.lpSum(data['MachineCosts'][m] * data['TimeRequired'][m][p] * batches[p] for m in range(1, data['NumMachines']) for p in P))
cost_machine1 = data['StandardCost'] * hours_machine1_standard + data['OvertimeCost'] * hours_machine1_overtime

problem += revenue - (cost_machines + cost_machine1), "Total_Profit"

#### Constraints

#### Machine Time Constraint for m = 2, ..., M
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in P) <= data['Availability'][m], f"Machine_Time_Constraint_{m}"

#### Machine 1 Time Partitioning
problem += pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in P) == hours_machine1_standard + hours_machine1_overtime, "Machine_1_Time_Partitioning"

#### Overtime Constraint for Machine 1
problem += hours_machine1_standard <= data['OvertimeHour'], "Overtime_Constraint_Machine_1"

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

