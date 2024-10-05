import pulp

# Data input
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y = data['y']
x = data['x']
K = len(y)

# Define the LP problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Define the variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
deviations = [pulp.LpVariable(f'dev_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations)

# Constraints for each data point
for k in range(K):
    problem += deviations[k] >= y[k] - (c * x[k]**2 + b * x[k] + a)
    problem += deviations[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a))

# Solve the problem
problem.solve()

# Retrieve and print the solution
quadratic = pulp.value(c)
linear = pulp.value(b)
constant = pulp.value(a)

output = {"quadratic": quadratic, "linear": linear, "constant": constant}
print(output)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')