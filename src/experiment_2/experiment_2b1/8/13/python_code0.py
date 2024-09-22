import pulp
import json

data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Define variables for the center and radius
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)  # center variables
r = pulp.LpVariable("r", lowBound=0)  # radius variable

# Objective function: maximize radius r
problem += r

# Constraints: for each inequality a_i^T y <= b_i + r (and a_i^T y >= b_i - r)
for i in range(M):
    constraint_expr = sum(A[i][j] * y[j] for j in range(N))
    problem += constraint_expr <= B[i] + r
    problem += constraint_expr >= B[i] - r

# Solve the problem
problem.solve()

# Prepare output
center = [y[j].varValue for j in range(N)]
radius = r.varValue

output = {
    "center": center,
    "radius": radius
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Printing the output in the required format
print(json.dumps(output))