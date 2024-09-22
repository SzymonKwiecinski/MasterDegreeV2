import pulp
import json

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract variables
K = data['K']
Y = data['Y']
X = data['X']

# Create a problem instance
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

# Variables for slope (b) and intercept (a)
b = pulp.LpVariable("slope", lowBound=None)
a = pulp.LpVariable("intercept", lowBound=None)

# Variables for absolute deviations
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(K)]

# Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(deviations), "Total_Absolute_Deviation"

# Constraints for absolute deviations
for k in range(K):
    problem += deviations[k] >= Y[k] - (b * X[k] + a), f"Upper_Bound_Deviation_{k}"
    problem += deviations[k] >= -(Y[k] - (b * X[k] + a)), f"Lower_Bound_Deviation_{k}"

# Solve the problem
problem.solve()

# Extracting the results
intercept = a.varValue
slope = b.varValue

# Output 
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')