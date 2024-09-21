import pulp
import numpy as np

# Given data
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

# Create the problem variable
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variable for radius
r = pulp.LpVariable("r", lowBound=0)  # r >= 0

# Objective function
problem += r, "Maximize_Radius"

# Constraints
for i in range(M):
    Ai = A[i]
    Bi = B[i]
    problem += (pulp.lpSum(Ai[j] * Ai[j] for j in range(N))**0.5) * r <= (Bi - 0), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')