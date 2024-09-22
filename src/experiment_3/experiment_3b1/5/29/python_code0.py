import pulp
import json

# Data as a JSON string
data_json = '{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

# Extract data
K = data['NumObs']
Y = data['Y']
X = data['X']

# Create a linear programming problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Variables
b = pulp.LpVariable("slope", lowBound=None)  # Slope
a = pulp.LpVariable("intercept", lowBound=None)  # Intercept
t = pulp.LpVariable("max_deviation", lowBound=0)  # Maximum deviation

# Objective function
problem += t, "Minimize_Max_Deviation"

# Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= t, f"Upper_Bound_Constraint_{k+1}"
    problem += -(Y[k] - (b * X[k] + a)) <= t, f"Lower_Bound_Constraint_{k+1}"

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')