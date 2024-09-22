import pulp

# Input data
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}

# Extracting the data
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of products and shops
num_parts = len(profit)
num_shops = len(capacity)

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Integer') for k in range(num_parts)]

# Objective Function
problem += pulp.lpSum([profit[k] * quantities[k] for k in range(num_parts)]), "Total Profit"

# Constraints
for s in range(num_shops):
    problem += pulp.lpSum([time[k][s] * quantities[k] for k in range(num_parts)]) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

# Solve the problem
problem.solve()

# Output the results
output = {"quantity": [pulp.value(quantities[k]) for k in range(num_parts)]}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')