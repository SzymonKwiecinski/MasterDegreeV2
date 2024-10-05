import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Indices
K = len(data['profit'])
S = len(data['capacity'])

# Problem definition
problem = pulp.LpProblem("Spare_Automobile_Parts_Production", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K))

# Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')