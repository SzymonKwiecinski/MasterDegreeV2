import pulp
import numpy as np

# Given data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Unpacking data
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the Pulp problem
problem = pulp.LpProblem("Chebychev_Center_Optimization", pulp.LpMaximize)

# Define variables
r = pulp.LpVariable("r", lowBound=0)  # radius
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)  # center coordinates

# Objective function
problem += r

# Constraints
for i in range(M):
    norm_ai = np.linalg.norm(A[i])
    problem += (np.dot(A[i], [y[j] for j in range(N)]) + r * norm_ai <= B[i]), f"constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')