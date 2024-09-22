import pulp
import json

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create the LP problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Create variables for coefficients
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
c = pulp.LpVariable("c", lowBound=None)

# Create variables for deviations
deviations = [pulp.LpVariable(f"deviation_{i}", lowBound=0) for i in range(len(data['y']))]

# Objective function: Minimize the sum of deviations
problem += pulp.lpSum(deviations)

# Constraints
for i in range(len(data['y'])):
    problem += deviations[i] >= data['y'][i] - (c * data['x'][i]**2 + b * data['x'][i] + a)
    problem += deviations[i] >= -(data['y'][i] - (c * data['x'][i]**2 + b * data['x'][i] + a))

# Solve the problem
problem.solve()

# Results
results = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(json.dumps(results))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')