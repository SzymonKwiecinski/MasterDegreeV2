import pulp
import numpy as np
import json

# Data
data = json.loads("{'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}")
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Define the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)  # Center variables
r = pulp.LpVariable("r", lowBound=0)  # Radius variable

# Objective function
problem += r  # We want to maximize r

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i, j] * y[j] for j in range(N)) - r * pulp.lpNorm(A[i]) <= B[i])

# Solve the problem
problem.solve()

# Print the results
center = [y[j].varValue for j in range(N)]
radius = r.varValue

print(f'Center: {center}')
print(f'Radius: {radius}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')