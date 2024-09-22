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
- The desired profit should surpass \var{min_profit}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour,
    "min_profit": min_profit
}

OBJECTIVE: Determine the quantity of batches for each part the manufacturer should produce every month, ensuring all constraints are met.

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
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import json
import pulp

#### Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'standard_cost': 20, 
    'overtime_cost': 30, 
    'overtime_hour': 400, 
    'min_profit': 5000
}

#### Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

#### Define variables
P = len(data['min_batches'])  #### Number of parts
M = len(data['time_required'])  #### Number of machines

#### Decision variables: number of batches produced
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

#### Objective function: Maximize profit
profit = pulp.lpSum([(data['prices'][p] * batches[p] - 
                       pulp.lpSum([data['machine_costs'][m] * data['time_required'][m][p] * batches[p] / 100.0 
                                    for m in range(M)])) 
                      for p in range(P)])
problem += profit

#### Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

#### Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]

#### Calculate total labor cost for Machine 1
#### Note: Machine 1 requires special handling for labor costs
problem += (pulp.lpSum([data['time_required'][0][p] * batches[p] for p in range(P)]) <= data['availability'][0] + 
              (data['overtime_hour'] - data['availability'][0]) 
              if data['overtime_hour'] > data['availability'][0] else 0)

#### Profit must exceed minimum profit requirement
problem += profit >= data['min_profit']

#### Solve the problem
problem.solve()

#### Result extraction
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

#### Output formatted result
result = {
    "batches": batches_result,
    "total_profit": total_profit
}

#### Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

