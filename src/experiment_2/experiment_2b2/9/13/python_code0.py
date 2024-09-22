import pulp
import json

# Given data
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables: y_i and r
y = pulp.LpVariable.dicts("y", (i for i in range(N)), lowBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective: Maximize the radius r
problem += r, "Maximize Radius"

# Constraints: a_i^T * y + ||a_i|| * r <= b_i for all i
for i in range(M):
    problem += (
        pulp.lpSum(A[i][j] * y[j] for j in range(N)) + 
        (pulp.lpSum(A[i][j]**2 for j in range(N))**0.5) * r <= B[i]
    ), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Gather the results
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Prepare the output in the specified format
output = {
    "center": center,
    "radius": radius
}

# Print the results
print(json.dumps(output, indent=4))

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')