import pulp

# Data from the JSON
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create a Linear Programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables: center y and radius r
y = [pulp.LpVariable(f'y_{i}', lowBound=None) for i in range(N)]
r = pulp.LpVariable('r', lowBound=0)

# Objective function: Maximize the radius
problem += r, "Objective"

# Constraints
for i in range(M):
    # a_i^T * y + r >= b_i
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r >= B[i], f'Constraint_{i}_1'
    
    # a_i^T * y - r <= b_i
    problem += pulp.lpSum(A[i][j] * y[j] for j in range(N)) - r <= B[i], f'Constraint_{i}_2'

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')