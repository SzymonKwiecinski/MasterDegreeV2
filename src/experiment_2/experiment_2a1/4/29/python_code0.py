import pulp
import json

# Data parsing
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Preparing the problem
num_obs = data['NumObs']
y_values = data['Y']
x_values = data['X']

# Create a linear programming problem
problem = pulp.LpProblem("LinearRegressionFit", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable("intercept", lowBound=None)
b = pulp.LpVariable("slope", lowBound=None)
deviations = pulp.LpVariable.dicts("deviations", range(num_obs), lowBound=0)

# Objective function: minimize the maximum deviation
problem += pulp.lpSum(deviations[i] for i in range(num_obs))

# Constraints for each observed value
for i in range(num_obs):
    problem += deviations[i] >= y_values[i] - (b * x_values[i] + a)
    problem += deviations[i] >= -(y_values[i] - (b * x_values[i] + a))

# Solve the problem
problem.solve()

# Output results
intercept = a.varValue
slope = b.varValue

output = {
    "intercept": intercept,
    "slope": slope
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')