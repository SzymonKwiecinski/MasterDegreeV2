import pulp

# Data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Production Planning", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective function
# Minimize cost: regular production + overtime production + storage
problem += (
    pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))
)

# Constraints
for n in range(N):
    # Demand constraints
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == demand[n] + inventory[n]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] == demand[n] + inventory[n]
    
    # Maximum regular production constraint
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Output the results
output = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')