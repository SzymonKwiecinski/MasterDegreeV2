import pulp
import json

# Given data in JSON format
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

# Create the problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', lowBound=None)  # intercept
b = pulp.LpVariable('b', lowBound=None)  # slope
z_plus = [pulp.LpVariable(f'z_plus_{k}', lowBound=0) for k in range(K)]  # positive deviations
z_minus = [pulp.LpVariable(f'z_minus_{k}', lowBound=0) for k in range(K)]  # negative deviations

# Objective function
problem += pulp.lpSum(z_plus[k] + z_minus[k] for k in range(K)), "Total_Absolute_Deviation"

# Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= z_plus[k], f"Pos_Deviation_{k}"
    problem += -(Y[k] - (b * X[k] + a)) <= z_minus[k], f"Neg_Deviation_{k}"

# Solve the problem
problem.solve()

# Output results
intercept = a.varValue
slope = b.varValue
print(f'Intercept (a): {intercept}, Slope (b): {slope}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')