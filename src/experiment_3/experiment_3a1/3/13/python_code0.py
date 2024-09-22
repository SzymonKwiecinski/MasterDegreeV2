import pulp
import numpy as np

# Data from the provided input
data = {
    'M': 4,
    'N': 2,
    'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]],
    'B': [2.0, 2.0, 3.0, 5.0]
}

# Define the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Variables
y = pulp.LpVariable.dicts("y", range(data['N']), lowBound=None)  # Center of the ball
r = pulp.LpVariable("r", lowBound=0)  # Radius of the ball

# Constraints
for i in range(data['M']):
    a_i = np.array(data['A'][i])
    b_i = data['B'][i]
    
    # Add the constraint: r * (a_i^T * u) <= (b_i - a_i^T * y)
    # Here we are assuming u is a unit vector in each direction defined by the constraints
    problem.addConstraint(pulp.LpConstraint(
        r * (a_i[0] if i < 2 else 0) + r * (a_i[1] if i % 2 == 0 else 0),
        sense=pulp.LpConstraintLE,
        rhs=b_i - (a_i[0] * y[0] + a_i[1] * y[1])
    ))

# Objective function
problem += r, "Maximize_Radius"

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')