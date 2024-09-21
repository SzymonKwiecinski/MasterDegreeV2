import pulp
import numpy as np

# Load data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
b = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables: center (x) and radius (r)
x = [pulp.LpVariable(f'x_{i}', cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective function: maximize the radius
problem += r, "Maximize_radius"

# Constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])
    problem += (pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * norm_Ai <= b[i]), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Get the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')