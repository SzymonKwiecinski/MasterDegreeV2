import pulp

# Data input from the JSON format
data = {
    'M': 4, 
    'N': 2, 
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Unpack the data
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Initialize the problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables: the center coordinates and the radius
y = [pulp.LpVariable(f'y_{j}', lowBound=None, upBound=None, cat='Continuous') for j in range(N)]
r = pulp.LpVariable('r', lowBound=0, cat='Continuous')

# Objective: Maximize the radius
problem += r, "Maximize_Radius"

# Constraints: Define each inequality constraint for the set P
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * (pulp.lpSum(A[i][j]**2 for j in range(N))**0.5) <= B[i]), f"Constraint_{i}"

# Solve the problem
problem.solve()

# Extract the solution
center = [pulp.value(y_var) for y_var in y]
radius = pulp.value(r)

# Output the results in the specified format
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')