import pulp

# Given data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = len(data['y'])

# Create a problem variable
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Variables for coefficients
c = pulp.LpVariable("c", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
a = pulp.LpVariable("a", lowBound=None)

# Auxiliary variables for absolute deviations
z = [pulp.LpVariable(f"z_{k}", lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(z)

# Constraints for the auxiliary variables
for k in range(K):
    problem += z[k] >= data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)
    problem += z[k] >= -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a))

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f' Coefficient c: {c.varValue}')
print(f' Coefficient b: {b.varValue}')
print(f' Coefficient a: {a.varValue}')