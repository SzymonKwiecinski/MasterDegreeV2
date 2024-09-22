import pulp
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the LP problem
problem = pulp.LpProblem("ChebyshevCenter", pulp.LpMaximize)

# Variables for the center of the ball
y = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective: maximize radius r
problem += r

# Constraints: a_i^T * y <= b_i - r for each constraint
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) <= B[i] - r)

# Solve the problem
problem.solve()

# Prepare the output
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

output = {
    "center": center,
    "radius": radius
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')