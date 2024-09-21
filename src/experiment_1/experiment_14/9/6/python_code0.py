import pulp
import numpy as np

# Data
data = {
    'M': 4, 
    'N': 2, 
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Parameters
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f"x_{i}", cat='Continuous') for i in range(N)]
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective
problem += r, "Maximize radius"

# Constraints
for i in range(M):
    norm_A_i = np.linalg.norm(A[i])
    problem += (pulp.lpSum(A[i][j] * x[j] for j in range(N)) + r * norm_A_i <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')