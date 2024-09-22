import pulp
import json

# Given data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Define the problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Define variables for coefficients
a = pulp.LpVariable("a", lowBound=None)  # constant term
b = pulp.LpVariable("b", lowBound=None)  # linear term
c = pulp.LpVariable("c", lowBound=None)  # quadratic term

# Define deviations as non-negative variables
deviations = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(len(data['y']))]

# Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "TotalDeviations"

# Constraints to ensure deviations represent the absolute differences
for k in range(len(data['y'])):
    predicted_y_k = c * data['x'][k] ** 2 + b * data['x'][k] + a
    problem += predicted_y_k + deviations[k] >= data['y'][k], f"UpperBound_{k}"
    problem += predicted_y_k - deviations[k] <= data['y'][k], f"LowerBound_{k}"

# Solve the problem
problem.solve()

# Extract the coefficients
quadratic = c.varValue
linear = b.varValue
constant = a.varValue

# Prepare the output
output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

# Print the results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')