import pulp
import json

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Create a linear programming problem
problem = pulp.LpProblem("Linear_Regression", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable("a", lowBound=None)  # intercept
b = pulp.LpVariable("b", lowBound=None)  # slope
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]  # deviations

# Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(d)

# Constraints: d_k >= y_k - (b*x_k + a) and d_k >= -(y_k - (b*x_k + a))
for k in range(K):
    problem += d[k] >= Y[k] - (b * X[k] + a)
    problem += d[k] >= -(Y[k] - (b * X[k] + a))

# Solve the problem
problem.solve()

# Extract the results
intercept = a.varValue
slope = b.varValue

# Output the results
output = {
    "intercept": intercept,
    "slope": slope
}

# Print results in required format
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')