import pulp

# Data from the JSON format
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}

# Extract data
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the Linear Programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective function: maximize the radius r
problem += r, "Objective"

# Constraints
for i in range(M):
    constraint_expr = sum(A[i][j] * y[j] for j in range(N))
    problem += constraint_expr + r * (A[i][0]**2 + A[i][1]**2)**0.5 <= B[i], f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the results
y_values = [pulp.value(y[i]) for i in range(N)]
radius = pulp.value(r)

# Print the results
print("Center of the ball:", y_values)
print("Radius of the ball:", radius)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')