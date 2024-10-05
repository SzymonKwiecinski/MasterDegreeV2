import pulp

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Extract data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Initialize problem
problem = pulp.LpProblem("Production Scheduling Problem", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective function
total_cost = (
    pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))
)
problem += total_cost

# Constraints
for n in range(N):
    # Demand satisfaction constraint
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - inventory[n] == demand[n]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] - inventory[n] == demand[n]
    
    # Maximum regular production constraint
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Extract results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

# Output
output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')