import pulp
import json

# Data
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

# Create the problem variable
problem = pulp.LpProblem("Linear_Regression_Problem", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable("a", lowBound=None)  # Intercept
b = pulp.LpVariable("b", lowBound=None)  # Slope
e = pulp.LpVariable.dicts("e", range(K), lowBound=0)  # Deviation variables

# Objective function: Minimize the sum of e_k
problem += pulp.lpSum(e[k] for k in range(K))

# Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= e[k]  # d_k <= e_k
    problem += -(Y[k] - (b * X[k] + a)) <= e[k]  # -d_k <= e_k

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')