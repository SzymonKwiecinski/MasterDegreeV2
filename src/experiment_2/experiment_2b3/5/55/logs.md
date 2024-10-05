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

#### Data from input
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

#### Indices for parts and machines
P = len(prices)
M = len(machine_costs)

#### Declare the LP problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

#### Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
machine_hours_used = [pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)]

#### Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_cost = pulp.lpSum(machine_costs[m] * machine_hours_used[m] for m in range(1, M))
labor_cost = standard_cost * pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
overtime_labor_cost = overtime_cost * (machine_hours_used[0] - overtime_hour)
overtime_labor_cost = pulp.lpSum([overtime_labor_cost, 0]) #### Only consider if there is overtime

total_cost = machine_cost + labor_cost + overtime_labor_cost
total_profit = profit - total_cost

problem += total_profit, "Total Profit"

#### Constraints
for m in range(1, M):  #### Machine hours constraints for m=2 to M
    problem += machine_hours_used[m] <= availability[m]

problem += total_profit >= min_profit

#### Solve the problem
problem.solve()

#### Prepare the results
result = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "total_profit": pulp.value(total_profit)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

