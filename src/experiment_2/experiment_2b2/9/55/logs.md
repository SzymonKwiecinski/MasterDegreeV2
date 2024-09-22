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
import pulp

#### Data from the input
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

#### Problem variables
num_machines = len(data['time_required'])
num_parts = len(data['time_required'][0])

#### Create the LP Problem
problem = pulp.LpProblem("Auto_Manufacturer_Profit", pulp.LpMaximize)

#### Decision Variables: number of batches to produce for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p]) for p in range(num_parts)]

#### Objective Function: maximize profit
profit = pulp.lpSum(
    data['prices'][p] * batches[p] for p in range(num_parts)
)

machine_cost = pulp.lpSum(
    data['time_required'][m][p] * batches[p] * data['machine_costs'][m] for m in range(1, num_machines) for p in range(num_parts)
)

#### Machine 1 (outsourced, separate handling)
machine_1_cost = (
    pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(num_parts)) * data['standard_cost']
)
machine_1_overtime = (
    pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(num_parts)) - data['overtime_hour']
)
overtime_cost = pulp.lpSum(
    machine_1_overtime * (data['overtime_cost'] - data['standard_cost'])
)

#### Total Cost
total_cost = machine_cost + machine_1_cost + overtime_cost

#### Profit
total_profit = profit - total_cost
problem += total_profit, "Total_Profit"

#### Constraints
#### Min profit
problem += total_profit >= data['min_profit']

#### Machine usage availability constraint
for m in range(1, num_machines):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(num_parts)) <= data['availability'][m]

#### Solve the problem
problem.solve()

#### Prepare output
output = {
    "batches": [int(pulp.value(batches[p])) for p in range(num_parts)],
    "total_profit": pulp.value(total_profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

