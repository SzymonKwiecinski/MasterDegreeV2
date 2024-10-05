import pulp
import json

data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables: y_j for j = 1,...,N (center of the ball) and r (radius of the ball)
center_vars = [pulp.LpVariable(f'y_{j}', lowBound=None, cat='Continuous') for j in range(N)]
radius_var = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Add constraints for each inequality: a_i^T * y <= b_i - r
for i in range(M):
    problem += pulp.lpSum(A[i][j] * center_vars[j] for j in range(N)) <= B[i] - radius_var
    problem += -pulp.lpSum(A[i][j] * center_vars[j] for j in range(N)) <= -B[i] + radius_var

# Objective function: Maximize the radius
problem += radius_var

# Solve the problem
problem.solve()

# Extract the results
center = [pulp.value(center_vars[j]) for j in range(N)]
radius = pulp.value(radius_var)

# Output results
output = {
    "center": center,
    "radius": radius
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')