import pulp
import numpy as np
import json

# Data provided in JSON format
data = json.loads('{"M": 4, "N": 2, "A": [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], "B": [2.0, 2.0, 3.0, 5.0]}')

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Define the problem
problem = pulp.LpProblem("Maximize_r", pulp.LpMaximize)

# Define decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective Function
problem += r

# Constraints
for i in range(M):
    problem += (np.dot(A[i], [y[j] for j in range(N)]) + np.linalg.norm(A[i]) * r <= B[i])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')