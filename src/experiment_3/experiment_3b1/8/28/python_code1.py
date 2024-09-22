import pulp
import json

data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("FitLine", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", lowBound=None)  # intercept
b = pulp.LpVariable("b", lowBound=None)  # slope
d_plus = [pulp.LpVariable(f"d_plus_{k}", lowBound=0) for k in range(K)]  # positive deviations
d_minus = [pulp.LpVariable(f"d_minus_{k}", lowBound=0) for k in range(K)]  # negative deviations

# Objective Function
problem += pulp.lpSum(d_plus[k] + d_minus[k] for k in range(K)), "Total_Absolute_Deviation"

# Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= d_plus[k], f"Positive_Deviation_Constraint_{k}"
    problem += -(Y[k] - (b * X[k] + a)) <= d_minus[k], f"Negative_Deviation_Constraint_{k}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')