import pulp
import json

# Input data
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

# Problem definition
problem = pulp.LpProblem("Linear_Regression", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable("a", lowBound=None)  # intercept
b = pulp.LpVariable("b", lowBound=None)  # slope
M = pulp.LpVariable("M", lowBound=0)     # maximum deviation

# Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= M
    problem += -(Y[k] - (b * X[k] + a)) <= M

# Objective function
problem += M

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')