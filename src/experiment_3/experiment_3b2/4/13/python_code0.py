import pulp
import numpy as np

# Data from the JSON format
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center_Problem", pulp.LpMaximize)

# Define variables
r = pulp.LpVariable("r", lowBound=0)  # Radius of the ball
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)

# Objective function
problem += r, "Objective"

# Constraints
for i in range(M):
    norm_a_i = np.linalg.norm(A[i])  # Calculate the Euclidean norm
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * norm_a_i <= B[i]), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')