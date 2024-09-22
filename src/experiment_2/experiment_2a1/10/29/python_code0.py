import pulp
import json

# Data input
data = {'NumObs': 19, 
        'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract y and x values
y_values = data['Y']
x_values = data['X']

# Create the LP problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable('intercept', lowBound=None)
b = pulp.LpVariable('slope', lowBound=None)
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(len(y_values))]

# Objective function: Minimize the maximum deviation
problem += pulp.lpSum(deviations)  # We will minimize total deviations

# Constraints for each observed value
for k in range(len(y_values)):
    problem += y_values[k] - (b * x_values[k] + a) <= deviations[k]
    problem += -(y_values[k] - (b * x_values[k] + a)) <= deviations[k]

# Solve the problem
problem.solve()

# Extract results
intercept = a.varValue
slope = b.varValue

# Output results
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')