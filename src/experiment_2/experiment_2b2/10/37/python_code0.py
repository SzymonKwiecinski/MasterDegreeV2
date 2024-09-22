import pulp

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Extracting data from the input
data = {'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}
time = data["time"]
profit = data["profit"]
capacity = data["capacity"]

# Number of parts and shops
num_parts = len(profit)
num_shops = len(capacity)

# Decision variables
quantity = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective function: Maximize total profit
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(num_parts)])

# Constraints: Capacity constraints for each shop
for s in range(num_shops):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(num_parts)]) <= capacity[s]

# Solve the problem
problem.solve()

# Output the solution
result = {
    "quantity": [pulp.value(quantity[k]) for k in range(num_parts)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')