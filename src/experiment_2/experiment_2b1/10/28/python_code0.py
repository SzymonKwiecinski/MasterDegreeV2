import pulp
import json

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract X and Y values
Y = data['Y']
X = data['X']
K = data['K']

# Create a linear programming problem
problem = pulp.LpProblem("FitBestLine", pulp.LpMinimize)

# Define variables for intercept and slope
intercept = pulp.LpVariable("intercept", lowBound=None)
slope = pulp.LpVariable("slope", lowBound=None)

# Define deviation variables
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(K)]

# Objective Function: Minimize the sum of deviations
problem += pulp.lpSum(deviations)

# Constraints: |y_k - (slope * x_k + intercept)| = deviations_k
for k in range(K):
    problem += deviations[k] >= Y[k] - (slope * X[k] + intercept)
    problem += deviations[k] >= -(Y[k] - (slope * X[k] + intercept))

# Solve the problem
problem.solve()

# Output the results
intercept_value = pulp.value(intercept)
slope_value = pulp.value(slope)

results = {
    "intercept": intercept_value,
    "slope": slope_value
}
print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')