import pulp
import numpy as np

# Data
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Chebychev_Center_Radius", pulp.LpMaximize)

# Define the decision variable
r = pulp.LpVariable("r", lowBound=0)

# Define the constraints
x_vars = [pulp.LpVariable(f'x_{j}', lowBound=None) for j in range(N)]  # Declare x variables outside the loop
for i in range(M):
    # The norm of the ith row of A
    norm_Ai = np.linalg.norm(A[i])
    problem += (pulp.lpSum(A[i, j] * x_vars[j] for j in range(N)) + r * norm_Ai <= B[i])  # Use lpSum

# Objective Function
problem += r

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')