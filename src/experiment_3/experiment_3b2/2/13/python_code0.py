import pulp
import numpy as np

# Data from JSON
data = {'M': 4, 'N': 2, 
        'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 
        'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the LP problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables for the center y and the radius r
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective Function
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    a_i = A[i]
    b_i = B[i]
    norm_a_i = np.linalg.norm(a_i)
    problem += (pulp.lpSum(a_i[j] * y[j] for j in range(N)) + r * norm_a_i <= b_i), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')