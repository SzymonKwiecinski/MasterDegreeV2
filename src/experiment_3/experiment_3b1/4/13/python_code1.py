import pulp
import numpy as np

# Data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Problem definition
problem = pulp.LpProblem("Chebyshev_Center", pulp.LpMaximize)

# Variables
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective function
problem += r, "Maximize the radius"

# Constraints
for i in range(data['M']):
    a_i = np.array(data['A'][i])
    b_i = data['B'][i]
    norm_a_i = np.linalg.norm(a_i)
    
    problem += r <= (b_i - np.dot(a_i, np.array([y[j] for j in range(data['N'])]))) / norm_a_i, f"Constraint_{i}")

# Solve the problem
problem.solve()

# Output the center and radius
center = [pulp.value(y[j]) for j in range(data['N'])]
radius = pulp.value(r)

print(f'Center: {center}')
print(f'Radius: {radius}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')