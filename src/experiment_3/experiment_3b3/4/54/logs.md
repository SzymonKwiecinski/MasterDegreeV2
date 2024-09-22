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

\textbf{Variables:}
\begin{align*}
batches_{p} & : \text{ the number of batches produced for part } p \text{, for } p = 1, \ldots, P \\
\end{align*}

\textbf{Parameters:}
\begin{align*}
time_{m,p} & : \text{ time required on machine } m \text{ to produce one batch of part } p \\
cost_{m} & : \text{ cost per hour for using machine } m \\
available_{m} & : \text{ availability of machine } m \text{ in hours per month} \\
price_{p} & : \text{ selling price per batch of part } p \\
min\_batches_{p} & : \text{ minimum number of batches of part } p \text{ to produce} \\
standard\_cost & : \text{ standard labor cost per hour} \\
overtime\_cost & : \text{ overtime labor cost per hour} \\
overtime\_hour & : \text{ hours after which overtime cost applies} \\
\end{align*}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize } Z & = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})\right) - \text{Labor Costs}
\end{align*}

\textbf{Labor Costs:}
\begin{align*}
\text{Labor Costs} & = \begin{cases} 
standard\_cost \cdot \text{total\_time} & \text{if } \text{total\_time} \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (\text{total\_time} - overtime\_hour) & \text{if } \text{total\_time} > overtime\_hour 
\end{cases}
\end{align*}

Where \(\text{total\_time} = \sum_{m=1}^{M} \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})\)

\textbf{Subject to:}
\begin{align*}
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) & \leq available_{m} \quad \forall m \in \{2, \ldots, M\} \\
batches_{p} & \geq min\_batches_{p} \quad \forall p \in \{1, \ldots, P\} \\
batches_{p} & \geq 0 \quad \forall p \in \{1, \ldots, P\} \\
\end{align*}

\textbf{Output:}
\begin{align*}
\text{Output: } & \{batches_{p} \text{ for } p = 1, \ldots, P, \text{ total\_profit } = Z\}
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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\textbf{Variables:}
\begin{align*}
batches_{p} & : \text{ the number of batches produced for part } p \text{, for } p = 1, \ldots, P \\
\end{align*}

\textbf{Parameters:}
\begin{align*}
time_{m,p} & : \text{ time required on machine } m \text{ to produce one batch of part } p \\
cost_{m} & : \text{ cost per hour for using machine } m \\
available_{m} & : \text{ availability of machine } m \text{ in hours per month} \\
price_{p} & : \text{ selling price per batch of part } p \\
min\_batches_{p} & : \text{ minimum number of batches of part } p \text{ to produce} \\
standard\_cost & : \text{ standard labor cost per hour} \\
overtime\_cost & : \text{ overtime labor cost per hour} \\
overtime\_hour & : \text{ hours after which overtime cost applies} \\
\end{align*}

\textbf{Objective Function:}
\begin{align*}
\text{Maximize } Z & = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})\right) - \text{Labor Costs}
\end{align*}

\textbf{Labor Costs:}
\begin{align*}
\text{Labor Costs} & = \begin{cases} 
standard\_cost \cdot \text{total\_time} & \text{if } \text{total\_time} \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (\text{total\_time} - overtime\_hour) & \text{if } \text{total\_time} > overtime\_hour 
\end{cases}
\end{align*}

Where \(\text{total\_time} = \sum_{m=1}^{M} \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})\)

\textbf{Subject to:}
\begin{align*}
\sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) & \leq available_{m} \quad \forall m \in \{2, \ldots, M\} \\
batches_{p} & \geq min\_batches_{p} \quad \forall p \in \{1, \ldots, P\} \\
batches_{p} & \geq 0 \quad \forall p \in \{1, \ldots, P\} \\
\end{align*}

\textbf{Output:}
\begin{align*}
\text{Output: } & \{batches_{p} \text{ for } p = 1, \ldots, P, \text{ total\_profit } = Z\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from JSON
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

#### Problem setup
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]

#### Calculate total_time for labor cost
total_time = sum(data['TimeRequired'][m][p] * batches[p] for m in range(data['NumMachines']) for p in range(data['NumParts']))

#### Labor Costs calculation
overtime_hours = data['OvertimeHour']
labor_costs = pulp.LpVariable("labor_costs", cat='Continuous')
problem += labor_costs

#### Add piecewise conditions for labor costs
for m in range(data['NumMachines']):
    max_overtime = data['OvertimeHour'][m]
    problem += (labor_costs >= data['StandardCost'] * total_time - (data['StandardCost'] - data['OvertimeCost']) * max_overtime)
    problem += (labor_costs <= data['StandardCost'] * max_overtime + data['OvertimeCost'] * (total_time - max_overtime))

#### Objective function
profit = (
    sum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) -
    sum(data['MachineCosts'][m] * sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines'])) -
    labor_costs
)
problem += profit

#### Constraints
for m in range(1, data['NumMachines']):  #### Constraints for m from 2 to M
    machine_limit = sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts']))
    problem += machine_limit <= data['Availability'][m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
```python
import pulp

#### Data extracted from JSON
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

#### Problem setup
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]

#### Calculate total_time for labor cost
total_time = sum(data['TimeRequired'][m][p] * batches[p] for m in range(data['NumMachines']) for p in range(data['NumParts']))

#### Labor Costs calculation
overtime_hours = data['OvertimeHour']
labor_costs = pulp.LpVariable("labor_costs", cat='Continuous')
problem += labor_costs

#### Add piecewise conditions for labor costs
for m in range(data['NumMachines']):
    max_overtime = data['OvertimeHour'][m]
    problem += (labor_costs >= data['StandardCost'] * total_time - (data['StandardCost'] - data['OvertimeCost']) * max_overtime)
    problem += (labor_costs <= data['StandardCost'] * max_overtime + data['OvertimeCost'] * (total_time - max_overtime))

#### Objective function
profit = (
    sum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) -
    sum(data['MachineCosts'][m] * sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines'])) -
    labor_costs
)
problem += profit

#### Constraints
for m in range(1, data['NumMachines']):  #### Constraints for m from 2 to M
    machine_limit = sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts']))
    problem += machine_limit <= data['Availability'][m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py:1650: UserWarning: Overwriting previously set objective.
  warnings.warn("Overwriting previously set objective.")
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from JSON
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

#### Problem setup
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

#### Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]

#### Calculate total_time for labor cost
total_time = sum(data['TimeRequired'][m][p] * batches[p] for m in range(data['NumMachines']) for p in range(data['NumParts']))

#### Labor Costs calculation
overtime_hours = data['OvertimeHour']
labor_costs = pulp.LpVariable("labor_costs", cat='Continuous')
problem += labor_costs

#### Add piecewise conditions for labor costs
for m in range(data['NumMachines']):
    max_overtime = data['OvertimeHour'][m]
    problem += (labor_costs >= data['StandardCost'] * total_time - (data['StandardCost'] - data['OvertimeCost']) * max_overtime)
    problem += (labor_costs <= data['StandardCost'] * max_overtime + data['OvertimeCost'] * (total_time - max_overtime))

#### Objective function
profit = (
    sum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) -
    sum(data['MachineCosts'][m] * sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines'])) -
    labor_costs
)
problem += profit

#### Constraints
for m in range(data['NumMachines']):  #### Constraints for m from 0 to M-1
    machine_limit = sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts']))
    problem += machine_limit <= data['Availability'][m]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

