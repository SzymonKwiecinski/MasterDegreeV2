import pulp
import numpy as np

# Data from the input
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create the problem variable
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables
r = pulp.LpVariable("r", lowBound=0)  # radius
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)  # center of the ball

# Objective function
problem += r, "Objective"

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * np.linalg.norm(A[i]) <= B[i]), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')