import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Extracting data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective function
problem += pulp.lpSum(reg_quant[n] * cost_regular + over_quant[n] * cost_overtime + inventory[n] * store_cost for n in range(N))

# Constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - demand[n] + inventory[n] == 0
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] - demand[n] + inventory[n] == 0
    
    problem += reg_quant[n] <= max_regular_amount  # Regular production limit

# Solve the problem
problem.solve()

# Collecting results
reg_quant_values = [pulp.value(var) for var in reg_quant]
over_quant_values = [pulp.value(var) for var in over_quant]

# Output format
output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')