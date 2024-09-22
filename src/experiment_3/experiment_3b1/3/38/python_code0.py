import pulp

# Data from the provided JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Number of months
N = len(data['demand'])

# Create a linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * inventory[n]
    for n in range(N)
])

# Constraints
# Demand Satisfaction
for n in range(N):
    if n == 0:
        problem += (0 + reg_quant[n] + over_quant[n] - data['demand'][n] == inventory[n])
    else:
        problem += (inventory[n-1] + reg_quant[n] + over_quant[n] - data['demand'][n] == inventory[n])

# Regular Production Capacity
for n in range(N):
    problem += (reg_quant[n] <= data['max_regular_amount'])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')