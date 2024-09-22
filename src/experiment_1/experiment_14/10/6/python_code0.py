import pulp
import numpy as np

# Data from JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective: Maximize the radius r
problem += r, "Maximize_radius"

# Constraints: A x + r ||A_i||_2 <= b_i for i = 1, 2, ..., M
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])
    problem += pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * norm_Ai <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')