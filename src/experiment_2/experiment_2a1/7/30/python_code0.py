import pulp
import json

data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = len(data['y'])
y_values = data['y']
x_values = data['x']

# Create the problem variable
problem = pulp.LpProblem("Quadratic_Fitting", pulp.LpMinimize)

# Coefficients for the quadratic equation
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')

# Create variables for the absolute deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0) for k in range(K)]

# Objective Function: Minimize the sum of deviations
problem += pulp.lpSum(deviations), "Total_Deviation"

# Constraints for the absolute deviations
for k in range(K):
    problem += deviations[k] >= y_values[k] - (c * (x_values[k] ** 2) + b * x_values[k] + a), f"Upper_Constraint_{k}")
    problem += deviations[k] >= -(y_values[k] - (c * (x_values[k] ** 2) + b * x_values[k] + a)), f"Lower_Constraint_{k}")

# Solve the problem
problem.solve()

# Retrieve coefficients
quadratic = c.varValue
linear = b.varValue
constant = a.varValue

# Output the results
result = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')