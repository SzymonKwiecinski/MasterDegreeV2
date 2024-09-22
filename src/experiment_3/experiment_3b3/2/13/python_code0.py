import pulp
import numpy as np

# Extracting data from JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Initialize the linear programming problem
problem = pulp.LpProblem("Maximize_Radius", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Adding constraints
for i in range(M):
    a_i = A[i]
    b_i = B[i]
    constraint = pulp.lpSum(a_i[j] * y[j] for j in range(N)) + r * np.linalg.norm(a_i) <= b_i
    problem += constraint

# Objective function
problem += r

# Solving the problem
problem.solve()

# Solution extraction
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output
output = {'center': center, 'radius': radius}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')