import pulp
import numpy as np

# Data from JSON
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']  # Number of constraints
N = data['N']  # Dimension of the space
A = data['A']  # Coefficients for constraints
B = data['B']  # RHS of constraints

# Define the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", (range(N)), cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')  # Radius, should be non-negative

# Objective function: Maximize the radius r
problem += r, "Maximize_Radius"

# Constraints
for i in range(M):
    a_i = np.array(A[i])
    norm_a_i = np.linalg.norm(a_i)
    
    # a_i^T * y + ||a_i||_2 * r <= b_i
    problem += pulp.lpSum([a_i[j] * y[j] for j in range(N)]) + norm_a_i * r <= B[i], f"Constraint_{i}"

# Solve the problem
status = problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Output the results
if status == pulp.LpStatusOptimal:
    print("Optimal solution found.")
else:
    print("Optimal solution not found.")

for j in range(N):
    print(f"y_{j} = {pulp.value(y[j])}")

print(f"r = {pulp.value(r)}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")