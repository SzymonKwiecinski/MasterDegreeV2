# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
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
<DATA>
{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
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
}

NumMachines = data['NumMachines']
NumParts = data['NumParts']
TimeRequired = data['TimeRequired']
MachineCosts = data['MachineCosts']
Availability = data['Availability']
Prices = data['Prices']
MinBatches = data['MinBatches']
StandardCost = data['StandardCost']
OvertimeCost = data['OvertimeCost']
OvertimeHour = data['OvertimeHour']

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
batches = pulp.LpVariable.dicts("batches", range(NumParts), lowBound=0, cat='Continuous')
machine_hours = pulp.LpVariable.dicts("machine_hours", (range(1, NumMachines)), lowBound=0, cat='Continuous')

#### Objective Function: Maximize Profit
revenue = pulp.lpSum([batches[p] * Prices[p] for p in range(NumParts)])
machine_costs = pulp.lpSum([machine_hours[m] * MachineCosts[m-1] for m in range(1, NumMachines)])
labor_cost = pulp.lpSum([pulp.lpSum([batches[p] * TimeRequired[0][p] for p in range(NumParts)]) * (StandardCost if pulp.lpSum([batches[p] * TimeRequired[0][p] for p in range(NumParts)]) <= OvertimeHour[0] else OvertimeCost)])

problem += revenue - machine_costs - labor_cost

#### Constraints
#### Minimum number of batches for each part
for p in range(NumParts):
    problem += batches[p] >= MinBatches[p]

#### Machine constraints
for m in range(1, NumMachines):
    problem += machine_hours[m] == pulp.lpSum([batches[p] * TimeRequired[m][p] for p in range(NumParts)])
    problem += machine_hours[m] <= Availability[m]

#### Solve the problem
problem.solve()

#### Extracting the results
batches_produced = [pulp.value(batches[p]) for p in range(NumParts)]
total_profit = pulp.value(problem.objective)

#### Output
output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

