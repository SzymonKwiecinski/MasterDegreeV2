import pulp

# Data from the provided JSON
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Create a linear programming problem
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Decision variable for radius
r = pulp.LpVariable("r", lowBound=0)  # r >= 0

# Decision variables for the center
y = [pulp.LpVariable(f"y_{j}", cat='Continuous') for j in range(data['N'])]

# Constraints
for i in range(data['M']):
    a_i = data['A'][i]
    b_i = data['B'][i]
    
    # Constraint: a_i^T * y - r <= b_i
    problem += (pulp.lpSum(a_i[j] * y[j] for j in range(data['N'])) - r <= b_i)

    # Constraint: -a_i^T * y + r <= b_i
    problem += (-pulp.lpSum(a_i[j] * y[j] for j in range(data['N'])) + r <= b_i)

# Objective function: Maximize r
problem += r

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')