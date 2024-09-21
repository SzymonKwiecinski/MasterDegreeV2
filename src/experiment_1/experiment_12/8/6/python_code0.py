import pulp
import numpy as np

# Data from JSON
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Extract data
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the LP problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{i}', cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')  # radius

# Objective: Maximize the radius r
problem += r, "Maximize the radius r"

# Constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i, :])
    problem += pulp.lpSum(A[i, j] * x[j] for j in range(N)) + r * norm_Ai <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("Optimal x values: ", [pulp.value(var) for var in x])
print("Optimal radius r: ", pulp.value(r))