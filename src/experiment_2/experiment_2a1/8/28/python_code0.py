import pulp
import json

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extracting Y and X values
y_values = data['Y']
x_values = data['X']
K = data['K']

# Create the problem
problem = pulp.LpProblem("Least_Absolute_Deviation_Regression", pulp.LpMinimize)

# Decision variables for slope (b) and intercept (a)
b = pulp.LpVariable('slope', lowBound=None)
a = pulp.LpVariable('intercept', lowBound=None)

# Decision variables for absolute deviations
deviations = [pulp.LpVariable(f'deviation_{k}', lowBound=0) for k in range(K)]

# Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "Total_Absolute_Deviation"

# Constraints: y_k = b*x_k + a + deviation_k for each k
for k in range(K):
    problem += y_values[k] == b * x_values[k] + a + deviations[k], f"Constraint_{k}"

# Solve the problem
problem.solve()

# Extract results
intercept = a.varValue
slope = b.varValue

# Output results
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')