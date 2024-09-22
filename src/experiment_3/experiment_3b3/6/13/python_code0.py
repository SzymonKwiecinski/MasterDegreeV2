import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']  # Number of constraints
N = data['N']  # Dimension of the space
A = np.array(data['A'])  # Coefficients of the constraints
B = np.array(data['B'])  # Right-hand side of the constraints

# Problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision Variables
y_vars = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective Function
problem += r, "Maximize_Radius"

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y_vars[j] for j in range(N)) + r * np.linalg.norm(A[i]) <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Results
center = [pulp.value(y_vars[j]) for j in range(N)]
radius = pulp.value(r)

result = {
    "center": center,
    "radius": radius
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')