import pulp
import numpy as np

# Data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Problem Definition
problem = pulp.LpProblem("Chebyshev_Center_Problem", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=None) for j in range(data['N'])]  # decision variables
r = pulp.LpVariable('r', lowBound=0)  # radius

# Constraints
A = np.array(data['A'])
B = np.array(data['B'])

for i in range(data['M']):
    problem += (pulp.lpSum(A[i, j] * x[j] for j in range(data['N'])) + r * np.linalg.norm(A[i]) <= B[i])

# Objective Function
problem += r, "Objective"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')