import pulp

# Data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

M = data['M']
N = data['N']
A = data['A']
b = data['B']

# Problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables
center = [pulp.LpVariable(f'y_{j}', lowBound=None) for j in range(N)]
radius = pulp.LpVariable('r', lowBound=0)

# Objective: Maximize the radius r
problem += radius, "Maximize_Radius"

# Constraints: Ensure the ball is contained within the polytope
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * center[j] for j in range(N)) + radius * (sum(A[i][j]**2 for j in range(N))**0.5) <= b[i]), f"Constraint_{i}"

# Solve
problem.solve()

# Output
center_solution = [pulp.value(center[j]) for j in range(N)]
radius_solution = pulp.value(radius)

output = {
    "center": center_solution,
    "radius": radius_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')