import pulp
import numpy as np

# Data provided
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Extracting data
M = data['M']  # Number of inequalities
N = data['N']  # Dimension of the ambient space
A = np.array(data['A'])  # Coefficient matrix
B = np.array(data['B'])  # Right-hand side vector

# Initialize the LP problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=None) for j in range(N)]
r = pulp.LpVariable('r', lowBound=0)  # The radius to maximize

# Objective function: Maximize the radius r
problem += r, "Maximize Radius"

# Adding constraints
for i in range(M):
    norm_A_i = np.linalg.norm(A[i])
    lhs = pulp.lpSum([A[i][j] * x[j] for j in range(N)]) + r * norm_A_i
    problem += (lhs <= B[i], f'Constraint_{i}')

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')