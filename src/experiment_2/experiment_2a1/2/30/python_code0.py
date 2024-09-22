import pulp
import json

# Input data
data = {"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create the LP problem
problem = pulp.LpProblem("Quadratic_Regression", pulp.LpMinimize)

# Coefficients
a = pulp.LpVariable("a", lowBound=None)  # constant term
b = pulp.LpVariable("b", lowBound=None)  # linear term
c = pulp.LpVariable("c", lowBound=None)  # quadratic term

# Absolute deviations
deviations = []
for k in range(len(data['y'])):
    y_pred = c * data['x'][k]**2 + b * data['x'][k] + a
    deviation = pulp.LpVariable(f"deviation_{k}", lowBound=0)  # absolute deviation
    deviations.append(deviation)
    problem += deviation >= data['y'][k] - y_pred
    problem += deviation >= y_pred - data['y'][k]

# Objective: minimize the sum of deviations
problem += pulp.lpSum(deviations)

# Solve the problem
problem.solve()

# Output the coefficients
output = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Final output
print(json.dumps(output))