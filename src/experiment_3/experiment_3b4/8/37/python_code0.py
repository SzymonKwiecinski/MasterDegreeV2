import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of parts (K) and shops (S)
K = len(data['profit'])
S = len(data['capacity'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables: quantity to produce for each spare part
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function: Maximize Z
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K))

# Constraints: Capacity constraints for each shop
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')