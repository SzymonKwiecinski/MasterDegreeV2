import pulp
import numpy as np

# Data from JSON
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Extracting data
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Initialize the problem
problem = pulp.LpProblem("Maximize_Radius", pulp.LpMaximize)

# Decision Variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)  # center of the ball
r = pulp.LpVariable("r", lowBound=0)  # radius of the ball

# Objective Function
problem += r, "Objective"

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + np.linalg.norm(A[i]) * r <= B[i]), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')