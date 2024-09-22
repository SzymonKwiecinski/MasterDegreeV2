import pulp

# Data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

M = data['M']
N = data['N']
Available = data['Available']
Requirements = data['Requirements']
Prices = data['Prices']

# Linear Programming Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{j+1}', lowBound=0) for j in range(M)]

# Objective Function
problem += pulp.lpSum(Prices[j] * x[j] for j in range(M))

# Constraints
for i in range(N):
    problem += pulp.lpSum(Requirements[j][i] * x[j] for j in range(M)) <= Available[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')