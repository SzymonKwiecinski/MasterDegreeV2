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
To model this problem as a Linear Programming problem, we'll define decision variables and constraints and then express the objective function in a mathematical form.

######### Decision Variables:
- Let \( x_p \) be the number of batches of part \( p \) produced each month.

######### Parameters:
- \( time_{m,p} \): Time required on machine \( m \) for part \( p \).
- \( cost_{m} \): Cost per hour for using machine \( m \).
- \( available_{m} \): Available hours for machine \( m \) per month.
- \( price_{p} \): Selling price per batch of part \( p \).
- \( min\_batches_{p} \): Minimum required batches of part \( p \) each month.
- \( standard\_cost \): Standard labor cost per hour for machine 1.
- \( overtime\_cost \): Overtime labor cost per hour for machine 1.
- \( overtime\_hour \): Threshold hours after which overtime cost applies.

######### Objective Function:
Maximize the total profit, which is the total revenue minus the total machine costs, including consideration for labor costs for Machine 1.

######### Constraints:
1. Demand constraints for each part \( p \).
2. Availability constraints for each machine \( m \).
3. Special handling of machine 1's labor costs.

Here's how the Linear Programming model looks in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the total profit

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p \right) - \sum_{m=2}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot x_p \right) \right) - \text{Labor Cost for Machine 1}
\]

\textbf{Labor Cost for Machine 1:}
\[
\text{Labor Cost} = 
\begin{cases} 
\text{standard\_cost} \cdot H_1, & \text{if } H_1 \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (H_1 - \text{overtime\_hour}), & \text{if } H_1 > \text{overtime\_hour}
\end{cases}
\]
where \( H_1 = \sum_{p=1}^{P} \left( \text{time}_{1,p} \cdot x_p \right)\)

\textbf{Constraints:}
1. Demand Constraints for each part \( p \):
\[
x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
\]

2. Machine Availability Constraints for each machine \( m \neq 1 \):
\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot x_p \right) \leq \text{available}_m, \quad \forall m = 2, \ldots, M
\]

\textbf{Decision Variables:}
- \( x_p \geq 0, \quad \forall p = 1, \ldots, P \)

\end{document}
```

This LaTeX code models the LP problem of maximizing the profit by deciding how many batches of each part to produce, while considering machine costs, labor costs, and constraints on production and machine availability.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the total profit

\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p \right) - \sum_{m=2}^{M} \left( \text{cost}_m \cdot \sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot x_p \right) \right) - \text{Labor Cost for Machine 1}
\]

\textbf{Labor Cost for Machine 1:}
\[
\text{Labor Cost} = 
\begin{cases} 
\text{standard\_cost} \cdot H_1, & \text{if } H_1 \leq \text{overtime\_hour} \\
\text{standard\_cost} \cdot \text{overtime\_hour} + \text{overtime\_cost} \cdot (H_1 - \text{overtime\_hour}), & \text{if } H_1 > \text{overtime\_hour}
\end{cases}
\]
where \( H_1 = \sum_{p=1}^{P} \left( \text{time}_{1,p} \cdot x_p \right)\)

\textbf{Constraints:}
1. Demand Constraints for each part \( p \):
\[
x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
\]

2. Machine Availability Constraints for each machine \( m \neq 1 \):
\[
\sum_{p=1}^{P} \left( \text{time}_{m,p} \cdot x_p \right) \leq \text{available}_m, \quad \forall m = 2, \ldots, M
\]

\textbf{Decision Variables:}
- \( x_p \geq 0, \quad \forall p = 1, \ldots, P \)

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

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(data['NumParts']), lowBound=0, cat='Continuous')

#### Objective function components
profit_terms = [data['Prices'][p] * x[p] for p in range(data['NumParts'])]
cost_terms = [data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) for m in range(1, data['NumMachines'])]
labor_cost = pulp.lpSum(data['StandardCost'] * pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))) if pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])) <= data['OvertimeHour'][0] else \
    data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'][0] * (pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])) - data['OvertimeHour'][0])

#### Full objective function
problem += pulp.lpSum(profit_terms) - pulp.lpSum(cost_terms) - labor_cost, "Total_Profit"

#### Constraints
#### Demand constraints
for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p], f"MinBatches_{p}"

#### Machine availability constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Availability_{m}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

