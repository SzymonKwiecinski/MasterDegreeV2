import pulp
import numpy as np
import json

# Given data in JSON format
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')

M = data['M']  # number of constraints
N = data['N']  # dimension of the space
A = np.array(data['A'])  # constraint coefficients
B = np.array(data['B'])  # constraint bounds

# Create the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective function
problem += r, "Maximize Radius"

# Constraints
for i in range(M):
    norm_a_i = np.linalg.norm(A[i])
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * norm_a_i <= B[i], f"Upper_Bound_Constraint_{i+1}"
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) - r * norm_a_i <= B[i], f"Lower_Bound_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Extract results
center = [y[j].varValue for j in range(N)]
radius = r.varValue

# Output results
print(f'Center: {center}')
print(f'Radius: {radius}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')