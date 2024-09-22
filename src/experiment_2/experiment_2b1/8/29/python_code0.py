import pulp
import json

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Prepare the problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("intercept", lowBound=None)  # Intercept
b = pulp.LpVariable("slope", lowBound=None)      # Slope
deviations_pos = pulp.LpVariable.dicts("deviation_pos", range(data['NumObs']), lowBound=0)  # Positive deviations
deviations_neg = pulp.LpVariable.dicts("deviation_neg", range(data['NumObs']), lowBound=0)  # Negative deviations

# Objective Function: Minimize the maximum deviation
max_deviation = pulp.LpVariable("max_deviation", lowBound=0)
problem += max_deviation

# Constraints
for k in range(data['NumObs']):
    problem += deviations_pos[k] >= (data['Y'][k] - (b * data['X'][k] + a)), f"pos_dev_{k}"
    problem += deviations_neg[k] >= -(data['Y'][k] - (b * data['X'][k] + a)), f"neg_dev_{k}"
    problem += max_deviation >= deviations_pos[k], f"max_pos_dev_{k}"
    problem += max_deviation >= deviations_neg[k], f"max_neg_dev_{k}"

# Solve the problem
problem.solve()

# Output the results
intercept = a.varValue
slope = b.varValue

output = {
    "intercept": intercept,
    "slope": slope
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')