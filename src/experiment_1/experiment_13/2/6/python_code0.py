import pulp
import numpy as np

# Data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']
N = data['N']
A = np.array(data['A'])
b = np.array(data['B'])

# Create the problem variable
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define the decision variable
r = pulp.LpVariable('r', lowBound=0)

# Add the constraints
for i in range(M):
    Ai = A[i]
    problem += (r * np.linalg.norm(Ai) <= b[i], f"Constraint_{i+1}")

# The objective function
problem += r

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')