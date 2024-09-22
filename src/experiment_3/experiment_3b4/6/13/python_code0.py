import pulp
import numpy as np

# Parse data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = np.array(data['A'])
B = np.array(data['B'])

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Radius", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective function
problem += r

# Constraints
for i in range(M):
    a_i = A[i]
    b_i = B[i]
    norm_a_i = np.linalg.norm(a_i)
    
    problem += pulp.lpSum([a_i[j] * y[j] for j in range(N)]) + r * norm_a_i <= b_i

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')