import pulp

# Problem Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data['y']
x_values = data['x']
K = len(y_values)

# Initialize problem
problem = pulp.LpProblem("Best_Quadratic_Fit", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable('a', lowBound=-1e5, upBound=1e5, cat='Continuous')
b = pulp.LpVariable('b', lowBound=-1e5, upBound=1e5, cat='Continuous')
c = pulp.LpVariable('c', lowBound=-1e5, upBound=1e5, cat='Continuous')
deviation = [pulp.LpVariable(f'dev_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviation)

# Constraints
for k in range(K):
    predicted_y = c * x_values[k]**2 + b * x_values[k] + a
    problem += y_values[k] - predicted_y <= deviation[k]
    problem += predicted_y - y_values[k] <= deviation[k]

# Solve the problem
problem.solve()

# Extract the results
quadratic = c.varValue
linear = b.varValue
constant = a.varValue

output = {
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')