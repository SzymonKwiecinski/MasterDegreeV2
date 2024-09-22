import pulp
import json

# Given data in JSON format
data_json = '{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

# Model creation
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Decision variables
b = pulp.LpVariable("b", lowBound=None)  # Slope
a = pulp.LpVariable("a", lowBound=None)  # Intercept
D = pulp.LpVariable("D", lowBound=0)     # Maximum deviation

# Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

# Constraints for the deviations
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= D
    problem += -(Y[k] - (b * X[k] + a)) <= D

# Objective function
problem += D

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')