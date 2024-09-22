import pulp

# Data from JSON
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Problem Setup
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('Intercept', lowBound=None)
b = pulp.LpVariable('Slope', lowBound=None)
d = pulp.LpVariable('MaxDeviation', lowBound=0)

# Objective
problem += d

# Constraints
for i in range(data['NumObs']):
    y_predicted = a + b * data['X'][i]
    problem += y_predicted - data['Y'][i] <= d
    problem += data['Y'][i] - y_predicted <= d

# Solve the problem
problem.solve()

# Outputs
solution = {
    'intercept': pulp.value(a),
    'slope': pulp.value(b)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')