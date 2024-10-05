import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Extract data
time = data['time']
profit = data['profit']
capacity = data['capacity']
num_parts = len(profit)
num_shops = len(capacity)

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

# Objective function
problem += pulp.lpSum([profit[k] * quantity[k] for k in range(num_parts)])

# Constraints
for s in range(num_shops):
    problem += pulp.lpSum([time[k][s] * quantity[k] for k in range(num_parts)]) <= capacity[s]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(num_parts)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')