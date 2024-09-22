import pulp
import numpy as np

# Given data
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Define the problem
problem = pulp.LpProblem("Maximize_Radius", pulp.LpMaximize)

# Define variables
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective function
problem += r, "Objective"

# Constraints
for i in range(data['M']):
    a_i = np.array(data['A'][i])
    b_i = data['B'][i]
    norm_a_i = np.linalg.norm(a_i)
    problem += (np.dot(a_i, [y[j] for j in range(data['N'])]) + norm_a_i * r <= b_i), f"Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')