import pulp
import json

# Data provided in JSON format
data = json.loads("""{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}""")

# Extracting data
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', cat='Continuous')  # Intercept
b = pulp.LpVariable('b', cat='Continuous')  # Slope
M = pulp.LpVariable('M', lowBound=0, cat='Continuous')  # Maximum deviation

# Constraints
for k in range(num_obs):
    problem += Y[k] - (b * X[k] + a) <= M
    problem += -(Y[k] - (b * X[k] + a)) <= M

# Objective function
problem += M

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')