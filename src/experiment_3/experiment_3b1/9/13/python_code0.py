import pulp
import json

# Data from the provided JSON input
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Radius", pulp.LpMaximize)

# Decision variables
r = pulp.LpVariable('r', lowBound=0)  # The radius of the ball
y = pulp.LpVariable.dicts('y', range(N), lowBound=None, cat='Continuous')  # Center of the ball

# Objective function: maximize radius r
problem += r

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * (A[i][0]**2 + A[i][1]**2)**0.5 <= B[i])

# Solve the problem
problem.solve()

# Extract the results
center = [y[j].varValue for j in range(N)]
radius = r.varValue

# Prepare the output in the specified format
output = {
    "center": center,
    "radius": radius
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Optionally, print the output
print(json.dumps(output))