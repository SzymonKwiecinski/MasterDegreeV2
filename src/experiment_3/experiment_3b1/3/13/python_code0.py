import pulp
import numpy as np

# Input data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Define the problem
problem = pulp.LpProblem("Chebyshev_Center_Problem", pulp.LpMaximize)

# Decision variables
r = pulp.LpVariable("r", lowBound=0)  # radius
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=None)  # center coordinates

# Objective function
problem += r

# Constraints
for i in range(data['M']):
    a_i = data['A'][i]
    b_i = data['B'][i]
    problem += (np.dot(a_i, [y[j] for j in range(data['N'])]) + r * np.linalg.norm(a_i) <= b_i)

# Solve the problem
problem.solve()

# Retrieve results
center = [y[j].varValue for j in range(data['N'])]
radius = r.varValue

# Output
output = {
    "center": center,
    "radius": radius
}

print(f'Output: {output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')