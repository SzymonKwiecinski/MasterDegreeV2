import pulp
import json

# Data provided in JSON format
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("Linear_Regression_Absolute_Deviations", pulp.LpMinimize)

# Define the variables
b = pulp.LpVariable("b", lowBound=None)  # Slope
a = pulp.LpVariable("a", lowBound=None)  # Intercept
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]  # Deviations

# Objective function: minimize the sum of deviations
problem += pulp.lpSum(d), "Total_Deviation"

# Constraints for each data point
for k in range(K):
    problem += d[k] >= Y[k] - (b * X[k] + a), f"Upper_Deviation_{k}"
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"Lower_Deviation_{k}"

# Solve the problem
problem.solve()

# Output the results
intercept = a.varValue
slope = b.varValue

print(f'Intercept: {intercept}')
print(f'Slope: {slope}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')