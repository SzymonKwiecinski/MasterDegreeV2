import pulp
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

m = data['M']
n = data['N']
A = data['A']
B = data['B']

# Create a LP problem
problem = pulp.LpProblem("Chebyshev_Center_Problem", pulp.LpMaximize)

# Define variables for the center of the ball and the radius
center = [pulp.LpVariable(f'c_{j}', cat='Continuous') for j in range(n)]
radius = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective function: maximize the radius
problem += radius

# Constraints for each inequality defining the set P
for i in range(m):
    problem += (pulp.lpSum(A[i][j] * center[j] for j in range(n)) <= B[i] - radius)

# Solve the problem
problem.solve()

# Retrieve results
center_solution = [pulp.value(center[j]) for j in range(n)]
radius_solution = pulp.value(radius)

# Prepare output
output = {
    "center": center_solution,
    "radius": radius_solution
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')