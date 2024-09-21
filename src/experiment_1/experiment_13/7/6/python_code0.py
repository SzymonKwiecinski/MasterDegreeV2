import pulp
import numpy as np

# Data extraction from JSON format
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Initialize the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variable for the radius r
r = pulp.LpVariable("r", lowBound=0)

# Adding constraints
for i in range(M):
    problem += (r * np.linalg.norm(A[i, :]) <= B[i], f"Constraint_{i+1}")

# Objective function
problem += r, "Maximize_radius"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')