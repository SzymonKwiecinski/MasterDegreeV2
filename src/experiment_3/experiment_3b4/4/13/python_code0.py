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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Radius_Ball", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective function: Maximize the radius 'r'
problem += r, "Objective"

# Constraints
for i in range(M):
    ai = A[i]
    norm_ai = np.linalg.norm(ai)
    problem += pulp.lpSum(ai[j] * y[j] for j in range(N)) + norm_ai * r <= B[i], f"Constraint_{i}"

# Solve the problem
problem.solve()

# Printing the results
print(f'Optimal radius (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')