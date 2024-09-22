import pulp
import json

# Data from the input
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
Y = data['Y']
X = data['X']
K = data['NumObs']

# Create the linear programming problem
problem = pulp.LpProblem("MinMaxDeviation", pulp.LpMinimize)

# Define variables for the slope (b), intercept (a), and deviations (d)
a = pulp.LpVariable("intercept", lowBound=None)
b = pulp.LpVariable("slope", lowBound=None)
d_pos = pulp.LpVariable.dicts("d_pos", range(K), lowBound=0)    # Positive deviations
d_neg = pulp.LpVariable.dicts("d_neg", range(K), lowBound=0)    # Negative deviations

# Objective function: Minimize the maximum deviation
max_deviation = pulp.LpVariable("max_deviation", lowBound=0)
problem += max_deviation

# Constraints for each observation
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= max_deviation + d_pos[k]
    problem += (b * X[k] + a) - Y[k] <= max_deviation + d_neg[k]

# Solve the problem
problem.solve()

# Extract the results
intercept = pulp.value(a)
slope = pulp.value(b)

# Output the results
output = {
    "intercept": intercept,
    "slope": slope
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')