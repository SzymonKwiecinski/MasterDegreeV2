import pulp
import numpy as np

# Data from the provided JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 
        'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Radius", pulp.LpMaximize)

# Variables: y is a vector of N dimensions and r is the radius
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective Function: Maximize the radius r
problem += r, "Objective"

# Constraints
for i in range(M):
    problem += (np.dot(A[i], [y[j] for j in range(N)]) + np.linalg.norm(A[i]) * r <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')