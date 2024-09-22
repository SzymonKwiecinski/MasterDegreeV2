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
B = np.array(data['B'])

# Create the problem
problem = pulp.LpProblem("Chebychev_Center_Problem", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)  # Center
r = pulp.LpVariable("r", lowBound=0)  # Radius

# Objective function: maximize r
problem += r, "Maximize Radius"

# Constraints for the ball
for i in range(M):
    for j in range(N):
        problem += y[j] - r <= A[i][j], f"Lower_Bound_Constraint_{i}_{j}"
        problem += y[j] + r >= A[i][j], f"Upper_Bound_Constraint_{i}_{j}"

# Constraints for the linear inequalities
for j in range(M):
    problem += pulp.lpSum(A[j][k] * y[k] for k in range(N)) <= B[j], f"Linear_Constraint_{j}"

# Solve the problem
problem.solve()

# Output result
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

print(f' (Objective Value): <OBJ>{radius}</OBJ>')
print(f'Center: {center}, Radius: {radius}')