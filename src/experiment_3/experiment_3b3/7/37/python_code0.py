import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Indices
K = len(data['profit'])  # Number of different spare parts
S = len(data['capacity'])  # Number of shops

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Problem
problem = pulp.LpProblem('Maximize_Profit', pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K))

# Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s]

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')