import pulp
import json

# Load data from JSON format
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

# Problem parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Create the problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Define decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inv = [pulp.LpVariable(f'inv_{n}', lowBound=0) for n in range(N)]

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inv[n] for n in range(N))

# Constraints
# Regular quantity constraint
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount

# Inventory balance constraint
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == demand[n] + inv[n]
    else:
        problem += reg_quant[n] + over_quant[n] + inv[n-1] == demand[n] + inv[n]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')