import pulp
import numpy as np
import json

# Given data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the problem variable
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define decision variables
r = pulp.LpVariable("r", lowBound=0)  # radius
y = pulp.LpVariable.dicts("y", range(N), lowBound=-pulp.lpInfinity, upBound=pulp.lpInfinity)  # center coordinates

# Objective function
problem += r, "Maximize_Radius"

# Constraints
for i in range(M):
    problem += r <= (B[i] - pulp.lpSum(A[i][j] * y[j] for j in range(N))) / (np.linalg.norm(A[i]) if np.linalg.norm(A[i]) > 0 else 1e-10), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Retrieve the results
center = [y[j].varValue for j in range(N)]
radius = pulp.value(problem.objective)

# Output results
print(f' (Objective Value): <OBJ>{radius}</OBJ>')
print(f'Center: {center}, Radius: {radius}')