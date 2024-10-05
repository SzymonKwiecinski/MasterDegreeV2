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
A = np.array(data['A'])
B = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variables
y = [pulp.LpVariable(f'y_{j}', lowBound=None, cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=None, cat='Continuous')

# Objective function
problem += r, "Objective"

# Constraints
for i in range(M):
    ai = A[i]
    bi = B[i]
    problem += (pulp.lpSum(ai[j] * y[j] for j in range(N)) + np.linalg.norm(ai) * r <= bi), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the value of the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')