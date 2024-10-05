import pulp

# Parse the input data
data = {'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}
M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Define the problem
problem = pulp.LpProblem("Maximize_Chebychev_Center", pulp.LpMaximize)

# Variables: center of the ball `y` and the radius `r`
y = pulp.LpVariable.dicts("y", range(N), lowBound=None, upBound=None, cat='Continuous')
r = pulp.LpVariable("r", lowBound=0, cat='Continuous')

# Objective: Maximize the radius `r`
problem += r

# Constraints: Each a_i^T * y + r * ||a_i|| <= b_i
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r * (sum(A[i][j]**2 for j in range(N))**0.5) <= B[i])

# Solve the problem
problem.solve()

# Retrieve the solution
center = [pulp.value(y[j]) for j in range(N)]
radius = pulp.value(r)

# Output the result
output = {
    "center": center,
    "radius": radius
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')