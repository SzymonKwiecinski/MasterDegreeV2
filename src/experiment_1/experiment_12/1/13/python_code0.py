import pulp

# Data from the problem
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    'profit': [30, 20, 40, 25, 10], 
    'capacity': [700, 1000]
}

# Number of spare parts (K) and machines (S)
K = len(data['profit'])
S = len(data['capacity'])

# Initialize the problem
problem = pulp.LpProblem("Spare_Parts_Production_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K))

# Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s]

# Solve the problem
problem.solve()

# Print results
for k in range(K):
    print(f"Quantity of spare part {k + 1} to produce: {pulp.value(x[k])}")

print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")