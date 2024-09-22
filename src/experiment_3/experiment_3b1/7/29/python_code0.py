import pulp
import json

# Given data
data_json = """{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}"""
data = json.loads(data_json.replace("'", '"'))

# Model setup
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

# Define the problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", cat="Continuous")
b = pulp.LpVariable("b", cat="Continuous")
D = pulp.LpVariable("D", lowBound=0, cat="Continuous")  # D is non-negative

# Constraints
for k in range(num_obs):
    problem += Y[k] - (b * X[k] + a) <= D
    problem += -(Y[k] - (b * X[k] + a)) <= D

# Objective
problem += D

# Solve the problem
problem.solve()

# Output results
print(f'Intercept (a): {a.varValue}, Slope (b): {b.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')