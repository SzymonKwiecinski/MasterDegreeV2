import pulp

# Data
data_json = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 
                   1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
             'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 
                   5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_data = data_json['y']
x_data = data_json['x']
num_points = len(y_data)

# Problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

# Variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(num_points)]

# Objective Function
problem += pulp.lpSum(d)

# Constraints
for k in range(num_points):
    problem += c * x_data[k]**2 + b * x_data[k] + a - y_data[k] <= d[k]
    problem += c * x_data[k]**2 + b * x_data[k] + a - y_data[k] >= -d[k]

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')