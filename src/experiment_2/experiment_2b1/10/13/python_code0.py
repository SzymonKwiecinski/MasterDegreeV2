import pulp
import json

# Input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']  # number of constraints
N = data['N']  # number of variables
A = data['A']  # coefficients for constraints
B = data['B']  # right-hand side values for constraints

# Create the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define decision variables for the center of the ball and the radius
y = [pulp.LpVariable(f'y_{j}', None) for j in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective function: maximize the radius r
problem += r, "Maximize Radius"

# Constraints to ensure the ball is within the feasible region defined by A*x <= B
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= B[i] - r), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Getting the results
center = [y[j].varValue for j in range(N)]
radius = r.varValue

# Output result as required format
result = {
    "center": center,
    "radius": radius
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')