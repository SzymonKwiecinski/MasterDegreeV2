import pulp
import numpy as np

# Data from the JSON format
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
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision variable: radius r
r = pulp.LpVariable("r", lowBound=0)

# Adding constraints for the ball to be completely within the set P
for i in range(M):
    norm_Ai = np.linalg.norm(A[i])
    problem += (pulp.lpSum(A[i][j] * 0 for j in range(N)) + r * norm_Ai <= B[i]), f"constraint_{i+1}"

# Objective function to maximize r
problem += r

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')