import pulp
import json

# Data input
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("Linear_Regression", pulp.LpMinimize)

# Variables
b = pulp.LpVariable("b", None)  # Slope
a = pulp.LpVariable("a", None)  # Intercept
t = pulp.LpVariable("t", 0)      # Maximum deviation

# Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= t
    problem += -(Y[k] - (b * X[k] + a)) <= t

# Objective
problem += t

# Solve the problem
problem.solve()

# Output the results
intercept = a.varValue
slope = b.varValue

print(f'{{"intercept": {intercept}, "slope": {slope}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')