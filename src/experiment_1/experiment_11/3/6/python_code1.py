import pulp
import numpy as np

# Data provided
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Number of inequalities and dimensions
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Define the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define the decision variable
r = pulp.LpVariable("r", lowBound=0)  # radius should be non-negative

# Define the decision variables for the dimensions
x = [pulp.LpVariable(f'x_{j}', lowBound=None) for j in range(N)]

# Add constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])  # Compute the Euclidean norm
    problem += (A[i] @ np.array(x) + r * norm_Ai <= B[i]), f"Constraint_{i+1}"

# Objective function
problem += r  # Maximizing radius

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')