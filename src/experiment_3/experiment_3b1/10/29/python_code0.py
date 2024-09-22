import pulp
import json

# Provided data
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Extracting the observed data
Y = data['Y']
X = data['X']
NumObs = data['NumObs']

# Create the linear programming problem
problem = pulp.LpProblem("Linear_Regression_Max_Deviation", pulp.LpMinimize)

# Define decision variables
a = pulp.LpVariable('a', lowBound=None)  # Intercept
b = pulp.LpVariable('b', lowBound=None)  # Slope
M = pulp.LpVariable('M', lowBound=0)     # Maximum deviation

# Define the constraints
for k in range(NumObs):
    problem += Y[k] - (b * X[k] + a) <= M
    problem += -(Y[k] - (b * X[k] + a)) <= M

# Define the objective function
problem += M

# Solve the problem
problem.solve()

# Print the results
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')