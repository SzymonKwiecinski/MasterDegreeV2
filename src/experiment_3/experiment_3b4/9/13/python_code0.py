import pulp
import numpy as np

# Data from JSON
data = {
    'M': 4, 
    'N': 2, 
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 
    'B': [2.0, 2.0, 3.0, 5.0]
}

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the linear programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
y = [pulp.LpVariable(f'y_{j}', cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective: Maximize r
problem += r, "Maximize_Radius"

# Constraints
for i in range(M):
    a_i = np.array(A[i])
    norm_a_i = np.linalg.norm(a_i)
    problem += pulp.lpSum([a_i[j] * y[j] for j in range(N)]) + norm_a_i * r <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')