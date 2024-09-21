import pulp
import numpy as np

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Define the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Define the variable
r = pulp.LpVariable("r", lowBound=0)

# Define variables for the center of the ball
x = pulp.LpVariable.dicts("x", range(N), lowBound=None)

# Objective Function
problem += r, "Objective"

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * np.linalg.norm(A[i]) <= B[i]), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')