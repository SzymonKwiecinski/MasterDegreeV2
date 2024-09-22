import json
import pulp

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create the LP problem
problem = pulp.LpProblem("Line_Fitting_Problem", pulp.LpMinimize)

# Variables for slope (b) and intercept (a)
b = pulp.LpVariable("slope", lowBound=None)
a = pulp.LpVariable("intercept", lowBound=None)

# Variables for deviations
deviations_positive = [pulp.LpVariable(f"dev_pos_{k}", lowBound=0) for k in range(data['NumObs'])]
deviations_negative = [pulp.LpVariable(f"dev_neg_{k}", lowBound=0) for k in range(data['NumObs'])]

# Objective function: minimize the maximum deviation
max_deviation = pulp.LpVariable("max_dev", lowBound=0)
problem += max_deviation

# Constraints for each observation
for k in range(data['NumObs']):
    problem += data['Y'][k] - (b * data['X'][k] + a) <= max_deviation + deviations_positive[k]
    problem += -(data['Y'][k] - (b * data['X'][k] + a)) <= max_deviation + deviations_negative[k]

# Solve the problem
problem.solve()

# Output results
intercept = a.varValue
slope = b.varValue

result = {
    "intercept": intercept,
    "slope": slope
}

# Print the result
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')