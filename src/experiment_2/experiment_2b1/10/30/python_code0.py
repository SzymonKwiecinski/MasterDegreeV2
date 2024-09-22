import pulp
import json

# Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = len(data['y'])

# Create the problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Coefficients
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
c = pulp.LpVariable('c', cat='Continuous')

# Deviations
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Sum of absolute deviations
problem += pulp.lpSum(deviations), "Total_Deviation"

# Constraints
for k in range(K):
    problem += deviations[k] >= data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a), f'Upper_Deviation_{k}'
    problem += deviations[k] >= -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)), f'Lower_Deviation_{k}'

# Solve the problem
problem.solve()

# Get results
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')