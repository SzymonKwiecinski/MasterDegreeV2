import pulp

# Data extraction
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Variables
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
r = pulp.LpVariable('r', lowBound=0)  # radius
y = [pulp.LpVariable(f'y_{i}', cat='Continuous') for i in range(N)]  # center coordinates

# Objective function
problem += r, "Objective to maximize radius"

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r <= B[i]), f"Constraint_Upper_{i+1}"
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) - r <= B[i]), f"Constraint_Lower_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')