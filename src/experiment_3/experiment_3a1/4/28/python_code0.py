import pulp
import json

# Data
data = {
    'K': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Create a linear programming problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables for slope (b) and intercept (a)
b = pulp.LpVariable("slope", lowBound=None)
a = pulp.LpVariable("intercept", lowBound=None)

# Variables for absolute deviations
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(data['K'])]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(d)

# Constraints for absolute deviations
for k in range(data['K']):
    problem += d[k] >= data['Y'][k] - (b * data['X'][k] + a)
    problem += d[k] >= -(data['Y'][k] - (b * data['X'][k] + a))

# Solve the problem
problem.solve()

# Print the results
intercept = a.varValue
slope = b.varValue
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Intercept: {intercept}, Slope: {slope}')