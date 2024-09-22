import pulp
import numpy as np

# Data provided
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

# Create variables
x = [pulp.LpVariable(f"x_{i}", cat='Continuous') for i in range(N)]
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective function: Maximize r
problem += r, "Objective: Maximize radius"

# Constraints
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])
    problem += pulp.lpDot(A[i], x) + r * norm_Ai <= B[i], f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')