import pulp
import numpy as np
import json

# Data from the provided JSON format
data = '{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}'
params = json.loads(data)

M = params['M']
N = params['N']
A = np.array(params['A'])
B = np.array(params['B'])

# Create a Linear Programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision Variables
y_vars = pulp.LpVariable.dicts("y", range(N), lowBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective Function: Maximize radius r
problem += r, "Maximize radius"

# Constraints
for i in range(M):
    a_i = A[i, :]
    b_i = B[i]
    a_i_norm = np.linalg.norm(a_i)
    
    # Constraint: a_i^T * y + r * ||a_i||_2 <= b_i
    problem += (pulp.lpSum([a_i[j] * y_vars[j] for j in range(N)]) + r * a_i_norm <= b_i), f"Constraint_pos_{i}"
    
    # Constraint: a_i^T * y - r * ||a_i||_2 <= b_i
    problem += (pulp.lpSum([a_i[j] * y_vars[j] for j in range(N)]) - r * a_i_norm <= b_i), f"Constraint_neg_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')