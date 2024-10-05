import pulp

# Data from JSON
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Problem definition
problem = pulp.LpProblem("Minimize_Max_Absolute_Deviation", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
z = pulp.LpVariable("z", lowBound=0)

# Objective Function
problem += z, "Objective"

# Constraints
for k in range(data['NumObs']):
    problem += (data['Y'][k] - (a + b * data['X'][k])) <= z, f"Constraint_Upper_{k}"
    problem += -(data['Y'][k] - (a + b * data['X'][k])) <= z, f"Constraint_Lower_{k}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')