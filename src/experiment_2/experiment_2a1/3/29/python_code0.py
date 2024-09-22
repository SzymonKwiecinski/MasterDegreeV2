import pulp
import json

# Input data
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Extracting x and y values
y_values = data['Y']
x_values = data['X']
num_obs = len(y_values)

# Define the problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable("intercept", lowBound=None)
b = pulp.LpVariable("slope", lowBound=None)
d_pos = [pulp.LpVariable(f"d_pos_{k}", lowBound=0) for k in range(num_obs)]
d_neg = [pulp.LpVariable(f"d_neg_{k}", lowBound=0) for k in range(num_obs)]

# Objective function: minimize the maximum deviation
problem += pulp.lpSum(d_pos) + pulp.lpSum(d_neg)

# Constraints for deviations
for k in range(num_obs):
    problem += y_values[k] - (b * x_values[k] + a) <= d_pos[k]
    problem += (b * x_values[k] + a) - y_values[k] <= d_neg[k]

# Solve the problem
problem.solve()

# Extract results
intercept = a.varValue
slope = b.varValue

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)