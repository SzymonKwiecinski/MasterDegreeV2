import pulp

# Data from the JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Extract data
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of spare parts and shops
K = len(profit)  # Number of spare parts
S = len(capacity)  # Number of shops

# Define the problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Define the decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Define the objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * x[k] for k in range(K))

# Define the constraints for worker-hours available in each shop
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')