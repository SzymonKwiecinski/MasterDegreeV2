import pulp
import json

# Given data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Initialize the problem
problem = pulp.LpProblem("Quadratic_Fitting", pulp.LpMinimize)

# Variables for coefficients of the quadratic equation
a = pulp.LpVariable("a", cat='Continuous')
b = pulp.LpVariable("b", cat='Continuous')
c = pulp.LpVariable("c", cat='Continuous')

# Create variables for the absolute deviations
deviations = [pulp.LpVariable(f"d_{k}", cat='Continuous') for k in range(len(data['y']))]

# Objective function: minimize the sum of deviations
problem += pulp.lpSum(deviations), "TotalDeviation"

# Constraints for each data point
for k in range(len(data['y'])):
    problem += deviations[k] >= data['y'][k] - (c * (data['x'][k] ** 2) + b * data['x'][k] + a), f"UpperBound_{k}"
    problem += deviations[k] >= -(data['y'][k] - (c * (data['x'][k] ** 2) + b * data['x'][k] + a)), f"LowerBound_{k}"

# Solve the problem
problem.solve()

# Extract results
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Prepare output
output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

# Print the output
print(json.dumps(output))