import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, upBound=max_regular_amount) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
storage = [pulp.LpVariable(f'storage_{n}', lowBound=0) for n in range(N+1)]  # Including storage at month 0

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * storage[n] for n in range(N)), "Total_Cost"

# Constraints
# Demand constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] + storage[n] == demand[n], f'demand_constraint_{n}'
    else:
        problem += reg_quant[n] + over_quant[n] + storage[n] == demand[n] + storage[n-1], f'demand_constraint_{n}'

# Storage constraints
for n in range(N):
    if n == 0:
        problem += storage[n] == 0, f'initial_storage_{n}'
    else:
        problem += storage[n] >= 0, f'storage_non_negative_{n}'

# Solve the problem
problem.solve()

# Output results
results = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Display results
print(json.dumps(results))