import pulp
import math

# Data from JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
b = data['B']

# Create a LP problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Create variables
x_vars = [pulp.LpVariable(f'x{i}', lowBound=None, upBound=None, cat='Continuous') for i in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Define the objective function to maximize the radius r
problem += r, "Maximize_Radius"

# Define the constraints
for i in range(M):
    norm_Ai = math.sqrt(sum(A[i][j] ** 2 for j in range(N)))
    lhs = pulp.lpDot(A[i], x_vars) + r * norm_Ai
    problem += lhs <= b[i], f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')