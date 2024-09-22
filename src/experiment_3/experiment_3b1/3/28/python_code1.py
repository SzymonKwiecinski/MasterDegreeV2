import pulp
import json

# Data in JSON format
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("Line_Fitting_Problem", pulp.LpMinimize)

# Define decision variables
a = pulp.LpVariable("a", lowBound=None)  # Intercept
b = pulp.LpVariable("b", lowBound=None)  # Slope
t = [pulp.LpVariable(f"t_{k}", lowBound=0) for k in range(K)]  # Slack variables

# Objective function
problem += pulp.lpSum(t[k] for k in range(K)), "Objective"

# Constraints
for k in range(K):
    problem += t[k] >= Y[k] - (b * X[k] + a), f"Upper_Bound_Constraint_{k}"
    problem += t[k] >= -(Y[k] - (b * X[k] + a)), f"Lower_Bound_Constraint_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')